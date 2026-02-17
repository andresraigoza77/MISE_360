
import pandas as pd

FILE = "020226_SPC_301225.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = xl.sheet_names[0] # Assume first sheet for now or search
    # Find sheet with data
    for s in xl.sheet_names:
        df = xl.parse(s, header=None)
        # Check if it has "Código Indicador"
        found = False
        for r in range(min(15, len(df))):
            row = [str(x).lower() for x in df.iloc[r].values]
            if any("código indicador" in v for v in row):
                sh = s
                found = True
                break
        if found: break
        
    print(f"Inspecting File: {FILE}, Sheet: {sh}")
    df = xl.parse(sh, header=None)
    
    for i in range(15):
        print(f"Row {i}: {list(df.iloc[i].values)}")
        
except Exception as e:
    print(e)
