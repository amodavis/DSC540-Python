# --------------------------------------------------------------------------------------
# File: Exercise_3.2.py
# Name: Amie Davis
# Date: 9/13/2019
# Course: DSC540 - Data Preparation
# Assignment Number: 3.2
#
# Usage: Uses Python 3.7.
#        Developed using PyCharm 2019.1.3.
#
# --------------------------------------------------------------------------------------
# Import libraries used
import os, csv, json, xlrd
from xml.etree import ElementTree as ET

# Set data directory
dirname = os.path.dirname(__file__)
data_dir3 = os.path.join(dirname, 'DW Code/data-wrangling-master/data/chp3/')

# 1 - Using Python, import the CSV file provided under Chapter 3 in the GitHub repository
#     using the csv library. Put the data in lists and print each record on its own dictionary
#     row (Hint: Page 51-52 of Data Wrangling with Python)

# Opens csv file for read
file_name = data_dir3 + 'data-text.csv'
try:
    csv_file = open(file_name, 'r')
except:
    print('File cannot be opened.')
    exit()

# Exports each row as a dictionary
# Note that with Python 3.6, DictReader now outputs a Ordered Dictionary
# Use dict() to output in a standard dictionary format
reader = csv.DictReader(csv_file)
for row in reader:
#    print(dict(row))
    pass

# --------------------------------------------------------------------------------------
# 2 - Using Python, import the JSON file provided in the GitHub repository under Chapter 3.
#     Print each record on its own dictionary row (Hint: page 53-54 of Data Wrangling with
#     Python).

# Opens json file for read
file_name = data_dir3 + 'data-text.json'
try:
    json_file = open(file_name, 'r')
except:
    print('File cannot be opened.')
    exit()

# Exports each row as a dictionary
json_data = json.load(json_file)
for item in json_data:
    print(item)

# --------------------------------------------------------------------------------------
# 3 - Using Python, import the XML file provided in the GitHub repository under Chapter 3.
# Print each record in its own dictionary row (Hint: page 64 of Data Wrangling with Python).

file_name = data_dir3 + 'data-text.xml'

# Parse xml file
tree = ET.parse(file_name)
root = tree.getroot()

# Review Element objects from XML
# print(list(root))
# Note 'Data' objects
xml_data = root.find('Data')

# print(list(xml_data))
# Note 'Observation' objects

# Loop through each XML Element
for observation in xml_data:

    # Initialize list for each observation record
    rec_dict = {}

    for item in observation:

        # Shows keywords
        # print(item.attrib.keys())

        # attrib.keys returns a dict_keys object.
        # Convert to list, so you can index
        lookup_key_lst = list(item.attrib.keys())
        lookup_key = lookup_key_lst[0]

        # Find keys and their values
        if lookup_key == 'Numeric':
            # Get Value from the Numeric attribute.  No label is provided for the Numeric attribute.
            xml_key = 'NUMERIC'
            xml_value = item.attrib['Numeric']
        else:
            # Get the keyword from the Category attribute and Value from the Code attribute
            xml_key = item.attrib[lookup_key]
            xml_value = item.attrib['Code']

        # Dictionary of Key Value Pairs
        data_dict = {}
        data_dict[xml_key] = xml_value
        # print(data_dict)

        # Append each item together in a dictionary
        rec_dict.update(data_dict)

    # Print each record
    print(rec_dict)

# --------------------------------------------------------------------------------------
# 4 - Using Python, import the Excel file provided in the GitHub repository under Chapter 4.
# Print each record in its own dictionary row. (Hint: page 85-88 of Data Wrangling with Python).

data_dir4 = os.path.join(dirname, 'DW Code/data-wrangling-master/data/chp4/')
file_name = data_dir4 + 'SOWC 2014 Stat Tables_Table 9.xlsx'

# Open Excel Workbook
try:
    book = xlrd.open_workbook(file_name)
except:
    print('File cannot be opened.')
    exit()

# Find Sheet Names
# for sheet in book.sheets():
#    print(sheet.name)

sheet = book.sheet_by_name('Table 9 ')
count = 0
data = {}

# Loop through rows with Countries
for i in range(14, 211):

    row = sheet.row_values(i)

    # Print row number for testing
    # print(i,row)

    # Get Country from the first column
    country = row[1]

    # Retrieving Child Labor, Child Marriage, and Birth Registration rows
    data[country] = {
        'country': row[1],
            'child_labor': {
                'total': [row[4], row[5]],
                'male': [row[6], row[7]],
                'female': [row[8], row[9]],
            },
            'child_marriage': {
                'married_by_15': [row[10], row[11]],
                'married_by_18': [row[12], row[13]],
            },
            'birth_registration': {
                'total': [row[14], row[15]],
            }
    }

    # Print output for each record.
    print(data[country])