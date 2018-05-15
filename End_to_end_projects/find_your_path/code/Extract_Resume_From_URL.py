

import time
from selenium import webdriver
import pandas as pd


if __name__ == '__main__':

    """
        Given a list of files with resume url,
        this code parses the files
        and stores the information from resumes into csv
    """

    txt_file = '../Data/Profile_URLs/Architect.txt'

    resume_list = open(txt_file).read().splitlines()

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    work_exp_list = []
    education = []
    university = []

    architect_resume = pd.DataFrame()
    # architect_resume.columns = ['work_experience', 'education', 'university']

    i = 1
    for resume in resume_list:
        i += 1
        driver.get(resume)

        individual_work_exp = []
        for e in driver.find_elements_by_class_name("rezemp-WorkExperience"):
            individual_work_exp.append(e.text)
        work_exp_list.append(individual_work_exp)

        individual_education = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-itemTitle"):
            individual_education.append(e.text)
        education.append(individual_education)

        individual_university = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-university"):
            individual_university.append(e.text)
        university.append(individual_university)

        table = [
            resume,
            individual_work_exp,
            individual_education,
            individual_university]
        df = pd.DataFrame(table)
        df = df.transpose()
        df.columns = ['resume', 'work_exp', 'edu', 'univ']

        architect_resume = architect_resume.append(df)

    # In[81]:

    architect_resume.to_csv('../Data/Profile_DFs/architect_resume.csv')

    #     Auditor

    # In[83]:

    txt_file = '../Data/Profile_URLs/Auditor.txt'

    resume_list = open(txt_file).read().splitlines()

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    work_exp_list = []
    education = []
    university = []

    auditor_resume = pd.DataFrame()
    # architect_resume.columns = ['work_experience', 'education', 'university']

    i = 1
    for resume in resume_list:
        i += 1
        driver.get(resume)

        individual_work_exp = []
        for e in driver.find_elements_by_class_name("rezemp-WorkExperience"):
            individual_work_exp.append(e.text)
        work_exp_list.append(individual_work_exp)

        individual_education = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-itemTitle"):
            individual_education.append(e.text)
        education.append(individual_education)

        individual_university = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-university"):
            individual_university.append(e.text)
        university.append(individual_university)

        table = [
            resume,
            individual_work_exp,
            individual_education,
            individual_university]
        df = pd.DataFrame(table)
        df = df.transpose()
        df.columns = ['resume', 'work_exp', 'edu', 'univ']

        auditor_resume = auditor_resume.append(df)

    # In[84]:

    auditor_resume.to_csv('../Data/Profile_DFs/auditor_resume.csv')

    #     Business Analyst

    # In[85]:

    txt_file = '../Data/Profile_URLs/Business Analyst.txt'

    resume_list = open(txt_file).read().splitlines()

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    work_exp_list = []
    education = []
    university = []

    business_analyst_resume = pd.DataFrame()
    # architect_resume.columns = ['work_experience', 'education', 'university']

    i = 1
    for resume in resume_list:
        i += 1
        driver.get(resume)

        individual_work_exp = []
        for e in driver.find_elements_by_class_name("rezemp-WorkExperience"):
            individual_work_exp.append(e.text)
        work_exp_list.append(individual_work_exp)

        individual_education = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-itemTitle"):
            individual_education.append(e.text)
        education.append(individual_education)

        individual_university = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-university"):
            individual_university.append(e.text)
        university.append(individual_university)

        table = [
            resume,
            individual_work_exp,
            individual_education,
            individual_university]
        df = pd.DataFrame(table)
        df = df.transpose()
        df.columns = ['resume', 'work_exp', 'edu', 'univ']

        business_analyst_resume = business_analyst_resume.append(df)

    # In[86]:

    business_analyst_resume.to_csv(
        '../Data/Profile_DFs/business_analyst_resume.csv')

    #     Business Strategist

    # In[87]:

    txt_file = '../Data/Profile_URLs/Business Strategist.txt'

    resume_list = open(txt_file).read().splitlines()

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    work_exp_list = []
    education = []
    university = []

    business_strategist_resume = pd.DataFrame()
    # architect_resume.columns = ['work_experience', 'education', 'university']

    i = 1
    for resume in resume_list:
        i += 1
        driver.get(resume)

        individual_work_exp = []
        for e in driver.find_elements_by_class_name("rezemp-WorkExperience"):
            individual_work_exp.append(e.text)
        work_exp_list.append(individual_work_exp)

        individual_education = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-itemTitle"):
            individual_education.append(e.text)
        education.append(individual_education)

        individual_university = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-university"):
            individual_university.append(e.text)
        university.append(individual_university)

        table = [
            resume,
            individual_work_exp,
            individual_education,
            individual_university]
        df = pd.DataFrame(table)
        df = df.transpose()
        df.columns = ['resume', 'work_exp', 'edu', 'univ']

        business_strategist_resume = business_strategist_resume.append(df)

    # In[88]:

    business_strategist_resume.to_csv(
        '../Data/Profile_DFs/business_strategist_resume.csv')

    #     Data Analyst

    # In[89]:

    txt_file = '../Data/Profile_URLs/Data Analyst.txt'

    resume_list = open(txt_file).read().splitlines()

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    work_exp_list = []
    education = []
    university = []

    data_analyst_resume = pd.DataFrame()

    i = 1
    for resume in resume_list:
        i += 1
        driver.get(resume)

        individual_work_exp = []
        for e in driver.find_elements_by_class_name("rezemp-WorkExperience"):
            individual_work_exp.append(e.text)
        work_exp_list.append(individual_work_exp)

        individual_education = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-itemTitle"):
            individual_education.append(e.text)
        education.append(individual_education)

        individual_university = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-university"):
            individual_university.append(e.text)
        university.append(individual_university)

        table = [
            resume,
            individual_work_exp,
            individual_education,
            individual_university]
        df = pd.DataFrame(table)
        df = df.transpose()
        df.columns = ['resume', 'work_exp', 'edu', 'univ']

        data_analyst_resume = data_analyst_resume.append(df)

    # In[90]:

    data_analyst_resume.to_csv('../Data/Profile_DFs/data_analyst_resume.csv')

    #     Data Engineer

    # In[91]:

    txt_file = '../Data/Profile_URLs/Data Engineer.txt'

    resume_list = open(txt_file).read().splitlines()

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    work_exp_list = []
    education = []
    university = []

    data_engineer_resume = pd.DataFrame()

    i = 1
    for resume in resume_list:
        i += 1
        driver.get(resume)

        individual_work_exp = []
        for e in driver.find_elements_by_class_name("rezemp-WorkExperience"):
            individual_work_exp.append(e.text)
        work_exp_list.append(individual_work_exp)

        individual_education = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-itemTitle"):
            individual_education.append(e.text)
        education.append(individual_education)

        individual_university = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-university"):
            individual_university.append(e.text)
        university.append(individual_university)

        table = [
            resume,
            individual_work_exp,
            individual_education,
            individual_university]
        df = pd.DataFrame(table)
        df = df.transpose()
        df.columns = ['resume', 'work_exp', 'edu', 'univ']

        data_engineer_resume = data_engineer_resume.append(df)

    # In[92]:

    data_engineer_resume.to_csv('../Data/Profile_DFs/data_engineer_resume.csv')

    #     Data Scientist

    # In[93]:

    txt_file = '../Data/Profile_URLs/Data Scientist.txt'

    resume_list = open(txt_file).read().splitlines()

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    work_exp_list = []
    education = []
    university = []

    data_scientist_resume = pd.DataFrame()

    i = 1
    for resume in resume_list:
        i += 1
        driver.get(resume)

        individual_work_exp = []
        for e in driver.find_elements_by_class_name("rezemp-WorkExperience"):
            individual_work_exp.append(e.text)
        work_exp_list.append(individual_work_exp)

        individual_education = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-itemTitle"):
            individual_education.append(e.text)
        education.append(individual_education)

        individual_university = []
        for e in driver.find_elements_by_class_name(
                "rezemp-ResumeDisplay-university"):
            individual_university.append(e.text)
        university.append(individual_university)

        table = [
            resume,
            individual_work_exp,
            individual_education,
            individual_university]
        df = pd.DataFrame(table)
        df = df.transpose()
        df.columns = ['resume', 'work_exp', 'edu', 'univ']

        data_scientist_resume = data_scientist_resume.append(df)

    # In[94]:

    data_scientist_resume.to_csv(
        '../Data/Profile_DFs/data_scientist_resume.csv')

    # In[97]:

    job_titles = [
        'Software Architect', 'Human Resource Manager', 'Recruiter',
        'Marketing Director']

    # In[98]:

    for f in job_titles:
        txt_file = '../Data/Profile_URLs/' + f + '.txt'
        print txt_file

        resume_list = open(txt_file).read().splitlines()

        driver = webdriver.Chrome('/usr/local/bin/chromedriver')

        work_exp_list = []
        education = []
        university = []

        output_df = pd.DataFrame()

        i = 1
        for resume in resume_list:
            i += 1
            driver.get(resume)

            individual_work_exp = []
            for e in driver.find_elements_by_class_name(
                    "rezemp-WorkExperience"):
                individual_work_exp.append(e.text)
            work_exp_list.append(individual_work_exp)

            individual_education = []
            for e in driver.find_elements_by_class_name(
                    "rezemp-ResumeDisplay-itemTitle"):
                individual_education.append(e.text)
            education.append(individual_education)

            individual_university = []
            for e in driver.find_elements_by_class_name(
                    "rezemp-ResumeDisplay-university"):
                individual_university.append(e.text)
            university.append(individual_university)

            table = [
                resume,
                individual_work_exp,
                individual_education,
                individual_university]
            df = pd.DataFrame(table)
            df = df.transpose()
            df.columns = ['resume', 'work_exp', 'edu', 'univ']

            output_df = output_df.append(df)

        output_df.to_csv('../Data/Profile_DFs/' + f + '.csv')

    # In[ ]:
