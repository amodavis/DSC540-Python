# --------------------------------------------------------------------------------------
# File: Exercise_11.2.py
# Name: Amie Davis
# Date: 11/7/2019
# Course: DSC540 - Data Preparation
# Assignment Number: 11.2
#
# Purpose:  Ch9 Review: Data Exploration and Analysis
#           Bring two datasets together
#
# Data Files: unicef_oct_2014.xls
#             corruption_perception_index.xls
#
# Usage: Uses Python 3.7.
#        Developed using PyCharm 2019.1.3.
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# Function import_xl_file()
#
# Description:  Opens Excel file for read and loads sheet into a list.
#
# Parameters:   file_name: name of xls file to open
#
# Returns:      Excel sheet data
#
def import_xl_file(file_name):
    import os, xlrd

    # Set data directory
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'DW Code/data-wrangling-master/data/chp9/')
    filepath = data_dir + file_name

    workbook = xlrd.open_workbook(filepath)

    if workbook.nsheets == 1:
        v_are = 'is'
        v_sheet = 'sheet'
    else:
        v_are = 'are'
        v_sheet = 'sheets'

    #print('There {} {} {} in your workbook.'.format(v_are, workbook.nsheets, v_sheet))

    # Return the first sheet
    return(workbook.sheets()[0])

# --------------------------------------------------------------------------------------
# Function get_rows()
#
# Description:  Pulls data from rows with country names
#
# Parameters:   sheet: name of Excel worksheet
#
# Returns:      Cleaned records
#
def get_rows(sheet):

    # Iterates through each row in the spreadsheet
    selected_rows = [sheet.row_values(r) for r in range(6, 114)]

    # Remove extra hyphens from dataset
    cleaned_rows = get_new_array(selected_rows, remove_bad_chars)

    return(cleaned_rows)

# --------------------------------------------------------------------------------------
# Function get_titles()
#
# Description:  Finds headers in worksheet
#
# Parameters:   sheet: name of Excel worksheet
#
# Returns:      Record of header names
#
def get_titles(sheet):

    # Pull title from designated rows - merging both rows
    # In this case 5th and 6th rows
    title_rows = list(zip(sheet.row_values(4), sheet.row_values(5)))
    titles = [t[0] + ' ' + t[1] for t in title_rows]

    # Remove spaces
    titles = [t.strip() for t in titles]

    return(titles)

# --------------------------------------------------------------------------------------
# Function get_data_types()
#
# Description:  Takes an empty list, iterates over the columns, and
#               creates a full list of all of the column types
#
# Parameters:   example_row: Excel row
#
# Returns:      agate.data_types object
#
def get_data_types(example_row):
    from xlrd.sheet import ctype_text

    # Initialize variables
    types = []

    # Loops through a sample row to identify data types of each column
    for v in example_row:
        value_type = ctype_text[v.ctype]
        if value_type == 'text':
            types.append(text_type)
        elif value_type == 'number':
            types.append(number_type)
        elif value_type == 'xldate':
            types.append(date_type)
        else:
            types.append(text_type)

    return(types)

# --------------------------------------------------------------------------------------
# Function remove_bad_chars()
#
# Description:  Removes hyphens from a string
#
# Parameters:   val: a string character
#
# Returns:      Character without hyphen
#
def remove_bad_chars(val):
    if val == '-':
        return(None)
    return(val)

# --------------------------------------------------------------------------------------
# Function get_new_array()
#
# Description:  Loops through an array to perform a function on it
#
# Parameters:   old_array: Array you wih to clean
#               function_to_clean: The function you want to perform on the array
#
# Returns:      Cleaned array
#
def get_new_array(old_array, function_to_clean):
    new_arr = []
    for row in old_array:
        cleaned_row = [function_to_clean(rv) for rv in row]
        new_arr.append(cleaned_row)
    return(new_arr)

# --------------------------------------------------------------------------------------
# Function reverse_percent()
#
# Description:  Reverses the % child labor data to return % of children working
#
# Parameters:   row: row from agate table
#
# Returns:      child_nw: number of children not working
#
def reverse_percent(row):
    child_nw = 100 - row['Total (%)']
    return(child_nw)

# --------------------------------------------------------------------------------------
# Function get_table()
#
# Description:  Creates agate table
#
# Parameters:   new_arr: array of data
#               types: data types for columns
#               titles: column headers
#
# Returns:      table: agate table
#
def get_table(new_arr, types, titles):
    try:
        table = agate.Table(new_arr, titles, types)
        return(table)
    except Exception as e:
        print(e)

# --------------------------------------------------------------------------------------
# Main function
#
def main():

    # Initialize variables
    sheet = []

    # Load UNICEF data from Excel sheet
    data_file = 'unicef_oct_2014.xls'
    sheet = import_xl_file(data_file)

    # Pull the titles from the worksheet
    titles = get_titles(sheet)

    # Pull records from rows using country names
    country_rec = get_rows(sheet)

    # Get agate data types
    data_types = get_data_types(sheet.row(6))

    # Load UNICEF data into an agate table
    table = agate.Table(country_rec, titles, data_types)

    ranked = table.compute([('Children not working (%)', agate.Formula(number_type, reverse_percent)),])

    # Load CPI data from Excel sheet
    cpi_file = 'corruption_perception_index.xls'
    cpi_sheet = import_xl_file(cpi_file)

    # Get titles
    # Note duplicate header - added "Duplicate"
    cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
    cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
    cpi_titles = [t.strip() for t in cpi_titles]
    cpi_titles[0] = cpi_titles[0] + ' Duplicate'

    # Load CPI data into an agate table
    cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]
    cpi_types = get_data_types(cpi_sheet.row(3))
    cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

    # Join data sets
    # Join the CPI agate table with the UNICEF (aka ranked) agate table
    cpi_and_cl = cpi_table.join(ranked, 'Country / Territory', 'Countries and areas', inner=True)

    # Review joined data
    print(cpi_and_cl.column_names)
    for r in cpi_and_cl.order_by('CPI 2013 Score').limit(10).rows:
        print('{}: {} - {}%'.format(r['Country / Territory'], r['CPI 2013 Score'], r['Total (%)']))

#----------------------------------------------------------------
# Run program

# Import libraries used
import agate

# Set agate data types
text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()

main()
