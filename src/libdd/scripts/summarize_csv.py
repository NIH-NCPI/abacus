from argparse import (ArgumentParser, FileType)
from rich import print
import pandas
from libdd.dd_toJSON import ddtoJSON
from libdd.clean_dd import cleanNullTerms
from libdd.summary import gensummary

def summarize_csv(args=None):
    """Based on user input, load the data dictionary and data set file into memory and summarize."""

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

    # print(ddJSON_clean)

    gensummary(ddJSON_clean, dtfile)

if __name__ == "__main__":
    summarize_csv()