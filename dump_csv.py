
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    # Save first 20 rows to csv
    df.head(20).to_csv("dump.csv", index=False, header=False, encoding="utf-8")
    print("Dumped dump.csv")
            
except Exception as e:
    print(e)
