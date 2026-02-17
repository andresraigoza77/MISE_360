
import pandas as pd
import sqlite3
import os
import re

# Configuration
EXCEL_FILE = "SegIndic_PPPC_300625.xlsx"
DB_FILE = "mise_digital.db"

# Column Mapping (0-based index from inspection)
# Based on 'Matriz_MISE_Cultura_300625' and 'Matriz_MISE_DAP_300625'
# Note: These indices are based on the inspection output. 
# We'll need to be robust. Best to find headers dynamically or use strict indices if format is fixed.
# Inspection showed:
# ID Ind: Unnamed: 3
# Subdim: Unnamed: 5
# Linea Base: Unnamed: 17
# Meta: Unnamed: 20
# Trim I Res: Unnamed: 24
# Trim II Res: Unnamed: 27
# Trim III Res: Unnamed: 30
# Trim IV Res: Unnamed: 33
# Responsable Cod: Unnamed: 44 (Reporte)
# Proyecto Cod: Unnamed: 49

# Let's try to map by column header text in row 5 (index 5, 0-based? or 4?)
# File has merged headers.
# Let's read with header=None and find the row with 'Código Indicador'.

def get_header_row_index(df):
    for i, row in df.iterrows():
        # Look for a row that contains 'Código Indicador' or specific known headers
        row_str = row.astype(str).values
        if 'Código Indicador' in row_str or 'Características del Indicador' in row_str:
            return i + 1 # The row after structural headers usually has the specific column names
        if 'Subdimensión' in row_str:
            return i
    return -1

def clean_value(val):
    if pd.isna(val) or val == 'No aplica' or val == 'nan':
        return None
    return val

def clean_numeric(val):
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return val
    s = str(val).strip().replace(',', '.')
    try:
        return float(s)
    except:
        return None

def run_etl():
    print(f"Loading Excel file: {EXCEL_FILE}")
    xl = pd.ExcelFile(EXCEL_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Collect Data
    dependencias_set = {} # code -> name
    proyectos_set = {} # code -> {name, budget, dep_code}
    indicadores_list = []
    reportes_list = []
    
    # Sheets to process
    target_sheets = [s for s in xl.sheet_names if s.startswith('Matriz_MISE_')]
    print(f"Found {len(target_sheets)} sheets to process: {target_sheets}")
    
    for sheet_name in target_sheets:
        print(f"Processing sheet: {sheet_name}")
        df_raw = xl.parse(sheet_name, header=None)
        
        # Locate extraction anchors
        # We'll use fixed indices based on the inspection since dynamic finding might be brittle with merged punctuation
        # Indices based on 'excel_structure.txt' which showed 'Unnamed: X'
        # Unnamed: 3 is index 3.
        
        # Determine start row for data
        # Data usually starts after the header row that contains 'Código Indicador'
        start_row = 0
        for i, row in df_raw.iterrows():
            if pd.notna(row[3]) and str(row[3]).strip() == 'Código Indicador':
                start_row = i + 1
                break
            # Fallback: look for numeric ID in col 3
            if isinstance(row[3], int) and row[3] > 100:
                start_row = i
                break
        
        if start_row == 0:
            print(f"  Warning: Could not determine start row for {sheet_name}. Guessing row 7.")
            start_row = 7

        # Iterate data rows
        for i in range(start_row, len(df_raw)):
            row = df_raw.iloc[i]
            
            # Extract ID Indicator
            id_ind_raw = row[3]
            if pd.isna(id_ind_raw) or not str(id_ind_raw).isdigit():
                continue # Skip empty or invalid rows
                
            id_indicador = int(id_ind_raw)
            nombre_indicador = str(row[4]) if pd.notna(row[4]) else "Sin Nombre"
            subdimension = str(row[5]) if pd.notna(row[5]) else None
            
            # Dependencies
            dep_cod_raw = row[44] # Col 44
            dep_cod = None
            if pd.notna(dep_cod_raw) and str(dep_cod_raw).isdigit():
                dep_cod = int(dep_cod_raw)
                # Infer name from sheet or just use code for now if name not in row
                # Often table has 'Responsables' in col 44 header, but value is code
                # We can try to map some known ones or use invalid name
                if dep_cod not in dependencias_set:
                    # Generic name until we have a master list
                    dependencias_set[dep_cod] = f"Dependencia {dep_cod}" 
            
            # Projects
            proj_cod_raw = row[49] # Col 49
            proj_cod = None
            presupuesto = clean_numeric(row[52]) # Col 52
            if pd.notna(proj_cod_raw) and str(proj_cod_raw).strip() != 'No aplica':
                proj_cod = str(proj_cod_raw).strip()
                if proj_cod not in proyectos_set:
                    proyectos_set[proj_cod] = {
                        'nombre': f"Proyecto {proj_cod}", # Placeholder
                        'presupuesto': presupuesto,
                        'dep': dep_cod
                    }

            # Indicator Attributes
            linea_base = clean_numeric(row[17]) # Col 17
            meta_total = clean_numeric(row[20]) # Col 20
            
            indicadores_list.append((
                id_indicador, nombre_indicador, subdimension, None, 'Gestión', 
                linea_base, 2024, meta_total, 2025, proj_cod, dep_cod
            ))
            
            # Quarterly Reports (Unpivoting)
            # Trim 1: Col 24
            # Trim 2: Col 27
            # Trim 3: Col 30
            # Trim 4: Col 33
            
            quarters = [
                (1, 24), (2, 27), (3, 30), (4, 33)
            ]
            
            for q, col_idx in quarters:
                val = clean_numeric(row[col_idx])
                if val is not None:
                    reportes_list.append((
                        id_indicador, 2025, q, None, val, None, None, None
                    ))

    # 2. Insert Data
    print("\nInserting Data...")
    
    # Dependencies
    print(f"Inserting {len(dependencias_set)} Dependencies...")
    for code, name in dependencias_set.items():
        cursor.execute("INSERT OR IGNORE INTO Dependencias (id_dependencia, nombre_dependencia) VALUES (?, ?)", (code, name))
        
    # Projects
    print(f"Inserting {len(proyectos_set)} Projects...")
    for code, data in proyectos_set.items():
        cursor.execute("INSERT OR IGNORE INTO Proyectos (codigo_bpin, nombre_proyecto, presupuesto_programado_total, id_dependencia) VALUES (?, ?, ?, ?)", 
                       (code, data['nombre'], data['presupuesto'], data['dep']))
        
    # Indicators
    print(f"Inserting {len(indicadores_list)} Indicators...")
    cursor.executemany("""
        INSERT OR REPLACE INTO Indicadores 
        (id_indicador, nombre_indicador, subdimension, unidad_medida, tipo_indicador, linea_base, anio_linea_base, meta_total, anio_meta, codigo_bpin_proyecto, id_dependencia_responsable)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, indicadores_list)
    
    # Reports
    print(f"Inserting {len(reportes_list)} Reports...")
    cursor.executemany("""
        INSERT OR REPLACE INTO Reportes_Trimestrales
        (id_indicador, anio, trimestre, valor_programado, valor_ejecutado, avance_fisico, avance_financiero, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, reportes_list)
    
    conn.commit()
    conn.close()
    print("\nETL Process Completed Successfully.")

if __name__ == "__main__":
    run_etl()
