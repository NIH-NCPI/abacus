import pandas as pd
import statistics

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

    summaryToWrite[columnName]['Total Count of Values'] = sum(summaryToWrite[columnName].values())
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
    summaryToWrite[columnName]['Total Count of Values'] = datasetfile[columnName].shape[0]
    summaryToWrite[columnName]['Total Missing Values'] = sum(datasetfile[columnName].isnull())

def summarize_strings(datasetfile, columnName, summaryToWrite):
    """ Identify columns which are string type and generate the following to pass into
        YAML format:

        StringVariableName:
          Total Count of Values: ##
          Total Missing Values: ##
          Total Unique Observations: ##
    """
    summaryToWrite[columnName] = {}
    summaryToWrite[columnName]['Total Count of Values'] = datasetfile[columnName].shape[0]
    summaryToWrite[columnName]['Total Unique Observations'] = len(pd.unique(datasetfile[columnName]))
    summaryToWrite[columnName]['Total Missing Values'] = sum(datasetfile[columnName].isnull())
