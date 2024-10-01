# Abacus
A data validation tool.


## Overview

The `abacus` repository includes scripts and tools that facilitate various forms
of validation between datasets and their data dictionaries(data expectiations).


## Installation

1. **Create and activate a virtual environment** (recommended):
    ```bash
    # cd into the directory to store the venv
    python3 -m venv abacus_venv
    source abacus_venv/bin/activate 
    # On Windows: venv\Scripts\activate
    ```

2. **Install the package and dependencies**:
    ```bash
    pip install git+https://github.com/NIH-NCPI/abacus.git
    ```

   ## Run 

    ### Run in CLI
    Check the `.toml` file for all available commands. Most are listed here.

    ## validate_csv
    `validate_csv` runs [cerberus]("https://docs.python-cerberus.org/index.html") validation on a datadictionary/dataset pair and returns results of the validation in the terminal. <br> 
    ```
    validate_csv -dd {path/to/datadictionary.csv} -dt {path/to/dataset.csv} -m {Format of missing values in the dataset choose one (i.e. NA, na, null, ...)}   

    # example
    validate_csv -dd data/input/data_dictionary.csv -dt data/input/dataset.csv -m NA 
    ```
    ## summarize_csv
    `summarize_csv` returns aggregates and attributes of the provided dataset which is exported as a yaml file.
    ```
    summarize_csv -dd {path/to/datadictionary.csv} -dt {path/to/dataset.csv} -m {Format of missing values in the dataset choose one (i.e. NA, na, null, ...)} -e {export/filepath/summary.yaml}

    # example 
    summarize_csv -dd data/input/data_dictionary.csv -dt data/input/dataset.csv -m NA -e data/output/summary.yaml
    ```
    ## validate_linkml
    `validate_linkml` runs [linkml]("https://linkml.io/linkml/index.html") validation on a datadictionary/dataset pair and returns results of the validation in the terminal.
    ```
    validate_linkml -dd {path/to/datadictionary.csv} -dt {path/to/dataset.csv} -dc {data class - linkml tree_root}

    # example 
    validate_linkml -dd data/input/assay.yaml -dt data/input/assay_data.yaml -dc Assay
    ```

    ## Working on a branch?
    If working on a new feature it is possible to install a package version within
    the remote or local branch
      ```
    # remote
    pip install git+https://github.com/NIH-NCPI/abacus.git@{branch_name}

    # local
    pip install -e .
    ```