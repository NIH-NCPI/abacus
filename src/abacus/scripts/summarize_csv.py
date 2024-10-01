""" 
Write to YAML (see https://docs.google.com/document/d/1zHsyAo6d-BkjExUi-gf_MJ7zoWDcVU_GG4YlH5A1pBs/edit?usp=sharing)


"""

from argparse import (ArgumentParser, FileType)
import pandas as pd
import yaml
import statistics
from helpers import *


def summarize_factors(dictionaryToReference, datasetfile, columnName, summaryToWrite):
    """ Identify columns which are factor types and generate the following to pass into
        YAML format:

        FactorVariableName:
          Level1: ##
          Level2: ##
          ...
          Total Count of Values: ##
          Total Missing Values: ##
          Total Unallowed Values: ..
    """

    elements = datasetfile[columnName].value_counts().to_dict()
    summaryToWrite[columnName]=elements

    # Fill out the unused possible values with 0 counts
    setA = list(dictionaryToReference[columnName]['allowed'])
    setB = list(pd.unique(datasetfile[columnName]))
    difAB = list(set(setA).difference(setB))

    if difAB != []:
        for p in range(len(difAB)):
            summaryToWrite[columnName][difAB[p]] = 0

    summaryToWrite[columnName]['Total Count of Observations'] = sum(summaryToWrite[columnName].values())
    summaryToWrite[columnName]['Total Missing Values'] = sum(datasetfile[columnName].isnull())

def summarize_numbers(datasetfile, columnName, summaryToWrite):
    """ Identify columns which are numerical and generate the following to pass into
        YAML format:

        NumberVariableName:
          Max: ##
          Mean: ##
          Median: ##
          Min: ##
          Q1: ##
          Q3: ##
          Total Count of Values: ##
          Total Missing Values: ##
    """
    summaryToWrite[columnName] = {}
    summaryToWrite[columnName]['Min'] = min(datasetfile[columnName])
    summaryToWrite[columnName]['Q1'] = statistics.quantiles(datasetfile[columnName], n=4)[0] # 25th percentile
    summaryToWrite[columnName]['Median'] = statistics.quantiles(datasetfile[columnName], n=4)[1] # median
    summaryToWrite[columnName]['Mean'] = round(statistics.mean(datasetfile[columnName]),2)
    summaryToWrite[columnName]['Q3'] = statistics.quantiles(datasetfile[columnName], n=4)[2] # 75th percentile
    summaryToWrite[columnName]['Max'] = max(datasetfile[columnName])
    summaryToWrite[columnName]['Total Count of Observations'] = datasetfile[columnName].shape[0]
    summaryToWrite[columnName]['Total Missing Values'] = sum(datasetfile[columnName].isnull())

def gensummary(datadictionary, datasetfile, filepath):
    # Figure out which columns are factor-like variables with allowed values
    factorCols = []
    numberCols = []
    stringCols = [] 

    for name in datadictionary:
        if 'allowed' in datadictionary[name].keys():
            factorCols.append(name)
        elif ('type', 'string') in datadictionary[name].items() and ('allowed' not in datadictionary[name].keys()):
            stringCols.append(name)
        elif ('type', 'integer') in datadictionary[name].items():
            numberCols.append(name)

    summarydata = {}

    for col in datasetfile:
        if col in factorCols:
            summarize_factors(datadictionary, datasetfile, col, summarydata)
        elif col in numberCols:
            summarize_numbers(datasetfile, col, summarydata)
        elif col in stringCols:
            summarize_strings(datasetfile, col, summarydata)

    with open(filepath, 'w') as f:
        yaml.dump(summarydata, f)

def summarize_strings(datasetfile, columnName, summaryToWrite):
    """ Identify columns which are string type and generate the following to pass into
        YAML format:

        StringVariableName:
          Total Count of Values: ##
          Total Missing Values: ##
          Total Unique Observations: ##
    """
    summaryToWrite[columnName] = {}
    summaryToWrite[columnName]['Total Count of Observations'] = datasetfile[columnName].shape[0]
    summaryToWrite[columnName]['Total Unique Observations'] = len(pd.unique(datasetfile[columnName]!=""))
    # pdb.set_trace()
    # print(sum(datasetfile[columnName]==""))
    # summaryToWrite[columnName]['Total Missing Values'] = sum(datasetfile[columnName].isnull())
    summaryToWrite[columnName]['Total Missing Values'] = sum(datasetfile[columnName]=="")

def summarize_csv(args=None):
    """Based on user input, load the data dictionary and data set file into memory and summarize.
    
    dataDictionary - a csv format file representing how the data are represented in an accompanying data file

    dataSet - a csv format file of collected data where columns are defined in the data dictionary (it is
    assumed that the data file already conforms to the data dictionary so this series of scripts can accurately summarize
    the contents based on data types)

    append- a meaningful name to be appended on the file summary_dat.yaml to indicate its derivative sources (e.g., "participant")
    
    """
    
    parser = ArgumentParser(prog='Application', description='pass the arguments to open a file')

    parser.add_argument('-dd', '--dataDictionary', type=FileType('rt'), required=True, 
                        help="Data Dictionary filepath(including filename)")

    parser.add_argument('-dt', '--dataSet', type=FileType('rt'), required=True, 
                        help = "Dataset to be compaired, filepath(including filename)")
    
    parser.add_argument('-m', '--missingNotation', action='store', type=str, 
                        help="Provide the way missing values are noted in the file (provide one)")

    parser.add_argument('-e', '--exportFilepath', action='store', type=str, required=True,
                        help="Provide the filepath(including filename) to export the summary to")

    # Parse the provided arguments
    user_args = parser.parse_args(args)

    # Set the global missing value representation
    missingRepresentation(msng= user_args.missingNotation)

    # Read the data dictionary CSV into a dataframe
    ddfile = pd.read_csv(user_args.dataDictionary.name, index_col=0)

    # Read the dataset CSV into a dataframe, replacing the provided missing notation
    dtfile = pd.read_csv(user_args.dataSet.name, na_values= user_args.missingNotation, keep_default_na=False)

    # Convert the data dictionary into a parsable format
    ddJSON = ddtoJSON(ddfile)

    # Set the file description to be added to the exported summary filename
    filepath = user_args.exportFilepath
 
    # Generate the summary and export to the configured location
    gensummary(ddJSON, dtfile, filepath)

if __name__ == "__main__":
    summarize_csv()