import cerberus
import pdb 

def validate_and_report(ddJSON_clean, dtfileParsed):
    schema = ddJSON_clean
    pdb.set_trace()
    v = cerberus.Validator(ddJSON_clean)

    for i in range(0, len(dtfileParsed)):
        print(i)
        print(dtfileParsed[i])
        pdb.set_trace()
        if v.validate(dtfileParsed[i]) == False:
            print(v.errors)
