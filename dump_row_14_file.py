
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    if sh not in xl.sheet_names:
        for s in xl.sheet_names:
            if "seguimiento" in s.lower() and "2025" in s.lower(): sh = s
    
    df = xl.parse(sh, header=None)
    
    r = 14
    with open("row_14.txt", "w", encoding="utf-8") as f:
        if r < len(df):
            row = df.iloc[r].values
            for i, val in enumerate(row):
                s_val = str(val).strip()
                if s_val and s_val.lower() != 'nan':
                     f.write(f"Col {i}: {s_val}\n")
            
except Exception as e:
    print(e)
