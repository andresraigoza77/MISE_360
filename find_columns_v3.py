
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    row = df.iloc[7].values
    with open("cols_v3.txt", "w", encoding="utf-8") as f:
        f.write(f"--- Columns 30-55 for Row 7 in {sh} ---\n")
        for i in range(30, min(56, len(row))):
            s_val = str(row[i]).lower().replace('\n', ' ')
            f.write(f"Col {i}: {s_val}\n")
            
except Exception as e:
    print(e)
