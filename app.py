
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO
import sqlite3
import auth
from fpdf import FPDF
from datetime import datetime

# --- Config ---
st.set_page_config(page_title="Tablero MISE", layout="wide", page_icon="📊")

# Custom CSS for styling
st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 24px;
        color: #004834; /* Institutional Green */
    }
    h1, h2, h3 {
        color: #004834;
    }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL CONSTANTS ---
DB_FILE = "mise_digital.db"
MASTER_FILE = "Matriz_Maestra_MISE_2025_Limpia.xlsx"

# --- DATABASE & LOGIC ---
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_from_db(username: str):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM Usuarios WHERE email = ?", (username,)).fetchone()
    conn.close()
    return user

@st.cache_data(ttl=600)
def load_data():
    if not os.path.exists(MASTER_FILE):
        return None
    try:
        df = pd.read_excel(MASTER_FILE)
        return df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None

def calculate_kpis(df, filters=None):
    if df is None: return {}

    # --- Column Mapping ---
    col_meta = "Meta_Limpia"
    col_ejec = "Ejecutado_Acumulado"
    col_pres_ejec = "Presupuesto_Ejecutado_Unificado"
    
    # Dynamic columns
    col_dep = next((c for c in df.columns if "nombre dependencia" in c.lower()), None)
    if not col_dep:
        col_dep = next((c for c in df.columns if "dependencia" in c.lower()), "nombre dependencia responsable (reporte)")
    
    col_ind = next((c for c in df.columns if "nombre indicador" in c.lower() or "indicador de producto" in c.lower()), "indicador de producto")
    col_pob = "población objetivo"
    col_terr = "comunas-corregimientos"
    col_pilar = "pilar o eje plan de desarrollo distrital"
    col_pres_prog = "presupuesto programado"

    # --- Filters ---
    if filters:
        if filters.get('poblacion') and filters['poblacion'] != "Todos" and col_pob in df.columns:
            df = df[df[col_pob].astype(str).str.contains(filters['poblacion'], case=False, na=False)]
            
        if filters.get('dependencia') and filters['dependencia'] != "Todas" and col_dep in df.columns:
            df = df[df[col_dep].astype(str).str.contains(filters['dependencia'], case=False, na=False)]

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
    if col_dep != 'nombre_dependencia':
         for d in dependencies: d['nombre_dependencia'] = d.pop(col_dep)

    # 5. Efficiency Alerts
    df['cumplimiento_fisico'] = df.apply(lambda r: (r['ejec_val'] / r['meta_val'] * 100) if r['meta_val'] > 0 else 0, axis=1)
    df['cumplimiento_financiero'] = df.apply(lambda r: (r['pres_ejec_val'] / r['pres_prog_val'] * 100) if r['pres_prog_val'] > 0 else 0, axis=1)

    efficiency_alerts = df[
        (df['cumplimiento_fisico'] < 40) & (df['cumplimiento_financiero'] > 70)
    ][[col_ind, col_dep, 'cumplimiento_fisico', 'cumplimiento_financiero', 'pres_ejec_val']].head(20)
    
    efficiency_alerts = efficiency_alerts.rename(columns={
        col_ind: 'Indicador', 
        col_dep: 'Dependencia',
        'cumplimiento_fisico': 'Avance_Fisico',
        'cumplimiento_financiero': 'Avance_Financiero'
    }).to_dict(orient='records')

    # 6. Scatter Data
    scatter_data = df[[col_ind, col_dep, 'cumplimiento_fisico', 'cumplimiento_financiero']].fillna(0).to_dict(orient='records')

    # 7. Population
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
        "param_dependencies": all_deps,
        "total_indicators": len(df)
    }

def generate_pdf_report(poblacion_filter):
    df = load_data()
    if df is None: return None
    
    # Reuse logic for simplicity (re-calc specific for PDF if needed but here we use loaded df)
    # Applying filter inside PDF logic for clean separate context
    col_pob = "población objetivo"
    if poblacion_filter and poblacion_filter != "Todos" and col_pob in df.columns:
        df = df[df[col_pob].astype(str).str.contains(poblacion_filter, case=False, na=False)]
    
    # --- PDF Validations & Setup ---
    # (Simplified from api.py logic for brevity in monolithic)
    col_meta = "Meta_Limpia"
    col_ejec = "Ejecutado_Acumulado"
    df['meta_val'] = pd.to_numeric(df[col_meta], errors='coerce').fillna(0)
    df['ejec_val'] = pd.to_numeric(df[col_ejec], errors='coerce').fillna(0)
    
    total_meta = df['meta_val'].sum()
    total_ejec = df['ejec_val'].sum()
    global_phy = (total_ejec / total_meta * 100) if total_meta > 0 else 0
    
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
    
    # Content
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Fecha de Corte: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
    if poblacion_filter: pdf.cell(0, 10, f"Filtro Poblacional: {poblacion_filter}", ln=1)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Resumen Ejecutivo", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, f"El cumplimiento físico consolidado es del {global_phy:.1f}%.")
    pdf.ln(5)
    
    # Output to bytes
    return pdf.output(dest='S').encode('latin-1')

# --- AUTH & STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = None
if 'user' not in st.session_state: st.session_state.user = None

def login():
    st.markdown("## 🔐 Iniciar Sesión MISE")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        user = get_user_from_db(username)
        if user and auth.verify_password(password, user['password_hash']):
            st.session_state.logged_in = True
            st.session_state.user = user['email']
            st.session_state.role = user['rol']
            st.success(f"Bienvenido {user['nombre']}")
            st.rerun()
        else:
            st.error("Credenciales inválidas.")

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user = None
    st.rerun()

# --- VIEWS ---

def view_decisor():
    st.title(f"📊 Tablero MISE 360")
    
    col_user, col_btn = st.columns([6, 1])
    with col_user:
        st.write(f"Usuario: **{st.session_state.user}** | Rol: **{st.session_state.role}**")
    with col_btn:
        if st.button("Cerrar Sesión"): logout()
    
    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Filtros Globales")
    
    if st.sidebar.button("🔄 Refrescar Datos"):
        st.cache_data.clear()
        st.rerun()

    # Load initial data for filters
    df_init = load_data()
    if df_init is None:
        st.error("No se pudo cargar la Matriz Maestra.")
        return

    # Check for dep col name
    col_dep = next((c for c in df_init.columns if "nombre dependencia" in c.lower()), None)
    if not col_dep: col_dep = "nombre dependencia"
    
    dep_list = sorted(df_init[col_dep].astype(str).unique().tolist()) if col_dep in df_init.columns else []

    sel_dep = st.sidebar.selectbox("Secretaría / Dependencia", ["Todas"] + dep_list)
    sel_pop = st.sidebar.selectbox("Población Objetivo", ["Todos", "Mujeres", "Jóvenes", "Víctimas", "Indígena", "Afrodescendiente"])
    
    # Calculate filtered data
    filters = {'dependencia': sel_dep, 'poblacion': sel_pop}
    with st.spinner("Analizando información estratégica..."):
        data = calculate_kpis(df_init, filters)

    # --- TABS ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Estratégico", "⚡ Eficiencia", "🌍 Territorio y Social", "📂 Datos Maestros"])
    
    # --- PROCESSED DATA ---
    global_kpi = data.get('global_compliance', 0)
    budget_kpi = data.get('budget_compliance', 0)
    
    # TAB 1: ESTRATÉGICO
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Cumplimiento Físico", f"{global_kpi}%", delta="Meta 2025")
        col2.metric("Ejecución Financiera", f"{budget_kpi}%", "Presupuesto Programado")
        col3.metric("Total Indicadores", data.get('total_indicators', 0))
        col4.metric("Alertas Activas", len(data.get('efficiency_alerts', [])), delta_color="inverse")
        
        st.markdown("---")
        
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("🎯 Cumplimiento por Pilares PDD")
            pillars = data.get('pillars', [])
            if pillars:
                df_pil = pd.DataFrame(pillars)
                fig_pil = px.bar(df_pil, x='cumplimiento', y='pilar o eje plan de desarrollo distrital', orientation='h', 
                                 text_auto='.1f',
                                 labels={'cumplimiento': '% Cumplimiento', 'pilar o eje plan de desarrollo distrital': 'Pilar'},
                                 color='cumplimiento', color_continuous_scale='Greens')
                fig_pil.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
                st.plotly_chart(fig_pil, use_container_width=True)
            else:
                st.info("No hay datos de pilares disponibles.")
                
        with c2:
            st.subheader("🏆 Ranking Secretarías")
            deps = data.get('dependencies', [])
            if deps:
                df_deps = pd.DataFrame(deps)
                st.dataframe(
                    df_deps[['nombre_dependencia', 'cumplimiento']].rename(columns={'nombre_dependencia': 'Dependencia', 'cumplimiento': '%'}).style.format({'%': '{:.1f}%'}).background_gradient(cmap="Greens", subset=['%']),
                    hide_index=True,
                    use_container_width=True,
                    height=400
                )

    # TAB 2: EFICIENCIA
    with tab2:
        st.subheader("💰 Brecha de Eficiencia: Gasto vs Resultados")
        st.markdown("Comparativo del **Avance Físico** (lo logrado) frente a la **Ejecución Financiera** (lo gastado) por dependencia.")
        
        scatter = data.get('scatter_data', [])
        if scatter:
            df_sc = pd.DataFrame(scatter)
            cols = df_sc.columns
            c_ind = next((c for c in cols if 'indicador' in c.lower()), None)
            c_dep = next((c for c in cols if 'dependencia' in c.lower()), None)
            rename_map = {}
            if c_ind: rename_map[c_ind] = 'Indicador'
            if c_dep: rename_map[c_dep] = 'Dependencia'
            if rename_map: df_sc.rename(columns=rename_map, inplace=True)
            
            if 'Dependencia' in df_sc.columns:
                df_agg = df_sc.groupby('Dependencia')[['cumplimiento_fisico', 'cumplimiento_financiero']].mean().reset_index()
                df_agg['Brecha'] = df_agg['cumplimiento_financiero'] - df_agg['cumplimiento_fisico']
                df_agg = df_agg.sort_values('Brecha', ascending=False).head(15)
                
                df_melt = df_agg.melt(id_vars='Dependencia', value_vars=['cumplimiento_fisico', 'cumplimiento_financiero'], 
                                      var_name='Tipo', value_name='Porcentaje')
                
                df_melt['Tipo'] = df_melt['Tipo'].map({
                    'cumplimiento_fisico': 'Avance Físico 🟢', 
                    'cumplimiento_financiero': 'Ejecución Financiera 🔴'
                })
                
                fig_bar = px.bar(df_melt, x='Dependencia', y='Porcentaje', color='Tipo', barmode='group',
                                 color_discrete_map={'Avance Físico 🟢': '#2ca25f', 'Ejecución Financiera 🔴': '#de2d26'},
                                 title="Top Dependencias con Mayor Brecha (Gasto > Avance)",
                                 text_auto='.0f')
                
                fig_bar.update_layout(xaxis={'title': None, 'tickangle': 45}, yaxis={'title': '%'}, legend_title=None)
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.warning("No se pudo agrupar por dependencia.")
        
        st.subheader("🚨 Alertas de Eficiencia (Gasto Alto / Avance Bajo)")
        alerts = data.get('efficiency_alerts', [])
        if alerts:
            df_alerts = pd.DataFrame(alerts)
            st.dataframe(
                df_alerts.style.format({'Avance_Fisico': '{:.1f}%', 'Avance_Financiero': '{:.1f}%', 'pres_ejec_val': '${:,.0f}'}), 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ No se detectaron alertas de ineficiencia crítica.")

    # TAB 3: TERRITORIO
    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📍 Ejecución por Comunas")
            terr_data = data.get('territorial_data', [])
            if terr_data:
                df_terr = pd.DataFrame(terr_data)
                fig_terr = px.bar(df_terr, x='territorial', y='cumplimiento', color='cumplimiento', color_continuous_scale='Blues',
                                  labels={'territorial': 'Comuna/Corregimiento', 'cumplimiento': '% Avance'})
                st.plotly_chart(fig_terr, use_container_width=True)
            else:
                st.info("Sin datos territoriales agregados.")
                
        with c2:
            st.subheader("👥 Población Objetivo")
            pop_data = data.get('population_data', [])
            if pop_data:
                df_pop = pd.DataFrame(pop_data)
                fig_pop = px.pie(df_pop, values='count', names='poblacion', hole=0.4, title="Distribución de Indicadores")
                st.plotly_chart(fig_pop, use_container_width=True)

    # TAB 4: DATOS MAESTROS
    with tab4:
        st.subheader("📂 Explorador de Datos Maestros")
        
        col_d1, col_d2 = st.columns([1, 4])
        with col_d1:
            # Direct download of local file
            with open(MASTER_FILE, "rb") as f:
                st.download_button("📥 Descargar Excel", f, "Matriz_Maestra_MISE_2025_Limpia.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        with col_d2:
            st.info("💡 Descargue la Matriz Maestra para realizar análisis detallados en Excel o PowerBI.")

    # --- HALLAZGOS PDF ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Reportes")
    if st.sidebar.button("📄 Informe Ejecutivo (PDF)"):
        with st.spinner("Generando PDF..."):
             pdf_bytes = generate_pdf_report(sel_pop)
             if pdf_bytes:
                 st.sidebar.download_button("⬇️ Descargar PDF", pdf_bytes, f"Informe_Ejecutivo_{sel_pop}.pdf", "application/pdf")
             else:
                 st.sidebar.error("Error al generar PDF")

def view_validador():
    st.title("🛡️ Panel de Validación")
    st.info("Funcionalidad simplificada para demo.")
    if st.button("Cerrar Sesión"): logout()

def view_capturista():
    st.title("📝 Panel de Captura")
    st.info("Funcionalidad simplificada para demo.")
    if st.button("Cerrar Sesión"): logout()

# --- Main Routing ---
if not st.session_state.logged_in:
    login()
else:
    role = st.session_state.role
    if role in ['Decisor', 'Admin']:
        view_decisor()
    elif role == 'Validador':
        view_validador()
    elif role == 'Capturista':
        view_capturista()
    else:
        st.error(f"Rol desconocido: {role}")
        if st.button("Salir"): logout()
