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

   ## Available actions:
   * [validate_csv](#validate_csv) <br>
   * [summarize_csv](#summarize_csv) <br> 
   * [validate_linkml](#validate_linkml) <br>
    


   ## Commands
    ### validate_csv
    `validate_csv` runs [cerberus]("https://docs.python-cerberus.org/index.html") validation on a datadictionary/dataset pair and returns results of the validation in the terminal. <br> 
     [See data expectations here](#csv-validationcerberus-and-summary)
    ```
    validate_csv -dd {path/to/datadictionary.csv} -dt {path/to/dataset.csv} -m {Format of missing values in the dataset choose one (i.e. NA, na, null, ...)}   

    # example
    validate_csv -dd data/input/data_dictionary.csv -dt data/input/dataset.csv -m NA 
    ```
    ### summarize_csv
    `summarize_csv` returns aggregates and attributes of the provided dataset which is exported as a yaml file. <br>
    [See data expectations here](#csv-validationcerberus-and-summary)
    ```
    summarize_csv -dd {path/to/datadictionary.csv} -dt {path/to/dataset.csv} -m {Format of missing values in the dataset choose one (i.e. NA, na, null, ...)} -e {export/filepath/summary.yaml}

    # example 
    summarize_csv -dd data/input/data_dictionary.csv -dt data/input/dataset.csv -m NA -e data/output/summary.yaml
    ```
    ### validate_linkml
     
    `validate_linkml` runs [linkml](https://linkml.io/linkml/index.html") validation on a datadictionary/dataset pair and returns results of the validation in the terminal from the directory that contains the datafiles. (datadictionary, dataset, AND iIMPORTS-adjoining datadictionaries)<br> 
    [See data expectations here](#yaml-validationlinkml)
    ```
    validate_linkml -dd {path/to/datadictionary.csv} -dt {path/to/dataset.csv} -dc {data class - linkml tree_root}

    # example 
    validate_linkml -dd data/input/assay.yaml -dt data/input/assay_data.yaml -dc Assay
    ```

    ## Data Expectations
    ### csv - validation(cerberus) and summary
    #### data dictionary format:
    [Visit this link for more indepth specs]("https://docs.google.com/document/d/1p5kIBoGf8U_axUo2ADUXQ5Mkx3zrDUJtywkZVi4sVkk/edit?usp=sharing")
  
    #### dataset format:
    Datasets should be csvs, follow the format described by the data dictionary, and have consitant notation of missing data [NULL, NA, etc.]. 

    ## yaml/json - validation(linkml)
    #### data dictionary format:
    Data dictionaries should be a yaml file formatted for linkml, and contain all
    dataset expectations for validation.
    Validation requires all data dictionaries referenced in the `imports` section
    present in the same file location. Imports beginning with `linkml:` can be ignored <br>
    Example seen below.
    ```
    id: https://w3id.org/include/assay
    imports:
    - linkml:types
    - include_core
    - include_participant
    - include_study
    ```

    #### dataset format:
    Datasets should be yaml, json or csv file formatted for linkml, follow the format 
    described by the data dictionary, and have consitant notation of missing 
    data [NULL, NA, etc.]. <br>
    <br>
    If the dataset is a csv, multivalue fields should have pipe separators <br>
    See examples below.
  
    ```bash
    # Yaml file representation
    # Instances of Biospecimen class
    - studyCode: "Study1"
      participantGlobalId: "PID123"
      ...
      ...
      ...
    - studyCode: "Study1"
      participantGlobalId: "PID123"

    ```
     CSV representation

    ```
    studyCode,studyTitle,program
    study_code,Study of Cancer,program1|program2
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