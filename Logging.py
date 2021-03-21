# --------------------------------------------------------------------------------------
# File: Exercise_10.2.py
# Name: Amie Davis
# Date: 10/31/2019
# Course: DSC540 - Data Preparation
# Assignment Number: 10.2
#
# Purpose:  Add logging to existing Python script (using 7.2).
#           Loads data from Excel file and json reference files.
#           Combines results into agate table for analysis.
#           Analyzes and plots the data.
#
# Data Files: unicef_oct_2014.xls
#             corruption_perception_index.xls
#             earth.json
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
    import xlrd

    logging.debug("PYSCRIPT: import_xl_file procedure started.")

    # Set data directory
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'DW Code/data-wrangling-master/data/chp9/')
    filepath = data_dir + file_name

    try:
        workbook = xlrd.open_workbook(filepath)

    except Exception:
        logging.exception('PYSCRIPT: Exception in import_xl_file() procedure.')
        logging.error('PYSCRIPT: File cannot be opened.')

        # Send email failure message
        mail(['ameesedav@gmail.com'],
             "Exercise 10.2 - FAILURE",
             "The Excel file failed to open.")

        exit()

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
# Function read_sheet()
#
# Description:  Iterates through each row in the spreadsheet
#               Prints each record
#
# Parameters:   sheet: name of Excel worksheet
#
# Returns:      No return value
#
def read_sheet(sheet):

    logging.debug("PYSCRIPT: read_sheet procedure started.")

    # Iterates through each row in the spreadsheet
    for r in range(sheet.nrows):
        # Print each record
        print(r, sheet.row(r))

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

    logging.debug("PYSCRIPT: get_rows procedure started.")

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

    logging.debug("PYSCRIPT: get_titles procedure started.")

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

    logging.debug("PYSCRIPT: get_data_types procedure started.")

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

    logging.debug("PYSCRIPT: remove_bad_chars procedure started.")

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

    logging.debug("PYSCRIPT: get_new_array procedure started.")

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

    logging.debug("PYSCRIPT: reverse_percent procedure started.")

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

    logging.debug("PYSCRIPT: get_table procedure started.")

    try:
        table = agate.Table(new_arr, titles, types)
        return(table)
    except Exception as e:
        logging.exception('PYSCRIPT: Exception in get_table() procedure.')
        logging.error('PYSCRIPT: Error creating agate table.')

        # Send email failure message
        mail(['ameesedav@gmail.com'],
             "Exercise 10.2 - FAILURE",
             "Unable to create agate table.")

    print(e)

# --------------------------------------------------------------------------------------
# Function get_continent()
#
# Description:  Retrieves continent from json file
#
# Parameters:   file_name: Name of json file
#
# Returns:      agate table w/ continent
#
def get_continent(file_name, cpi_and_cl):
    import json

    logging.debug("PYSCRIPT: get_continent procedure started.")

    # Set data directory
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'DW Code/data-wrangling-master/data/chp9/')
    filepath = data_dir + file_name

    try:
        f = open(filepath)

    except Exception:
        logging.exception('PYSCRIPT: Exception in get_continent() procedure.')
        logging.error('PYSCRIPT: File cannot be opened.')

        # Send email failure message
        mail(['ameesedav@gmail.com'],
             "Exercise 10.2 - FAILURE",
             "The json file failed to open.")

        exit()

    else:
        with f:
            country_json = json.loads(f.read())


    country_dict = {}
    for dct in country_json:
        country_dict[dct['name']] = dct['parent']

    def get_country(country_row):
        return(country_dict.get(country_row['Country / Territory'].lower()))

    cpi_and_cl = cpi_and_cl.compute([('continent', agate.Formula(text_type, get_country)), ])

    return(cpi_and_cl)

# --------------------------------------------------------------------------------------
# Function plot_cpi_cl()
#
# Description:  Displays perceived corruption scores compared to the child labor percentages
#
# Parameters:   africa_cpi_cl: agate table of scores from African countries
#               title: Title of the chart
#
# Returns:      No return value
#
def plot_cpi_cl(africa_cpi_cl, title):
    import matplotlib.pyplot as plt

    logging.debug("PYSCRIPT: plot_cpi_cl procedure started.")

    # Plots Perceived Corruption vs Child Labor
    plt.plot(africa_cpi_cl.columns['CPI 2013 Score'], africa_cpi_cl.columns['Total (%)'])
    plt.xlabel('CPI Score - 2013')
    plt.ylabel('Child Labor Percentage')
    plt.title(title)
    plt.show()

# --------------------------------------------------------------------------------------
# Function start_logger()
#
# Description:  Creates log file for use in logging messages.
#
# Parameters:   None
#
# Returns:      No return value
#
def start_logger():

    from datetime import datetime

    # Set data directory
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'Logs')

    logging.basicConfig(filename = data_dir + '/daily_report_%s.log' % datetime.strftime(datetime.now(), '%m%d%Y_%H%M%S'),
                        level = logging.DEBUG,
                        format = '%(asctime)s %(message)s',
                        datefmt = '%m-%d %H:%M:%S')

# --------------------------------------------------------------------------------------
# Function get_config()
#
# Description:  Reads configuration file.
#               Can be modified to use different files for different environments.
#
# Parameters:   None
#
# Returns:      No return value
#
def get_config():

    file_name = 'python_amd.cfg'

    # Set data directory
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'Config/')
    filepath = data_dir + file_name

    config = configparser.ConfigParser()
    config.read([filepath])

    return(config)

# --------------------------------------------------------------------------------------
# Function mail()
#
# Description:  Sends email
#
# Parameters:   to: Comma-delimited list of email addresses for recipients
#               subject: Subject for email
#               text: Body of text for email
#
# Returns:      No return value
#
def mail(to, subject, text, config=None):

    # Import libraries
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    if not config:
        config = get_config()

    msg = MIMEMultipart()
    msg['From'] = config.get('email', 'user')
    msg['To'] = ", ".join(to)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    mailServer = smtplib.SMTP("smtp.office365.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(config.get('email', 'user'),
                     config.get('email', 'password'))
    mailServer.sendmail(config.get('email', 'user'), to, msg.as_string())
    mailServer.close()

# --------------------------------------------------------------------------------------
# Main function
#
def main():

    # Start logging
    start_logger()
    logging.debug("PYSCRIPT: Main procedure started.")

    # Identify data files
    data_file = 'unicef_oct_2014.xls'
    cpi_file = 'corruption_perception_index.xls'
    json_file = 'earth.json'

    # Initialize variables
    sheet = []

    ############################################################
    # Part I - Load the data
    # Load data from Excel sheet
    sheet = import_xl_file(data_file)

    # Loop through each record in the sheet
    # Uncomment to review sheet data
    # read_sheet(sheet)

    # Pull the titles from the worksheet
    titles = get_titles(sheet)

    # Pull records from rows using country names
    country_rec = get_rows(sheet)

    # Get agate data types
    data_types = get_data_types(sheet.row(6))

    # Load into an agate table
    table = agate.Table(country_rec, titles, data_types)

    ############################################################
    # Part II - Explore the data
    # 1 - Which countries have the highest rates of child labor?
    # Sort the data in descending order by total percentage
    # Limit to the top 10 offenders
    print("HIGHEST CHILD LABOR RATES")
    print("=========================")
    most_egregious = table.order_by('Total (%)', reverse=True).limit(10)
    for r in most_egregious.rows:
        print('{}: {}%'.format(r['Countries and areas'], r['Total (%)']))

    # 2 - Which countries have the most girls working?
    # Sort the data in descending order by total percentage
    # Limit to the top 10 countries
    print("\n")
    print("MOST GIRLS WORKING")
    print("==================")
    female_data = table.where(lambda r: r['Female'] is not None)
    most_females = female_data.order_by('Female', reverse=True).limit(10)
    for r in most_females.rows:
        print('{}: {}%'.format(r['Countries and areas'], r['Female']))

    # 3 - What is the average percentage of child labor in cities?
    # Ignores values set to None
    has_por = table.where(lambda r: r['Place of residence (%) Urban'] is not None)
    avg_urban = has_por.aggregate(agate.Mean('Place of residence (%) Urban'))
    print("\n")
    print('Average urban child labor: {}%'.format(round(avg_urban,2)))

    # 4 - Find a row with more than 50% of rural child labor.
    first_match = has_por.find(lambda x: x['Rural'] > 50)
    print('{} has more than 50% rural child labor.'.format(first_match['Countries and areas']))

    # 5 - Rank the worst offenders in terms of child labor percentages by country.
    print("\n")
    print("COUNTRY RANKS FOR CHILD LABOR")
    print("=========================")
    ranked = table.compute([('Total Child Labor Rank',
                             agate.Rank('Total (%)', reverse=True)), ])
    for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
        print('{} is ranked {} with {}%.'.format(row['Countries and areas'], row['Total Child Labor Rank'], row['Total (%)']))

    # 6 - Calculate the percentage of children not involved in child labor.
    print("\n")
    print("COUNTRY RANKS FOR CHILDREN NOT WORKING")
    print("======================================")
    number_type = agate.Number()
    ranked = table.compute([('Children not working (%)', agate.Formula(number_type, reverse_percent)),])

    for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
        print('{} has {}% children not working.'.format(row['Countries and areas'], row['Children not working (%)']))

    ############################################################
    # Part III - Plot CPI data
    # Load data from Excel sheet
    cpi_sheet = import_xl_file(cpi_file)

    # Get titles
    # Note duplicate header - added "Duplicate"
    cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
    cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
    cpi_titles = [t.strip() for t in cpi_titles]
    cpi_titles[0] = cpi_titles[0] + ' Duplicate'

    # Load data into agate table
    cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]
    cpi_types = get_data_types(cpi_sheet.row(3))
    cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

    # Join data sets
    cpi_and_cl = cpi_table.join(ranked, 'Country / Territory', 'Countries and areas', inner=True)

    # Get continent
    cpi_and_cl = get_continent(json_file, cpi_and_cl)

    # Get data for African nations only
    africa_cpi_cl = cpi_and_cl.where(lambda x: x['continent'] == 'africa')

    # Chart the perceived corruption scores compared to the child labor percentages.
    plot_cpi_cl(africa_cpi_cl, 'CPI & Child Labor Correlation')

    # Find the worst offenders
    # Show the countries with highest child labor and worst perceived corruption
    # (where the values are worse than the mean)
    cl_mean = africa_cpi_cl.aggregate(agate.Mean('Total (%)'))
    cpi_mean = africa_cpi_cl.aggregate(agate.Mean('CPI 2013 Score'))

    def highest_rates(row):
        if row['Total (%)'] > cl_mean and row['CPI 2013 Score'] < cpi_mean:
            return(True)
        return(False)

    highest_cpi_cl = africa_cpi_cl.where(lambda x: highest_rates(x))

    # Chart again using only the worst offenders
    plot_cpi_cl(highest_cpi_cl, 'CPI & Child Labor Correlation - Worst Offenders')

    logging.debug("PYSCRIPT: Main procedure completed.")

    # Send email success message
    mail(['ameesedav@gmail.com'],
         "Exercise 10.2 - SUCCESS",
         "The Python script for DSC540 Exercise 10.2 completed successfully.")


#----------------------------------------------------------------
# Run program

# Import libraries used
import agate, logging, os, configparser

# Set agate data types
text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()

main()
