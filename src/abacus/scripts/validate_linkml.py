
import os
import tempfile
import argparse
import pandas as pd
import yaml
from rich import print
from linkml_runtime.utils.schemaview import SchemaView
from linkml.validator import validate_file


def get_multivalued_fields(ddict):
    """Extracts fields (slots) from the schema where 'multivalued = true'."""
    schema = SchemaView(ddict)
    
    array_fields = [
        slot.name for slot in schema.all_slots().values() if slot.multivalued
    ]
    
    return array_fields

def get_classes(ddict):
    """Extracts class names from the data dictionary"""
    schema = SchemaView(ddict)

    class_names = list(schema.all_classes().keys())
    
    return class_names

def csv_to_yaml(ddict, dataset):
    """Converts CSV to YAML format and handles array fields."""
    
    # Extract a list of fields that should be arrays according to the dd.
    array_fields = get_multivalued_fields(ddict)

    df = pd.read_csv(dataset)

    # Convert DataFrame to a list of dictionaries (each row becomes a dict)
    records = df.to_dict(orient='records')

    # Process each record to convert the relevant fields into arrays
    for record in records:
        for field in array_fields:
            if field in record and isinstance(record[field], str):
                record[field] = record[field].split('|')

    # Create a temporary YAML file to store the output
    temp_yaml_file = tempfile.mktemp(suffix=".yaml")
    with open(temp_yaml_file, 'w') as file:
        yaml.dump(records, file, default_flow_style=False)

    print(f"YAML data written to temporary file: {temp_yaml_file}")
    return temp_yaml_file

def run_linkml_validate(ddict, dataset, dataclass):
    """Validates the dataset using LinkML's validate_file function.

    Args:
        ddict (str): Path to the LinkML schema file (YAML).
        dataset (str): Path to the dataset file (YAML or CSV) to be validated.
        dataclass (str): The target class of the validation

    """
    dd_classes = get_classes(ddict)
    # Ensure the target class exists in the schema
    if dataclass not in dd_classes:
        raise ValueError(f"Class {dataclass} not found. Available classes: {dd_classes}.")

    try:
        report = validate_file(dataset, ddict, dataclass)
        print(f"Validation Report:")
        print(report)
    except Exception as e:
        print(f"Validation failed: {e}")

def main():
    """Main function to run the LinkML validation with a temporary tree_root modification."""
    
    parser = argparse.ArgumentParser(description="Run linkml-validate with temporary tree_root modification.")
    parser.add_argument('-dd', '--dataDictionary', required=True, help='Path to the LinkML schema file (YAML).')
    parser.add_argument('-dt', '--dataSet', required=True, help='Path to the data file (CSV or YAML) to be validated.')
    parser.add_argument('-dc', '--dataClass', required=True, help='Target class to set as tree_root.')

    args = parser.parse_args()

    yaml_ds = None 

    try:
        # Check the file extension of the dataset
        _, ext = os.path.splitext(args.dataSet)
        
        if ext.lower() == '.csv':
            # Convert CSV to YAML before validation
            yaml_ds = csv_to_yaml(args.dataDictionary, args.dataSet)
            run_linkml_validate(args.dataDictionary, yaml_ds, args.dataClass)
        elif ext.lower() == '.yaml':
            # Directly validate the YAML dataset
            run_linkml_validate(args.dataDictionary, args.dataSet, args.dataClass)
        else:
            raise ValueError(f"Unsupported file type: Only CSV and YAML files are supported.")

    except ValueError as e:
        print(e)  # Handle the case where the class is not found
        return  # Ensure we exit here to avoid cleanup
    
    finally:
        # Clean up the temporary YAML file if it exists
        if yaml_ds and os.path.exists(yaml_ds):
            os.remove(yaml_ds)
            print(f"Temporary file {yaml_ds} has been cleaned up.")

if __name__ == '__main__':
    main()
