from flask import Flask, render_template
from doc2vec import *
import sys

app = Flask(__name__, template_folder=os.getcwd())

@app.route("/")
def articles():
    """
    Shows all the aritcles in the corpus in a web page
    """
    links = [article[0] for article in articles]
    titles = [article[1] for article in articles]
    return render_template('articles.html', links = links, titles = titles)


@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Show an article in a web page with links to similar articles in the side.
    """
    path = os.path.join(topic,filename)
    index = None
    for i in range(len(articles)):
        if path == articles[i][0]:
            index = i
            break

    title = articles[index][1]
    text = articles[index][2].split('\n\n')
    seealso = recommended(path, articles, 5)
    rec_links = [rec[0].split('/')[1] for rec in seealso]
    rec_titles = [rec[1] for rec in seealso]

    return render_template('article.html', title = title, text = text, rec_links = rec_links, rec_titles = rec_titles)


# initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)
