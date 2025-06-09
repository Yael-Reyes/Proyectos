# app_vocacional.py
import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch
import os

# --- Configuración de la Página ---
# st.set_page_config se usa para configurar el título de la pestaña del navegador, el ícono y el layout.
st.set_page_config(page_title="Orientador Vocacional AI", page_icon="🎓", layout="centered")

# --- Caching de Recursos ---
# El caching es VITAL para el rendimiento de una app de Streamlit.
# @st.cache_resource se usa para cosas que no cambian y no quieres recargar cada vez, como un modelo de ML.
@st.cache_resource
def load_model():
    """Carga el modelo de sentence-transformers desde el cache."""
    print("Cargando modelo de embeddings...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Modelo cargado.")
    return model

# @st.cache_data se usa para datos que no cambian, como un CSV o los embeddings.
@st.cache_data
def load_data():
    """Carga los datos de vocaciones y los embeddings pre-calculados desde el cache."""
    print("Cargando datos y embeddings...")
    
    # Rutas a los archivos
    csv_file = "vocations_processed.csv"
    npy_file = "vocation_embeddings.npy"

    if not os.path.exists(csv_file) or not os.path.exists(npy_file):
        st.error(f"Error: No se encontraron los archivos necesarios ('{csv_file}', '{npy_file}').")
        st.error("Por favor, asegúrate de ejecutar los scripts de preparación de datos y generación de embeddings primero.")
        return None, None

    df = pd.read_csv(csv_file)
    embeddings = np.load(npy_file)
    print("Datos y embeddings cargados.")
    return df, torch.tensor(embeddings)

# --- Carga Principal ---
# Se llama a las funciones de carga. Gracias al cache, esto solo se ejecutará la primera vez que inicies la app.
model = load_model()
df_vocations, vocation_embeddings = load_data()


# --- Interfaz de Usuario (UI) ---
st.title("🎓 Orientador Vocacional AI")
st.write(
    "¡Bienvenido a tu asistente de orientación vocacional! Describe en el siguiente cuadro "
    "tus intereses, pasatiempos, las materias que te gustan y lo que te imaginas haciendo en el futuro."
)

# Verificamos si los datos se cargaron correctamente antes de continuar
if df_vocations is not None and vocation_embeddings is not None:
    # Área de texto para la entrada del usuario
    user_input = st.text_area(
        "Escribe aquí sobre ti:",
        height=170,
        placeholder="Ej: Me encantan los videojuegos, especialmente el diseño de personajes y mundos. Soy bueno dibujando y se me da bien la tecnología. Me gusta trabajar en equipo para crear cosas nuevas y visualmente atractivas."
    )

    # Botón para iniciar la búsqueda de vocaciones
    if st.button("✨ Encontrar mi Vocación"):
        if user_input:
            # Usamos un spinner para que el usuario sepa que algo está pasando
            with st.spinner("Analizando tu perfil y buscando las mejores opciones..."):
                # 1. Generar embedding para la entrada del usuario
                user_embedding = model.encode(user_input, convert_to_tensor=True)

                # 2. Calcular la similitud del coseno
                cosine_scores = util.cos_sim(user_embedding, vocation_embeddings)

                # 3. Obtener los N mejores resultados (en este caso, 10)
                top_results = torch.topk(cosine_scores[0], k=10)

                st.success("¡Análisis completado! Aquí están tus recomendaciones principales:")

                # 4. Mostrar los resultados

                for score, idx in zip(top_results[0], top_results[1]):
                    vocation = df_vocations.iloc[idx.item()]

                    
                    # Usamos st.expander para un diseño más limpio
                    with st.expander(f"**{vocation['Title']}** (Similitud: {score:.0%})"):
                        st.write(f"**Descripción:** {vocation['Description']}")
                        
                        # Mostramos algunas tareas para dar más contexto
                        tasks = str(vocation.get('Task Statements', 'No hay tareas específicas disponibles.')).split('.')
                        if tasks:
                            st.write("**Algunas tareas incluyen:**")
                            # Mostramos un máximo de 3 tareas para no saturar
                            for task in tasks[:3]:
                                if task.strip():
                                    st.markdown(f"- {task.strip()}")

        else:
            # Advertencia si el usuario no ha escrito nada
            st.warning("Por favor, escribe algo sobre ti para poder darte una recomendación.")

# streamlit run app_vocacional.py