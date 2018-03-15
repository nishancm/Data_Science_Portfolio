from tfidf import *

zipfilename = sys.argv[1]
summarizefile = sys.argv[2]

corpus = load_corpus(zipfilename) # contain all xml filenames and there raw xmltext as a dictionary

tfidf = compute_tfidf(corpus)

f = open(sys.argv[2])
xmltext = f.read() #read file text with xml data
f.close()

sum_tfidf = summarize(tfidf, xmltext, 20)

for word in sum_tfidf:
    print word[0], word[1]