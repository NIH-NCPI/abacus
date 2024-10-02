"""
Runs linkml validation on a datadictionary/dataset pair defined in the command
arguments. 

Process:
Places the data dictionary and required imports into a temp directory.
 - The data dictionary must be edited to define the `tree_root` for validation
   so a temporary copy is made and edited for this purpose.
Runs linkml validation
Returns the results in the terminal

"""

import argparse
import yaml
import subprocess
import os
import tempfile
import shutil

def modify_yaml_add_tree_root(ddict, target_class):
    """Modifies the data dictionary file to add `tree_root: true` to the specified class.
    The root signifies the starting point for the relationships to branch off of.

    Example:
      Biospecimen:
        tree_root: true

    Args:
        ddict (str): Path to the LinkML schema file (YAML).
        target_class (str): The target class to set as tree_root.

    Returns:
        tuple: A tuple containing the path to the temporary modified schema file and the temporary directory.
    """
    # Find and open the data dictionary
    if not os.path.exists(ddict):
        raise FileNotFoundError(f"File not found: {ddict}")

    with open(ddict, 'r') as f:
        data = yaml.safe_load(f)

    # Ensure the target class exists in the schema
    if 'classes' not in data or target_class not in data['classes']:
        raise ValueError(f"Class {target_class} not found. Available classes: {list(data['classes'].keys())}.")

    # Define the tree_root for the specified class
    data['classes'][target_class]['tree_root'] = True

    # Create a temporary directory and file path
    temp_dir = tempfile.mkdtemp()  
    temp_ddict = os.path.join(temp_dir, os.path.basename(ddict)) 
    
    print(f"Temporary schema file path: {temp_ddict}")
    
    # Write the updated content to the temporary file
    with open(temp_ddict, 'w') as f:
        yaml.dump(data, f)

    # If exiting, copy the dd required imports into the temp dir
    if 'imports' in data:
        original_imports = data['imports']
        data['imports'] = [imp for imp in original_imports if not imp.startswith('linkml:')]
        
        for imp in data['imports']:
            imp_path = os.path.join(os.path.dirname(ddict), imp + '.yaml')
            if not os.path.exists(imp_path):
                raise FileNotFoundError(f"Imported file not found: {imp_path}")
            shutil.copy(imp_path, os.path.join(temp_dir, imp + '.yaml'))
            
    return temp_ddict, temp_dir

def run_linkml_validate(temp_ddict, dataset):
    """Runs the linkml-validate command

    Args:
        ddict (str): Path to the modified LinkML schema file (YAML).
        dataset (str): Path to the dataset file (YAML) to be validated.

    Raises:
        subprocess.CalledProcessError: If the validation command fails.
    """
    command = ['linkml-validate', '-s', temp_ddict, dataset]
    print(command)
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Validation output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Validation failed with return code {e.returncode}:")
        print("Error output:\n", e.stdout)
        print("Standard output:\n", e.stderr)


def main():
    """Main function to run the LinkML validation with a temporary tree_root modification."""
    
    parser = argparse.ArgumentParser(description="Run linkml-validate with temporary tree_root modification.")
    parser.add_argument('-dd', '--dataDictionary', required=True, help='Path to the LinkML schema file (YAML).')
    parser.add_argument('-dt', '--dataSet', required=True, help='Path to the data file (YAML) to be validated.')
    parser.add_argument('-dc', '--dataClass', required=True, help='Target class to set as tree_root.')

    args = parser.parse_args()
    
    temp_dir = None

    # Modify the schema to add tree_root temporarily, run validation, remove the temp dir
    try:
        temp_ddict, temp_dir = modify_yaml_add_tree_root(args.dataDictionary, args.dataClass)
        run_linkml_validate(temp_ddict, args.dataSet)
    except ValueError as e:
        print(e)  # Handle the case where the class is not found
        return  # Ensure we exit here to avoid cleanup
    finally:
        # Clean up temporary files if temp_dir is created
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    main()
