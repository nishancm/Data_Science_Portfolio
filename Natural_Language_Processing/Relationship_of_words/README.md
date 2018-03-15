# Introduction

This project use results from the [Stanford GLoVE](https://nlp.stanford.edu/projects/glove/) project. In simple terms GloVe provides a vector representation of the words (e.g. 300 dimension space). And this vector representation of the words can be used identify relationships between the words.

# The project

Program offers user two options. If the user provides word in the prompt, program will return n closest words matching the word entered.
```
Enter a word or 'x:y as z:'
> student
student is similar to {students teacher graduate campus undergraduate}}
```
If the user provide an analogy and a word, program will return a word matching the analogy provided by the user.
```
Enter a word or 'x:y as z:'
> teacher:school as doctor:
teacher is to school as doctor is to {medical school doctors hospital clinic}
```

# the data

File containing 300 dimension representation of words are downloaded from [Stanford GLoVE](https://nlp.stanford.edu/projects/glove/). And sample lines of the looks like this.
```
sandberger 0.429191 -0.296897 0.15011 0.245201 ... 
```

# Running the app
```
python wordsim.py <path to 300d glove file>
```
User will be iterative prompt for words and analogies in the command line. Users can kill the program by pressing `control-c`
