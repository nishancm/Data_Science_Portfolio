# Introduction

This project will host a webserver in AWS to display,
* Top 100 tweets of a twitter user with a color gradient to represent thier sentiment (red - post). This can be accessed by  ```<URL of AWS instance>/<screen name of the user>```
* Followers of a user sorted in descending order by the number of followers of them. This can be accessed by ```<URL of AWS instance>/following/<screen name of the user>```

# Running the app

In login to AWS instance and clone the folder with files. Then install `flask, tweepy, gunicorn, vaderSentiment, colour` python libraries. Then run the application using,
```
gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log server:app <path to twitter key file>
```
