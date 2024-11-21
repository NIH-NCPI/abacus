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


def read_dt(ddfile, dtfile, na_values):
    """Reads the dataset and sets the columns to the dtype specified by 
    the ddfile. If a record is not able to be set to the dtype the record
    will be counted as a 'skipped' record."""

    dd_specified_types = {}
    for col_name, row in ddfile.iterrows():
        col_type = row["type"]

        if col_type in ["int", "integer"]:
            dd_specified_types[col_name] = "Int64"
        elif col_type in ["float", "number"]:
            dd_specified_types[col_name] = "float64"
        elif col_type == "string":
            dd_specified_types[col_name] = "string"
        else:
            dd_specified_types[col_name] = "object"

    # Read raw data from CSV
    raw_dtfile = pd.read_csv(dtfile, na_values=na_values, keep_default_na=False)

    formatted_dtfile = raw_dtfile.copy()
    skipped_data = pd.DataFrame()

    for col, dtype in dd_specified_types.items():
        if col not in formatted_dtfile.columns:
            print(f"Column {col} from data dictionary not found in dataset.")
            continue

        try:
            # Attempt to convert column to the specified dtype
            if dtype == "string":
                formatted_dtfile[col] = formatted_dtfile[col].astype("string")
                message = col
            elif dtype == "Int64" or dtype == "float64":
                formatted_dtfile[col] = pd.to_numeric(
                    formatted_dtfile[col], errors="coerce"
                )
            else:
                formatted_dtfile[col] = formatted_dtfile[col].astype(dtype)

        except Exception as e:
            print(
                f"Error during type conversion for column '{col}' to dtype '{dtype}': {e}"
            )
            problematic_rows = formatted_dtfile[[col]].copy()
            skipped_data = pd.concat(
                [skipped_data, problematic_rows], ignore_index=True
            )
            formatted_dtfile[col] = pd.to_numeric(
                formatted_dtfile[col], errors="coerce"
            )

    # Log and return clean data
    clean_data = formatted_dtfile[
        ~formatted_dtfile.index.isin(skipped_data.index)
    ].reset_index(drop=True)

    return clean_data, skipped_data
