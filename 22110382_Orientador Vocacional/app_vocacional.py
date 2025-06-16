# app_vocacional_completo.py (Versión con Asistente Paso a Paso)
import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch
import os
from collections import Counter

# --- Configuración de la Página y Caching ---
st.set_page_config(page_title="Orientador Vocacional PRO", page_icon="✨", layout="centered") # Centered layout es mejor para un wizard

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def load_data():
    csv_file = "vocations_riasec_processed.csv"
    npy_file = "vocation_embeddings.npy"
    if not os.path.exists(csv_file) or not os.path.exists(npy_file):
        return None, None
    df = pd.read_csv(csv_file)
    embeddings = np.load(npy_file)
    return df, torch.tensor(embeddings)

# --- BANCO DE PREGUNTAS (Sin cambios) ---
QUESTIONS_EXPANDED = {
    "Realista (R) - Los Hacedores": ["Armar, arreglar o mantener aparatos mecánicos.", "Trabajar con herramientas manuales o eléctricas.", "Construir algo con madera, metal o ladrillos.", "Seguir un plano o un diagrama para ensamblar algo.", "Trabajar al aire libre en cualquier condición climática.", "Cuidar plantas o animales.", "Realizar actividades que requieran esfuerzo físico.", "Manejar vehículos o maquinaria pesada.", "Entender cómo funcionan las cosas (ej. un motor).", "Tomar una clase de taller o carpintería."],
    "Investigador (I) - Los Pensadores": ["Resolver problemas complejos de lógica o matemáticas.", "Utilizar un microscopio o equipo de laboratorio.", "Leer artículos científicos o técnicos.", "Desarrollar una teoría para explicar un fenómeno.", "Analizar datos para encontrar patrones.", "Programar en una computadora.", "Investigar sobre un tema hasta entenderlo a fondo.", "Formular una hipótesis y diseñar un experimento.", "Trabajar con ideas y conceptos abstractos.", "Tomar una clase de química o física."],
    "Artístico (A) - Los Creadores": ["Dibujar, pintar, o hacer bocetos.", "Escribir historias, poesía, o artículos.", "Tocar un instrumento musical.", "Actuar en una obra de teatro o película.", "Diseñar ropa, muebles o espacios.", "Crear gráficos o animaciones por computadora.", "Tomar fotografías o videos artísticos.", "Crear o arreglar música.", "Expresar mis emociones a través del arte.", "Visitar museos o galerías de arte."],
    "Social (S) - Los Ayudadores": ["Enseñar una habilidad a alguien.", "Ayudar a mis amigos con sus problemas.", "Trabajar como voluntario en una causa social.", "Cuidar de niños, ancianos o personas que necesitan ayuda.", "Mediar en un conflicto entre dos personas.", "Organizar actividades y eventos para un grupo.", "Escuchar atentamente los problemas de los demás.", "Trabajar en equipo para mejorar la comunidad.", "Explicar cosas de manera clara.", "Tomar una clase de psicología o sociología."],
    "Emprendedor (E) - Los Persuasores": ["Iniciar y liderar un proyecto o negocio.", "Vender un producto o una idea.", "Dar un discurso a un grupo de personas.", "Negociar para llegar a un acuerdo.", "Motivar a un equipo para que alcance sus metas.", "Tomar decisiones importantes que impliquen riesgos.", "Organizar una campaña de marketing.", "Buscar oportunidades para obtener ganancias.", "Ser el responsable de un grupo o evento.", "Tomar una clase de administración de empresas."],
    "Convencional (C) - Los Organizadores": ["Mantener registros y archivos de manera ordenada.", "Trabajar con números y hojas de cálculo.", "Seguir un conjunto de reglas y procedimientos.", "Detectar errores en un texto o en datos.", "Crear un horario o un plan detallado.", "Clasificar y organizar información sistemáticamente.", "Operar equipo de oficina.", "Manejar correspondencia y reportes.", "Trabajar en un ambiente estructurado.", "Tomar una clase de contabilidad o bases de datos."]
}

# --- Carga de Recursos ---
model = load_model()
df_vocations, vocation_embeddings = load_data()

# --- Título Principal ---
st.title("✨ Orientador Vocacional PRO")
st.write("Un sistema experto para ayudarte a descubrir tu vocación.")

if df_vocations is None:
    st.error("Error: Faltan los archivos de datos. Asegúrate de ejecutar los scripts de preparación.")
else:
    # --- Pestañas ---
    tab1, tab2 = st.tabs(["**Test Vocacional Guiado**", "**Búsqueda por Descripción Libre**"])

    # --- Pestaña 1: TEST GUIADO ---
    with tab1:
        # --- INICIALIZACIÓN DEL ESTADO ---
        if 'step' not in st.session_state:
            st.session_state.step = 0
            st.session_state.answers = {}

        categories = list(QUESTIONS_EXPANDED.keys())
        options = ["No me gusta", "Indiferente", "Me gusta"]
        
        # --- LÓGICA DE NAVEGACIÓN PASO A PASO ---
        # Paso 0: Pantalla de bienvenida del test
        if st.session_state.step == 0:
            st.header("Descubre tu Perfil Vocacional")
            st.markdown("A continuación, te presentaremos 6 series de 10 actividades. Para cada una, indica qué tanto te atrae la idea de realizarla.")
            st.markdown("Esto nos ayudará a construir un perfil de tus intereses y a recomendarte las carreras más afines a ti. ¡Comencemos!")
            if st.button("▶️ Iniciar Test"):
                st.session_state.step += 1
                st.rerun()

        # Pasos 1-6: Mostrar las preguntas de cada categoría
        elif 1 <= st.session_state.step <= len(categories):
            current_category_index = st.session_state.step - 1
            current_category = categories[current_category_index]
            
            st.header(f"Paso {st.session_state.step} de {len(categories)}: {current_category}")
            st.progress(st.session_state.step / len(categories))
            
            for q in QUESTIONS_EXPANDED[current_category]:
                # Si la respuesta no existe, se establece en 'Indiferente' por defecto
                st.session_state.answers[q] = st.radio(
                    q, options, 
                    index=options.index(st.session_state.answers.get(q, "Indiferente")), 
                    key=q, 
                    horizontal=True
                )
            
            # Columnas para los botones de navegación
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Anterior"):
                    st.session_state.step -= 1
                    st.rerun()
            with col2:
                if st.button("Siguiente ➡️"):
                    st.session_state.step += 1
                    st.rerun()

        # Paso 7: Pantalla de resultados
        else:
            st.header("🎉 ¡Test Completado!")
            with st.spinner("Analizando tus respuestas y calculando tu perfil..."):
                # Lógica de conteo
                scores = {category.split(' ')[0]: 0 for category in QUESTIONS_EXPANDED.keys()}
                for category_full, questions in QUESTIONS_EXPANDED.items():
                    category_short = category_full.split(' ')[0]
                    for q in questions:
                        answer = st.session_state.answers.get(q, "Indiferente")
                        if answer == "Me gusta":
                            scores[category_short] += 2
                        elif answer == "Indiferente":
                            scores[category_short] += 1
                
                sorted_scores = Counter(scores).most_common(6)
                user_holland_code = "".join([cat[0] for cat, score in sorted_scores[:3]])
                top_3_categories = [cat for cat, score in sorted_scores[:3]]

            st.success(f"### Tu perfil RIASEC es: **{user_holland_code}**")
            st.markdown(f"Tus áreas de mayor interés son: **{top_3_categories[0]}**, **{top_3_categories[1]}** y **{top_3_categories[2]}**.")
            
            chart_data = pd.DataFrame.from_dict(scores, orient='index', columns=['Puntuación']).sort_values('Puntuación', ascending=False)
            st.bar_chart(chart_data)

            st.subheader("Vocaciones recomendadas para tu perfil:")
            
            def partial_match(code, user_code):
                if pd.isna(code): return False
                return sum(1 for char in user_code if char in user_code) >= 2

            perfect_matches = df_vocations[df_vocations['Holland Code'] == user_holland_code]
            partial_matches = df_vocations[df_vocations['Holland Code'].apply(partial_match, user_code=user_holland_code)]
            results_df = pd.concat([perfect_matches, partial_matches]).drop_duplicates().head(15)

            if not results_df.empty:
                for index, row in results_df.iterrows():
                    with st.expander(f"**{row['Title']}** (Código: {row['Holland Code']})"):
                        st.write(row['Description'])
            
            if st.button("🔁 Realizar el test de nuevo"):
                st.session_state.step = 0
                st.session_state.answers = {}
                st.rerun()

    # --- Pestaña 2: Búsqueda por Descripción ---
    with tab2:
        st.header("Busca por tus Propias Palabras")
        st.markdown("Si ya tienes una idea de lo que te gusta, descríbelo aquí para encontrar vocaciones con tareas y descripciones similares.")
        
        user_input = st.text_area("Escribe aquí sobre ti:", height=170, key="text_search_area")

        if st.button("Buscar por Descripción"):
            if user_input:
                with st.spinner("Buscando por similitud semántica..."):
                    user_embedding = model.encode(user_input, convert_to_tensor=True)
                    cosine_scores = util.cos_sim(user_embedding, vocation_embeddings)
                    top_results = torch.topk(cosine_scores[0], k=5)

                    st.success("Resultados basados en la descripción:")
                    for score, idx in zip(top_results[0], top_results[1]):
                        vocation = df_vocations.iloc[idx.item()]
                        with st.expander(f"**{vocation['Title']}** (Similitud: {score:.0%})"):
                            st.write(vocation['Description'])
            else:
                st.warning("Por favor, introduce una descripción.")

                
# streamlit run app_vocacional.py