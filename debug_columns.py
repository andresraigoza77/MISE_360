
import pandas as pd

try:
    df = pd.read_excel('Matriz_Maestra_MISE_2025_Limpia.xlsx')
    print("--- Presupuesto Programado ---")
    if 'presupuesto programado' in df.columns:
        print(df['presupuesto programado'].head(10).tolist())
        print(df['presupuesto programado'].dtype)
    else:
        print("Column MISSING")

    print("\n--- Pilar ---")
    if 'pilar o eje plan de desarrollo distrital' in df.columns:
        print(df['pilar o eje plan de desarrollo distrital'].head(10).tolist())
        print(df['pilar o eje plan de desarrollo distrital'].unique())
    else:
        print("Column MISSING")

    print("\n--- Meta ---")
    print(df['Meta_Limpia'].head(5).tolist())

except Exception as e:
    print(e)
