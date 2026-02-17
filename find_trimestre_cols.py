
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    for s in xl.sheet_names:
        df = xl.parse(s, header=None)
        for r in range(min(15, len(df))):
            row = [str(x).lower() for x in df.iloc[r].values]
            if any("código indicador" in v for v in row):
                print(f"Sheet: {s}, Header Row: {r}")
                for idx, col in enumerate(row):
                    if "trimestre" in col:
                        print(f"  Col {idx}: {col}")
                break
except Exception as e:
    print(e)
