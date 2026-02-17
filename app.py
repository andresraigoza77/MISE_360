
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import os
from io import BytesIO

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

# API URL
API_URL = "http://localhost:8000"

# --- AUTH & STATE ---
if 'token' not in st.session_state: st.session_state.token = None
if 'role' not in st.session_state: st.session_state.role = None
if 'user' not in st.session_state: st.session_state.user = None

def login():
    st.markdown("## 🔐 Iniciar Sesión MISE")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        try:
            r = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
            if r.status_code == 200:
                data = r.json()
                st.session_state.token = data['access_token']
                # Decode role roughly or fetch user data
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                r_me = requests.get(f"{API_URL}/users/me/", headers=headers)
                if r_me.status_code == 200:
                    user_data = r_me.json()
                    st.session_state.role = user_data['rol']
                    st.session_state.user = user_data['username']
                    st.success(f"Bienvenido {user_data['full_name']}")
                    st.rerun()
            else:
                st.error("Credenciales inválidas.")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

def logout():
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.user = None
    st.rerun()

def download_hallazgos(poblacion_filter):
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        params = {}
        if poblacion_filter and poblacion_filter != "Todos": params['poblacion'] = poblacion_filter
        
        r = requests.get(f"{API_URL}/reports/hallazgos", headers=headers, params=params)
        if r.status_code == 200:
            return r.content
        return None
    except: return None

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
    
    # Refresh
    if st.sidebar.button("🔄 Refrescar Datos"):
        st.cache_data.clear()
        st.rerun()

    token = st.session_state.token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Fetch Dependencies for Filter
    try:
        r_init = requests.get(f"{API_URL}/dashboard/kpis", headers=headers)
        if r_init.status_code == 200:
             init_data = r_init.json()
             dep_list = init_data.get('param_dependencies', [])
        else: dep_list = []
    except: dep_list = []

    sel_dep = st.sidebar.selectbox("Secretaría / Dependencia", ["Todas"] + dep_list)
    sel_pop = st.sidebar.selectbox("Población Objetivo", ["Todos", "Mujeres", "Jóvenes", "Víctimas", "Indígena", "Afrodescendiente"])
    
    # Fetch Filtered Data
    params = {}
    if sel_dep and sel_dep != "Todas": params['dependencia'] = sel_dep
    if sel_pop and sel_pop != "Todos": params['poblacion'] = sel_pop
    
    with st.spinner("Analizando información estratégica..."):
        try:
            r = requests.get(f"{API_URL}/dashboard/kpis", headers=headers, params=params)
            if r.status_code == 200:
                data = r.json()
            else:
                st.error(f"Error API {r.status_code}: {r.text}")
                return
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            return

    # --- TABS ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Estratégico", "⚡ Eficiencia", "🌍 Territorio y Social", "📂 Datos Maestros"])
    
    # --- PROCESSED DATA ---
    global_kpi = data.get('global_compliance', 0)
    budget_kpi = data.get('budget_compliance', 0)
    
    # TAB 1: ESTRATÉGICO
    with tab1:
        # KPI Cards
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
            
            # Dynamic Rename (Re-using logic just in case)
            cols = df_sc.columns
            c_ind = next((c for c in cols if 'indicador' in c.lower()), None)
            c_dep = next((c for c in cols if 'dependencia' in c.lower()), None)
            
            rename_map = {}
            if c_ind: rename_map[c_ind] = 'Indicador'
            if c_dep: rename_map[c_dep] = 'Dependencia'
            if rename_map: df_sc.rename(columns=rename_map, inplace=True)
            
            if 'Dependencia' in df_sc.columns:
                # Aggregate by Dependency
                df_agg = df_sc.groupby('Dependencia')[['cumplimiento_fisico', 'cumplimiento_financiero']].mean().reset_index()
                
                # Calculate Gap for Sorting (Financial - Physical)
                df_agg['Brecha'] = df_agg['cumplimiento_financiero'] - df_agg['cumplimiento_fisico']
                df_agg = df_agg.sort_values('Brecha', ascending=False).head(15) # Top 15 worst gaps
                
                # Transform to Long Format for Grouped Bar Chart
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
                st.caption("Nota: Se muestran las dependencias donde la inversión supera más notablemente al avance físico.")
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
            # Download Clean Excel
            if st.button("📥 Descargar Matriz Limpia"):
                 r_down = requests.get(f"{API_URL}/reports/export", headers=headers)
                 if r_down.status_code == 200:
                    st.download_button("💾 Guardar Excel (Limpio)", r_down.content, "Matriz_Maestra_MISE_2025_Limpia.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        with col_d2:
            st.info("💡 Descargue la Matriz Maestra para realizar análisis detallados en Excel o PowerBI. Esta matriz contiene los datos normalizados y limpios.")

    # --- HALLAZGOS PDF ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Reportes")
    if st.sidebar.button("📄 Informe Ejecutivo (PDF)"):
        with st.spinner("Generando PDF..."):
             pdf_bytes = download_hallazgos(sel_pop)
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
if not st.session_state.token:
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
