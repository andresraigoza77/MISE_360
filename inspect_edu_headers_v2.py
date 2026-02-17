
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    print(f"Sheets: {xl.sheet_names}")
    with open("headers_edu.txt", "w", encoding="utf-8") as f:
        for s in xl.sheet_names:
            df = xl.parse(s, header=None)
            found = False
            for r in range(min(15, len(df))):
                row = [str(x).lower() for x in df.iloc[r].values]
                if any("código indicador" in v for v in row):
                    f.write(f"Sheet: {s}, Header Row: {r}\n")
                    f.write(f"Headers: {row}\n")
                    found = True
                    break
            if found: break
except Exception as e:
    print(e)
