# --------------------------------------------------------------------------------------
# File: Mid-Term_Project.py
# Name: Amie Davis
# Date: 10/4/2019
# Course: DSC540 - Data Preparation
#
# Purpose: Select and clean a dataset.
#
# Primary Data Source:  Open Source Sports
# Dataset:              Batting.csv
# Link:                 https://www.kaggle.com/open-source-sports/baseball-databank
#
# Reference Data Source:
# Dataset:  BB_Stat_Desc.csv
# Link:     https://www.baseball-reference.com/bullpen/Baseball_statistics
#
# Functions: load_file(), strip_blank_csv(), change_headers(), format_data(),
#            find_missing_data(), rem_bad_data(), find_dups(), fuzzy_match(),
#            write_outfile()
#
# Usage: Uses Python 3.7.
#        Developed using PyCharm 2019.1.3.
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# Function load_file()
#
# Description:  Opens csv file for read and loads into a dictionary.
#
# Parameters:   file_name: name of csv file to open
#
# Returns:      Dictionary reader object
#
def load_file(file_name):

    # Set data directory
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'Data/')
    filepath = data_dir + file_name

    # Open file for read
    try:
        data_file = open(filepath, 'r', encoding='UTF8')
    except:
        print('File cannot be opened.')
        exit()

    # Load into Dictionary Reader object
    dict_reader = csv.DictReader(data_file)
    return dict_reader

# --------------------------------------------------------------------------------------
# Function strip_blank_csv()
#
# Description:  Strips whitespaces from data fields in a csv file.
#               Overwrites existing output file.
#
# Parameters:   in_file: name of input csv file to read
#               out_file: name of output csv file to write
#
# Returns:      No return object.  Output is written to file.
#
def strip_blank_csv(in_file, out_file):

    # Set data directory and file paths
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'Data/')
    in_filepath = data_dir + in_file
    out_filepath = data_dir + out_file

    # If output file exists, create a new file
    if os.path.isfile(out_filepath):
        with open(out_filepath, 'w') as f:
            pass

    # Loop through each line in file and strip whitespaces
    with open(in_filepath, 'r') as reader:
        for line in reader:
            stripped_line = line.strip()

            # Write stripped data to output file
            with open(out_filepath, 'a') as fileHandler:
                fileHandler.write(stripped_line)
                fileHandler.write('\n')

# --------------------------------------------------------------------------------------
# Function change_headers()
#
# Description:  Changes header in data csv file to match headers in reference data csv file.
#
# Parameters:   data_file: csv file in which headers need to be changed
#               header_file: csv file that contains header cross-reference information
#
# Returns:      List of dictionary pairs for each record in file

def change_headers(data_file, header_file):

    # Strip whitespaces from data fields in header file
    new_header_file = header_file + '.new'
    strip_blank_csv(header_file, new_header_file)

    # Open files and load into dictionaries
    data_rdr = load_file(data_file)
    header_rdr = load_file(new_header_file)

    # Load datasets into record lists
    data_rows = [d for d in data_rdr]
    header_rows = [h for h in header_rdr]

    # Loop through each data row to set the keyword to match the header record.
    # Create a new dictionary for each row (new_row) to create a new array (new_rows)
    new_rows = []
    for data_dict in data_rows:
        new_row = {}

        # For each dictionary key-value pair in the list
        for dkey, dval in data_dict.items():

            # Note that spaces remain before and after comma separators in header file,
            # so need to compare data file codes with added space
            new_dkey = dkey + ' '

            # Match any keys that are in the header reference file
            for header_dict in header_rows:
                if new_dkey in header_dict.values():
                    new_row[header_dict.get('Short Description')] = dval

        new_rows.append(new_row)

    # Return list of dictionary pairs for each record in data_file
    return new_rows

# --------------------------------------------------------------------------------------
# Function format_data()
#
# Description:  Formats record list into a readable format.
#
# Parameters:   record_list: List of dictionary pairs representing the dataset
#
# Returns:      List of dictionary pairs for each record in file

def format_data(record_list):

    # Loop through items in the dictionary for each record
    for dict_item in record_list:
        print('\n')
        print('************************************New record******************************************')
        for dkey, dval in dict_item.items():
            print('{}: {}'.format(dkey, dval))

# --------------------------------------------------------------------------------------
# Function find_missing_data()
#
# Description:  Finds missing values.
#
# Parameters:   record_list: List of dictionary pairs representing the dataset
#
# Returns:      No return value.  Missing data returned to screen.

def find_missing_data(record_list):

    # Loop through items in the dictionary for each record
    record_counter = 0
    for dict_item in record_list:

        # Variables to set at the record-level
        record_counter +=1
        rec_year = ''

        # Loops through each key-value pair
        for dkey, dval in dict_item.items():

            # Set year to determine allowable null values
            if dkey == ' Year ':
                rec_year = dval

            # Identify records with missing values
            if not dval or dval is None or  dval == 'NA':
                missing_rpt = 'Y'

                # Discount records with null values based on the year measurement of the specific statistic began
                if dkey == ' Intentional base on balls' and int(rec_year) < 1955:
                    missing_rpt = 'N'
                if dkey == ' Hit by pitch ' and int(rec_year) < 1884:
                    missing_rpt = 'N'
                if dkey == ' Sacrifice hit ' and int(rec_year) < 1895:
                    missing_rpt = 'N'
                if dkey == ' Sacrifice fly ' and int(rec_year) < 1954:
                    missing_rpt = 'N'
                if dkey == ' Grounded into double play ' and int(rec_year) < 1933:
                    missing_rpt = 'N'

                # NA is a valid value for League
                if dkey == ' League ' and dval == 'NA':
                    missing_rpt = 'N'

                # If not a known exception, include on output for review
                if missing_rpt == 'Y':
                    print('Missing value in record number {} for the{} field.'.format(record_counter,dkey))

# --------------------------------------------------------------------------------------
# Function find_bad_data()
#
# Description:  Finds bad data.
#
# Parameters:   record_list: List of dictionary pairs representing the dataset
#
# Returns:      No return value.  Bad data returned to screen.

def find_bad_data(record_list):

    # Loop through items in the dictionary for each record
    record_counter = 0
    for dict_item in record_list:

        # Variables to set at the record-level
        record_counter += 1

        # Loop through each key-value pair
        for dkey, dval in dict_item.items():

            # Look for records without valid At Bat (AB) values
            # Only want to analyze hitting statistics for players who have been at bat.
            if dkey == ' At bat ' and (not dval or int(dval) < 1):
                print('Not enough at bats in record number {}.'.format(record_counter))

            # Check for bad data types
            if dkey != ' Player ID code' and dkey != ' Team ' and dkey != ' League ':
                if dval and not dval.isdigit():
                    print('Invalid numeric data type in record number {}.'.format(record_counter))

# --------------------------------------------------------------------------------------
# Function find_dups()
#
# Description:  Identifies Duplicate Records.
#               Record should be unique to player_id, year, stint
#
# Parameters:   record_list: List of dictionary pairs representing the dataset
#
# Returns:      No return value.  Bad data returned to screen.

def find_dups(record_list):

    # Loop through items in the dictionary for each record
    record_counter = 0
    data_dict = {}
    for dict_item in record_list:

        # Variables to set at the record-level
        record_counter += 1

        # Combine key fields to make unique key.
        key = '%s-%s-%s' % (dict_item.get(' Player ID code'), dict_item.get(' Year '), dict_item.get(' Stint '))

        # Append each unique key to a dictionary
        if key in data_dict.keys():
            data_dict[key].append(dict_item)
        else:
            data_dict[key] = [dict_item]

    # Outputs the unique number of keys
    # If the number of unique keys matches the number of records in the dataset, there are no duplicate records.
    print(len(data_dict))

# --------------------------------------------------------------------------------------
# Function fuzzy_match()
#
# Description:  Performs fuzzy matching categorical column.
#
# Parameters:   record_list: List of dictionary pairs representing the dataset
#
# Returns:      No return value. Matching results output to screen.

def fuzzy_match(record_list):

    # Loop through items in the dictionary for each record
    match_list = []
    for dict_item in record_list:

        # Loop through each key-value pair
        for dkey, dval in dict_item.items():

            # Add values for the position category to a list
            if dkey == ' Position ':
                match_list.append(dval)

    # Loop through sequential position values to compute a fuzzy match score
    for i in range(0,len(match_list)):
        print('The fuzzy ratio between {} and {} is {}.'.format(match_list[i],match_list[i+1],
                                                                 fuzz.ratio(match_list[i],match_list[i+1])))

# --------------------------------------------------------------------------------------
# Function rem_bad_data()
#
# Description:  Removes data identified as "bad."
#
# Parameters:   record_list: List of dictionary pairs representing the dataset
#
# Returns:      upd_record_list: The updated record list with bad records removed.

def rem_bad_data(record_list):

    # Loop through items in the dictionary for each record
    new_rows = []
    for dict_item in record_list:
        new_row = {}

        # Variables to set at the record-level
        record_keep = 'N'

        # Loop through each key-value pair
        for dkey, dval in dict_item.items():

            # Only include batting records without at least one At Bat (AB)
            if dkey == ' At bat ' and (dval and int(dval) >= 1):
                record_keep = 'Y'

            new_row[dkey] = dval

        if record_keep == 'Y':
            new_rows.append(new_row)

    # Return updated list of dictionary pairs for each record in data_file
    return new_rows

# --------------------------------------------------------------------------------------
# Function write_outfile()
#
# Description:  Writes updated record list to a new csv file.
#
# Parameters:   record_list: List of dictionary pairs representing the dataset
#               out_file: name of output csv file
#
# Returns:      No return value.  Output is written to a file.
#
def write_outfile(record_list, out_file):

        # Set data directory and file paths
        dirname = os.path.dirname(__file__)
        data_dir = os.path.join(dirname, 'Data/')
        out_filepath = data_dir + out_file

        # Open file for write and output each record
        with open(out_filepath, 'w') as fileHandler:
            fileHandler.writelines(["%s\n" % item for item in record_list])

# --------------------------------------------------------------------------------------
# Main function
#
# Description: Select and clean a dataset.
#
def main():

    # Identify data files
    # Use smaller file with less records for testing.  Decreases processing time while troubleshooting.
    # data_file = 'Batting_Short.csv'
    data_file = 'Batting.csv'
    header_file = 'BB_Stat_Desc.csv'

    # Replace headers in data file
    record_list = change_headers(data_file, header_file)

    # Format record list into a readable format
    # Uncomment to review output to screen
    # format_data(record_list)

    # Find missing data
    # Uncomment to analyze
    # find_missing_data(record_list)

    # Find bad data
    # Uncomment to analyze
    # find_bad_data(record_list)

    # Find Duplicates
    # Uncomment to analyze
    # find_dups(record_list)

    # Find fuzzy matches
    # Uncomment to analyze
    # fuzzy_match(record_list)

    # Remove bad data
    upd_record_list = rem_bad_data(record_list)

    # Output updated data file
    write_outfile(upd_record_list,'Updated_Batting.txt')

# --------------------------------------------------------------------------------------
# Run program

# Import libraries used
import os, csv
from fuzzywuzzy import fuzz

main()
