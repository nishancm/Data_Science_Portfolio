# install pymongo to access from python --> python -m pip install pymongo

from pymongo import MongoClient  # Install for using this lib.
import subprocess


def import_query(dbname, collection_name, input_file_name):
    """produce mongodb import query for given database, collection,
    and input file

    input
    -----
    dbname: (str) name of database to connect to
    collection_name: (str) name of collection within database
    input_file_name: (str) name of input file

    output
    -----
    mongoimport_query: fully-formed query for mongodb with given
    database name, collection name, input file name
    """
    mongoimport_query = 'mongoimport --db ' + dbname + \
                        ' --collection ' + collection_name + \
                        ' ' + input_file_name
    return mongoimport_query


if __name__ == '__main__':

    dbname = 'find_your_path'
    collection_name = 'Resumes'
    input_file_name = '/home/ec2-user/findyourpath/Data/\
                       Resume_cleaned/data_extraction.json'

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
