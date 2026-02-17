
import pandas as pd
import sqlite3
import os
import re

# Configuration
EXCEL_FILE = "SegIndic_PPPC_300625.xlsx"
DB_FILE = "mise_digital.db"

def clean_numeric(val):
    if pd.isna(val) or val == 'No aplica' or str(val).strip() == '':
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
    # Search first 10 rows for key headers
    header_map = {}
    header_row_idx = -1
    
    # We look for a row that ideally has "Código Indicador" and "Trimestre" info
    # But headers might be split across rows (merged cells). 
    # We'll scan row by row and accumulate findings.
    
    found_cols = {
        'id_ind': None,
        'nombre_ind': None,
        'subdim': None,
        'dep_cod': None,
        'proj_cod': None,
        'trim_1': None,
        'trim_2': None,
        'trim_3': None,
        'trim_4': None
    }
    
    # Heuristic: Scan rows 0-10
    # We associate column indices with their "best" header found so far.
    
    for r in range(min(10, len(df))):
        row_vals = df.iloc[r].astype(str).values
        for c, val in enumerate(row_vals):
            val = val.strip().lower()
            if 'código indicador' in val:
                found_cols['id_ind'] = c
                header_row_idx = r # assumed data starts after this
            elif 'subdimensión' in val:
                found_cols['subdim'] = c
            elif 'código dependencia responsable (reporte)' in val:
                found_cols['dep_cod'] = c
            elif 'código del proyecto' in val:
                found_cols['proj_cod'] = c
            elif 'meta del indicador' in val:
                found_cols['meta'] = c
            elif 'línea base' in val:
                found_cols['linea_base'] = c
            
            # Quarters - logic: search for "Trimestre X" and check if it's "Resultado" 
            # OR check the row below?
            # In the inspection, "Trimestre I - 2025" is in one row, and "Resultado" in the same column or below?
            # Inspection: 
            # Row 4: ...
            # Row ?: Unnamed: 24: 'Trimestre I - 2025', 'Resultado'
            # This implies the column itself handles it.
            if 'trimestre i - 2025' in val or 'trimestre i -2025' in val: # Note typo in 'Juventud' sheet
                found_cols['trim_1'] = c
            elif 'trimestre ii - 2025' in val or 'trimestre ii- 2025' in val:
                found_cols['trim_2'] = c
            elif 'trimestre iii - 2025' in val or 'trimestre iii- 2025' in val:
                found_cols['trim_3'] = c
            elif 'trimestre iv - 2025' in val:
                found_cols['trim_4'] = c

    # Fallbacks / Heuristics if exact names vary
    # If we found id_ind, we can assume relative positions if needed, but safer to assume 
    # we might miss some columns if headers are too weird.
    
    # Assuming data starts 1 or 2 rows after the header row of 'Código Indicador'
    start_row = header_row_idx + 1 if header_row_idx != -1 else 7
    
    return found_cols, start_row

def run_etl():
    print(f"Loading Excel file: {EXCEL_FILE}")
    xl = pd.ExcelFile(EXCEL_FILE)
    
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
        print(f"  Mappings: {cols}, Start Data Row: {start_row}")
        
        if cols['id_ind'] is None:
            print("  Skipping sheet: Could not find 'Código Indicador' column.")
            continue
            
        for i in range(start_row, len(df_raw)):
            row = df_raw.iloc[i]
            
            # Robust extraction
            try:
                id_eff = row[cols['id_ind']]
                if pd.isna(id_eff) or not str(id_eff).isdigit():
                    continue
                
                id_indicador = int(id_eff)
                
                # Name usually is next to ID or we search for it? 
                # let's assume index + 1 is name if we didn't find specific header
                name_idx = cols['id_ind'] + 1
                nombre_indicador = str(row[name_idx]) if name_idx < len(row) else "Desconocido"
                
                subdimension = str(row[cols['subdim']]) if cols['subdim'] else None
                linea_base = clean_numeric(row[cols['linea_base']]) if cols.get('linea_base') else None
                meta_total = clean_numeric(row[cols['meta']]) if cols.get('meta') else None
                
                # Dependency
                dep_cod = None
                if cols['dep_cod']:
                    raw_dep = row[cols['dep_cod']]
                    if pd.notna(raw_dep) and str(raw_dep).replace('.','').isdigit():
                         dep_cod = int(float(raw_dep))
                         if dep_cod not in dependencias_set:
                             dependencias_set[dep_cod] = f"Dependencia {dep_cod}"

                # Project
                proj_cod = None
                if cols['proj_cod']:
                     raw_proj = row[cols['proj_cod']]
                     if pd.notna(raw_proj) and str(raw_proj).strip() != 'No aplica':
                         proj_cod = str(raw_proj).strip()
                         if proj_cod not in proyectos_set:
                             proyectos_set[proj_cod] = {
                                 'nombre': f"Proyecto {proj_cod}",
                                 'presupuesto': 0, # Placeholder
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
                            
            except Exception as e:
                # print(f"  Error processing row {i}: {e}")
                continue

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
        c = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"Table {table}: {c} rows")

    conn.close()

if __name__ == "__main__":
    run_etl()
