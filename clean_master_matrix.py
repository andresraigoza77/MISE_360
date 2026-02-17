
import pandas as pd
import sqlite3
import re
import os

INPUT_FILE = "Matriz_Maestra_MISE_2025_Consolidada.xlsx"
OUTPUT_FILE = "Matriz_Maestra_MISE_2025_Limpia.xlsx"
DB_FILE = "mise_digital.db"

def clean_value(v):
    if pd.isna(v): return None
    s = str(v).strip()
    if s == "" or s.lower() == "nan" or s.lower() == "n/a": return None
    return s

def clean_meta(v):
    if pd.isna(v): return 0.0
    s = str(v).strip().replace(',', '.')
    if '%' in s:
        s = s.replace('%', '')
    try:
        val = float(re.findall(r"[-+]?\d*\.\d+|\d+", s)[0])
        return val
    except:
        return 0.0

def clean_matrix():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file {INPUT_FILE} not found.")
        return

    print("🚀 Starting Master Matrix Cleaning...")
    df = pd.read_excel(INPUT_FILE)
    
    # Normalize headers
    df.columns = [str(c).lower().strip() for c in df.columns]
    
    # 1. Producto Fusion
    print("  ... Merging 'Producto' cols")
    prod_cols = [c for c in df.columns if 'producto' in c and 'indicador' not in c]
    def get_prod(row):
        for c in prod_cols:
            val = clean_value(row[c])
            if val: return val
        return "N/A"
    df['Producto_Final'] = df.apply(get_prod, axis=1)
    
    # 2. Q Mapping
    rename_map = {
        'resultado': 'Resultado_Q1',
        'resultado.1': 'Resultado_Q2',
        'resultado.2': 'Resultado_Q3',
        'resultado.3': 'Resultado_Q4',
        'observaciones': 'Observaciones_Q1',
        'observaciones .1': 'Observaciones_Q2',
        'observaciones .2': 'Observaciones_Q3',
        'observaciones .3': 'Observaciones_Q4',
        'fuente de verificacion': 'Fuente_Q1',
        'fuente de verificacion.1': 'Fuente_Q2',
        'fuente de verificacion.2': 'Fuente_Q3',
        'fuente de verificacion.3': 'Fuente_Q4'
    }
    
    actual_cols = df.columns
    final_rename = {}
    for k, v in rename_map.items():
        if k in actual_cols: final_rename[k] = v
            
    df.rename(columns=final_rename, inplace=True)
    
    # 3. Presupuesto
    print("  ... Merging 'Presupuesto' cols")
    budg_cols = [c for c in df.columns if 'presupuesto ejecutado' in c]
    def get_budget(row):
        for c in budg_cols:
            val = row[c]
            if pd.notna(val) and val != 0 and val != "N/A":
                return val
        return 0
    df['Presupuesto_Ejecutado_Unificado'] = df.apply(get_budget, axis=1)

    # 4. Meta Cleaning
    meta_col = next((c for c in df.columns if 'meta del indicador' in c or 'meta_2025' in c), None)
    if not meta_col:
        meta_col = next((c for c in df.columns if 'meta' in c and 'proyecto' not in c), None)
    
    if meta_col:
        print(f"  ... Cleaning Meta: {meta_col}")
        df['Meta_Limpia'] = df[meta_col].apply(clean_meta)
        df.rename(columns={meta_col: 'Meta_Original'}, inplace=True)
    else:
        df['Meta_Limpia'] = 0.0

    # 5. NEW: Pillar Cleaning
    col_pilar = next((c for c in df.columns if "pilar" in c.lower()), "pilar o eje plan de desarrollo distrital")
    if col_pilar in df.columns:
        print(f"  ... Cleaning Pillar: {col_pilar}")
        def clean_pilar_val(p):
            p = str(p).strip()
            if "pilar 1" in p.lower(): return "Pilar 1: Bienestar Social"
            if "pilar 2" in p.lower(): return "Pilar 2: Agenda Social"
            if "pilar 3" in p.lower(): return "Pilar 3: Transformación Educativa"
            if "pilar 4" in p.lower(): return "Pilar 4: Ecociudad"
            if "pilar 5" in p.lower(): return "Pilar 5: Gobernanza"
            if "transversal" in p.lower(): return "Transversal"
            return "Otros"
        df['pilar o eje plan de desarrollo distrital'] = df[col_pilar].apply(clean_pilar_val)

    # 6. NEW: Programmed Budget Cleaning
    col_pres_prog = next((c for c in df.columns if "presupuesto programado" in c.lower()), "presupuesto programado")
    if col_pres_prog in df.columns:
        print(f"  ... Cleaning Programmed Budget: {col_pres_prog}")
        df[col_pres_prog] = pd.to_numeric(df[col_pres_prog], errors='coerce').fillna(0)
        # Rename strictly for API use
        df.rename(columns={col_pres_prog: 'presupuesto programado'}, inplace=True)

    # 7. Ejecutado Acumulado
    q_cols = ['Resultado_Q1', 'Resultado_Q2', 'Resultado_Q3', 'Resultado_Q4']
    found_q = [c for c in q_cols if c in df.columns]
    
    def sum_q(row):
        total = 0.0
        for c in found_q:
            try:
                v = row[c]
                if isinstance(v, str): v = clean_meta(v)
                if pd.notna(v): total += float(v)
            except: pass
        return total

    df['Ejecutado_Acumulado'] = df.apply(sum_q, axis=1)

    # 8. Save
    print(f"  ... Saving to {OUTPUT_FILE}")
    core_cols = [
        'código indicador', 'indicador de producto', 'Meta_Limpia', 'Ejecutado_Acumulado',
        'Presupuesto_Ejecutado_Unificado', 'Producto_Final',
        'código dependencia responsable (reporte)', 'nombre dependencia responsable (reporte)',
        'población objetivo', 'comunas-corregimientos',
        'pilar o eje plan de desarrollo distrital', 'presupuesto programado'
    ]
    core_cols += found_q
    
    existing_core = [c for c in core_cols if c in df.columns]
    others = [c for c in df.columns if c not in existing_core]
    
    df_final = df[existing_core + others]
    df_final.to_excel(OUTPUT_FILE, index=False)
    df_final.to_csv(OUTPUT_FILE.replace('.xlsx', '.csv'), index=False)
    
    # 9. Update DB
    print("  ... Updating Database")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    id_col = 'código indicador'
    if id_col not in df.columns:
        id_col = next((c for c in df.columns if 'código' in c and 'indicador' in c), None)

    if id_col:
        count = 0
        for idx, row in df.iterrows():
            try:
                iid = row[id_col]
                if pd.isna(iid): continue
                iid = int(float(str(iid)))
                meta = row['Meta_Limpia']
                prod = row['Producto_Final']
                
                c.execute("UPDATE Indicadores SET meta_total = ?, nombre_indicador = COALESCE(?, nombre_indicador) WHERE id_indicador = ?", (meta, prod, iid))
                
                for i, q_col in enumerate(found_q):
                    q_num = i + 1
                    val = row[q_col]
                    try: val = float(clean_meta(val))
                    except: val = 0.0
                    
                    c.execute("SELECT 1 FROM Reportes_Trimestrales WHERE id_indicador=? AND anio=2025 AND trimestre=?", (iid, q_num))
                    if c.fetchone():
                        c.execute("UPDATE Reportes_Trimestrales SET valor_ejecutado=? WHERE id_indicador=? AND anio=2025 AND trimestre=?", (val, iid, q_num))
                    else:
                        c.execute("INSERT INTO Reportes_Trimestrales (id_indicador, anio, trimestre, valor_ejecutado) VALUES (?, 2025, ?, ?)", (iid, q_num, val))
                count += 1
            except: pass
        conn.commit()
        print(f"✅ DB Updated ({count} rows)")
    
    conn.close()

if __name__ == "__main__":
    clean_matrix()
