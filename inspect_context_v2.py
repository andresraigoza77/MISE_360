
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    with open("context_v2.txt", "w", encoding="utf-8") as f:
        for s in xl.sheet_names:
            df = xl.parse(s, header=None)
            found = False
            target_r = -1
            for r in range(min(15, len(df))):
                row = [str(x).lower() for x in df.iloc[r].values]
                if any("código indicador" in v for v in row):
                    target_r = r
                    found = True
                    break
            
            if found:
                f.write(f"Sheet: {s}, Main Header Row: {target_r}\n")
                start = max(0, target_r - 2)
                end = min(len(df), target_r + 3)
                for i in range(start, end):
                    f.write(f"Row {i}: {[str(x) for x in df.iloc[i].values]}\n")
                break
except Exception as e:
    print(e)
