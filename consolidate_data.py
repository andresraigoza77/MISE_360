
import pandas as pd
import os
import re

# Files to process
FILES = [
    "SegIndic_PPPC_300625.xlsx", 
    "020226_SPC_301225.xlsx", 
    "030226_GerenciaÉtnica.xlsx", 
    "090226_SISF_301225.xlsx", 
    "230126_Mujeres__MISE.xlsx", 
    "230126_SGHSC_300925.xlsx", 
    "260126_DAP.xlsx", 
    "270126_Sec_Educación.xlsx"
]

OUTPUT_FILE = "Matriz_Maestra_MISE_2025_Consolidada.xlsx"

def normalize_header(h):
    # Basic normalization: lower, strip, remove extra spaces
    if pd.isna(h): return f"col_{id(h)}"
    h = str(h).strip().lower()
    h = re.sub(r'\s+', ' ', h)
    return h

def consolidate():
    all_frames = []
    
    print(f"Starting consolidation of {len(FILES)} files...")
    
    total_rows = 0
    known_columns = set()

    for f in FILES:
        if not os.path.exists(f):
            print(f"⚠️ File not found: {f}")
            continue
            
        print(f"📄 Processing {f}...")
        try:
            xl = pd.ExcelFile(f)
            
            for s in xl.sheet_names:
                # Heuristic to find data table
                df_raw = xl.parse(s, header=None)
                header_row_idx = None
                
                # Scan first 20 rows for "Código Indicador" or "Nombre Indicador"
                for r in range(min(20, len(df_raw))):
                    row_vals = [str(x).lower() for x in df_raw.iloc[r].values]
                    if any("código indicador" in v or "nombre indicador" in v for v in row_vals):
                        header_row_idx = r
                        break
                
                if header_row_idx is None:
                    # print(f"  Skipping sheet {s} (no header found)")
                    continue
                
                print(f"  + Sheet: {s}")
                
                # Parse with correct header
                df = xl.parse(s, header=header_row_idx)
                
                # Clean headers
                df.columns = [normalize_header(c) for c in df.columns]
                
                # Add Source Metadata
                df['source_file'] = os.path.basename(f)
                df['source_sheet'] = s
                
                # Drop rows where 'código indicador' is likely empty or summary lines
                # Find the ID column
                id_cols = [c for c in df.columns if "código indicador" in c or "codigo indicador" in c]
                if id_cols:
                    # Filter invalid IDs
                    df = df[df[id_cols[0]].astype(str).str.match(r'^\d+(\.\d+)?$')]
                
                if not df.empty:
                    all_frames.append(df)
                    total_rows += len(df)
                    known_columns.update(df.columns)
                    
        except Exception as e:
            print(f"❌ Error processing {f}: {e}")

    if not all_frames:
        print("No data collected.")
        return

    print(f"Merging {len(all_frames)} dataframes with {len(known_columns)} distinct columns...")
    
    # Concatenate (Outer Join by default)
    master_df = pd.concat(all_frames, ignore_index=True, sort=False)
    
    # Fill N/A
    master_df = master_df.fillna("N/A")
    
    # Export
    print(f"Writing to {OUTPUT_FILE} ({len(master_df)} rows)...")
    master_df.to_excel(OUTPUT_FILE, index=False)
    print("✅ Consolidation complete.")

if __name__ == "__main__":
    consolidate()
