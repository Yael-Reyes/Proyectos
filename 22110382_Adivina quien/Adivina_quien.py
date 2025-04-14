import json
import os
import math
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk # Para widgets más modernos si se desea
from PIL import Image, ImageTk

# Nombre del archivo para la base de conocimientos (sin cambios)
ARCHIVO_CONOCIMIENTO = "conocimiento_animales.json"

# --- Clase SistemaInferenciaAnimales (Lógica del Juego) ---
class SistemaInferenciaAnimales:
    def __init__(self, archivo_conocimiento=ARCHIVO_CONOCIMIENTO):
        self.archivo_conocimiento = archivo_conocimiento
        self.animales_caracteristicas = self._cargar_conocimiento()
        self.reset_game_state() # Inicializar estado

    def _cargar_conocimiento(self):
        # Método privado para encapsular la carga
        if os.path.exists(self.archivo_conocimiento):
            try:
                with open(self.archivo_conocimiento, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convertir listas a sets
                    return {animal: set(caracteristicas) for animal, caracteristicas in data.items()}
            except (json.JSONDecodeError, IOError) as e:
                messagebox.showerror("Error de Carga", f"Error al cargar la base de conocimientos: {e}\nSe iniciará con una base vacía.")
                return {}
        return {}

    def _guardar_conocimiento(self):
        # Método privado para encapsular el guardado
        try:
            data_to_save = {animal: sorted(list(caracteristicas))
                            for animal, caracteristicas in self.animales_caracteristicas.items()}
            with open(self.archivo_conocimiento, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False, sort_keys=True)
            print(f"Base de conocimientos guardada en {self.archivo_conocimiento}") # Log en consola
        except IOError as e:
            messagebox.showerror("Error de Guardado", f"Error al guardar la base de conocimientos: {e}")

    def reset_game_state(self):
        """Reinicia las variables para un nuevo juego."""
        self.posibles_animales = set(self.animales_caracteristicas.keys())
        self.caracteristicas_preguntadas = set()
        self.caracteristicas_confirmadas = set()
        self.caracteristicas_negadas = set()
        self.current_question = None
        self.last_guess = None # Para saber qué se adivinó incorrectamente

    def is_knowledge_base_empty(self):
        """Verifica si hay animales en la base de datos."""
        return not bool(self.animales_caracteristicas)

    def get_next_question(self):
        """
        Determina y devuelve la siguiente mejor pregunta o un estado final.

        Returns:
            tuple: (estado, data) donde estado puede ser:
                'QUESTION', 'GUESS', 'NO_OPTIONS', 'LEARN_NO_QUESTIONS'
                y data es la pregunta (str), el animal/es a adivinar (str/set), o None.
        """
        if not self.posibles_animales:
            return ('NO_OPTIONS', None)

        if len(self.posibles_animales) == 1:
            self.last_guess = list(self.posibles_animales)[0]
            return ('GUESS', self.last_guess)

        mejor_caracteristica = self._seleccionar_mejor_pregunta()

        if mejor_caracteristica is None:
            # No hay más preguntas que distingan, pero hay varios animales
            if len(self.posibles_animales) > 1:
                # Elegir uno al azar o el primero para intentar adivinar
                self.last_guess = random.choice(list(self.posibles_animales))
                # Devolver todos los posibles por si falla y necesita aprender
                return ('LEARN_NO_QUESTIONS', self.posibles_animales)
            else: # Esto no debería pasar si la lógica es correcta, pero por si acaso
                return ('NO_OPTIONS', None)


        self.current_question = mejor_caracteristica
        return ('QUESTION', f"¿Tu animal {mejor_caracteristica}?")


    def _seleccionar_mejor_pregunta(self):
        """Lógica interna para seleccionar la mejor pregunta."""
        mejor_caracteristica = None
        mejor_score = -1

        caracteristicas_relevantes = set()
        for animal in self.posibles_animales:
            if animal in self.animales_caracteristicas:
                caracteristicas_relevantes.update(self.animales_caracteristicas[animal] - self.caracteristicas_preguntadas)

        if not caracteristicas_relevantes:
            return None

        for caracteristica in caracteristicas_relevantes:
            animales_con = sum(1 for animal in self.posibles_animales if animal in self.animales_caracteristicas and caracteristica in self.animales_caracteristicas[animal])
            animales_sin = len(self.posibles_animales) - animales_con

            if animales_con == 0 or animales_sin == 0:
                continue

            score = min(animales_con, animales_sin)
            if score > mejor_score:
                mejor_score = score
                mejor_caracteristica = caracteristica

        return mejor_caracteristica

    def process_answer(self, respuesta_si):
        """
        Actualiza el estado basado en la respuesta ('si' o 'no') a self.current_question.

        Args:
            respuesta_si (bool): True si la respuesta fue 'si', False si fue 'no'.
        """
        if self.current_question is None:
            return # No debería pasar si el flujo es correcto

        question_feature = self.current_question # La característica actual
        self.caracteristicas_preguntadas.add(question_feature)

        animales_a_eliminar = set()
        if respuesta_si:
            self.caracteristicas_confirmadas.add(question_feature)
            for animal in self.posibles_animales:
                if animal not in self.animales_caracteristicas or question_feature not in self.animales_caracteristicas[animal]:
                    animales_a_eliminar.add(animal)
        else: # Respuesta fue 'no'
            self.caracteristicas_negadas.add(question_feature)
            for animal in self.posibles_animales:
                if animal in self.animales_caracteristicas and question_feature in self.animales_caracteristicas[animal]:
                    animales_a_eliminar.add(animal)

        self.posibles_animales -= animales_a_eliminar
        self.current_question = None # Resetear pregunta actual después de procesar

    def aprender_nuevo_animal(self, nombre_animal_correcto, caracteristica_distintiva):
        """
        Añade un nuevo animal a la base de conocimientos. Usa el estado interno
        (confirmadas, negadas) del juego actual.

        Args:
            nombre_animal_correcto (str): El nombre del animal a aprender.
            caracteristica_distintiva (str): La característica clave proporcionada por el usuario.

        Returns:
            bool: True si el aprendizaje fue exitoso, False en caso contrario.
        """
        nombre_animal_correcto = nombre_animal_correcto.lower().strip()
        caracteristica_distintiva = caracteristica_distintiva.lower().strip()

        if not nombre_animal_correcto or not caracteristica_distintiva:
            messagebox.showwarning("Aprendizaje Fallido", "Debe proporcionar un nombre y una característica distintiva.")
            return False

        if nombre_animal_correcto in self.animales_caracteristicas:
            # Lógica para manejar animales existentes (informar, no sobrescribir por simplicidad)
            conocimiento_existente = self.animales_caracteristicas[nombre_animal_correcto]
            conflictos_si = self.caracteristicas_confirmadas - conocimiento_existente
            conflictos_no = self.caracteristicas_negadas.intersection(conocimiento_existente)
            if conflictos_si or conflictos_no:
                msg = f"Ya conozco al '{nombre_animal_correcto}', pero tus respuestas contradicen mi información:\n"
                if conflictos_si: msg += f"- Confirmaste: {conflictos_si}\n"
                if conflictos_no: msg += f"- Negaste características que tenía: {conflictos_no}\n"
                msg += "No modificaré la entrada existente."
                messagebox.showinfo("Conflicto de Conocimiento", msg)
            else:
                messagebox.showinfo("Animal Conocido", f"Ya conozco al '{nombre_animal_correcto}' y tus respuestas coinciden. ¡Quizás fallé en adivinar antes!")
            return False # No se aprendió nada nuevo en este caso

        # Crear nuevo animal
        nuevas_caracteristicas = set(self.caracteristicas_confirmadas) # Copia
        nuevas_caracteristicas.add(caracteristica_distintiva)
        nuevas_caracteristicas -= self.caracteristicas_negadas # Asegurar consistencia

        self.animales_caracteristicas[nombre_animal_correcto] = nuevas_caracteristicas
        self._guardar_conocimiento() # Guardar inmediatamente
        messagebox.showinfo("¡Aprendizaje Exitoso!", f"¡He aprendido sobre el '{nombre_animal_correcto}'!")
        return True


# --- Clase AnimalGuesserApp (Interfaz Gráfica Tkinter) ---
class AnimalGuesserApp:
    def __init__(self, master):
        self.master = master
        master.title("Adivinador de Animales")
        master.geometry("800x700") # Tamaño inicial
        master.iconbitmap("icono.ico")

        # Estilo (opcional, para botones más modernos)
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 16))
        style.configure("TLabel", padding=6, font=('Helvetica', 18))
        style.configure("Header.TLabel", font=('Helvetica', 20, 'bold'))

        # Instancia del sistema de inferencia
        self.sistema_inferencia = SistemaInferenciaAnimales()

        # --- Widgets ---

        # >>> WIDGET PARA LA IMAGEN <<<
        self.image_tk = None # Variable para mantener la referencia a la imagen
        self.image_label = None
        if True:
            try:
                image_path = "Capibara.png" # Asegúrate que este archivo exista
                img = Image.open(image_path)
                # Redimensionar imagen (ajusta el tamaño según necesites)
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                self.image_tk = ImageTk.PhotoImage(img) # Guardar referencia
                self.image_label = ttk.Label(master, image=self.image_tk)
                self.image_label.pack(pady=(10, 5)) # Espacio arriba y abajo
            except FileNotFoundError:
                messagebox.showwarning("Imagen no encontrada",
                                    f"No se encontró el archivo '{image_path}'.\n"
                                    "El programa funcionará sin la imagen.")
            except Exception as e:
                messagebox.showerror("Error de Imagen", f"No se pudo cargar la imagen: {e}")

        # Header (después de la imagen)
        self.header_label = ttk.Label(master, text="Adivinador de Animales", style="Header.TLabel")
        self.header_label.pack(pady=5)

        # Etiqueta de pregunta/estado
        # >>> MODIFICADO pack para centrar mejor <<<
        self.question_label = ttk.Label(master, text="Piensa en un animal y presiona 'Iniciar'.",
                                        wraplength=480, # Ajusta si es necesario
                                        justify="center") # Centra texto multilínea
        # Quitar fill=tk.X para que no se expanda horizontalmente y pueda centrarse
        self.question_label.pack(pady=15, padx=10)

        # --- Frames para botones y aprendizaje ---

        # Frame para botones de respuesta Si/No
        self.answer_frame = ttk.Frame(master)
        self.yes_button = ttk.Button(self.answer_frame, text="Sí", command=lambda: self.handle_answer(True), state=tk.DISABLED)
        self.no_button = ttk.Button(self.answer_frame, text="No", command=lambda: self.handle_answer(False), state=tk.DISABLED)
        self.yes_button.pack(side=tk.LEFT, padx=20, ipadx=10) # Añadido ipadx para más anchura
        self.no_button.pack(side=tk.RIGHT, padx=20, ipadx=10) # Añadido ipadx

        # Frame para botones de confirmación Correcto/Incorrecto
        self.confirm_frame = ttk.Frame(master)
        self.correct_button = ttk.Button(self.confirm_frame, text="¡Correcto!", command=lambda: self.handle_confirmation(True), state=tk.DISABLED)
        self.incorrect_button = ttk.Button(self.confirm_frame, text="Incorrecto", command=lambda: self.handle_confirmation(False), state=tk.DISABLED)
        self.correct_button.pack(side=tk.LEFT, padx=20)
        self.incorrect_button.pack(side=tk.RIGHT, padx=20)
        # confirm_frame se mostrará/ocultará

        # Frame para controles de inicio/reinicio
        self.control_frame = ttk.Frame(master)
        self.start_button = ttk.Button(self.control_frame, text="Iniciar Juego", command=self.start_game)
        self.start_button.pack(pady=10)
        self.control_frame.pack() # Siempre visible

        # Elementos de aprendizaje (inicialmente ocultos)
        self.learn_frame = ttk.Frame(master)
        self.learn_label = ttk.Label(self.learn_frame, text="Ayúdame a aprender:")
        self.animal_name_label = ttk.Label(self.learn_frame, text="Nombre del animal:")
        self.animal_name_entry = ttk.Entry(self.learn_frame, width=30)
        self.feature_label = ttk.Label(self.learn_frame, text="Característica distintiva (verdadera para tu animal):")
        self.feature_entry = ttk.Entry(self.learn_frame, width=40)
        self.submit_learn_button = ttk.Button(self.learn_frame, text="Enseñar al sistema", command=self.submit_learning)

        self.learn_label.grid(row=0, column=0, columnspan=2, pady=5)
        self.animal_name_label.grid(row=1, column=0, sticky=tk.W, padx=5)
        self.animal_name_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        self.feature_label.grid(row=2, column=0, sticky=tk.W, padx=5)
        self.feature_entry.grid(row=2, column=1, sticky=tk.EW, padx=5)
        self.submit_learn_button.grid(row=3, column=0, columnspan=2, pady=10)
        # learn_frame se mostrará/ocultará

        # Comprobar si la base de datos está vacía al inicio
        if self.sistema_inferencia.is_knowledge_base_empty():
            messagebox.showwarning("Base de Datos Vacía", "La base de conocimientos está vacía. El sistema necesita aprender al menos un animal para empezar.")
            # Podríamos forzar el modo aprendizaje aquí, pero es más simple pedir que se reinicie tras aprender.
            self.start_button.config(text="Aprender Primer Animal", command=self.setup_initial_learning)


    def setup_initial_learning(self):
        """Prepara la UI para aprender el primer animal si la BD está vacía."""
        self.question_label.config(text="La base de datos está vacía. Por favor, enseña el primer animal.")
        self.control_frame.pack_forget() # Ocultar botón de inicio normal
        self.show_learning_ui("Enséñame sobre el primer animal en el que piensas:")


    def start_game(self):
        """Inicia o reinicia una partida."""
        if self.sistema_inferencia.is_knowledge_base_empty():
            self.setup_initial_learning()
            return

        self.sistema_inferencia.reset_game_state()
        self.hide_all_frames() # Ocultar frames específicos
        self.control_frame.pack() # Asegurar que el de control esté
        self.start_button.config(text="Reiniciar Juego") # Cambiar texto

        self.enable_answer_buttons(True)
        self.enable_confirm_buttons(False)
        self.answer_frame.pack(pady=10) # Mostrar botones Si/No

        # Obtener la primera pregunta
        status, data = self.sistema_inferencia.get_next_question()
        self.process_status(status, data)


    def handle_answer(self, respuesta_si):
        """Procesa la respuesta 'Sí' o 'No' del usuario."""
        self.sistema_inferencia.process_answer(respuesta_si)
        # Obtener el siguiente estado/pregunta
        status, data = self.sistema_inferencia.get_next_question()
        self.process_status(status, data)

    def handle_confirmation(self, es_correcto):
        """Procesa si la adivinanza fue correcta o no."""
        self.enable_confirm_buttons(False)
        self.hide_all_frames()
        self.control_frame.pack() # Mostrar botón de reiniciar

        if es_correcto:
            self.question_label.config(text="¡Genial! ¡He adivinado! :)")
            messagebox.showinfo("¡Éxito!", "¡He adivinado tu animal!")
        else:
            # Preparar para aprender
            animal_incorrecto = self.sistema_inferencia.last_guess
            prompt = f"Vaya, fallé. Pensé que era '{animal_incorrecto.capitalize()}'.\n¿En qué animal estabas pensando?"
            self.show_learning_ui(prompt, animal_incorrecto)


    def process_status(self, status, data):
        """Actualiza la UI basado en el estado devuelto por sistema_inferencia."""

        if status == 'QUESTION':
            self.question_label.config(text=data)
            self.enable_answer_buttons(True)
        elif status == 'GUESS':
            self.question_label.config(text=f"¡Creo que es un... {data.capitalize()}!\n¿Es correcto?")
            self.enable_answer_buttons(False)
            self.enable_confirm_buttons(True)
            self.hide_all_frames() # Ocultar frames específicos
            self.confirm_frame.pack(pady=10) # Mostrar botones Correcto/Incorrecto
            self.control_frame.pack() # Mostrar Reiniciar
        elif status == 'NO_OPTIONS':
            self.question_label.config(text="Hmm, según tus respuestas, no coincide ningún animal que conozca.")
            self.enable_answer_buttons(False)
            self.hide_all_frames() # Ocultar frames específicos
            self.control_frame.pack() # Mostrar Reiniciar
            # Iniciar aprendizaje directamente
            self.show_learning_ui("Parece que no conozco ese animal o tus respuestas son contradictorias. ¿Cuál era?")
        elif status == 'LEARN_NO_QUESTIONS':
            posibles = data
            if len(posibles) > 1:
                guess = self.sistema_inferencia.last_guess # El que se eligió al azar
                self.question_label.config(text=f"No pude distinguirlo más.\nPodría ser: {', '.join(a.capitalize() for a in posibles)}.\nMe arriesgo... ¿Es un {guess.capitalize()}?")
                self.enable_answer_buttons(False)
                self.enable_confirm_buttons(True)
                self.hide_all_frames()
                self.confirm_frame.pack(pady=10)
                self.control_frame.pack()
            else: # Si solo queda uno (caso raro aquí), adivinarlo directamente
                self.process_status('GUESS', list(posibles)[0])


    def show_learning_ui(self, prompt, animal_incorrecto=None):
        """Muestra los controles para que el usuario enseñe un nuevo animal."""
        self.hide_all_frames()
        self.learn_label.config(text=prompt)
        self.animal_name_entry.delete(0, tk.END)
        self.feature_entry.delete(0, tk.END)

        # Preparar texto de ayuda para la característica
        feature_prompt = "Dame una característica VERDADERA para tu animal"
        animal_comparacion = animal_incorrecto or self.sistema_inferencia.last_guess # Usar el último adivinado si existe
        if animal_comparacion and animal_comparacion in self.sistema_inferencia.animales_caracteristicas:
            feature_prompt += f"\n(y preferiblemente FALSA para un '{animal_comparacion.capitalize()}')"
        else:
            feature_prompt += "\n(Ej: 'vive en el agua', 'tiene plumas')"

        self.feature_label.config(text=feature_prompt)

        self.learn_frame.pack(pady=10)
        self.control_frame.pack() # Mostrar botón Reiniciar también
        self.animal_name_entry.focus() # Poner foco en el primer campo


    def submit_learning(self):
        """Recoge los datos de aprendizaje y los envía al sistema de inferencia."""
        nombre_nuevo = self.animal_name_entry.get()
        caracteristica_nueva = self.feature_entry.get()

        if not nombre_nuevo or not caracteristica_nueva:
            messagebox.showwarning("Datos Incompletos", "Por favor, introduce el nombre del animal y una característica.")
            return

        aprendido = self.sistema_inferencia.aprender_nuevo_animal(nombre_nuevo, caracteristica_nueva)

        if aprendido:
            # Limpiar y volver al estado inicial para jugar de nuevo
            self.hide_all_frames()
            self.control_frame.pack()
            self.start_button.config(text="Jugar de Nuevo")
            self.question_label.config(text="¡Gracias por enseñarme! Presiona 'Jugar de Nuevo'.")
            # Asegurarse de que el botón de inicio funcione correctamente la próxima vez
            if self.start_button['text'] == "Aprender Primer Animal":
                self.start_button.config(text="Iniciar Juego", command=self.start_game)

        else:
            # Si no se aprendió (ej. conflicto, animal existente), mantener UI de aprendizaje?
            # O simplemente permitir reiniciar
            messagebox.showinfo("Aprendizaje", "Puedes intentar enseñar de nuevo o reiniciar el juego.")


    # --- Helpers para habilitar/deshabilitar y mostrar/ocultar ---
    def enable_answer_buttons(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.yes_button.config(state=state)
        self.no_button.config(state=state)

    def enable_confirm_buttons(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.correct_button.config(state=state)
        self.incorrect_button.config(state=state)

    def hide_all_frames(self):
        """Oculta los frames específicos de respuesta, confirmación y aprendizaje."""
        self.answer_frame.pack_forget()
        self.confirm_frame.pack_forget()
        self.learn_frame.pack_forget()


# --- Ejecución Principal ---
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#E8F5E9')
    app = AnimalGuesserApp(root)
    root.mainloop()