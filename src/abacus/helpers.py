import pandas as pd
import cerberus
import pdb 
import yaml 
import pandas as pd
from collections import defaultdict
import statistics

 # Sets default missing notation. Will be used if none set by the user.
_missingRepresentation = 0

def missingRepresentation(msng = None):
    """
    Sets or retrieves the global `_missingRepresentation` value.

    This function allows setting a new global value for `_missingRepresentation` 
    or retrieving its current value. If a new value (`msng`) is provided, 
    `_missingRepresentation` is updated; otherwise, it returns the current value.

    Args:
        msng (Optional[Any]): The new value to set for `_missingRepresentation`. 
            If None, the current value is returned. Default is None.

    Returns:
        Any: The current value of `_missingRepresentation`, after setting it if 
        a new value is provided.
    """
    global _missingRepresentation
    if msng is not None:
        _missingRepresentation = msng
    return _missingRepresentation


def ddtoJSON(ddfile):
    """
    Convert CSV to a dictionary (JSON) format.

    This function processes a data dictionary in CSV format and converts it into a dictionary.
    Fields that are not null are included in the dictionary. The 'allowed' field, if present, 
    is split into a list of values.

    Args:
        ddfile (pandas.DataFrame): The imported data dictionary as a pandas dataframe.

    Returns:
        dict: A dictionary object where each row of the data dictionary is represented 
              as a key-value pair. Only non-null values are included, and 'allowed' 
              values are converted to a list.
    """

    dictionaryObject = defaultdict(dict)

    for i, row in ddfile.iterrows():
        # Initialize a temporary dictionary for the current record
        record = {}

        # Convert 'allowed' to a list only if it's not empty
        if pd.notna(row.allowed):
            record['allowed'] = row.allowed.split(";")

        # Add other fields to record only if they are not empty
        for key, value in row.items():
            if key != 'allowed' and pd.notna(value) and value != '':
                record[key] = value

        dictionaryObject[i] = record

    return dictionaryObject

