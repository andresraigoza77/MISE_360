
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    found = False
    if sh in xl.sheet_names:
        found = True
    else:
        for s in xl.sheet_names:
            if "seguimiento" in s.lower() and "2025" in s.lower():
                sh = s
                found = True
                break
    
    if not found:
        print("Sheet not found")
        exit()

    print(f"Sheet: {sh}")
    df = xl.parse(sh, header=None)
    
    r = 14
    if r < len(df):
        row = df.iloc[r].values
        print(f"--- Row {r} Content ---")
        for i, val in enumerate(row):
            s_val = str(val).strip()
            if s_val and s_val.lower() != 'nan':
                 print(f"Col {i}: {s_val}")
            
except Exception as e:
    print(e)
