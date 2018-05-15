
# coding: utf-8

# In[122]:

import pandas as pd
import json
import regex as re
import datefinder


def degree_json(education):
    """
    :param education: is a string of educations of a profile
    :return: the json blob for education in chronological order
    """
    i = 1
    degree_json_list = []
    for degree in education:
        degree_json_list.append(
            'degree_' +
            str(i) +
            " : " +
            degree.replace(
                "'",
                "").replace(
                'u',
                '').replace(
                '[',
                '').replace(
                    ']',
                ''))
        i += 1
    return (', ').join(degree_json_list)


if __name__ == '__main__':
    resume_list = ['Engineering Manager.csv', 'Software Engineer.csv',
                   'Finance Manager.csv', 'VP of Engineering.csv',
                   'Financial Analyst.csv', 'VP of Marketing.csv',
                   'Human Resource Manager.csv', 'VP of Operations.csv',
                   'Marketing Director.csv', 'architect_resume.csv',
                   'Operation Analyst.csv', 'auditor_resume.csv',
                   'Operation Manager.csv', 'business_analyst_resume.csv',
                   'Product Manager.csv', 'business_strategist_resume.csv',
                   'Recruiter.csv', 'data_analyst_resume.csv',
                   'Sales Associate.csv', 'data_engineer_resume.csv',
                   'Sales Manager.csv', 'data_scientist_resume.csv',
                   'Software Architect.csv']

    resume['education_json'] = resume['edu'].apply(
        lambda x: degree_json(x.split(',')))

    for f in resume_list:
        txt_file = '../Data/Profile_DFs/' + f
        print txt_file

        resume = pd.read_csv(txt_file, index_col=0)
        resume['education_json'] = resume['edu'].apply(
            lambda x: degree_json(x.split(',')))

        resume.to_csv(txt_file)
