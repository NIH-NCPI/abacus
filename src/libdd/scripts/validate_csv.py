 # for taking terminal arguments
from argparse import (ArgumentParser, FileType)
# for reading in csv files
import pandas 
# related function to create JSON/Dictionary object
from libdd.dd_toJSON import ddtoJSON 
# related function to clean data dictionary of missing data
from libdd.clean_dd import cleanNullTerms 
from libdd.validation import validate_and_report
import json 
import pdb

def validate_csv(args=None):
    """ Docstring in progress :) 
    """
    parser = ArgumentParser(prog='Application')
     
    parser.add_argument('-dd', '--dataDictionary', type=FileType('rt'), required=True,
                         help = "Name of Data Dictionary file")
    
    parser.add_argument('-dt', '--dataSet', type=FileType('rt'), required=True,
                         help = "Data set file to validate against data dictionary")
    
    user_args = parser.parse_args(args)
    
    # Data dictionary is also expected to be in a particular format (see https://docs.google.com/document/d/1p5kIBoGf8U_axUo2ADUXQ5Mkx3zrDUJtywkZVi4sVkk/edit?usp=sharing for more info)
    ddfile = pandas.read_csv(user_args.dataDictionary.name, index_col=0)
    # It is expected that the data set file conforms to the data dictionary defined as ddfile
    dtfile = pandas.read_csv(user_args.dataSet.name)
    dtfileJSON = dtfile.to_json(orient="records")
    dtfileParsed = json.loads(dtfileJSON)

    pdb.set_trace()
    ddJSON = ddtoJSON(ddfile)
    ddJSON_clean = cleanNullTerms(ddJSON)

    validate_and_report(ddJSON_clean, dtfileParsed)

if __name__ == "__main__":
    validate_csv()