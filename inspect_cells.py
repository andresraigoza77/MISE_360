
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    # Check Row 5, Cols 24, 49, and maybe +25 = 74?
    indices = [24, 49, 74, 99] 
    print(f"--- Checking Row 5 at indices {indices} ---")
    for idx in indices:
        if idx < df.shape[1]:
            val = df.iloc[5, idx]
            print(f"Col {idx}: {val}")
        else:
            print(f"Col {idx}: Out of bounds")
            
except Exception as e:
    print(e)
