Find Your Path Tutorial
=======================

Environment Setup:

1. Before you can create a virtual environment, you must first pip install the virtualenv package. Then you can create a virtual Python 3 environment and subsequently source activate it so it may be used on your machine. 
2. Pip install any relevant packages for your project so they are available in your environment.
3. Freeze the installations and save them to a text file so collaborators can easily install them from the file. 

1. Before you can create a virtual environment, you must first pip install the virtualenv package. Then you can create a virtual Python 3 environment and subsequently source activate it so it may be used on your machine. 
2. Pip install any relevant packages for your project so they are available in your environment.
3. Freeze the installations and save them to a text file so collaborators can easily install them from the file. 

Data Acquisition Process:

1. First we make a list of all the job titles that we want to target. This includes jobs from 'Data Scientist', 'Architect' to 'Finance Manager' and 'VP of Sales'
2. Scrape websites (primarily Indeed.com) for approximately 500 resumes per role in URL_extraction.py 
3. Using Selenium, reformat the resumes into CSVs in Extract_Resume_From_URL.py
4. Extract relevant information from the resumes by parsing them with regular expressions in Resume_Extract_Education.py and Resume_Extract_Work_Experience.py. The focus is on the following components: list of degrees earned, areas they were earned, job titles, and constructing a timeline to fit the pieces together. 
5. All information parsed from the resume is stored in dataframes, with one for each job type. 

Storage Process:

1. Create and configure MongoDB database using pymongo (MongoDB_create.py)
2. Upload/import data to MongoDB database (upload_data_to_MongoDB.py)
3. We are currently experimenting with a web-page as well as a slack application. Scripts to create both are also present (flask_server.py, script.js)
4. Update the database as necessary during deployment to AWS (deploy.py)

Pipeline:

1. First we make a list of all the job titles that we want to target. This includes jobs from 'Data Scientist', 'Architect' to 'Finance Manager' and 'VP of Sales'
2. Scrape websites (primarily Indeed.com) for approximately 500 resumes per role in URL_extraction.py 
3. Using Selenium, reformat the resumes into CSVs in Extract_Resume_From_URL.py
4. Extract relevant information from the resumes by parsing them with regular expressions in Resume_Extract_Education.py and Resume_Extract_Work_Experience.py. The focus is on the following components: list of degrees earned, areas they were earned, job titles, and constructing a timeline to fit the pieces together. 
5. All information parsed from the resume is stored in dataframes, with one for each job type. 

