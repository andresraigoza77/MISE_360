
import sqlite3
import os

db_file = "mise_digital.db"

# Remove existing db if exists to start fresh (optional, but good for clean slate based on user request "Create...")
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"Removed existing database: {db_file}")

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# DDL Script adapted for SQLite
ddl_script = """
-- 1. Tabla: Dependencias
CREATE TABLE Dependencias (
    id_dependencia INTEGER PRIMARY KEY,
    nombre_dependencia TEXT NOT NULL,
    codigo_misional TEXT
);

-- 2. Tabla: Proyectos
CREATE TABLE Proyectos (
    codigo_bpin TEXT PRIMARY KEY,
    nombre_proyecto TEXT,
    objetivo_proyecto TEXT,
    presupuesto_programado_total REAL,
    id_dependencia INTEGER,
    FOREIGN KEY (id_dependencia) REFERENCES Dependencias(id_dependencia)
);

-- 3. Tabla: Indicadores
CREATE TABLE Indicadores (
    id_indicador INTEGER PRIMARY KEY,
    nombre_indicador TEXT NOT NULL,
    subdimension TEXT,
    unidad_medida TEXT,
    tipo_indicador TEXT,
    linea_base REAL,
    anio_linea_base INTEGER,
    meta_total REAL,
    anio_meta INTEGER,
    codigo_bpin_proyecto TEXT,
    id_dependencia_responsable INTEGER,
    FOREIGN KEY (codigo_bpin_proyecto) REFERENCES Proyectos(codigo_bpin),
    FOREIGN KEY (id_dependencia_responsable) REFERENCES Dependencias(id_dependencia)
);

-- 4. Tabla: Reportes_Trimestrales
CREATE TABLE Reportes_Trimestrales (
    id_reporte INTEGER PRIMARY KEY AUTOINCREMENT,
    id_indicador INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    trimestre INTEGER NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    valor_programado REAL,
    valor_ejecutado REAL,
    avance_fisico REAL,
    avance_financiero REAL,
    observaciones TEXT,
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_indicador) REFERENCES Indicadores(id_indicador),
    UNIQUE (id_indicador, anio, trimestre)
);
"""

try:
    print("Executing DDL script...")
    cursor.executescript(ddl_script)
    conn.commit()
    print("Tables created successfully.")

    # Verify tables
    print("\nVerifying tables:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        # Check if empty
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f" - Table '{table_name}' created. Row count: {count}")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
