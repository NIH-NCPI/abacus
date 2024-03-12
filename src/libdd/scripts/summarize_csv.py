 # for taking terminal arguments
from argparse import (ArgumentParser, FileType)
# for pretty terminal print formatting
from rich import print 
# for reading in csv files
import pandas 
# related function to create JSON/Dictionary object
from libdd.dd_toJSON import ddtoJSON 
# related function to clean data dictionary of missing data
from libdd.clean_dd import cleanNullTerms 
# related function to summarize data based on input ddfile and dtfile
from libdd.summary import gensummary 

def summarize_csv(args=None):
    """Based on user input, load the data dictionary and data set file into memory and summarize.
    dataDictionary - a csv format file representing how the data are represented in an accompanying data file

    dataSet - a csv format file of collected data where columns are defined in the data dictionary (it is
    assumed that the data file already conforms to the data dictionary so this series of scripts can accurately summarize
    the contents based on data types)

    text- a meaningful name to be appended on the file summary_dat.yaml to indicate its derivative sources (e.g., "participant")
    
    """
    
    parser = ArgumentParser(prog='Application', description='pass the arguments to open a file')

    parser.add_argument('-dd', '--dataDictionary', type=FileType('rt'), required=True, 
                        help="Data Dictionary file name")

    parser.add_argument('-dt', '--dataSet', type=FileType('rt'), required=True, 
                        help = "File to be compared to Data Dictionary")

    parser.add_argument('-text', action='store', type=str, 
                        help="Provide a description of the content of the file to be appended to the output YAML file")

    user_args = parser.parse_args(args)
    
    # Data dictionary is also expected to be in a particular format (see https://docs.google.com/document/d/1p5kIBoGf8U_axUo2ADUXQ5Mkx3zrDUJtywkZVi4sVkk/edit?usp=sharing for more info)
    ddfile = pandas.read_csv(user_args.dataDictionary.name, index_col=0)

    ddJSON = ddtoJSON(ddfile)

    ddJSON_clean = cleanNullTerms(ddJSON)

    # It is expected that the data set file conforms to the data dictionary defined as ddfile
    dtfile = pandas.read_csv(user_args.dataSet.name)
    appendToYAML = user_args.text

    gensummary(ddJSON_clean, dtfile, appendToYAML)

if __name__ == "__main__":
    summarize_csv()