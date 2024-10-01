"""
This script performs a validation of a dataset against a data dictionary,
both provided in CSV format. 

The data dictionary defines the expected structure and allowed values for each
column in the dataset. The script ensures that the dataset adheres to the rules
defined by the data dictionary, flags any inconsistencies, and generates a 
report on validation errors. The missing data notation is also handled 
according to the user-provided specification (e.g., NA or other values).

Data dictionary is also expected to be in a particular format (see 
https://docs.google.com/document/d/1p5kIBoGf8U_axUo2ADUXQ5Mkx3zrDUJtywkZVi4sVkk/edit?usp=sharing 
for more info)

"""

import pandas as pd
import cerberus
import json
from argparse import (ArgumentParser, FileType)
from collections import defaultdict
from helpers import *

def validate_and_report(ddJSON_clean, dtfileParsed):
    """
    Validate parsed data against a cleaned data dictionary schema and report errors.

    This function uses the Cerberus data validator to validate each record in `dtfileParsed` 
    against the schema provided in `ddJSON_clean`. It generates a report with validation 
    errors, or confirms if no validation errors are found.

    Args:
        ddJSON_clean (dict): The cleaned data dictionary (schema) in JSON format, used 
                             as the validation schema.
        dtfileParsed (list[dict]): The parsed data records to be validated against the 
                                   schema.

    Returns:
        None: Prints validation results. If no errors are found, it outputs a message 
              confirming that validation was successful. If errors exist, it prints them.

    Note:
        Does not catch '1' as integer instead of 'Visit 1' 

    """
    v = cerberus.Validator(ddJSON_clean)
    counts = 0
    for i in range(0, len(dtfileParsed)):
        if v.validate(dtfileParsed[i]) == True:
            counts = counts+1
            if counts == len(dtfileParsed):
                print('No validation errors noted!')
        else:
            print('Error detected in row', i+1, ':', v.errors)

def validate_csv(args=None):
    """
    Perform validation of a harmonized dataset against a data dictionary.

    This function validates a dataset (CSV format) against a data dictionary (also CSV format). 
    It ensures that the dataset conforms to the structure and rules defined in the data dictionary, 
    flagging any inconsistencies or missing data that don't match the expected notation.

    Args:
        args (list, optional): List of command-line arguments. 
            - `--dataDictionary` (`-dd`): Path to the data dictionary CSV file.
            - `--dataSet` (`-dt`): Path to the dataset CSV file.
            - `--missingNotation` (`-missing`): String to represent missing data values.

    Returns:
        None: Outputs the validation results, either confirming successful validation 
              or printing errors for rows that do not conform to the data dictionary.
    """
    parser = ArgumentParser(prog='Application')
    
    parser.add_argument('-dd', '--dataDictionary', type=FileType('rt'), required=True, 
                        help="Data Dictionary filepath(including filename)")

    parser.add_argument('-dt', '--dataSet', type=FileType('rt'), required=True, 
                        help = "Dataset to be compaired, filepath(including filename)")
    
    parser.add_argument('-m', '--missingNotation', action='store', type=str, 
                        help="Provide the way missing values are noted in the file (provide one)") 
    
    # Parse the provided arguments
    user_args = parser.parse_args(args)
    
    # Set the global missing value representation
    missingRepresentation(msng= user_args.missingNotation)

    # Read the data dictionary CSV into a dataframe
    ddfile = pd.read_csv(user_args.dataDictionary.name, index_col=0)

    # Read the dataset CSV into a dataframe, replacing the provided missing notation
    dtfile = pd.read_csv(user_args.dataSet.name, na_values= user_args.missingNotation, keep_default_na=False)

    # Convert dataset into a format parsable by the data validator
    dtfileJSON = dtfile.to_json(orient="records")
    dtfileParsed = json.loads(dtfileJSON)

    # Convert the data dictionary into a format parsable by the data validator
    ddJSON = ddtoJSON(ddfile)

    # Run the validator and print results
    validate_and_report(ddJSON, dtfileParsed)

if __name__ == "__main__":
    validate_csv()