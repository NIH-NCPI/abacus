dummyoutput = '''Down Syndrome Status:
  D21: 370
  T21: 685
  Total Count of Values: 1055
Ethnicity:
  Hispanic or Latino: 153
  Not Hispanic or Latino: 862
  Prefer not to answer: 0
  Total Count of Values: 1055
  Unknown: 40
Family Relationship:
  Father: 0
  Mother: 0
  Other: 122
  Other relative: 0
  Parent: 91
  Proband: 685
  Sibling: 157
  Total Count of Values: 1055
Family Type:
  Control-only: 152
  Duo: 52
  Other: 235
  Proband-only: 538
  Total Count of Values: 1055
  Trio: 22
  Trio+: 56
First Patient Engagement Event:
  Baseline visit: 0
  Biospecimen collection: 0
  Enrollment: 1055
  Total Count of Values: 1055
Outcomes Vital Status:
  Alive: 1049
  Dead: 6
  Total Count of Values: 1055
  Unknown or not available: 0
Participant External ID: 1055
Participant Global ID: 1055
Race:
  American Indian or Alaska Native: 7
  Asian: 19
  Black or African American: 24
  East Asian: 0
  Latin American: 0
  Middle Eastern or North African: 0
  More than one race: 68
  Native Hawaiian or Other Pacific Islander: 2
  Other: 0
  Prefer not to answer: 0
  South Asian: 0
  Total Count of Values: 1055
  Unknown: 45
  White: 890
Sex:
  Female: 549
  Male: 506
  Other: 0
  Total Count of Values: 1055
  Unknown: 0
'''
import yaml 
import statistics
import pandas as pd


example_summary = yaml.safe_load(dummyoutput)

def gensummary(datadictionary, datasetfile):
    
    # Figure out which columns are factor-like variables with allowed values
    factorCols = []
    numberCols = []
    stringCols = []  # have to do something about integer and number values
    # Have to do something about string type data such as id's


    # ('type','integer')  in ddJSON['Age at First Patient Engagement'].items()
    # 'allowed' in ddJSON['Ethnicity'].keys()

    # 'allowed' not in ddJSON['Ethnicity'].keys()

    for name in datadictionary:
       if 'allowed' in datadictionary[name].keys():
         factorCols.append(name)
       elif ('type', 'string') in datadictionary[name].items() and ('allowed' not in datadictionary[name].keys()):
         stringCols.append(name)
       elif ('type', 'integer') in datadictionary[name].items():
         numberCols.append(name)

    dictionary = {}

    for col in datasetfile:
        if col in factorCols:
          elements = pd.value_counts(datasetfile[col]).to_dict()
          dictionary[col]=elements

          # Fill out the unused possible values with 0 counts
          setA = list(datadictionary[col]['allowed'])
          setB = list(pd.unique(datasetfile[col]))
          difAB = list(set(setA).difference(setB))

          if difAB != []:
              for p in range(len(difAB)):
                 dictionary[col][difAB[p]] = 0

          dictionary[col]['Total Count of Values'] = sum(dictionary[col].values())

        elif col in numberCols:
          dictionary[col]['Min'] = min(datasetfile[col])
          dictionary[col]['Max'] = max(datasetfile[col])
          dictionary[col]['Median'] = statistics.median(datasetfile[col])

        elif col in stringCols:
          dictionary[col]=len(pd.unique(datasetfile[col]))

    # Write to YAML (see https://docs.google.com/document/d/1zHsyAo6d-BkjExUi-gf_MJ7zoWDcVU_GG4YlH5A1pBs/edit?usp=sharing)

    with open('C:/Users/ann14/dev/INCLUDE/libdd/data/summary_dat.yaml', 'w') as f:
       yaml.dump(dictionary, f)

    # print(yaml.dump(dictionary))