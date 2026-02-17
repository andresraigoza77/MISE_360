
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    print("--- Searching for 'III' ---")
    for r in range(5, 9):
        if r >= len(df): break
        row = df.iloc[r].values
        for i, val in enumerate(row):
            s = str(val).upper() # Case insensitive
            if "III" in s:
                print(f"Row {r}, Col {i}: {val}")
                        
except Exception as e:
    print(e)
