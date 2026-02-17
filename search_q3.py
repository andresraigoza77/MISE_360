
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    with open("search_q3.txt", "w", encoding="utf-8") as f:
        # Row 5 (Index 5)
        f.write("--- ROW 5 ---\n")
        if 5 < len(df):
            for i, val in enumerate(df.iloc[5].values):
                s = str(val).strip()
                if len(s) > 2 and s.lower() != 'nan':
                    f.write(f"Col {i}: {s}\n")
        
        # Row 7 (Index 7)
        f.write("--- ROW 7 ---\n")
        if 7 < len(df):
            for i, val in enumerate(df.iloc[7].values):
                s = str(val).strip()
                if len(s) > 2 and s.lower() != 'nan':
                    f.write(f"Col {i}: {s}\n")

except Exception as e:
    print(e)
