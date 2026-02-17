
import pandas as pd
import sys

file_path = "SegIndic_PPPC_300625.xlsx"

try:
    xl = pd.ExcelFile(file_path)
    print(f"Excel file loaded: {file_path}")
    print(f"Sheet names: {xl.sheet_names}")
    
    for sheet_name in xl.sheet_names:
        print(f"\n--- Analysis of Sheet: {sheet_name} ---")
        df = xl.parse(sheet_name)
        
        print(f"Dimensions: {df.shape}")
        print("Columns:")
        for col in df.columns:
            print(f"  - {col} ({df[col].dtype})")
            
        print("\nFirst 5 rows:")
        print(df.head().to_string())
        
        # Basic redundancy check
        duplicates = df.duplicated().sum()
        print(f"\nDuplicate rows: {duplicates}")
        
        # Check for potential master data columns (low cardinality)
        print("\nPotential Categorical Columns (Cardinality < 20):")
        for col in df.columns:
            if df[col].nunique() < 20 and df[col].dtype == 'object':
                print(f"  - {col}: {df[col].unique()}")

except Exception as e:
    print(f"Error inspecting Excel file: {e}")
    sys.exit(1)
