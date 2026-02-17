
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import sqlite3
import uvicorn
from typing import List, Optional, Union
from datetime import datetime, timedelta
import auth
from jose import JWTError, jwt
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from fpdf import FPDF

# --- Configuration ---
app = FastAPI()

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "mise_digital.db"
SECRET_KEY = "super-secret-key-mise-digital-medellin"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

MASTER_FILE = "Matriz_Maestra_MISE_2025_Limpia.xlsx"

# --- Database ---
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Security Models ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    rol: str
    disabled: Union[bool, None] = None
    id_dependencia: Union[int, None] = None

class UserInDB(User):
    hashed_password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    user = db.execute("SELECT * FROM Usuarios WHERE email = ?", (username,)).fetchone()
    if user:
        return UserInDB(
            username=user['email'],
            email=user['email'],
            full_name=user['nombre'],
            rol=user['rol'],
            hashed_password=user['password_hash'],
            id_dependencia=user['id_dependencia']
        )
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    conn = get_db_connection()
    user = get_user(conn, username=token_data.username)
    conn.close()
    
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

# --- Endpoints ---

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    user = get_user(conn, form_data.username)
    conn.close()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.rol}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# --- DASHBOARD LOGIC ---

@app.get("/dashboard/kpis")
def get_dashboard_kpis(
    poblacion: Optional[str] = None, 
    dependencia: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    # Decisors only
    if current_user.rol not in ['Decisor', 'Admin']:
         raise HTTPException(status_code=403, detail="Acceso denegado.")

    if not os.path.exists(MASTER_FILE):
        return {"global_compliance": 0, "error": "Matriz Limpia no encontrada."}
    
    try:
        df = pd.read_excel(MASTER_FILE)
    except Exception as e:
        return {"global_compliance": 0, "error": str(e)}

    # --- Column Mapping ---
    col_meta = "Meta_Limpia"
    col_ejec = "Ejecutado_Acumulado"
    col_pres_ejec = "Presupuesto_Ejecutado_Unificado"
    
    # Dynamic columns
    # Prioritize 'nombre' for dependency to avoid codes (e.g. 954)
    col_dep = next((c for c in df.columns if "nombre dependencia" in c.lower()), None)
    if not col_dep:
        col_dep = next((c for c in df.columns if "dependencia" in c.lower()), "nombre dependencia responsable (reporte)")
    
    col_ind = next((c for c in df.columns if "nombre indicador" in c.lower() or "indicador de producto" in c.lower()), "indicador de producto")
    col_pob = "población objetivo"
    col_terr = "comunas-corregimientos"
    col_pilar = "pilar o eje plan de desarrollo distrital"
    col_pres_prog = "presupuesto programado"

    # --- Filters ---
    if poblacion and poblacion != "Todos" and col_pob in df.columns:
        df = df[df[col_pob].astype(str).str.contains(poblacion, case=False, na=False)]
        
    if dependencia and dependencia != "Todas" and col_dep in df.columns:
        df = df[df[col_dep].astype(str).str.contains(dependencia, case=False, na=False)]

    # --- Calculations ---
    # Ensure numeric
    df['meta_val'] = pd.to_numeric(df[col_meta], errors='coerce').fillna(0)
    df['ejec_val'] = pd.to_numeric(df[col_ejec], errors='coerce').fillna(0)
    df['pres_ejec_val'] = pd.to_numeric(df[col_pres_ejec], errors='coerce').fillna(0)
    
    if col_pres_prog in df.columns:
        df['pres_prog_val'] = pd.to_numeric(df[col_pres_prog], errors='coerce').fillna(0)
    else:
        df['pres_prog_val'] = 0

    # 1. Global Compliance (Sum / Sum)
    total_meta = df['meta_val'].sum()
    total_ejec = df['ejec_val'].sum()
    global_compliance = (total_ejec / total_meta * 100) if total_meta > 0 else 0
    
    # 2. Budget Compliance
    total_pres_prog = df['pres_prog_val'].sum()
    total_pres_ejec = df['pres_ejec_val'].sum()
    budget_compliance = (total_pres_ejec / total_pres_prog * 100) if total_pres_prog > 0 else 0

    # 3. Pillars (Estrategia)
    pillars_data = []
    if col_pilar in df.columns:
        pil_stats = df.groupby(col_pilar).apply(
            lambda x: (x['ejec_val'].sum() / x['meta_val'].sum() * 100) if x['meta_val'].sum() > 0 else 0
        ).reset_index(name='cumplimiento').sort_values('cumplimiento', ascending=False)
        pillars_data = pil_stats.head(10).to_dict(orient='records')

    # 4. Dependencies Ranking
    dep_stats = df.groupby(col_dep).apply(
        lambda x: (x['ejec_val'].sum() / x['meta_val'].sum() * 100) if x['meta_val'].sum() > 0 else 0
    ).reset_index(name='cumplimiento').sort_values('cumplimiento', ascending=False)
    
    dependencies = dep_stats.head(20).to_dict(orient='records')
    # Rename for frontend
    if col_dep != 'nombre_dependencia':
         for d in dependencies: d['nombre_dependencia'] = d.pop(col_dep)

    # 5. Efficiency Alerts (Individual)
    # Calc individual %
    df['cumplimiento_fisico'] = df.apply(lambda r: (r['ejec_val'] / r['meta_val'] * 100) if r['meta_val'] > 0 else 0, axis=1)
    df['cumplimiento_financiero'] = df.apply(lambda r: (r['pres_ejec_val'] / r['pres_prog_val'] * 100) if r['pres_prog_val'] > 0 else 0, axis=1)

    # Logic: Physical < 40 AND Financial > 70
    efficiency_alerts = df[
        (df['cumplimiento_fisico'] < 40) & (df['cumplimiento_financiero'] > 70)
    ][[col_ind, col_dep, 'cumplimiento_fisico', 'cumplimiento_financiero', 'pres_ejec_val']].head(20)
    
    efficiency_alerts = efficiency_alerts.rename(columns={
        col_ind: 'Indicador', 
        col_dep: 'Dependencia',
        'cumplimiento_fisico': 'Avance_Fisico',
        'cumplimiento_financiero': 'Avance_Financiero'
    }).to_dict(orient='records')

    # 6. Scatter Data (All indicators for Efficiency Plot)
    scatter_data = df[[col_ind, col_dep, 'cumplimiento_fisico', 'cumplimiento_financiero']].fillna(0).to_dict(orient='records')

    # 7. Population (Social)
    population_data = []
    if col_pob in df.columns:
        pop_counts = df[col_pob].value_counts().head(10).reset_index()
        pop_counts.columns = ['poblacion', 'count']
        population_data = pop_counts.to_dict(orient='records')

    # 8. Territorial
    territorial_data = []
    if col_terr in df.columns:
         terr_stats = df.groupby(col_terr).apply(
            lambda x: (x['ejec_val'].sum() / x['meta_val'].sum() * 100) if x['meta_val'].sum() > 0 else 0
         ).reset_index(name='cumplimiento').sort_values('cumplimiento', ascending=False)
         territorial_data = terr_stats.head(20).rename(columns={col_terr: 'territorial'}).to_dict(orient='records')

    # Dependencies List for filter
    all_deps = sorted(df[col_dep].astype(str).unique().tolist()) if col_dep in df.columns else []

    return {
        "global_compliance": round(global_compliance, 1),
        "budget_compliance": round(budget_compliance, 1),
        "pillars": pillars_data,
        "dependencies": dependencies,
        "efficiency_alerts": efficiency_alerts,
        "scatter_data": scatter_data,
        "population_data": population_data,
        "territorial_data": territorial_data,
        "param_dependencies": all_deps, # For dropdown
        "total_indicators": len(df)
    }

@app.get("/reports/export")
def export_consolidated_report(current_user: User = Depends(get_current_active_user)):
    if not os.path.exists(MASTER_FILE):
         raise HTTPException(status_code=404, detail="Matriz Limpia no encontrada")
    return FileResponse(MASTER_FILE, filename="Matriz_Maestra_MISE_2025_Limpia.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.get("/reports/hallazgos")
def export_hallazgos_pdf(poblacion: Optional[str] = None, current_user: User = Depends(get_current_active_user)):
    if not os.path.exists(MASTER_FILE):
         raise HTTPException(status_code=404, detail="Matriz Limpia no encontrada")
    
    try:
        df = pd.read_excel(MASTER_FILE)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # --- Column Mapping (Same as Dashboard) ---
    col_meta = "Meta_Limpia"
    col_ejec = "Ejecutado_Acumulado"
    col_pres_ejec = "Presupuesto_Ejecutado_Unificado"
    col_dep = next((c for c in df.columns if "nombre dependencia" in c.lower()), None)
    if not col_dep: col_dep = next((c for c in df.columns if "dependencia" in c.lower()), "nombre dependencia responsable (reporte)")
    col_ind = next((c for c in df.columns if "nombre indicador" in c.lower() or "indicador de producto" in c.lower()), "indicador de producto")
    col_pob = "población objetivo"
    col_pilar = "pilar o eje plan de desarrollo distrital"
    col_pres_prog = "presupuesto programado"

    # --- Filter ---
    if poblacion and poblacion != "Todos" and col_pob in df.columns:
        df = df[df[col_pob].astype(str).str.contains(poblacion, case=False, na=False)]
    
    # --- Analysis Engine ---
    
    # 1. Global Metrics
    df['meta_val'] = pd.to_numeric(df[col_meta], errors='coerce').fillna(0)
    df['ejec_val'] = pd.to_numeric(df[col_ejec], errors='coerce').fillna(0)
    df['pres_ejec_val'] = pd.to_numeric(df[col_pres_ejec], errors='coerce').fillna(0)
    if col_pres_prog in df.columns:
        df['pres_prog_val'] = pd.to_numeric(df[col_pres_prog], errors='coerce').fillna(0)
    else:
        df['pres_prog_val'] = 0

    total_meta = df['meta_val'].sum()
    total_ejec = df['ejec_val'].sum()
    global_phy = (total_ejec / total_meta * 100) if total_meta > 0 else 0
    
    total_pres_prog = df['pres_prog_val'].sum()
    total_pres_ejec = df['pres_ejec_val'].sum()
    global_fin = (total_pres_ejec / total_pres_prog * 100) if total_pres_prog > 0 else 0

    # 2. Pillars Analysis
    pillar_text = "No disponible."
    if col_pilar in df.columns:
        pil_stats = df.groupby(col_pilar).apply(
            lambda x: (x['ejec_val'].sum() / x['meta_val'].sum() * 100) if x['meta_val'].sum() > 0 else 0
        ).reset_index(name='cumplimiento').sort_values('cumplimiento', ascending=False)
        
        best_pil = pil_stats.iloc[0]
        worst_pil = pil_stats.iloc[-1]
        pillar_text = f"El pilar con mejor desempeño es '{best_pil[col_pilar]}' ({best_pil['cumplimiento']:.1f}%), mientras que '{worst_pil[col_pilar]}' presenta el mayor rezago ({worst_pil['cumplimiento']:.1f}%)."

    # 3. Efficiency Gaps (Dependencies)
    gap_text = "No disponible."
    if col_dep in df.columns:
        # Agg by dep
        dep_stats = df.groupby(col_dep).apply(
            lambda x: pd.Series({
                'fisico': (x['ejec_val'].sum() / x['meta_val'].sum() * 100) if x['meta_val'].sum() > 0 else 0,
                'financiero': (x['pres_ejec_val'].sum() / x['pres_prog_val'].sum() * 100) if x['pres_prog_val'].sum() > 0 else 0
            })
        ).reset_index()
        dep_stats['brecha'] = dep_stats['financiero'] - dep_stats['fisico']
        
        # Worst gaps (High spend, low result)
        worst_gaps = dep_stats.sort_values('brecha', ascending=False).head(3)
        gaps_list = [f"{row[col_dep]} (Brecha: +{row['brecha']:.1f}%)" for _, row in worst_gaps.iterrows()]
        gap_text = "Las dependencias con mayor ineficiencia financiera (Gasto > Avance) son: " + ", ".join(gaps_list) + "."

    # 4. Critical Indicators
    df['cumplimiento_ind'] = df.apply(lambda r: (r['ejec_val'] / r['meta_val'] * 100) if r['meta_val'] > 0 else 0, axis=1)
    critical_count = len(df[df['cumplimiento_ind'] < 25])

    # --- PDF Generation ---
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Informe Ejecutivo: Análisis Inteligente MISE', 0, 1, 'C')
            self.ln(5)
            
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Title Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Fecha de Corte: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
    if poblacion: pdf.cell(0, 10, f"Filtro Poblacional: {poblacion}", ln=1)
    pdf.ln(5)

    # 1. Executive Summary
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "1. Resumen Ejecutivo", ln=1)
    pdf.set_font("Arial", size=11)
    summary = (
        f"A la fecha, el Distrito presenta un cumplimiento físico consolidado del {global_phy:.1f}% "
        f"frente a las metas propuestas para 2025. La ejecución presupuestal se sitúa en {global_fin:.1f}%."
    )
    if global_fin > (global_phy + 10):
        summary += " Se detecta una alerta de eficiencia financiera global, donde el gasto supera significativamente el avance físico."
    elif global_phy >= 90:
        summary += " El desempeño general es altamente satisfactorio."
    
    pdf.multi_cell(0, 7, summary)
    pdf.ln(5)

    # 2. Performance by Pillars
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "2. Análisis Estratégico (Pilares)", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, pillar_text)
    pdf.ln(5)

    # 3. Efficiency & Risks
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "3. Hallazgos de Eficiencia y Riesgos", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, gap_text)
    pdf.ln(2)
    pdf.multi_cell(0, 7, f"Se han identificado {critical_count} indicadores en estado CRÍTICO (Avance < 25%). Se recomienda focalizar esfuerzos de seguimiento en estas áreas.")
    pdf.ln(5)

    # 4. Recommendations (AI Simulated)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "4. Recomendaciones Inteligentes", ln=1)
    pdf.set_font("Arial", size=11)
    recs = [
        "- Revisar la ejecución de recursos en las dependencias con brechas positivas (>10%).",
        "- Establecer planes de choque para los indicadores críticos del pilar más rezagado.",
        "- Validar la calidad del reporte en dependencias con 0% de avance registrado."
    ]
    for r in recs:
        pdf.multi_cell(0, 7, r)
    
    file_path = "hallazgos.pdf"
    pdf.output(file_path)
    return FileResponse(file_path, filename="Informe_Ejecutivo_Inteligente.pdf", media_type='application/pdf')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
