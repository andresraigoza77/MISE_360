
import pandas as pd
import sys

file_path = "SegIndic_PPPC_300625.xlsx"
output_file = "excel_structure.txt"

try:
    with open(output_file, "w", encoding="utf-8") as f:
        xl = pd.ExcelFile(file_path)
        f.write(f"Excel file loaded: {file_path}\n")
        f.write(f"Sheet names: {xl.sheet_names}\n")
        
        for sheet_name in xl.sheet_names:
            f.write(f"\n--- Analysis of Sheet: {sheet_name} ---\n")
            df = xl.parse(sheet_name)
            
            f.write(f"Dimensions: {df.shape}\n")
            f.write("Columns:\n")
            for col in df.columns:
                f.write(f"  - {col} ({df[col].dtype})\n")
                
            f.write("\nFirst 5 rows:\n")
            f.write(df.head().to_string())
            f.write("\n")
            
            # Check for potential master data columns (low cardinality)
            f.write("\nPotential Categorical Columns (Cardinality < 20):\n")
            for col in df.columns:
                if df[col].nunique() < 20 and df[col].dtype == 'object':
                    unique_vals = df[col].unique()
                    f.write(f"  - {col}: {unique_vals}\n")

    print(f"Analysis saved to {output_file}")

except Exception as e:
    print(f"Error inspecting Excel file: {e}")
    sys.exit(1)
