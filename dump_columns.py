
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025" # Hardcoded from previous finding
    df = xl.parse(sh, header=None)
    
    # Header was at row 7
    row = df.iloc[7].values
    print(f"--- Columns for Row 7 in {sh} ---")
    for i, val in enumerate(row):
        s_val = str(val).lower()
        # Clean newlines
        s_val = s_val.replace('\n', ' ')
        print(f"Col {i}: {s_val}")
        
except Exception as e:
    print(e)
