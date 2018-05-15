
# coding: utf-8

# In[3]:

from pymongo import MongoClient  # Install for using this lib.
import subprocess


def import_query(dbname, collection_name, input_file_name):
    """
    create mongodb
    """
    mongoimport_query = 'mongoimport --db ' + dbname + \
        ' --collection ' + collection_name + ' ' + input_file_name
    return mongoimport_query


if __name__ == '__main__':
    dbname = 'find_your_path'
    collection_name = 'Resumes'
    input_file_name = 'Data/Resume_cleaned/sample_resume.json'

    # Create connection
    client = MongoClient()  # default-localhost:27017
    # Connect to database
    db = client[dbname]

    # Drop table of exist
    db[collection_name].drop()

    # Insert data from the input_file_name.
    mongoimport_query = import_query(dbname, collection_name, input_file_name)
    subprocess.call(mongoimport_query, shell=True)

    client.close()
