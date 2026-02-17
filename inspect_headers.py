
import pandas as pd
import os

FILES = [
    "SegIndic_PPPC_300625.xlsx", 
    "020226_SPC_301225.xlsx"
]

def inspect():
    for f in FILES:
        if not os.path.exists(f): continue
        print(f"--- Inspecting {f} ---")
        try:
            xl = pd.ExcelFile(f)
            for s in xl.sheet_names:
                df = xl.parse(s, header=None)
                # Look for header row
                for r in range(min(20, len(df))):
                    row = [str(x).lower().strip() for x in df.iloc[r].values]
                    if "código indicador" in row or "nombre indicador" in row:
                        print(f"  Sheet: {s}, Header Row: {r}")
                        # Print potential interesting columns
                        for c, val in enumerate(row):
                            if any(k in val for k in ["terr", "comuna", "poblaci", "grupo", "desapreg"]):
                                print(f"    found col {c}: {val}")
                        break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
