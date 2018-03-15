import sys
import re
import string
import os
import numpy as np
import codecs

# From scikit learn that got words from:
# http://ir.dcs.gla.ac.uk/resources/linguistic_utils/stop_words
ENGLISH_STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves"])


def load_glove(filename):
    """
    load glove file in to a word vector dictionary
    """
    with open(filename) as f:
        dict = {}
        for line in f.readlines():
            line = line.split(' ')
            dict[line[0]] = np.array([float(i) for i in line[1:] ])
    return dict


def filelist(root):
    """
    Return a fully-qualified list of filenames
    """
    allfiles = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            allfiles.append(os.path.join(path, name))
    return allfiles


def get_text(filename):
    """
    Load and return the text of a text file, assuming latin-1 encoding as that
    is what the BBC corpus uses.
    """
    f = codecs.open(filename, encoding='latin-1', mode='r')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    normalizing a string (sentence)
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    txt = regex.sub(" ", text)
    wds = txt.split(' ')
    wds = [wd.lower() for wd in wds if len(wd)>2]
    wds = [wd for wd in wds if wd not in ENGLISH_STOP_WORDS]
    return wds

def load_articles(articles_dirname, gloves):
    """
    Load all .txt files under articles_dirname and return a list of lists
    """

    filenames = []
    for folder in os.walk(articles_dirname):
        filenames += [os.path.join(folder[0], file) for file in folder[2]]
    filenames = filenames[1:] #remove .dir file
    fnames = [re.sub('^.*bbc/', "", fl) for fl in filenames]


    titles = []
    articles = []
    doc_centroids = []

    for filename in filenames:
        text = get_text(filename)
        titles.append(text.splitlines()[0])
        text = '\n'.join(text.splitlines()[1:])
        articles.append(text)
        doc_centroids.append(doc2vec(text, gloves))

    return [(fnames[i], titles[i], articles[i], doc_centroids[i]) for i in range(len(filenames))]


def doc2vec(text, gloves):
    """
    Return the word vector centroid for the article.
    """
    wds = words(text)
    vec_sum = np.zeros((1,300)) #dimention of word vec
    for wd in wds:
        if wd in gloves:
            vec_sum += gloves[wd]

    return vec_sum/len(wds)


def distances(article, articles):
    """
    Compute the euclidean distance from article to every other article
    """
    index = None
    for i in range(len(articles)): # find the index of an article
        if article == articles[i][0]:
            index = i
            break

    return [(np.linalg.norm(a[3]- articles[index][3]), a) for a in articles]


def recommended(article, articles, n):
    """
    Return a list of the n articles closest to article's word vector centroid. 
    """
    dists = distances(article, articles)
    dists = sorted(dists)[1:] # remove the current article after sorting
    return [dists[i][1] for i in range(n)]


