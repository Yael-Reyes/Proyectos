import tkinter as tk
import json
import os
import pygame

class AnimalGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🦁 Adivina el Animal 🐯")
        self.root.geometry("800x800")
        self.root.minsize(800, 800)
        self.root.iconbitmap("icono.ico")

        # Cargar la base de datos
        self.datos = self.cargar_base_datos()
        self.current_question = 0
        self.respuestas = []

        # Esquema de colores
        self.colors = {
            'primary': '#2E7D32',
            'secondary': '#1565C0',
            'background': '#E8F5E9',
            'button_bg': '#4CAF50',
            'button_hover': '#388E3C',
            'error': '#D32F2F',
            'success': '#2E7D32'
        }

        # Configurar el color de fondo de la ventana
        self.root.configure(bg=self.colors['background'])

        # Marco del título
        self.title_frame = tk.Frame(root, bg=self.colors['background'])
        self.title_frame.pack(fill='x', padx=20, pady=10)

        self.title_label = tk.Label(
            self.title_frame,
            text="🎮 Juego de Adivinanzas de Animales 🎮",
            font=('Helvetica', 24, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        self.title_label.pack()

        # Marco y lienzo para la imagen del capibara
        self.canvas_frame = tk.Frame(root, bg=self.colors['background'])
        self.canvas_frame.pack(fill='x', padx=20, pady=10)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=300,
            height=200,
            bg=self.colors['background'],
            highlightthickness=0
        )
        self.canvas.pack()

        # Cargar y mostrar la imagen del capibara
        try:
            self.capybara_image = tk.PhotoImage(file="Capibara.png")
            # Redimensionar imagen
            self.capybara_image = self.capybara_image.subsample(2, 2)  # Adjust the division factors as needed
            self.canvas.create_image(150, 100, image=self.capybara_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Si la imagen no carga, mostrar una representación alternativa
            self.canvas.create_oval(30, 10, 130, 150, fill='brown', outline='black')
            self.canvas.create_text(150, 100, text='🦫', font=('Arial', 40))

        # Botón para iniciar el juego
        self.start_button = tk.Button(
            self.canvas_frame,
            text="¡Empezar a Jugar! 🎮",
            command=self.start_game,
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['button_bg'],
            fg='white',
            relief='raised',
            cursor='hand2'
        )
        self.start_button.pack(pady=10)

        # Marco principal con borde y efecto de sombra
        self.main_frame = tk.Frame(
            root,
            bg=self.colors['background'],
            highlightbackground=self.colors['primary'],
            highlightthickness=2,
            relief='ridge'
        )
        self.main_frame.pack(expand=True, fill='both', padx=40, pady=20)

        # Marco secundario con efecto de profundidad
        self.secondary_frame = tk.Frame(
            self.main_frame,
            bg='white',
            relief='groove',
            bd=5
        )
        self.secondary_frame.pack(expand=True, fill='both', padx=30, pady=30)

        # Label para mostrar mensajes
        self.message_label = tk.Label(
            self.main_frame,
            text="",
            fg=self.colors['error'],
            font=('Helvetica', 14),
            bg=self.colors['background'],
            wraplength=600
        )
        self.message_label.pack(pady=15)

        # Label de pregunta con estilo mejorado
        self.question_label = tk.Label(
            self.secondary_frame,
            text="¡Bienvenido al Juego de Adivinanzas de Animales!",
            wraplength=500,
            font=('Helvetica', 16, 'bold'),
            bg='white',
            fg=self.colors['secondary']
        )
        self.question_label.pack(pady=30)

        # Frame para los botones con estilo mejorado
        self.button_frame = tk.Frame(self.secondary_frame, bg='white')
        self.button_frame.pack(pady=20)

        # Estilo común para botones
        button_style = {
            'width': 15,
            'height': 2,
            'font': ('Helvetica', 12, 'bold'),
            'relief': 'raised',
            'bd': 2
        }

        # Botón "Sí"
        self.yes_button = tk.Button(
            self.button_frame,
            text="✅ Sí",
            command=lambda: self.process_answer("si"),
            bg=self.colors['button_bg'],
            fg='white',
            cursor='hand2',
            **button_style
        )
        self.yes_button.pack(side=tk.LEFT, padx=20)

        # Botón "No"
        self.no_button = tk.Button(
            self.button_frame,
            text="❌ No",
            command=lambda: self.process_answer("no"),
            bg=self.colors['error'],
            fg='white',
            cursor='hand2',
            **button_style
        )
        self.no_button.pack(side=tk.LEFT, padx=20)

        # Configurar eventos hover para los botones
        for button in (self.yes_button, self.no_button):
            button.bind('<Enter>', lambda e, b=button: b.config(relief='sunken'))
            button.bind('<Leave>', lambda e, b=button: b.config(relief='raised'))

        # Deshabilitar los botones hasta que el juego inicie
        self.disable_game_buttons()

    # Cargar la base de datos con las preguntas y animales
    def cargar_base_datos(self):
        if os.path.exists("lista.json"):
            with open("lista.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {"preguntas": [], "animales": {}}
    
    # Guardar base de datos
    def guardar_base_datos(self):
        with open("lista.json", "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=2)

    # Iniciar el juego
    def start_game(self):
        if not self.datos["preguntas"]:
            self.message_label.config(text="Error: No hay preguntas en la base de datos")
            return
        self.current_question = 0
        self.respuestas = []
        self.message_label.config(text="")  # Limpiar mensajes previos
        self.enable_game_buttons() #Enable buttons at the start
        self.start_button.pack_forget()  # Hide start button
        self.show_question()
        self.continue_button.pack_forget()
        self.not_this_animal.pack_forget()

    # Mostrar la siguiente pregunta
    def show_question(self):
        if self.current_question < len(self.datos["preguntas"]):
            question_text = self.datos["preguntas"][self.current_question]
            self.question_label.config(text=question_text)

    # Procesar la respuesta del usuario
    def process_answer(self, answer):
        self.respuestas.append(1 if answer == "si" else 0)
        self.current_question += 1

        if self.current_question < len(self.datos["preguntas"]):
            self.show_question()
        else:
            self.check_animal()

    def check_animal(self):
        animales = self.encontrar_coincidencia()
        if animales:
            self.disable_game_buttons()
            if len(animales) == 1:
                mensaje = f"¡Tu animal es un {animales[0]}!"

            else:
                mensaje = f"Podría ser uno de estos animales: {', '.join(animales)}\n¿Cuál de ellos era?"

            self.message_label.config(text=mensaje, fg="green")

            # Frame for result buttons
            self.result_buttons = tk.Frame(self.main_frame, bg=self.colors['background'])
            self.result_buttons.pack(pady=5)

            # Continue button
            self.continue_button = tk.Button(
                self.result_buttons,
                text="¡Sí, es correcto!",
                command=self.start_game,
                font=('Arial', 10),
                bg='#2196F3',
                fg='white'
            )
            self.continue_button.pack(side=tk.LEFT, padx=5)

            # Not this animal button
            self.not_this_animal = tk.Button(
                self.result_buttons,
                text="No es este animal",
                command=self.ask_new_animal,
                font=('Arial', 10),
                bg='#f44336',
                fg='white'
            )
            self.not_this_animal.pack(side=tk.LEFT, padx=5)
        else:
            self.ask_new_animal()

    # Buscar coincidencias en la base de datos
    def encontrar_coincidencia(self):
        matches = []
        for animal, caracteristicas in self.datos["animales"].items():
            if caracteristicas == self.respuestas:
                matches.append(animal)
        return matches

    def ask_new_animal(self):
        self.disable_game_buttons()
        self.message_label.config(text="No encontré el animal. ¿En qué animal estabas pensando?", fg="black")

        # Entry para escribir el nuevo animal
        self.entry_animal = tk.Entry(self.main_frame, font=('Arial', 12))
        self.entry_animal.pack(pady=5)

        # Frame para botones
        self.new_animal_buttons = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.new_animal_buttons.pack(pady=5)

        # Botón para confirmar
        self.confirm_button = tk.Button(
            self.new_animal_buttons,
            text="Guardar Animal",
            command=self.save_new_animal,
            font=('Arial', 10),
            bg='#2196F3',
            fg='white'
        )
        self.confirm_button.pack(side=tk.LEFT, padx=5)

        # Botón para cancelar
        self.cancel_button = tk.Button(
            self.new_animal_buttons,
            text="Cancelar",
            command=self.cancel_new_animal,
            font=('Arial', 10),
            bg='#f44336',
            fg='white'
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    # Deshabilitar los botones del juego
    def disable_game_buttons(self):
        self.yes_button.config(state='disabled')
        self.no_button.config(state='disabled')

    # Habilitar los botones del juego
    def enable_game_buttons(self):
        self.yes_button.config(state='normal')
        self.no_button.config(state='normal')

    def clean_up_new_animal_ui(self):
        if hasattr(self, 'entry_animal'):
            self.entry_animal.destroy()
        if hasattr(self, 'new_animal_buttons'):
            self.new_animal_buttons.destroy()
        if hasattr(self, 'result_buttons'):
            self.result_buttons.destroy()
        self.enable_game_buttons() #Re-enable game buttons after cleanup

    def cancel_new_animal(self):
        self.clean_up_new_animal_ui()
        self.message_label.config(text="Operación cancelada", fg="red")
        self.root.after(1000,self.start_game)

    def save_new_animal(self):
        nuevo_animal = self.entry_animal.get().strip()

        if nuevo_animal:
            if nuevo_animal in self.datos["animales"]:
                self.message_label.config(text="Ese animal ya está registrado.", fg="red")
            else:
                self.datos["animales"][nuevo_animal] = self.respuestas
                self.guardar_base_datos()
                self.message_label.config(text=f"¡Ahora conozco a {nuevo_animal}!", fg="green")

        self.root.after(1000,self.clean_up_new_animal_ui)
        self.root.after(1000,self.start_game)

# Función principal
def main():
    root = tk.Tk()
    app = AnimalGuessingGame(root)
    root.mainloop()

if __name__ == "__main__":

    # pygame.mixer.init()  # Inicializa el módulo de sonido
    # pygame.mixer.music.load("musica.mp3")  # Carga el archivo de música
    # pygame.mixer.music.play(-1)  # Reproduce en bucle (-1 significa infinito)

    main()