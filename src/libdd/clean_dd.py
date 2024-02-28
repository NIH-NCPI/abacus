''' Clean Null Terms from Data Dictionaries
Data dictionary as csv [read_csv(ddfile)] -> Data dictionary to JSON [ddtoJSON(ddfile)] -> 
Data Dictionary clean null terms [cleanNullTerms(ddJSON)]

ddJSON input argument - Data dictionary in JSON/Dictionary format so function dd_toJSON() should be run 
first on a csv data dictionary file one wants to transform

k,v - iterations to go through nested data dictionary structure in JSON/Dictionary format and remove
instances where the value of a key is equal to 0 (see _missingRepresentation in dd_toJSON.py)
'''

def cleanNullTerms(ddJSON):
   clean = {}
   for k, v in ddJSON.items():
        if isinstance(v, dict):
            nested = cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v != 0:
            clean[k] = v
   return clean