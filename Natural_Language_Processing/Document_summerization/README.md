# Introduction

This project tries to find the words that best summerize an article using a technique called TFIDF. Data for this project is an article corpus from Reuters (9164 articles) and each article is in XML format.

# Running the app

Running the following command will return the top 20 words that will summerize an article of interest with thier corresponding TFIDF score
```
python summarize.py <path to article corpus> <filename of article to summerize>
```
