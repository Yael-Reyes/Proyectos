# generar_embeddings.py
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import time

print("Iniciando la generación de embeddings...")

# --- Carga del Modelo ---
# Se utiliza el modelo 'all-MiniLM-L6-v2', que es rápido y muy efectivo para tareas de similitud semántica.
print("Cargando el modelo de SentenceTransformer...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Modelo cargado.")

# --- Carga de los Datos Procesados ---
try:
    df_vocations = pd.read_csv("vocations_processed.csv")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'vocations_processed.csv'.")
    print("Asegúrate de que el archivo generado en el paso anterior esté en la misma carpeta.")
    exit()

# Extraer la lista de descripciones completas
# .fillna('') asegura que si alguna descripción está vacía, no cause un error.
descriptions = df_vocations['description_full'].fillna('').tolist()

print(f"Se procesarán {len(descriptions)} descripciones de vocaciones.")

# --- Generación de Embeddings ---
# Este es el paso que más tiempo consume. Puede tardar varios minutos dependiendo de tu CPU.
print("Generando embeddings... Esto puede tardar unos minutos.")
start_time = time.time()

# El método model.encode() convierte la lista de textos en una matriz de vectores (embeddings).
# show_progress_bar=True muestra una barra de progreso muy útil.
vocation_embeddings = model.encode(descriptions, show_progress_bar=True)

end_time = time.time()
print(f"Generación de embeddings completada en {end_time - start_time:.2f} segundos.")

# --- Verificación y Guardado ---
# La forma de la matriz será (número de vocaciones, 384) porque 'all-MiniLM-L6-v2' crea vectores de 384 dimensiones.
print(f"Forma de la matriz de embeddings: {vocation_embeddings.shape}")

# Guardar la matriz de embeddings en un archivo .npy para un acceso rápido en el futuro.
# np.save es mucho más eficiente que guardar texto en un CSV.
output_filename = "vocation_embeddings.npy"
np.save(output_filename, vocation_embeddings)

print("-" * 50)
print(f"¡Éxito! ✨")
print(f"Los embeddings han sido generados y guardados en el archivo '{output_filename}'.")
print("Ya tienes todo lo necesario para el motor de recomendación.")
print("-" * 50)