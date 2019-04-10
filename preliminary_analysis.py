import pandas as pd

overdose_data = pd.read_json("https://data.cdc.gov/resource/a3uk-kgrx.json")
print(overdose_data.columns.tolist())