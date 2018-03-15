import sys
import nltk
from nltk.stem.porter import *
from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import xml.etree.cElementTree as ET
from collections import Counter
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import zipfile
import os
import re

PARTIALS = False

def gettext(xmltext):
    """
    Parse xmltext and return the text from <title> and <text> tags
    """
    xmltext = xmltext.encode('ascii', 'ignore')

    tree = ET.ElementTree(ET.fromstring(xmltext))

    text = ""
    for elem in tree.iter(tag = 'title'):
        text = text+elem.text

    for elem in tree.iter(tag = 'p'):
        text = text+'\n'
        text = text+elem.text

    return text


def tokenize(text):
    """
    Tokenize text and return a non-unique list of tokenized words
    found in the text. Normalize to lowercase, strip punctuation,
    remove stop words, drop words of length < 3.
    """
    text1 = text.lower()
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    text1 = regex.sub(" ",text1) #replace punctuation, numbers, and \r, \n, \t with a space
    words = nltk.word_tokenize(text1)
    words = [word for word in words if len(word)>2]
    words = [word for word in words if word not in ENGLISH_STOP_WORDS]

    return words


def stemwords(words):
    """
    Given a list of tokens/words, return a new list with each word
    stemmed using a PorterStemmer.
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in words]


def tokenizer(text):
    return stemwords(tokenize(text))


def compute_tfidf(corpus):
    """
    Create and return a TfidfVectorizer object after training it on
    the list of articles pulled from the corpus
    """
    tfidf = TfidfVectorizer(input='content',
                        analyzer='word',
                        preprocessor=gettext,
                        tokenizer=tokenizer,
                        stop_words='english',
                        decode_error = 'ignore')

    doc_text = [corpus[key] for key in corpus]
    #print doc_text
    tfidf.fit(doc_text)

    return tfidf


def summarize(tfidf, text, n):
    """
    return 20 words with heighest tfidf scores
    """
    data = tfidf.transform([text])
    words = tfidf.get_feature_names()
    index = data.nonzero()[1]

    word_score = zip([words[i] for i in index], [data[0, x] for x in index])
    word_score = [(sc[0], sc[1]) for sc in word_score if sc[1] >= 0.09]
    word_score = sorted(word_score, key = lambda x: x[1], reverse=True)

    if len(word_score)>20:
        return word_score[:20]
    else:
        return word_score


def load_corpus(zipfilename):
    """
    Extract file names and and their corresponding content from a zipped corpus of
    articles in to a dictionary
    """
    zip_rf = zipfile.ZipFile(zipfilename, 'r')

    file_text = {}

    for xml_f in zip_rf.namelist():
        if  xml_f.endswith('.xml') and not xml_f.startswith('_'):
            with zip_rf.open(xml_f) as f:
                xml_f = xml_f.split('/')[1]  # get only file name
                file_text[xml_f] = ' '.join(f.readlines()) #join list of lines together form a string

    return file_text




