
import pandas as pd
import sqlite3
import os
import re

# Configuration
# Map filename -> Dependency ID
FILE_MAP = {
    "SegIndic_PPPC_300625.xlsx": None, # Dynamic or multiple? The original file had multiple deps (Cultura, Juventud, Salud)
    "020226_SPC_301225.xlsx": 725, # Participación Ciudadana
    "030226_GerenciaÉtnica.xlsx": 954, # Gerencia Étnica
    "090226_SISF_301225.xlsx": 722, # Inclusión Social
    "230126_Mujeres__MISE.xlsx": 723, # Mujeres
    "230126_SGHSC_300925.xlsx": 706, # Gestión Humana
    "260126_DAP.xlsx": 761, # DAP
    "270126_Sec_Educación.xlsx": 711 # Educación
}

DB_FILE = "mise_digital.db"

def clean_numeric(val):
    if pd.isna(val) or val == 'No aplica' or str(val).strip() == '' or str(val).lower() == 'nan':
        return None
    if isinstance(val, (int, float)):
        return val
    s = str(val).strip().replace(',', '.')
    s = re.sub(r'[^\d\.-]', '', s)
    try:
        return float(s)
    except:
        return None

def find_header_row_and_cols(df):
    found_cols = {
        'id_ind': None,
        'nombre_ind': None, 'subdim': None, 'dep_cod': None,
        'proj_cod': None, 'meta': None, 'linea_base': None,
        'trim_1': None, 'trim_2': None, 'trim_3': None, 'trim_4': None
    }
    header_row_idx = -1

    for r in range(min(15, len(df))):
        row_vals = [str(x).lower() for x in df.iloc[r].values]
        for c, val in enumerate(row_vals):
            if 'código indicador' in val:
                found_cols['id_ind'] = c
                header_row_idx = r 
            elif 'subdimensión' in val:
                found_cols['subdim'] = c
            # We skip dep_cod detection if we force it from filename, but keep it for mixed files
            elif ('código dependencia' in val) or ('responsables' in val and 'dependencia' in val):
                found_cols['dep_cod'] = c
            elif 'código' in val and 'proyecto' in val:
                found_cols['proj_cod'] = c
            elif 'meta' in val and 'indicador' in val:
                found_cols['meta'] = c
            elif 'línea base' in val:
                found_cols['linea_base'] = c
            
            # Quarters
            if 'trimestre i ' in val and '2025' in val: found_cols['trim_1'] = c
            elif 'trimestre ii' in val and '2025' in val: found_cols['trim_2'] = c
            elif 'trimestre iii' in val and '2025' in val: found_cols['trim_3'] = c
            elif 'trimestre iv' in val and '2025' in val: found_cols['trim_4'] = c
            
    return found_cols, header_row_idx + 1

def run_etl():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    total_inds = 0
    total_reps = 0
    
    for file_path, forced_dep_id in FILE_MAP.items():
        if not os.path.exists(file_path):
            print(f"Skipping {file_path}: Not found")
            continue
            
        print(f"Processing {file_path} (Forced Dep: {forced_dep_id})...")
        try:
            xl = pd.ExcelFile(file_path)
        except Exception as e:
            print(f"  Error opening: {e}")
            continue

        target_sheet = None
        cols = None
        start_row = 0
        
        # Find valid sheet
        for s in xl.sheet_names:
            df_raw = xl.parse(s, header=None)
            c, sr = find_header_row_and_cols(df_raw)
            if c['id_ind'] is not None:
                target_sheet = s
                cols = c
                start_row = sr
                break
        
        if not target_sheet:
            print(f"  No valid sheet found.")
            continue
            
        print(f"  Sheet: {target_sheet}")
        df = xl.parse(target_sheet, header=None)
        
        proyectos_set = {}
        indicadores_list = []
        reportes_list = []
        
        for i in range(start_row, len(df)):
            row = df.iloc[i]
            try:
                # ID
                id_eff = row[cols['id_ind']]
                if pd.isna(id_eff) or not str(id_eff).replace('.','').isdigit(): continue
                id_indicador = int(float(str(id_eff)))
                
                # Name
                name_idx = cols['id_ind'] + 1
                nombre_indicador = str(row[name_idx]) if name_idx < len(row) else "Desconocido"
                
                # Dep Logic
                dep_cod = forced_dep_id
                if dep_cod is None:
                    # Try fallback to column
                    if cols['dep_cod'] is not None:
                        raw_dep = row[cols['dep_cod']]
                        val_dep = clean_numeric(raw_dep)
                        if val_dep: dep_cod = int(val_dep)
                
                # If still None, we have a problem for this row.
                # However, for the original file, we rely on column.
                
                # Project
                proj_cod = None
                if cols['proj_cod'] is not None:
                    raw_proj = row[cols['proj_cod']]
                    if pd.notna(raw_proj) and str(raw_proj).strip() not in ['No aplica', '', 'nan']:
                        proj_cod = str(raw_proj).strip()
                        proyectos_set[proj_cod] = {'nombre': f"Proyecto {proj_cod}", 'dep': dep_cod}
                
                # Meta / Linea Base
                meta = clean_numeric(row[cols['meta']]) if cols['meta'] else None
                lb = clean_numeric(row[cols['linea_base']]) if cols['linea_base'] else None
                subdim = str(row[cols['subdim']]) if cols['subdim'] else None

                indicadores_list.append((
                    id_indicador, nombre_indicador, subdim, None, 'Gestión', 
                    lb, 2024, meta, 2025, proj_cod, dep_cod
                ))
                
                # Quarters
                q_map = {1: cols['trim_1'], 2: cols['trim_2'], 3: cols['trim_3'], 4: cols['trim_4']}
                for q, col_idx in q_map.items():
                    if col_idx is not None:
                        val = clean_numeric(row[col_idx])
                        if val is not None:
                           reportes_list.append((id_indicador, 2025, q, None, val, None, None, None))

            except Exception as e:
                continue

        # Inset dependencies names just in case? Or rely on clean_deps.py?
        # We assume dependencies table is populated or at least has IDs.
        # But if ID is new (e.g. 725), we need to insert it.
        # Let's insert dummy names if missing, then clean.
        
        # Projects
        cursor.executemany("INSERT OR IGNORE INTO Proyectos (codigo_bpin, nombre_proyecto, presupuesto_programado_total, id_dependencia) VALUES (?, ?, ?, ?)", 
                           [(k, v['nombre'], 0, v['dep']) for k, v in proyectos_set.items()])
        
        # Indicators (Replace to update metadata)
        cursor.executemany("""
            INSERT OR REPLACE INTO Indicadores 
            (id_indicador, nombre_indicador, subdimension, unidad_medida, tipo_indicador, linea_base, anio_linea_base, meta_total, anio_meta, codigo_bpin_proyecto, id_dependencia_responsable)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, indicadores_list)
        
        # Reports (Replace to update values)
        cursor.executemany("""
            INSERT OR REPLACE INTO Reportes_Trimestrales
            (id_indicador, anio, trimestre, valor_programado, valor_ejecutado, avance_fisico, avance_financiero, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, reportes_list)
        
        print(f"  Inserted: {len(indicadores_list)} Inds, {len(reportes_list)} Reports")
        total_inds += len(indicadores_list)
        total_reps += len(reportes_list)
        conn.commit()

    print(f"\nTotal Processed: {total_inds} Indicators, {total_reps} Reports")
    conn.close()

if __name__ == "__main__":
    run_etl()
