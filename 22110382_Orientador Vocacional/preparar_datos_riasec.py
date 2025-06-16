# preparar_datos_riasec.py (Versión Final y Corregida)
import pandas as pd
import os

print("Iniciando el procesamiento FINAL de la base de datos O*NET (con RIASEC)...")

# --- Configuración de Rutas ---
data_directory = "db_29_3_excel/"
output_filename = "vocations_riasec_processed.csv"

# --- Carga de Datos ---
print("Cargando archivos Excel...")
df_occupations = pd.read_excel(os.path.join(data_directory, "Occupation Data.xlsx"))
df_tasks = pd.read_excel(os.path.join(data_directory, "Task Statements.xlsx"))
df_interests = pd.read_excel(os.path.join(data_directory, "Interests.xlsx"))

# --- LÓGICA DE PROCESAMIENTO RIASEC CORREGIDA ---
print("Procesando los códigos de Holland (RIASEC) a partir de códigos numéricos...")

# 1. Filtrar por el Scale ID que contiene los puntos altos de interés
df_interests_high = df_interests[df_interests['Scale ID'] == 'IH']

# 2. Pivotar la tabla para tener una fila por vocación
riasec_pivot = df_interests_high.pivot_table(
    index='O*NET-SOC Code', 
    columns='Element Name', 
    values='Data Value'
).reset_index()

# 3. Diccionario para mapear el código numérico de O*NET a la letra RIASEC
CODE_TO_LETTER = {
    1.0: 'R', 2.0: 'I', 3.0: 'A', 4.0: 'S', 5.0: 'E', 6.0: 'C',
    # Incluimos el 0.0 por si acaso, para que no dé error
    0.0: '' 
}

# 4. Función para construir el código Holland a partir de los códigos numéricos
def build_holland_code(row):
    # Obtenemos los códigos numéricos de las tres columnas de interés
    code1 = row.get('First Interest High-Point', 0.0)
    code2 = row.get('Second Interest High-Point', 0.0)
    code3 = row.get('Third Interest High-Point', 0.0)
    
    # Usamos el diccionario para convertir cada código a su letra correspondiente
    letter1 = CODE_TO_LETTER.get(code1, '')
    letter2 = CODE_TO_LETTER.get(code2, '')
    letter3 = CODE_TO_LETTER.get(code3, '')
    
    # Unimos las letras para formar el código final (ej. "ESC")
    return letter1 + letter2 + letter3

# 5. Aplicamos la función para crear la nueva columna 'Holland Code'
riasec_pivot['Holland Code'] = riasec_pivot.apply(build_holland_code, axis=1)


# --- Agregación de Tareas ---
print("Agregando tareas...")
tasks_agg = df_tasks.groupby('O*NET-SOC Code')['Task'].apply(lambda tasks: '. '.join(tasks)).reset_index()
tasks_agg.rename(columns={'Task': 'Task Statements'}, inplace=True)

# --- Unión de todos los DataFrames ---
print("Uniendo toda la información...")
df_final = pd.merge(df_occupations, tasks_agg, on='O*NET-SOC Code', how='left')
# Unimos solo las columnas que necesitamos del pivote de riasec
df_final = pd.merge(df_final, riasec_pivot[['O*NET-SOC Code', 'Holland Code']], on='O*NET-SOC Code', how='left')

# --- Creación de la Columna Descriptiva Unificada ---
print("Creando la columna de descripción completa...")
df_final['Task Statements'] = df_final['Task Statements'].fillna('')
df_final['Holland Code'] = df_final['Holland Code'].fillna('') # Asegurarnos que no haya NaNs
df_final['description_full'] = "Título: " + df_final['Title'] + ". Descripción: " + df_final['Description'] + ". Tareas: " + df_final['Task Statements']

# --- Guardado del Resultado ---
df_final.to_csv(output_filename, index=False)

print("-" * 50)
print(f"¡Proceso completado con éxito! ✨")
print(f"Se ha creado el archivo '{output_filename}' con los códigos de Holland correctos.")
print("Ejemplo del resultado final:")
print(df_final[['Title', 'Holland Code']].head())
print("-" * 50)