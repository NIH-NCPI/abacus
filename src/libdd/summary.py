import yaml 
import pandas as pd
from libdd.column_handlers import summarize_factors, summarize_numbers, summarize_strings
import pdb 

def gensummary(datadictionary, datasetfile, appendToYAML):
  # Figure out which columns are factor-like variables with allowed values
  factorCols = []
  numberCols = []
  stringCols = [] 

  _numericTypes = set([
    'integer',
    'number'
  ])
  for name in datadictionary:
    if 'allowed' in datadictionary[name].keys() and datadictionary[name]['allowed'] != []:
      print(f"{name} - '{datadictionary[name]['allowed']}'")
      factorCols.append(name)
    elif ('type', 'string') in datadictionary[name].items():
      stringCols.append(name)
    elif datadictionary[name]['type'] in _numericTypes:
    # elif ('type', 'integer') in datadictionary[name].items():
      numberCols.append(name)
    else:
      print(f"WARNING: Unrecognized Type! ({datadictionary[name].items()})")

  print(f"{len(datadictionary)} variables found in data dictionary")
  summarydata = {}
  # pdb.set_trace()

  unassigned = []
  for col in datasetfile:
    if col in factorCols:
      summarize_factors(datadictionary, datasetfile, col, summarydata)
    elif col in numberCols:
      summarize_numbers(datasetfile, col, summarydata)
    elif col in stringCols:
      summarize_strings(datasetfile, col, summarydata)
    else:
      unassigned.append(col)
  # Write to YAML (see https://docs.google.com/document/d/1zHsyAo6d-BkjExUi-gf_MJ7zoWDcVU_GG4YlH5A1pBs/edit?usp=sharing)

  fileName = 'summary_dat_' + appendToYAML + '.yaml'
  with open('data/' + fileName, 'w') as f:
    yaml.dump(summarydata, f)

  print(f"{len(summarydata)} variables written to {fileName}")
  print(f"{len(unassigned)} unrecognized variables:")
  print("\t"+"\n\t".join(unassigned))
