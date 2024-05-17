# for creating default empty dictionary objects
from collections import defaultdict
import pdb
import math

_missingRepresentation = 0
def missingRepresentation(msng = None):
    global _missingRepresentation
    if msng is not None:
        _missingRepresentation = msng
    return _missingRepresentation

def checkisnan(value):
    if type(value) is float:
        return math.isnan(value)
    return value == "nan"

def ddtoJSON(ddfile):
    """ Convert CSV to Dictionary/JSON Format
    Data dictionary as csv [read_csv(ddfile)] -> Data dictionary to JSON [ddtoJSON(ddfile)] -> 
    Data Dictionary clean null terms [cleanNullTerms(ddJSON)]

    input argument ddfile - the pandas representation of the data dictionary after loading it in 
    using read_csv()

    missingRepresentation - 0 is chosen as a placeholder for NA/None/null values imported in the
    data dictionary pandas object.
    
    """

    dictionaryObject = defaultdict(dict)
    pdb.set_trace()
    # ddfileReplaceMissing = ddfile.fillna(missingRepresentation())
    for i, row in ddfile.iterrows():
        print(row.allowed)
        print(type(row.allowed))
        if not checkisnan(row.allowed) and row.allowed != 0 and row.allowed.strip() != '':
            # pdb.set_trace()
            row.allowed = row.allowed.split(";")
        else:
            row.allowed = []
        dictionaryObject[i] = row.to_dict()
    
    return dictionaryObject
