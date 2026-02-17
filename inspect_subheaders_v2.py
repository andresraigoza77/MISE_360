
import pandas as pd

FILE = "270126_Sec_Educación.xlsx"

try:
    xl = pd.ExcelFile(FILE)
    sh = "4. Seguimiento 2025"
    df = xl.parse(sh, header=None)
    
    with open("headers_map.txt", "w", encoding="utf-8") as f:
        f.write("--- Mapping Row 6 (Headers) vs Row 7 (Sub-headers) ---\n")
        # Columns 24 to 60
        for c in range(24, 60):
            if c >= df.shape[1]: break
            h1 = str(df.iloc[6, c]).replace('\n', ' ') if 6 < len(df) else "" # Row 6
            h2 = str(df.iloc[7, c]).replace('\n', ' ') if 7 < len(df) else "" # Row 7
            f.write(f"Col {c}: [R6] {h1[:30]:<30} | [R7] {h2}\n")

except Exception as e:
    print(e)
