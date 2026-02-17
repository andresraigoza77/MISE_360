
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

def find_header_row_and_cols(df):
    found_cols = {
        'trim_1': None, 'trim_2': None, 'trim_3': None, 'trim_4': None
    }

    for r in range(min(15, len(df))):
        row_vals = [str(x).lower() for x in df.iloc[r].values]
        for c, val in enumerate(row_vals):
            # Same logic as ETL v6
            if 'trimestre i ' in val and '2025' in val: 
                found_cols['trim_1'] = (c, val)
            elif 'trimestre ii' in val: 
                found_cols['trim_2'] = (c, val)
            elif 'trimestre iii' in val: 
                found_cols['trim_3'] = (c, val)
            elif 'trimestre iv' in val: 
                found_cols['trim_4'] = (c, val)
            
    return found_cols

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    cols = find_header_row_and_cols(df)
    print("--- Detected Columns ---")
    for k, v in cols.items():
        print(f"{k}: {v}")
            
except Exception as e:
    print(e)
