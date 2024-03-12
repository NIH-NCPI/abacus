import cerberus
import pdb 

def validate_and_report(ddJSON_clean, dtfileParsed):
    """ Create a report of the errors thrown by the cerberus data validator.
    If there are no errors, a report of row-level issues is not created but 
    there will be a message indicating no validation errors.
    """
    schema = ddJSON_clean
    v = cerberus.Validator(ddJSON_clean)
    counts = 0
    for i in range(0, len(dtfileParsed)):
        if v.validate(dtfileParsed[i]) == True:
            counts = counts+1
            if counts == len(dtfileParsed):
                print('No validation errors noted!')
        else:
            print('Error detected in row', i+1, ':', v.errors)

# Does not catch '1' as integer instead of 'Visit 1' 
