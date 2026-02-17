
import sqlite3
import pandas as pd

def verify():
    conn = sqlite3.connect('mise_digital.db')
    
    query = """
    SELECT 
        d.id_dependencia,
        d.nombre_dependencia, 
        COUNT(r.id_reporte) as num_reportes 
    FROM Dependencias d
    LEFT JOIN Indicadores i ON d.id_dependencia = i.id_dependencia_responsable
    LEFT JOIN Reportes_Trimestrales r ON i.id_indicador = r.id_indicador
    GROUP BY d.id_dependencia, d.nombre_dependencia
    ORDER BY num_reportes DESC
    """
    
    df = pd.read_sql_query(query, conn)
    print(df.to_string())
    conn.close()

if __name__ == "__main__":
    verify()
