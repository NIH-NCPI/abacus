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
example_summary = yaml.safe_load(dummyoutput)

def gensummary(datadictionary, datasetfile):
    # TBD actually do the summary :) 
    return example_summary