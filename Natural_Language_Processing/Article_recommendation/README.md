# Introduction

This project will host a webserver in AWS to display a list of [bbc](http://mlg.ucd.ie/datasets/bbc.html) articles. When an article link is clicked a new web page will show the content of the article along with similar articles as recommnedations in the side. 

# Finding similar articles

For each article, article centroid is derived by taking the mean of word vectors available from [Stanfor Glove project](https://nlp.stanford.edu/projects/glove/). Then for each article euclidean distance to all other articles are calculated. Articles with minimum euclidean distance to a particlar article will be identified as similar articles.

# Running the app

Login to AWS instance and install `flask and gunicorn` python libraries. Download 300 dimension glove file, and bbc article corpus. Run the following command.
```
gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app <path to glove file> <path to bbc corpus>
```
