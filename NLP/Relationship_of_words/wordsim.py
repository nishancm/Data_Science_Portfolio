import sys
import numpy as np
import re

def load_glove(filename):
    fname = open(filename)

    dict = {}
    for line in fname.readlines():
        line = line.split(' ')
        dict[line[0]] = np.array([float(i) for i in line[1:] ])

    return dict


def closest_words(gloves, word, n):

    dist_word = []
    for item in gloves:
        dist_word.append((np.linalg.norm(gloves[word] - gloves[item]), item) )

    dist_word.sort( key = lambda x: x[0] )

    close  = [tup[1] for tup in dist_word]
    close.remove(word)

    return close[0:n]


def analogies(gloves, x, y, z, n):

    dif = gloves[x] - gloves[y]
    dif_word = []

    for item in gloves:
        z_dif = gloves[z] - gloves[item]
        dif_word.append((np.linalg.norm(dif - z_dif), item))

    dif_word.sort( key = lambda x: x[0])

    close_dif = [tup[1] for tup in dif_word]
    close_dif.remove(z)

    return close_dif[0:n]


if __name__ == '__main__':
    glove_filename = sys.argv[1]
    gloves = load_glove(glove_filename)

    print("Enter a word or 'x:y as z:'")
    cmd = raw_input("> ")
    while cmd != None:
        match = re.search(r'(\w+):(\w+) as (\w+):', cmd)
        if match is not None and len(match.groups()) == 3:
            x = match.group(1).lower()
            y = match.group(2).lower()
            z = match.group(3).lower()
            words = analogies(gloves, x, y, z, 5)
            print "%s is to %s as %s is to {%s}" % (x, y, z, ' '.join(words))
        elif re.match(r'\w+', cmd) is not None:
            words = closest_words(gloves, cmd, 5)
            print "%s is similar to {%s}" % (cmd, ' '.join(words))
        else:
            print("Enter a word or 'x:y as z:'")
        cmd = raw_input("> ")