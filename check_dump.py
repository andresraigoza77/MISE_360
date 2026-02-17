
import pandas as pd

def check_dump():
    try:
        df = pd.read_csv("dump.csv", header=None, encoding='utf-8', on_bad_lines='skip') # or latin1
        # It's likely messy. Let's look for "Código Indicador"
        
        target_indices = []
        for i in range(min(50, len(df))):
            row = [str(x).lower() for x in df.iloc[i].values]
            if any("código indicador" in v for v in row):
                print(f"Found Header at row {i}")
                # Analyze cols
                # Assuming standard layout
                # Just iterate and try to find IDs
                pass

        # Since CSV structure is unknown, let's just grep for IDs
        # Valid IDs are numbers.
        # But that's too loose.
        
        # Let's try parsing with header=8 (common in others)
        # Or just find the column index dynamically
        pass
        
    except Exception as e:
        print(f"Error: {e}")

# Re-using logic from import_missing_indicators but adapted for CSV
# Actually, just use grep/text processing if pandas fails
import csv

def count_ids():
    seen_ids = set()
    with open("dump.csv", "r", encoding='latin1') as f: # Excel often saves as latin1/cp1252
        reader = csv.reader(f)
        for row in reader:
            # Look for ID in likely columns (e.g. col 3?)
            # Or just scan all columns for integer-like values > 100?
            for cell in row:
                s = str(cell).strip()
                if s.isdigit() and len(s) >= 3 and len(s) <= 4:
                    # Likely an ID? (e.g. 101, 705)
                    # Exclude years (2025)
                    if s.startswith('20'): continue
                    try:
                        seen_ids.add(int(s))
                    except: pass
    
    print(f"Found {len(seen_ids)} potential IDs in dump.csv (heuristic).")
    print(f"First 10: {list(seen_ids)[:10]}")

if __name__ == "__main__":
    count_ids()
