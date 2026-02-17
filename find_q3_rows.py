
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    with open("found_q3_rows.txt", "w", encoding="utf-8") as f:
        for r_idx in range(5, 9): # Check 5, 6, 7, 8
            if r_idx >= len(df): break
            row = df.iloc[r_idx].values
            f.write(f"--- ROW {r_idx} ---\n")
            for i, val in enumerate(row):
                s_val = str(val).lower().replace('\n', ' ')
                if any(x in s_val for x in ["trimestre", "trim", "iii", "3", "iv", "4"]):
                    f.write(f"Col {i}: {s_val}\n")
            
except Exception as e:
    print(e)
