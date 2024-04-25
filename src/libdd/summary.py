import yaml 
import pandas as pd
from libdd.column_handlers import summarize_factors, summarize_numbers, summarize_strings

def gensummary(datadictionary, datasetfile, appendToYAML):
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
  # Write to YAML (see https://docs.google.com/document/d/1zHsyAo6d-BkjExUi-gf_MJ7zoWDcVU_GG4YlH5A1pBs/edit?usp=sharing)

  fileName = 'summary_dat_' + appendToYAML + '.yaml'
  with open('C:/Users/holmea9/OneDrive - VUMC/Documents/dev/INCLUDE/libdd/data/' + fileName, 'w') as f:
     yaml.dump(summarydata, f)
