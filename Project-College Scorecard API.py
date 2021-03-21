# --------------------------------------------------------------------------------------
# File: Final_Project.py
# Name: Amie Davis
# Date: 11/11/2019
# Course: DSC540 - Data Preparation
# Assignment Number: 12.3
#
# Purpose: Retrieve and cleanse data from an API.
#
# Usage: Uses API at https://collegescorecard.ed.gov
#
# Functions: StartLogger(), GetConfig(), GetFieldString(), GetVariableName(),
#            RetrieveCollegeData(), ParseResponse(), main()
#
# Usage: Uses Python 3.7.
#        Developed using PyCharm 2019.1.3.
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# Function StartLogger()
#
# Description:  Creates log file for use in logging messages.
#
# Parameters:   None
#
# Returns:      No return value
#
def StartLogger():

    from datetime import datetime

    # Set data directory
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'Logs')

    logging.basicConfig(filename = data_dir + '/scorecard_%s.log' % datetime.strftime(datetime.now(), '%m%d%Y_%H%M%S'),
                        level = logging.DEBUG,
                        format = '%(asctime)s %(message)s',
                        datefmt = '%m-%d %H:%M:%S')

# --------------------------------------------------------------------------------------
# Function GetConfig()
#
# Description:  Reads configuration file.
#
# Parameters:   None
#
# Returns:      config: Data from configuration file
#
def GetConfig():

    file_name = 'python_amd.cfg'

    # Set data directory
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'Config/')
    filepath = data_dir + file_name

    config = configparser.ConfigParser()
    config.read([filepath])

    return(config)

# --------------------------------------------------------------------------------------
# Function GetFieldString()
#
# Description:  Gets list of variables to pass to API.
#               Added as proc for readability.
#
# Parameters:   None
#
# Returns:      field_string: Parameter to pass to API that corresponds to variable list

def GetFieldString():

    logging.debug("GetFieldString procedure started.")

    # Initialize variables
    field_string = '&fields='

    # Append each variable to retrieve to the field_string
    field_string += 'id,'
    field_string += 'school.name,'
    field_string += 'school.city,'
    field_string += 'school.main_campus,'
    field_string += 'school.state,'
    field_string += 'school.ownership,'
    field_string += 'school.carnegie_size_setting,'
    field_string += 'latest.student.size,'
    field_string += 'latest.completion.completion_rate_four_year_100_pooled,'
    field_string += 'latest.earnings.6_yrs_after_entry.median,'
    field_string += 'latest.cost.tuition.out_of_state,'
    field_string += 'latest.admissions.sat_scores.average.overall,'
    field_string += 'latest.admissions.act_scores.midpoint.cumulative,'
    field_string += 'latest.admissions.admission_rate.overall,'
    field_string += 'latest.academics.program.bachelors.visual_performing,'
    field_string += 'latest.academics.program.bachelors.biological,'
    field_string += 'latest.academics.program.bachelors.legal,'
    field_string += 'latest.academics.program.bachelors.language,'
    field_string += 'latest.academics.program.bachelors.security_law_enforcement,'
    field_string += 'latest.academics.program.bachelors.physical_science'

    # Return parameter to use in API call
    return field_string

# --------------------------------------------------------------------------------------
# Function GetVariableName()
#
# Description:  Assigns descriptive variable names based on API data dictionary.
#
# Parameters:   dkey: Field key from API results
#
# Returns:      var_name: Variable name

def GetVariableName(dkey):

    var_name = ''

    if dkey == 'id':
        var_name = 'School ID'
    elif dkey == 'school.name':
        var_name = 'School Name'
    elif dkey == 'school.city':
        var_name = 'City'
    elif dkey == 'school.main_campus':
        var_name = 'Main Campus Indicator'
    elif dkey == 'school.state':
        var_name = 'State'
    elif dkey == 'school.ownership':
        var_name = 'Public-Private Indicator'
    elif dkey == 'school.carnegie_size_setting':
        var_name = 'School Type Code'
    elif dkey == 'latest.student.size':
        var_name = 'School Size'
    elif dkey == 'latest.completion.completion_rate_four_year_100_pooled':
        var_name = 'Completion Rate'
    elif dkey == 'latest.earnings.6_yrs_after_entry.median':
        var_name = '6 Yr Average Earnings'
    elif dkey == 'latest.cost.tuition.out_of_state':
        var_name = 'Tuition'
    elif dkey == 'latest.admissions.sat_scores.average.overall':
        var_name = 'Average SAT Score'
    elif dkey == 'latest.admissions.act_scores.midpoint.cumulative':
        var_name = 'Average ACT Score'
    elif dkey == 'latest.admissions.admission_rate.overall':
        var_name = 'Admission Rate'
    elif dkey == 'latest.academics.program.bachelors.visual_performing':
        var_name = 'Visual and Performing Arts Program Indicator'
    elif dkey == 'latest.academics.program.bachelors.biological':
        var_name = 'Biological Program Indicator'
    elif dkey == 'latest.academics.program.bachelors.legal':
        var_name = 'Legal Program Indicator'
    elif dkey == 'latest.academics.program.bachelors.language':
        var_name = 'Language Program Indicator'
    elif dkey == 'latest.academics.program.bachelors.security_law_enforcement':
        var_name = 'Law Enforcement Program Indicator'
    elif dkey == 'latest.academics.program.bachelors.physical_science':
        var_name = 'Physical Science Program Indicator'
    else:
        var_name = 'VARIABLE NAME UNMATCHED'

    # Return variable name
    return var_name

# --------------------------------------------------------------------------------------
# Function RetrieveCollegeData()
#
# Description:  Retrieves college scorecard data from Data.gov API
#
# Parameters:   page_cnt: The number of pages to retrieve from API
#
# Returns:      response_str: full response from API as a string
#
def RetrieveCollegeData(page_cnt):
    import urllib.request

    logging.debug("RetrieveCollegeData procedure started.")

    # Set api url
    url = 'https://api.data.gov/ed/collegescorecard/v1/schools'

    # Add API key as provided by Data.gov
    # Note that the API key is stored in config file
    config = GetConfig()
    api_key = config.get('Data.gov', 'api_key')
    url += '?api_key=' + api_key

    # Add page count to api url
    page_str = '&_page=' + str(page_cnt)
    url += page_str

    # Add requested variables to api url
    field_str = GetFieldString()
    url += field_str


    # Add query to api url
    # In this case, we are only interested in large, 4-year colleges
    # (where school.carnegie_size_setting=16)
    querystring = '&school.carnegie_size_setting=16'
    url += querystring

    # print(url)
    logging.debug(url)

    # Call API
    request = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(request)

    except:
        print('Web service is unavailable.  Try again later')
        logging.exception('Exception in RetrieveCollegeData() procedure.')
        logging.error('Web service unavailable.')

    else:
        # print('Web service connection successful.')
        logging.debug("Web service connection successful.")
        

        # Convert HTTP response into a string
        response_str = response.read().decode('utf-8')

        # FOR TESTING - Displays URL
        # print(response.read().decode('utf-8'))

        # Return API response
        return response_str

# --------------------------------------------------------------------------------------
# Function ParseResponse()
#
# Description:  Parses JSON response into Python dictionary.
#               Exports API response in readable format to file.
#
# Parameters:   response: String result returned from API
#               output_file: Name of file to export results
#
# Returns:      id_list: List of school IDs strings returned from API
#
def ParseResponse(response_str, output_file):
    import json


    logging.debug("ParseResponse procedure started.")

    # Parse JSON data into dictionary object
    data = json.loads(response_str)

    # FOR TESTING - Dump to string to display readable API response
    # print(json.dumps(data, indent=4, sort_keys=True))

    # Get record count from metadata
    for dkey, dval in data['metadata'].items():
        # print('{}: {}'.format(dkey, dval))
        if dkey == 'total':
            record_count = dval

    # Review records to determine page count
    # print('Number of records returned: {}'.format(record_count))
    logging.debug("Number of records returned: {}".format(record_count))

    # Get page count needed for request
    # API returns 20 record per page
    # Note that the first page starts at 0
    num_pages = round((record_count / 20) + 1)
    # print(num_pages)
    logging.debug("Number of pages needed: {}".format(num_pages))

    # Format and display info received into export file
    # Loop through each result record
    # Uses 'results' keyword from JSON root-level
    try:
        with open(output_file, 'a') as fileHandler:
            id_list = []
            for school_rec in data['results']:

                # Header for each record
                fileHandler.write('\n')
                fileHandler.write('**********NEW SCHOOL RECORD**********')
                fileHandler.write('\n')

                # Loop through each key-value pair
                for dkey, dval in school_rec.items():

                    # Get variable name
                    var_name = GetVariableName(dkey)

                    # Store IDs in list to determine uniqueness
                    if var_name == 'School ID':
                        id_list.append(dval)

                    # Write each value to file
                    fileHandler.write('{}: {}'.format(var_name, dval))
                    fileHandler.write('\n')

    except:
        print('Error in ParseResponse() procedure.')
        logging.exception('Exception in ParseResponse() procedure.')

    return(id_list)
# --------------------------------------------------------------------------------------
# Main function
#
def main():

    import numpy as np

    # Start logging
    StartLogger()
    logging.debug("Main procedure started.")

    # Prepare output file
    # Set output directory
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, 'Output/')

    # Prompts user for output filename
    filename = input('Enter a file name for the output : ')
    output_file = data_dir + filename

    # Check for previous existence of file
    if os.path.isfile(output_file):
        overwrite = input('This file already exist.  Enter Y to overwrite the existing file.')

        if overwrite != 'Y' and overwrite != 'y':
            exit()

    # Creates file header
    header1 = 'College Scorecard Results '
    header2 = '-------------------------'

    # Create new output file
    try:
        with open(output_file, 'w') as fileHandler:

            fileHandler.write(header1)
            fileHandler.write('\n')
            fileHandler.write(header2)
    except:
        print('Unable to open file {} for write'.format(output_file))
        logging.exception('Exception in main() procedure.')

    # Loop to return each page of API results.
    # API only returns a page at a time up to a maximum of 100 records.
    merged_id_list = []
    for page_cnt in range(0,7):

        # Retrieve college scorecard data from API
        response_str = RetrieveCollegeData(page_cnt)

        # Format & output data retrieved from API
        id_list = ParseResponse(response_str, output_file)

        # Combine lists of School IDs returned from the API
        merged_id_list.extend(id_list)

    # Look for duplicates
    unique_lst = np.unique(merged_id_list)
    if len(merged_id_list) == len(unique_lst):
        print('No duplicate records found.')
        logging.debug("No duplicate records found.")

    logging.debug("Main procedure completed.")

# --------------------------------------------------------------------------------------
# Run program
import logging, os, configparser

main()
