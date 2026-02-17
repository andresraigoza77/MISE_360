
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    print("--- Mapping Row 6 (Headers) vs Row 7 (Sub-headers) ---")
    # Columns 24 to 60
    for c in range(24, 60):
        if c >= df.shape[1]: break
        h1 = str(df.iloc[6, c]).replace('\n', ' ')[:20] if 6 < len(df) else "" # Row 6
        h2 = str(df.iloc[7, c]).replace('\n', ' ')[:20] if 7 < len(df) else "" # Row 7
        print(f"Col {c}: [R6] {h1:<20} | [R7] {h2}")

except Exception as e:
    print(e)
