# --------------------------------------------------------------------------------------
# File: Exercise_4.2.py
# Name: Amie Davis
# Date: 9/17/2019
# Course: DSC540 - Data Preparation
# Assignment Number: 4.2
#
# Description: Working with PDFs and Setting up a database.
#
# Usage: Uses Python 3.7.
#        Developed using PyCharm 2019.1.3.
#
# --------------------------------------------------------------------------------------
# Part One: Convert PDF into readable format.
#
# Problem 1:    Errors installing the slate package.
# Conclusion:   slate and pdfminer packages are not compatible with Python v3.
#               In lieu of reverting to Paython v2, I elected to use the tabula package instead.
#               Reference: https://blog.chezo.uno/tabula-py-extract-table-from-pdf-into-python-dataframe-6c7acfa5f302
#               To install tabula: pip install tabula-py
#
# Problem 2:    Unable to open files with tabula
# Conclusion:   Requires java installation.
#               Installed Java and added java path to path environment variable.
#
# Problem 3:    Tabula not showing countries
# Conclusion:   Tabula thinks there are lines for a spreadsheet.
#               Added stream=True option.
# --------------------------------------------------------------------------------------
# Import libraries used
import os
from tabula import read_pdf, convert_into

# Set data directory
dirname = os.path.dirname(__file__)
data_dir = os.path.join(dirname, 'DW Code/data-wrangling-master/data/chp5/')

# Renamed data source file to remove blank spaces.
# Opens pdf file for read into a dataframe
file_name = file_name = data_dir + 'EN-FINAL Table 9.pdf'
try:
    df = read_pdf(file_name, stream=True)
except:
    print('File cannot be opened.')
    exit()

#print(df)
# Outputs only 21 rows and 2 columns.

# Convert PDF into CSV.
# stream=True to capture 1st column
# Set ares to exclude rows after the countries
#convert_into(file_name, "output.csv", output_format="csv", pages='all', stream=True, area=(30, 0, 170, 1000))
# The resulting csv includes all country records, but is still pretty garbled.

# --------------------------------------------------------------------------------------
# Part Two: Setup a local database and load in a dataset
#
# SQLite installed.
# First install dataset package with pip
#
# Using dataset from Canadian Cybersecurity group referenced in this week's discussion item.
# TimeBasedFeatures-Dataset-15s.csv
# Edited header meanually.

# Import libraries used
import csv, dataset

# Open sqllite database connection
db = dataset.connect('sqlite:///data_wrangling.db')

# Create table to store data
table = db['vpn_data']

# Opens csv file for read
data_dir2 = os.path.join(dirname, 'Data/')
file_name2 = data_dir2 + 'TimeBasedFeatures-Dataset-15s.csv'

try:
    csv_file = open(file_name2, 'r')
except:
    print('File cannot be opened.')
    exit()

# Load dataset into a Python dictionary
reader = csv.DictReader(csv_file)

for row in reader:
#    print(dict(row))

    # Insert dataset into table
    table.insert(dict(row))



