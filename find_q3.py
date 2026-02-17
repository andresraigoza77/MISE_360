
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    row = df.iloc[7].values
    with open("found_q3.txt", "w", encoding="utf-8") as f:
        for i, val in enumerate(row):
            s_val = str(val).lower().replace('\n', ' ')
            if any(x in s_val for x in ["trimestre", "trim", "iii", "3", "iv", "4", "ejecutado"]):
                f.write(f"Col {i}: {s_val}\n")
            
except Exception as e:
    print(e)
