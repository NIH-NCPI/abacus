from argparse import (ArgumentParser, FileType) # for taking terminal arguments
from rich import print # for pretty terminal print formatting
import pandas # for reading in csv files
from libdd.dd_toJSON import ddtoJSON # related function to create JSON/Dictionary object
from libdd.clean_dd import cleanNullTerms # related function to clean data dictionary of missing data
from libdd.summary import gensummary # related function to summarize data based on input ddfile and dtfile

def summarize_csv(args=None):
    '''Based on user input, load the data dictionary and data set file into memory and summarize.
    dataDictionary - a csv format file representing how the data are represented in an accompanying data file

    dataSet - a csv format file of collected data where columns are defined in the data dictionary (it is
    assumed that the data file already conforms to the data dictionary so this series of scripts can accurately summarize
    the contents based on data types)
    
    '''
    
    parser = ArgumentParser(prog='Application', description='pass the arguments to open a file')

    parser.add_argument('-dd', '--dataDictionary', type=FileType('rt'), required=True, help="Data Dictionary file name")

    parser.add_argument('-dt', '--dataSet', type=FileType('rt'), required=True, help = "File to be compared to Data Dictionary")

    user_args = parser.parse_args(args)
    
    # Data dictionary is also expected to be in a particular format (see https://docs.google.com/document/d/1p5kIBoGf8U_axUo2ADUXQ5Mkx3zrDUJtywkZVi4sVkk/edit?usp=sharing for more info)
    ddfile = pandas.read_csv(user_args.dataDictionary.name, index_col=0)

    ddJSON = ddtoJSON(ddfile)

    ddJSON_clean = cleanNullTerms(ddJSON)

    # It is expected that the data set file conforms to the data dictionary defined as ddfile
    dtfile = pandas.read_csv(user_args.dataSet.name)

    gensummary(ddJSON_clean, dtfile)

if __name__ == "__main__":
    summarize_csv()