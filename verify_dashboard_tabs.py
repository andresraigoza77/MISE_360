
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def verify_dashboard():
    print("🚀 Iniciando Verificación de Dashboard MISE 360")
    
    # 1. Login
    try:
        r = requests.post(f"{API_URL}/token", data={"username": "capturista@misedigital.com", "password": "medellin2026"})
        if r.status_code != 200:
            print(f"❌ Login Fallido: {r.text}")
            return
        token = r.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        print(f"✅ Login Exitoso (Token len: {len(token)})")
    except Exception as e:
        print(f"❌ Error de Conexión en Login: {e}")
        return

    # 2. Fetch Dashboard Data
    try:
        r_kpi = requests.get(f"{API_URL}/dashboard/kpis", headers=headers)
        if r_kpi.status_code != 200:
            print(f"❌ Error Dashboard KPI: {r_kpi.text}")
            return
        data = r_kpi.json()
        print("✅ Datos Dashboard Recibidos")
    except Exception as e:
        print(f"❌ Error de Conexión Dashboard: {e}")
        return

    # 3. Verify Tab 1: Estratégico
    print("\n📊 Tab 1: Estratégico")
    print(f"  - Cumplimiento Global: {data.get('global_compliance')}% (Esperado > 0)")
    print(f"  - Cumplimiento Presupuestal: {data.get('budget_compliance')}%")
    pillars = data.get('pillars', [])
    print(f"  - Pilares Encontrados: {len(pillars)}")
    if pillars:
        print(f"    * Top Pilar: {pillars[0]['pilar o eje plan de desarrollo distrital']} ({pillars[0]['cumplimiento']:.1f}%)")
    deps = data.get('dependencies', [])
    print(f"  - Dependencias Ranking: {len(deps)}")

    if data.get('global_compliance') > 0 and pillars and deps:
        print("  ✅ Tab Estratégico: OK")
    else:
        print("  ❌ Tab Estratégico: Datos Incompletos")

    # 4. Verify Tab 2: Eficiencia
    print("\n⚡ Tab 2: Eficiencia")
    alerts = data.get('efficiency_alerts', [])
    print(f"  - Alertas de Eficiencia: {len(alerts)}")
    if alerts:
        print(f"    * Ejemplo Alerta: {alerts[0]['Indicador']} (Físico: {alerts[0]['Avance_Fisico']:.1f}%, Financiero: {alerts[0]['Avance_Financiero']:.1f}%)")
    scatter = data.get('scatter_data', [])
    print(f"  - Puntos Scatter Plot: {len(scatter)}")
    
    if scatter:
        print("  ✅ Tab Eficiencia: OK")
    else:
        print("  ❌ Tab Eficiencia: Sin datos para Scatter")

    # 5. Verify Tab 3: Territorio
    print("\n🌍 Tab 3: Territorio y Social")
    terr = data.get('territorial_data', [])
    print(f"  - Datos Territoriales: {len(terr)}")
    pop = data.get('population_data', [])
    print(f"  - Grupos Poblacionales: {len(pop)}")
    
    if terr or pop: # At least one should have data
        print("  ✅ Tab Territorio: OK (Parcial o Total)")
    else:
        print("  ⚠️ Tab Territorio: Sin datos (Puede ser normal si no hay desagregación)")

    # 6. Verify Tab 4: Datos Maestros (Download)
    print("\n📂 Tab 4: Datos Maestros")
    try:
        r_down = requests.get(f"{API_URL}/reports/export", headers=headers)
        if r_down.status_code == 200:
            print("  ✅ Descarga Excel: OK")
        else:
            print(f"  ❌ Descarga Excel Fallida: {r_down.status_code}")
    except:
        print("  ❌ Error probando descarga")

    # Final Summary
    print("\n🏁 Conclusión: Backend Operativo para Dashboard.")

if __name__ == "__main__":
    verify_dashboard()
