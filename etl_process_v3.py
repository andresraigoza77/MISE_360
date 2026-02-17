
import pandas as pd
import sqlite3
import os
import re
import math

# Configuration
EXCEL_FILE = "SegIndic_PPPC_300625.xlsx"
DB_FILE = "mise_digital.db"

def clean_numeric(val):
    if pd.isna(val) or val == 'No aplica' or str(val).strip() == '' or str(val).lower() == 'nan':
        return None
    if isinstance(val, (int, float)):
        return val
    s = str(val).strip().replace(',', '.')
    # Handle cases like "30 %" or "$ 5.000"
    s = re.sub(r'[^\d\.-]', '', s)
    try:
        return float(s)
    except:
        return None

def find_header_row_and_cols(df):
    
    found_cols = {
        'id_ind': None,
        'nombre_ind': None, 
        'subdim': None,
        'dep_cod': None,
        'proj_cod': None,
        'meta': None,
        'linea_base': None,
        'trim_1': None,
        'trim_2': None,
        'trim_3': None,
        'trim_4': None
    }
    
    header_row_idx = -1

    # Heuristic: Scan rows 0-10
    for r in range(min(10, len(df))):
        # Force conversion to string list safely
        row_vals = [str(x) for x in df.iloc[r].values]
        
        for c, val in enumerate(row_vals):
            val = val.strip().lower()
            if 'código indicador' in val:
                found_cols['id_ind'] = c
                header_row_idx = r 
            elif 'subdimensión' in val:
                found_cols['subdim'] = c
            elif 'código dependencia responsable' in val or 'responsables' in val:
                # Prefer "código" if available, but "responsables" might be the header for the code column too in some sheets
                # We check if we already found a "better" one? No, usually "Responsables" is merged above "Código..."
                # Use strict match for code if possible
                if 'código' in val:
                    found_cols['dep_cod'] = c
                elif found_cols['dep_cod'] is None:
                    found_cols['dep_cod'] = c
            elif 'código del proyecto' in val:
                found_cols['proj_cod'] = c
            elif 'meta del indicador' in val:
                found_cols['meta'] = c
            elif 'línea base' in val:
                found_cols['linea_base'] = c
            
            # Quarters
            if 'trimestre i - 2025' in val or 'trimestre i -2025' in val or 'trimestre i- 2025' in val: 
                found_cols['trim_1'] = c
            elif 'trimestre ii' in val and '2025' in val:
                found_cols['trim_2'] = c
            elif 'trimestre iii' in val and '2025' in val:
                found_cols['trim_3'] = c
            elif 'trimestre iv' in val and '2025' in val:
                found_cols['trim_4'] = c

    # Fallbacks 
    # If header row found but some cols missing, try to infer? 
    # For now, rely on what we found.
    
    start_row = header_row_idx + 1 if header_row_idx != -1 else 7
    return found_cols, start_row

def run_etl():
    print(f"Loading Excel file: {EXCEL_FILE}")
    try:
        xl = pd.ExcelFile(EXCEL_FILE)
    except Exception as e:
        print(f"Error opening Excel: {e}")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    dependencias_set = {} 
    proyectos_set = {}
    indicadores_list = []
    reportes_list = []
    
    target_sheets = [s for s in xl.sheet_names if s.startswith('Matriz_MISE_')]
    
    for sheet_name in target_sheets:
        print(f"Processing sheet: {sheet_name}")
        df_raw = xl.parse(sheet_name, header=None)
        
        cols, start_row = find_header_row_and_cols(df_raw)
        
        if cols['id_ind'] is None:
            print(f"  Skipping {sheet_name}: Could not find 'Código Indicador' column.")
            continue
            
        ROW_COUNT = 0
        for i in range(start_row, len(df_raw)):
            row = df_raw.iloc[i]
            
            try:
                id_eff = row[cols['id_ind']]
                # Check for valid ID (integer-like)
                if pd.isna(id_eff) or not str(id_eff).replace('.','').isdigit():
                    continue
                
                id_indicador = int(float(str(id_eff)))
                
                # Name
                name_idx = cols['id_ind'] + 1
                nombre_indicador = str(row[name_idx]) if name_idx < len(row) else "Desconocido"
                
                # Subdimension
                subdimension = str(row[cols['subdim']]) if cols['subdim'] is not None else None
                
                # Linea Base / Meta
                linea_base = clean_numeric(row[cols['linea_base']]) if cols.get('linea_base') else None
                meta_total = clean_numeric(row[cols['meta']]) if cols.get('meta') else None
                
                # Dependency
                dep_cod = None
                if cols['dep_cod'] is not None:
                    raw_dep = row[cols['dep_cod']]
                    val_dep = clean_numeric(raw_dep)
                    if val_dep:
                         dep_cod = int(val_dep)
                         if dep_cod not in dependencias_set:
                             dependencias_set[dep_cod] = f"Dependencia {dep_cod}"

                # Project
                proj_cod = None
                if cols['proj_cod'] is not None:
                     raw_proj = row[cols['proj_cod']]
                     if pd.notna(raw_proj) and str(raw_proj).strip() not in ['No aplica', '', 'nan']:
                         proj_cod = str(raw_proj).strip()
                         if proj_cod not in proyectos_set:
                             proyectos_set[proj_cod] = {
                                 'nombre': f"Proyecto {proj_cod}",
                                 'presupuesto': 0, 
                                 'dep': dep_cod
                             }
                
                indicadores_list.append((
                    id_indicador, nombre_indicador, subdimension, None, 'Gestión', 
                    linea_base, 2024, meta_total, 2025, proj_cod, dep_cod
                ))
                
                # Quarters
                q_map = {1: cols['trim_1'], 2: cols['trim_2'], 3: cols['trim_3'], 4: cols['trim_4']}
                for q, col_idx in q_map.items():
                    if col_idx is not None:
                        val = clean_numeric(row[col_idx])
                        if val is not None:
                           reportes_list.append((id_indicador, 2025, q, None, val, None, None, None))
                
                ROW_COUNT += 1
            except Exception as e:
                # print(f"  Row {i} error: {e}")
                continue
        print(f"  Extracted {ROW_COUNT} indicators.")

    # Insert Data
    print(f"\nInserting {len(dependencias_set)} Dependencies...")
    cursor.executemany("INSERT OR IGNORE INTO Dependencias (id_dependencia, nombre_dependencia) VALUES (?, ?)", 
                       [(k, v) for k, v in dependencias_set.items()])
        
    print(f"Inserting {len(proyectos_set)} Projects...")
    cursor.executemany("INSERT OR IGNORE INTO Proyectos (codigo_bpin, nombre_proyecto, presupuesto_programado_total, id_dependencia) VALUES (?, ?, ?, ?)", 
                       [(k, v['nombre'], v['presupuesto'], v['dep']) for k, v in proyectos_set.items()])
        
    print(f"\nInserting {len(indicadores_list)} Indicators...")
    cursor.executemany("""
        INSERT OR REPLACE INTO Indicadores 
        (id_indicador, nombre_indicador, subdimension, unidad_medida, tipo_indicador, linea_base, anio_linea_base, meta_total, anio_meta, codigo_bpin_proyecto, id_dependencia_responsable)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, indicadores_list)
    
    print(f"Inserting {len(reportes_list)} Reports...")
    cursor.executemany("""
        INSERT OR REPLACE INTO Reportes_Trimestrales
        (id_indicador, anio, trimestre, valor_programado, valor_ejecutado, avance_fisico, avance_financiero, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, reportes_list)
    
    conn.commit()
    
    # Validation
    for table in ['Dependencias', 'Proyectos', 'Indicadores', 'Reportes_Trimestrales']:
        try:
            c = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"Table {table}: {c} rows")
        except:
            print(f"Error querying table {table}")

    conn.close()

if __name__ == "__main__":
    run_etl()
