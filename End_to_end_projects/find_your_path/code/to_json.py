
# coding: utf-8

# In[204]:

import json
import os

from pprint import pprint
import pandas as pd

source_file = '../Data/Profile_DFs/'
destination_folder = '../Data/Resume_cleaned/'


titles = ['architect',
          'auditor',
          'business strategist',
          'recruiter',
          'software architect',
          'vp of engineering',
          'vp of marketing',
          'vp of operations',
          'analyst',
          'strategist',
          'associate'
          'manager',
          'director',
          'engineer',
          'associate',
          'scientist']


def job_extract(folder_profile_df, titles, destination_folder):
    """
    :param folder_profile_df: This folder consist of all the files parsed
                              from Indeed for different profiles
    :param titles: list of all the titles to be extracted
    :param destination_folder: This folder consist is the destination where
                               the extracted data will be saved in teh form
                               of multiple files
    :return: saves the extracted data in the destination folder
    """

    user_detail_dict = {}
    user_detail_list = []

    with open(destination_folder + "json_resume.json", 'w') as outfile:
        for file_item in os.listdir(source_file):
            raw_text = pd.read_csv(source_file + str(file_item))

            data = {}
            for index, row in raw_text.iterrows():

                d = {}
                d['id'] = str(row['resume'].split('/')[-1])
                data['user'] = d

                job = {}
                job_list = []

                # get job from work_experience
                v = row['work_exp'].lower()[1:].split(",")
                v = [item.split("\\n") for item in v]
                v = [item for sublist in v for item in sublist]
                j = {}
                ct, k = 0, 0
                for item in v:
                    j = {}
                    ct = ct + 1
                    if any(title in item for title in titles) and len(
                            item) < 50:
                        k = k + 1
                        j['title'] = item.strip().replace(
                            "u'", "")  # extracted job title

                        # extracting year from jobs
                        try:
                            if any(char.isdigit() for char in v[ct + 1]):
                                j['year'] = v[ct + 1].strip().\
                                    replace("'", "").\
                                    replace("]", "").replace("[", "")
                            elif any(char.isdigit() for char in v[ct + 2]):
                                j['year'] = v[ct + 2].strip().\
                                    replace("'", "").\
                                    replace("]", "").replace("[", "")
                            else:
                                j['year'] = "NA"
                        except BaseException:
                            j['year'] = "NA"

                        j['is_job'] = 'Y'
                        job_list.append(j)

                # get degrees from education
                degrees = row["education_json"].split(",")
                years = row['univ'].replace(
                    "'", "").replace(
                    'u', '').replace(
                    '[', '').replace(
                    ']', '').split("\\n")[
                    1:]

                if len(years) == 0:
                    j = {}
                    for i in range(len(degrees)):
                        j['title'] = degrees[i].strip().replace(
                            "degree_%s : " % str(i + 1), "")
                        j['year'] = 'NA'
                        j['is_job'] = 'N'
                        job_list.append(j)
                else:
                    j = {}
                    for i in range(len(degrees)):
                        j['title'] = degrees[i].strip().replace(
                            "degree_%s : " % str(i + 1), "")
                        try:
                            j['year'] = years[i].split(",")[0].replace('"', '')
                        except BaseException:
                            j['year'] = "NA"
                        j['is_job'] = 'N'
                        job_list.append(j)

                data['Experience'] = job_list
                user_detail_list.append(data)

        user_detail_dict['user_details'] = user_detail_list
        json.dump(user_detail_dict, outfile)


job_extract(source_file, titles, destination_folder)
