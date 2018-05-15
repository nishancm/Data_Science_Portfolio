import numpy as np
import pandas as pd
import os


def job_extract(folder_profile_df, titles, destination_folder):
    """
    :param folder_profile_df: This folder consist of all the files parsed
                              from Indeed for different profiles
    :param titles: list of all the titles to be extracted
    :param destination_folder: This folder consist is the destination where
                               the extracted data will be saved in the form
                               of multiple files
    :return: saves the extracted data in the destination folder
    """

    with open(destination_folder + "data_extraction.json", 'w') as outfile:

        for file_item in os.listdir(folder_profile_df):
            raw_text = pd.read_csv(folder_profile_df + str(file_item))
            data = {}
            data["Job_Title"] = file_item.replace("_resume.csv", "")
            for i in range(raw_text.shape[0]):
                work_exp_example = raw_text["work_exp"][i]
                v = work_exp_example.lower()[1:].split(",")
                v = [item.split("\\n") for item in v]
                v = [item for sublist in v for item in sublist]
                data["userID"] = (
                    file_item +
                    "_" +
                    str(i)).replace(
                    "_resume.csv",
                    "")
                data["Experience"] = {}
                ct, k = 0, 0
                for item in v:
                    ct = ct + 1
                    if any(title in item for title in titles) and len(
                            item) < 50:
                        k = k + 1
                        data["Experience"]["job" + str(k)] = {}
                        data["Experience"]["job" + str(k)]["designation"] = \
                            item.strip()
                        try:
                            if any(char.isdigit() for char in v[ct + 1]):
                                data["Experience"]["job" + str(k)]["year"] = \
                                    v[ct + 1].strip()
                            elif any(char.isdigit() for char in v[ct + 2]):
                                data["Experience"]["job" + str(k)]["year"] = \
                                    v[ct + 2].strip()
                            else:
                                data["Experience"]["job" + str(k)]["year"] = \
                                    "Year_Not_Found"
                        except BaseException:
                            data["Experience"]["job" +
                                               str(k)]["year"] = "Error"

                data["Education"] = {}
                degrees = raw_text["education_json"][i].split(",")
                years = raw_text["univ"][i].replace("'", "").replace('u', '').\
                    replace('[', '').replace(']', '').split("\\n")[1:]

                if len(degrees) == 0:
                    data["Education"] = "degree not found"

                elif len(years) == 0:
                    for i in range(len(degrees)):
                        data["Education"]["degree" + str(i + 1)] = \
                            degrees[i].strip().replace("degree_%s : " %
                                                       str(i + 1), "")
                        data["Education"]["year" + str(i + 1)] = \
                            "Year not found"

                else:
                    for i in range(len(degrees)):
                        data["Education"]["degree" + str(i + 1)] = \
                            degrees[i].strip().replace("degree_%s : " %
                                                       str(i + 1), "")
                        try:
                            data["Education"]["year" + str(i + 1)] = \
                                years[i].split(",")[0].replace('"', '')
                        except BaseException:
                            data["Education"]["year" + str(i + 1)] = \
                                "Year not found"
                outfile.write("%s\n" % data)


if __name__ == '__main__':
    # These are the titles being parsed
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

    folder_profile_df = "../Data/Profile_DFs/"
    destination_folder = "../Data/Resume_cleaned/"
    job_extract(folder_profile_df, titles, destination_folder)
