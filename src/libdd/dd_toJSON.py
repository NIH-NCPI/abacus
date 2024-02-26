from collections import defaultdict

def ddtoJSON(ddfile):
   
   di = defaultdict(dict)

   df2 = ddfile.fillna(0)
   for i, row in df2.iterrows():
        if df2.loc[i, 'allowed'] != 0:
            df2.loc[i, 'allowed'] = df2.loc[i, 'allowed'].split(";")
            di[row.name] = row.to_dict()
        else:
            di[row.name] = row.to_dict()

   return di
   # prettyDictionary = json.dumps(di_clean, indent = 4)




