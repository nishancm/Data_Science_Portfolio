# Introduction

This python script helps to load BART data avaiable [here](https://www.bart.gov/about/reports/ridership) in to a local PostgreSQL database. Script will perform following tasks

* Extract the downloaded BART zip files
* Get the ridership information required from each Excel workbook and reshape the data in to a long format
* Store the data in a PostgreSQL database
