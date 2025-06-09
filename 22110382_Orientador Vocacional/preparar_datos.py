import pandas as pd
import os

print("Iniciando el procesamiento de la base de datos O*NET...")

# --- Configuración de Rutas ---
data_directory = "db_29_3_excel/"

files = {
    "occupations": os.path.join(data_directory, "Occupation Data.xlsx"),
    "tasks": os.path.join(data_directory, "Task Statements.xlsx"),
    "activities": os.path.join(data_directory, "Work Activities.xlsx"),
    "knowledge": os.path.join(data_directory, "Knowledge.xlsx")
}

for file_key, file_path in files.items():
    if not os.path.exists(file_path):
        print(f"Error: El archivo no se encontró en la ruta '{file_path}'")
        print("Asegúrate de que la carpeta 'db_29_3_excel' exista y contenga los archivos de O*NET.")
        exit()

# --- Carga de Datos ---
print("Cargando archivos Excel en DataFrames de Pandas...")
df_occupations = pd.read_excel(files["occupations"])
df_tasks = pd.read_excel(files["tasks"])
df_activities = pd.read_excel(files["activities"])
df_knowledge = pd.read_excel(files["knowledge"])
print("Archivos cargados correctamente.")

# --- Agregación de Información Textual ---
print("Agregando las tareas para cada vocación...")
tasks_agg = df_tasks.groupby('O*NET-SOC Code')['Task'].apply(lambda tasks: '. '.join(tasks)).reset_index()
tasks_agg.rename(columns={'Task': 'Task Statements'}, inplace=True)

print("Agregando las actividades de trabajo...")
activities_agg = df_activities.groupby('O*NET-SOC Code')['Element Name'].apply(lambda activities: '. '.join(activities)).reset_index()
activities_agg.rename(columns={'Element Name': 'Work Activities'}, inplace=True)

print("Agregando los conocimientos requeridos...")
knowledge_agg = df_knowledge.groupby('O*NET-SOC Code')['Element Name'].apply(lambda elements: ', '.join(elements)).reset_index()
knowledge_agg.rename(columns={'Element Name': 'Knowledge'}, inplace=True)

# --- Unión (Merge) de los DataFrames ---
print("Uniendo toda la información en un único DataFrame...")
df_final = df_occupations.copy()
df_final = pd.merge(df_final, tasks_agg, on='O*NET-SOC Code', how='left')
df_final = pd.merge(df_final, activities_agg, on='O*NET-SOC Code', how='left')
df_final = pd.merge(df_final, knowledge_agg, on='O*NET-SOC Code', how='left')

# --- Creación de la Columna Descriptiva Unificada ---
print("Creando la columna de descripción completa para los embeddings...")
df_final['Task Statements'] = df_final['Task Statements'].fillna('')
df_final['Work Activities'] = df_final['Work Activities'].fillna('')
df_final['Knowledge'] = df_final['Knowledge'].fillna('')

df_final['description_full'] = (
    "Título de la vocación: " + df_final['Title'] + ". " +
    "Descripción general: " + df_final['Description'] + ". " +
    "Tareas típicas: " + df_final['Task Statements'] + ". " +
    "Actividades laborales: " + df_final['Work Activities'] + ". " +
    "Conocimientos necesarios: " + df_final['Knowledge'] + "."
)

# --- Guardado del Resultado ---
output_filename = "vocations_processed.csv"
df_final.to_csv(output_filename, index=False)

print("-" * 50)
print(f"¡Proceso completado con éxito! ✨")
print(f"Se ha creado el archivo '{output_filename}'.")
print(f"Este archivo contiene {len(df_final)} vocaciones, cada una con su descripción consolidada.")
print("\nEjemplo de una descripción generada:")
print(df_final[['Title', 'description_full']].head(1).iloc[0]['description_full'])
print("-" * 50)