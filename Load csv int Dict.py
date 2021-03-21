# --------------------------------------------------------------------------------------
# File: Exercise_6.2.py
# Name: Amie Davis
# Date: 10/2/2019
# Course: DSC540 - Data Preparation
# Assignment Number: 6.2
#
# Purpose: Reads a data file into a set of ordered dictionaries.
#          Cross-references file headers (now dictionary keys) with interview questions from a separate file.
#          Formats results into a readable question and answer format.
#          Created function for reusable code, to demonstrate coding best practices.
#
# Data Source: UNICEF
# Data Set: Multiple Indicator Cluster Surveys (MICS)
#
# Usage: Uses Python 3.7.
#        Developed using PyCharm 2019.1.3.
# --------------------------------------------------------------------------------------
# Problem:    codec traceback error thrown at various lines reading header file.
# Solution:   Added encoding='UTF8' to file read statement.
# --------------------------------------------------------------------------------------
# Import libraries used
import os, csv

# --------------------------------------------------------------------------------------
# Function load_file()
#
# Description:  Opens csv file for read and loads into a dictionary.
#
# Parameters:   file_name: name of csv file to open
#
# Returns: Dictionary reader object
#
def load_file(file_name):

    # Set data directory
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'DW Code/data-wrangling-master/data/unicef/')
    filepath = data_dir + file_name

    try:
        data_file = open(filepath, 'r', encoding='UTF8')
    except:
        print('File cannot be opened.')
        exit()

    # Load into Dictionary Reader object
    dict_reader = csv.DictReader(data_file)
    return dict_reader

# --------------------------------------------------------------------------------------
# Open data file and load into dictionary
# Use smaller file with less records for testing.  Decreases processing time while troubleshooting.
#data_rdr = load_file('mn_short.csv')
data_rdr = load_file('mn.csv')

# 1 - Fixing Labels/Headers
# Header definitions are found in mn_headers.csv
# Open header csv file and load into dictionary
header_rdr = load_file('mn_headers_updated.csv')

# Load both datasets into record lists
data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr]

#print(data_rows[:5])
#print(header_rows[:5])

# Loop through each data row to set the keyword to match the header record.
# Create a new dictionary for each row (new_row) to create a new array (new_rows)
new_rows = []
for data_dict in data_rows:
    new_row = {}
    for dkey, dval in data_dict.items():
        for header_dict in header_rows:
            if dkey in header_dict.values():
                new_row[header_dict.get('Label')] = dval
    new_rows.append(new_row)
#print(new_rows[0])
#print(new_rows)

# 2 - Make the output readable using the format function
# Loop through Q&A items in the dictionary for each record
for interview_dict in new_rows:
    print('************************************New interview******************************************')
    for dkey, dval in interview_dict.items():

# 3 - Format the dates to determine when the interview started and ended.
# Assign better variable names to datetime elements for readability
# Print datetime values after last time stamp
        if dkey == 'Day of interview':
            int_day = dval
        elif dkey == 'Month of interview':
            int_mth = dval
        elif dkey == 'Year of interview':
            int_yr = dval
        elif dkey == 'Start of interview - Hour':
            start_hr = dval
        elif dkey == 'Start of interview - Minutes':
            start_min = dval
        elif dkey == 'End of interview - Hour':
            end_hr = dval
        elif dkey == 'End of interview - Minutes':
            end_min = dval
            print('\n')
            print('Interview started at {}/{}/{} {}:{}, and ended at {}:{}.'.format(int_mth, int_day, int_yr,
                start_hr, start_min, end_hr, end_min))

        # Print question and answer for all non-datetime fields
        else:
            print('\n')
            print('Question: {}\nAnswer: {}'.format(dkey, dval))
