import pygame
import random
import sys
import os # Necesario para construir rutas de archivo

# --- Constantes del Juego ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (230, 230, 0) # Para el botón de recap

# --- Elementos del Juego ---
SOSPECHOSOS = ["Profesor Violeta", "Señorita Escarlata", "Coronel Mostaza", "Señora Celeste", "Señor Verde"]
LUGARES = ["Biblioteca", "Salón de Baile", "Conservatorio", "Cocina", "Estudio"]
ARMAS = ["Candelabro", "Daga", "Tubería de Plomo", "Llave Inglesa", "Cuerda"]
ESCENARIOS = [
    {"culpable": "Señorita Escarlata", "lugar": "Biblioteca", "arma": "Daga"},
    {"culpable": "Coronel Mostaza", "lugar": "Cocina", "arma": "Llave Inglesa"},
    {"culpable": "Profesor Violeta", "lugar": "Estudio", "arma": "Candelabro"},
    {"culpable": "Señora Celeste", "lugar": "Salón de Baile", "arma": "Cuerda"},
    {"culpable": "Señor Verde", "lugar": "Conservatorio", "arma": "Tubería de Plomo"}
]


IMAGE_DIR = "imagenes"

def obtener_pista(tipo, item_preguntado, escenario_actual, todas_las_pistas):
    """Función unificada para obtener y almacenar pistas."""
    pista_generada = []
    if tipo == "personaje":
        pista_generada = obtener_pista_personaje(item_preguntado, escenario_actual)
    elif tipo == "lugar":
        pista_generada = obtener_pista_lugar(item_preguntado, escenario_actual)
    elif tipo == "arma":
        pista_generada = obtener_pista_arma(item_preguntado, escenario_actual)

    if pista_generada:
        # Añadir un separador visual entre pistas en la recapitulación
        if todas_las_pistas: # Añadir solo si ya hay pistas previas
            todas_las_pistas.append("-" * 40)
        todas_las_pistas.extend(pista_generada) # Añadir las nuevas líneas
    return pista_generada # Devolver solo la pista actual para mostrarla

def obtener_pista_personaje(personaje_preguntado, escenario_actual):
    culpable = escenario_actual["culpable"]
    lugar_crimen = escenario_actual["lugar"]
    arma_crimen = escenario_actual["arma"]
    lugar_mencionado = random.choice([l for l in LUGARES if l != lugar_crimen])
    arma_mencionada = random.choice([a for a in ARMAS if a != arma_crimen])

    testimonio = f"{personaje_preguntado} dice que estuvo en {lugar_mencionado} y vio la {arma_mencionada}."
    verificacion = ""

    if personaje_preguntado == culpable:
        if random.random() < 0.6:
            lugar_mencionado = random.choice([l for l in LUGARES if l != lugar_crimen])
        else:
            arma_mencionada = random.choice([a for a in ARMAS if a != arma_crimen])
        testimonio = f"{personaje_preguntado} afirma haber estado en {lugar_mencionado} y quizás vio algo como una {arma_mencionada}."
        verificacion = f"Sin embargo, su coartada parece débil y nadie más lo/la vio allí en ese momento."
        if random.random() < 0.4:
            verificacion += f" Curiosamente, alguien mencionó haberlo/a visto cerca de la {lugar_crimen}."
    else:
        vio_arma_real = random.random() < 0.3
        estuvo_lugar_real = random.random() < 0.3
        if vio_arma_real:
            lugar_donde_vio_arma = random.choice([l for l in LUGARES if l != lugar_crimen])
            testimonio = f"{personaje_preguntado} recuerda haber estado en {lugar_mencionado}. Dice haber visto la {arma_crimen} en {lugar_donde_vio_arma}."
            verificacion = f"Se confirma que {personaje_preguntado} estuvo en {lugar_mencionado}. El arma ({arma_crimen}) fue vista por última vez en {lugar_donde_vio_arma} según los reportes."
        elif estuvo_lugar_real:
            arma_irrelevante = random.choice([a for a in ARMAS if a != arma_crimen])
            testimonio = f"{personaje_preguntado} pasó un tiempo en la {lugar_crimen}, pero dice no haber visto nada extraño, solo una {arma_irrelevante} fuera de lugar."
            verificacion = f"Hay testigos que ubican a {personaje_preguntado} en la {lugar_crimen}, pero su testimonio sobre el arma no coincide con otros."
        else:
            testimonio = f"{personaje_preguntado} jura que estuvo en {lugar_mencionado} toda la noche y vio la {arma_mencionada}."
            verificacion = f"Las notas indican que {personaje_preguntado} efectivamente estuvo en {lugar_mencionado}. La {arma_mencionada} fue encontrada allí."

    return [
        f"--- Testimonio de {personaje_preguntado} ---",
        testimonio,
        verificacion
    ]

def obtener_pista_lugar(lugar_preguntado, escenario_actual):
    culpable = escenario_actual["culpable"]
    lugar_crimen = escenario_actual["lugar"]
    arma_crimen = escenario_actual["arma"]
    testigo = random.choice([p for p in SOSPECHOSOS if p != culpable])
    arma_vista = random.choice(ARMAS)

    info = f"Alguien recuerda haber visto a {testigo} merodeando cerca de {lugar_preguntado}."
    detalle_arma = f"También se mencionó haber visto {arma_vista} por esa zona."

    if lugar_preguntado == lugar_crimen:
        info = f"Notas fragmentadas sugieren actividad sospechosa en {lugar_preguntado}."
        if random.random() < 0.5:
            info += f" Se susurra que {culpable} estuvo allí."
        else:
            info += f" Un invitado anónimo reportó ruidos extraños desde {lugar_preguntado}."
        if random.random() < 0.6:
            detalle_arma = f"Importante: ¡La {arma_crimen} fue vista cerca de {lugar_preguntado} poco antes del incidente!"
        else:
            detalle_arma = f"Se encontró una {random.choice([a for a in ARMAS if a != arma_crimen])} abandonada cerca, pero podría ser una distracción."

    return [
        f"--- Investigación en {lugar_preguntado} ---",
        info,
        detalle_arma
    ]

def obtener_pista_arma(arma_preguntada, escenario_actual):
    culpable = escenario_actual["culpable"]
    lugar_crimen = escenario_actual["lugar"]
    arma_crimen = escenario_actual["arma"]
    personaje_asociado = random.choice(SOSPECHOSOS)
    lugar_asociado = random.choice(LUGARES)

    info = f"Según un testimonio, {personaje_asociado} fue visto/a manipulando la {arma_preguntada} en {lugar_asociado} más temprano."
    veracidad = "Este testimonio aún no ha sido corroborado."

    if arma_preguntada == arma_crimen:
        info = f"¡Atención! La {arma_preguntada} es considerada un objeto de interés."
        if random.random() < 0.5:
            lugar_donde_se_vio = random.choice([l for l in LUGARES if l != lugar_crimen])
            veracidad = f"Se sabe que {culpable} tuvo acceso a ella recientemente. Fue vista por última vez en {lugar_donde_se_vio}."
        else:
            veracidad = f"Fue encontrada cerca de la {lugar_crimen}, aunque limpiada de huellas."
            if random.random() < 0.3:
                inocente_implicado = random.choice([p for p in SOSPECHOSOS if p != culpable])
                veracidad += f" Curiosamente, las huellas parciales podrían coincidir con las de {inocente_implicado}."

    return [
        f"--- Información sobre {arma_preguntada} ---",
        info,
        veracidad
    ]

# --- Funciones Auxiliares de Pygame ---
# draw_text, create_button, draw_button 
def draw_text(surface, text, font, color, rect, aa=True, bkg=None):
    """Dibuja texto en una superficie, con opción de centrado y salto de línea."""
    y = rect.top
    line_spacing = -2 # Ajusta el espacio entre líneas

    # Obtener altura de fuente
    font_height = font.size("Tg")[1]

    lines = text.split('\n') # Manejar saltos de línea explícitos

    for line in lines:
        while line:
            i = 1
            # Determinar si la línea actual cabe en el rectángulo
            if y + font_height > rect.bottom:
                 # No caben más líneas en el rect actual
                 return # Detener el dibujo si no cabe

            # Determinar cuánto texto cabe en una línea
            while font.size(line[:i])[0] < rect.width and i < len(line):
                i += 1

            # Si nos pasamos en ancho, buscamos el último espacio
            if font.size(line[:i])[0] >= rect.width:
                i = line.rfind(" ", 0, i) + 1
                if i == 0: # Si una sola palabra es demasiado larga
                     i = len(line) # Forzar el dibujo

            # Renderizar la línea o trozo de línea
            image = font.render(line[:i].rstrip(), aa, color) # Usar rstrip

            surface.blit(image, (rect.left, y))
            y += font_height + line_spacing

            # Eliminar el texto renderizado de la línea actual
            line = line[i:]

    return # Todo el texto fue dibujado

def create_button(text, rect_coords, inactive_color=GRAY, active_color=DARK_GRAY):
    """Crea un diccionario representando un botón."""
    return {
        "text": text,
        "rect": pygame.Rect(rect_coords), # (left, top, width, height)
        "inactive_color": inactive_color,
        "active_color": active_color,
        "current_color": inactive_color # Color actual para hover
    }

def draw_button(surface, font, button):
    """Dibuja un botón y actualiza su color si el ratón está encima."""
    mouse_pos = pygame.mouse.get_pos()

    # Actualizar color basado en hover
    if button['rect'].collidepoint(mouse_pos):
        button['current_color'] = button['active_color']
    else:
        button['current_color'] = button['inactive_color']

    pygame.draw.rect(surface, button['current_color'], button['rect'])
    # Dibuja el texto centrado en el botón
    text_surf = font.render(button['text'], True, BLACK)
    text_rect = text_surf.get_rect(center=button['rect'].center)
    surface.blit(text_surf, text_rect)

# --- Función para Cargar Imágenes ---
def load_images(item_list, subfolder, filename_formatter=lambda x: x.replace(" ", "_") + ".png"):
    """Intenta cargar imágenes para una lista de items desde una subcarpeta."""
    images = {}
    base_path = os.path.join(IMAGE_DIR, subfolder) # Ruta a la subcarpeta específica
    if not os.path.isdir(base_path):
        print(f"Advertencia: Carpeta de imágenes no encontrada: {base_path}")
        # Es seguro continuar, simplemente no se cargarán imágenes de esta categoría.
        return images # Retorna diccionario vacío si la carpeta no existe

    print(f"Buscando imágenes en: {base_path}") # Mensaje útil para depuración

    for item in item_list:
        filename = filename_formatter(item)
        path = os.path.join(base_path, filename)
        try:
            # print(f"Intentando cargar: {path}") # Descomentar para depuración detallada
            # Cargar imagen y convertirla para optimizar el dibujado
            image = pygame.image.load(path).convert_alpha()
            images[item] = image
            # print(f"Imagen cargada: {path}") # Descomentar para depuración detallada
        except FileNotFoundError:
            print(f"Info: Archivo no encontrado para '{item}' en {path}. Se usará texto.")
            pass
        except pygame.error as e:
            print(f"Advertencia: Error de Pygame al cargar imagen para '{item}' en {path}: {e}")
            pass # Continúa con el siguiente item
        except Exception as e:
             # Atrapa cualquier otro error inesperado durante la carga
             print(f"Advertencia: Error inesperado al cargar imagen para '{item}' en {path}: {e}")
             pass

    return images

# --- Función Principal del Juego ---
def game_loop():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Misterio en la Mansión Blackwood")
    clock = pygame.time.Clock()
    font_titulo = pygame.font.Font(None, 48)
    font_subtitulo = pygame.font.Font(None, 36)
    font_normal = pygame.font.Font(None, 28)
    font_boton = pygame.font.Font(None, 32)
    font_recap = pygame.font.Font(None, 24) # Fuente más pequeña para recapitulación

    # --- Cargar Imágenes Opcionales ---
    # Asegúrate de que la carpeta IMAGE_DIR ('imagenes') exista
    # y dentro de ella, subcarpetas 'sospechosos', 'lugares', 'armas'.
    # Los nombres deben coincidir (ej. 'Profesor_Violeta.png')
    suspect_images = load_images(SOSPECHOSOS, "sospechosos")
    location_images = load_images(LUGARES, "lugares")
    weapon_images = load_images(ARMAS, "armas")
    # Tamaño deseado para mostrar las imágenes (ajusta según tus imágenes)
    IMAGE_DISPLAY_SIZE = (200, 200) # Ancho, Alto


    # --- Variables del estado del juego ---
    def reset_game():
        """Función para reiniciar las variables del juego."""
        nonlocal game_state, escenario_actual, consultas_restantes, todas_las_pistas, pista_actual_mostrada, acusacion, resultado_final, previous_accuse_state
        game_state = "INTRO" # Estados: INTRO, INFO_DISPLAY, CHOOSE_ACTION, CHOOSE_SUSPECT, CHOOSE_PLACE, CHOOSE_WEAPON, SHOW_CLUE, ACCUSE_SUSPECT, ACCUSE_PLACE, ACCUSE_WEAPON, SHOW_RECAP, REVEAL, GAME_OVER
        escenario_actual = random.choice(ESCENARIOS)
        consultas_restantes = 5
        todas_las_pistas = [] # Lista para acumular TODAS las pistas
        pista_actual_mostrada = [] # Para la pista que se muestra actualmente
        acusacion = {"culpable": None, "lugar": None, "arma": None}
        resultado_final = ""
        previous_accuse_state = None # Para saber a dónde volver desde el recap

    # Inicializar variables del juego
    game_state = ""
    escenario_actual = {}
    consultas_restantes = 0
    todas_las_pistas = []
    pista_actual_mostrada = []
    acusacion = {}
    resultado_final = ""
    previous_accuse_state = ""
    reset_game() # Llama a la función para establecer valores iniciales

    # --- Crear Botones ---
    button_ask_person = create_button("Preguntar por Personaje", (50, 200, 300, 50))
    button_ask_place = create_button("Investigar Habitación", (50, 270, 300, 50))
    button_ask_weapon = create_button("Indagar sobre Arma", (50, 340, 300, 50))
    item_buttons = [] # Se generan dinámicamente
    button_continue = create_button("Continuar", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50)) # Un poco más arriba
    button_play_again = create_button("Jugar Otra Vez", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, 300, 50))
    # Botón de Recapitulación
    button_recap = create_button("Ver Pistas", (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70, 150, 50), YELLOW, DARK_GRAY)
    # Botón para volver del Recap
    button_back_to_accuse = create_button("Volver a Acusar", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 70, 300, 50))


    running = True
    while running:
        mouse_clicked = False
        mouse_pos = (0, 0)
        # --- 1. Manejo de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clic izquierdo
                    mouse_pos = event.pos
                    mouse_clicked = True

        # --- 2. Actualizar Estado ---
        if mouse_clicked:
            if game_state == "INTRO":
                game_state = "INFO_DISPLAY"
                pygame.time.wait(150)
            elif game_state == "INFO_DISPLAY":
                 if button_continue['rect'].collidepoint(mouse_pos):
                     game_state = "CHOOSE_ACTION"
                     pygame.time.wait(150)

            elif game_state == "CHOOSE_ACTION":
                if button_ask_person['rect'].collidepoint(mouse_pos):
                    game_state = "CHOOSE_SUSPECT"
                elif button_ask_place['rect'].collidepoint(mouse_pos):
                    game_state = "CHOOSE_PLACE"
                elif button_ask_weapon['rect'].collidepoint(mouse_pos):
                    game_state = "CHOOSE_WEAPON"
                pygame.time.wait(150)

            elif game_state in ["CHOOSE_SUSPECT", "CHOOSE_PLACE", "CHOOSE_WEAPON"]:
                 item_list = []
                 tipo_pista = ""
                 if game_state == "CHOOSE_SUSPECT": item_list, tipo_pista = SOSPECHOSOS, "personaje"
                 elif game_state == "CHOOSE_PLACE": item_list, tipo_pista = LUGARES, "lugar"
                 elif game_state == "CHOOSE_WEAPON": item_list, tipo_pista = ARMAS, "arma"

                 for i, btn in enumerate(item_buttons):
                     if btn['rect'].collidepoint(mouse_pos):
                         selected_item = item_list[i]
                         # Obtener y guardar la pista actual
                         pista_actual_mostrada = obtener_pista(tipo_pista, selected_item, escenario_actual, todas_las_pistas)
                         consultas_restantes -= 1
                         game_state = "SHOW_CLUE"
                         pygame.time.wait(150)
                         break

            elif game_state == "SHOW_CLUE":
                 if button_continue['rect'].collidepoint(mouse_pos):
                     if consultas_restantes > 0:
                         game_state = "CHOOSE_ACTION"
                     else:
                         game_state = "ACCUSE_SUSPECT" # Iniciar acusación
                     pygame.time.wait(150)

            elif game_state in ["ACCUSE_SUSPECT", "ACCUSE_PLACE", "ACCUSE_WEAPON"]:
                # Primero, verificar clic en botón de Recapitulación
                if button_recap['rect'].collidepoint(mouse_pos):
                    previous_accuse_state = game_state # Guardar de dónde venimos
                    game_state = "SHOW_RECAP"
                    pygame.time.wait(150)
                else:
                    # Si no es recap, verificar clic en items de acusación
                    item_list = []
                    next_state = ""
                    if game_state == "ACCUSE_SUSPECT": item_list, next_state = SOSPECHOSOS, "ACCUSE_PLACE"
                    elif game_state == "ACCUSE_PLACE": item_list, next_state = LUGARES, "ACCUSE_WEAPON"
                    elif game_state == "ACCUSE_WEAPON": item_list, next_state = ARMAS, "REVEAL"

                    for i, btn in enumerate(item_buttons):
                         if btn['rect'].collidepoint(mouse_pos):
                             selected_item = item_list[i]
                             if game_state == "ACCUSE_SUSPECT": acusacion["culpable"] = selected_item
                             elif game_state == "ACCUSE_PLACE": acusacion["lugar"] = selected_item
                             elif game_state == "ACCUSE_WEAPON": acusacion["arma"] = selected_item

                             game_state = next_state
                             pygame.time.wait(150)
                             break # Salir del bucle de botones de item

            elif game_state == "SHOW_RECAP":
                if button_back_to_accuse['rect'].collidepoint(mouse_pos):
                    if previous_accuse_state: # Asegurarse de que hay un estado previo
                        game_state = previous_accuse_state # Volver
                    else:
                        game_state = "ACCUSE_SUSPECT" #Fallback por si acaso
                    pygame.time.wait(150)

            elif game_state == "REVEAL":
                # Ya no hay clics aquí, la transición a GAME_OVER es automática
                pass

            elif game_state == "GAME_OVER":
                 if button_play_again['rect'].collidepoint(mouse_pos):
                     reset_game() # Reiniciar todas las variables
                     pygame.time.wait(200)

        # --- 3. Dibujar en Pantalla ---
        screen.fill(WHITE)

        if game_state == "INTRO":
            intro_text = [
                "MISTERIO EN LA MANSIÓN BLACKWOOD", "",
                "¡Han encontrado sin vida al Dr. Samuel Blackwood!",
                "Uno de los invitados es el culpable.",
                "Tienes 5 consultas para investigar.", "",
                "Haz clic para comenzar..."
            ]
            y_offset = 100
            for line in intro_text:
                is_title = "MANSIÓN BLACKWOOD" in line
                current_font = font_titulo if is_title else font_normal
                draw_text(screen, line, current_font, BLACK, pygame.Rect(50, y_offset, SCREEN_WIDTH - 100, 50))
                y_offset += 40 if line else 60

        elif game_state == "INFO_DISPLAY":
            draw_text(screen, "Información del Caso:", font_titulo, BLACK, pygame.Rect(50, 30, SCREEN_WIDTH - 100, 50))
            col_width = SCREEN_WIDTH // 3 - 30
            col1_x = 50
            col2_x = col1_x + col_width + 15
            col3_x = col2_x + col_width + 15
            list_y_start = 100
            line_height = 30
            # Sospechosos
            draw_text(screen, "Sospechosos:", font_subtitulo, BLUE, pygame.Rect(col1_x, list_y_start, col_width, 40))
            y_offset = list_y_start + 40
            for i, p in enumerate(SOSPECHOSOS):
                draw_text(screen, f"{i+1}. {p}", font_normal, BLACK, pygame.Rect(col1_x, y_offset, col_width, line_height))
                y_offset += line_height
            # Lugares
            draw_text(screen, "Lugares:", font_subtitulo, BLUE, pygame.Rect(col2_x, list_y_start, col_width, 40))
            y_offset = list_y_start + 40
            for i, l in enumerate(LUGARES):
                draw_text(screen, f"{i+1}. {l}", font_normal, BLACK, pygame.Rect(col2_x, y_offset, col_width, line_height))
                y_offset += line_height
            # Armas
            draw_text(screen, "Armas:", font_subtitulo, BLUE, pygame.Rect(col3_x, list_y_start, col_width, 40))
            y_offset = list_y_start + 40
            for i, a in enumerate(ARMAS):
                draw_text(screen, f"{i+1}. {a}", font_normal, BLACK, pygame.Rect(col3_x, y_offset, col_width, line_height))
                y_offset += line_height
            draw_button(screen, font_boton, button_continue)


        elif game_state == "CHOOSE_ACTION":
            draw_text(screen, f"Consultas restantes: {consultas_restantes}", font_normal, BLACK, pygame.Rect(50, 50, SCREEN_WIDTH - 100, 30))
            draw_text(screen, "¿Qué quieres investigar?", font_titulo, BLACK, pygame.Rect(50, 120, SCREEN_WIDTH - 100, 50))
            draw_button(screen, font_boton, button_ask_person)
            draw_button(screen, font_boton, button_ask_place)
            draw_button(screen, font_boton, button_ask_weapon)

        elif game_state in ["CHOOSE_SUSPECT", "CHOOSE_PLACE", "CHOOSE_WEAPON", "ACCUSE_SUSPECT", "ACCUSE_PLACE", "ACCUSE_WEAPON"]:
             item_list = []
             prompt = ""
             image_dict = {} # Diccionario de imágenes relevante para este estado
             is_accusing = "ACCUSE" in game_state

             if game_state == "CHOOSE_SUSPECT" or game_state == "ACCUSE_SUSPECT":
                 item_list, image_dict = SOSPECHOSOS, suspect_images
                 prompt = "¿Sobre quién preguntar?" if not is_accusing else "ACUSACIÓN: ¿Quién es el culpable?"
             elif game_state == "CHOOSE_PLACE" or game_state == "ACCUSE_PLACE":
                 item_list, image_dict = LUGARES, location_images
                 prompt = "¿Qué habitación investigar?" if not is_accusing else "ACUSACIÓN: ¿Dónde ocurrió?"
             elif game_state == "CHOOSE_WEAPON" or game_state == "ACCUSE_WEAPON":
                 item_list, image_dict = ARMAS, weapon_images
                 prompt = "¿Sobre qué arma indagar?" if not is_accusing else "ACUSACIÓN: ¿Con qué arma?"

             draw_text(screen, prompt, font_titulo, BLACK, pygame.Rect(50, 50, SCREEN_WIDTH - 100, 50))

             # Crear/Actualizar y dibujar botones (o imágenes)
             item_buttons = []
             start_y = 120
             max_items_per_row = 3 # Cuántos items/imágenes caben en una fila
             current_col = 0
             current_row = 0
             item_width = IMAGE_DISPLAY_SIZE[0] + 20 # Ancho imagen + padding
             item_height = IMAGE_DISPLAY_SIZE[1] + 40 # Alto imagen + espacio para texto debajo
             row_width = max_items_per_row * item_width
             start_x = (SCREEN_WIDTH - row_width) // 2 # Centrar la fila

             for item in item_list:
                 item_x = start_x + (current_col * item_width)
                 item_y = start_y + (current_row * item_height)

                 # Crear el rectángulo del botón/área clickeable
                 btn_rect = pygame.Rect(item_x, item_y, IMAGE_DISPLAY_SIZE[0] + 10, IMAGE_DISPLAY_SIZE[1] + 30) # Ajustar tamaño rect
                 btn = create_button("", btn_rect) # Botón sin texto por defecto
                 item_buttons.append(btn)

                 # Comprobar si hay imagen
                 if item in image_dict:
                     try:
                         # Escalar imagen si es necesario (opcional, mejor prepararlas)
                         scaled_image = pygame.transform.smoothscale(image_dict[item], IMAGE_DISPLAY_SIZE)
                         screen.blit(scaled_image, (item_x + 5, item_y + 5)) # Dibujar imagen con padding
                         # Dibujar texto debajo de la imagen
                         draw_text(screen, item, font_recap, BLACK, pygame.Rect(item_x, item_y + IMAGE_DISPLAY_SIZE[1] + 10, IMAGE_DISPLAY_SIZE[0] + 10, 20))
                     except Exception as e:
                         print(f"Error al escalar/dibujar imagen {item}: {e}")
                         # Fallback a botón de texto si falla el dibujado de imagen
                         btn['text'] = item # Añadir texto al botón
                         draw_button(screen, font_boton, btn)
                 else:
                     # Si no hay imagen, dibujar botón con texto normal
                     btn['text'] = item # Añadir texto al botón
                     # Ajustar tamaño si es solo texto? Por ahora usamos el mismo rect
                     draw_button(screen, font_boton, btn)

                 current_col += 1
                 if current_col >= max_items_per_row:
                     current_col = 0
                     current_row += 1

             # Dibujar botón de Recapitulación SOLO durante la acusación
             if is_accusing:
                 draw_button(screen, font_boton, button_recap)


        elif game_state == "SHOW_CLUE":
             # ... (código de dibujo sin cambios, usa pista_actual_mostrada) ...
             y_offset = 100
             text_rect = pygame.Rect(50, y_offset, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 250) # Área para texto de pista
             full_text = "\n".join(pista_actual_mostrada)
             draw_text(screen, full_text, font_normal, BLACK, text_rect)
             draw_button(screen, font_boton, button_continue) # Botón para salir de la pista

        elif game_state == "SHOW_RECAP":
            draw_text(screen, "Recapitulación de Pistas:", font_titulo, BLACK, pygame.Rect(50, 30, SCREEN_WIDTH - 100, 50))
            # Área para mostrar las pistas (podría necesitar scroll para muchas pistas)
            recap_rect = pygame.Rect(50, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200)
            pygame.draw.rect(screen, GRAY, recap_rect, 1) # Borde opcional
            full_recap_text = "\n".join(todas_las_pistas)
            draw_text(screen, full_recap_text, font_recap, BLACK, recap_rect.inflate(-20, -20)) # Padding
            # Dibujar botón para volver
            draw_button(screen, font_boton, button_back_to_accuse)


        elif game_state == "REVEAL":
            # ... (código de dibujo sin cambios, cálculo y pausa) ...
            if not resultado_final: # Calcular solo una vez
                 if (acusacion["culpable"] == escenario_actual["culpable"] and
                     acusacion["lugar"] == escenario_actual["lugar"] and
                     acusacion["arma"] == escenario_actual["arma"]):
                     resultado_final = [
                         "¡¡¡FELICIDADES, DETECTIVE!!!", "",
                         "Has descubierto la verdad:",
                         f"Fue {escenario_actual['culpable']} en {escenario_actual['lugar']} con {escenario_actual['arma']}.",
                         "¡Caso resuelto!"
                     ]
                 else:
                     resultado_final = [
                         "¡Oh no! Tu acusación es incorrecta.", "",
                         f"Tu acusación: {acusacion['culpable']} en {acusacion['lugar']} con {acusacion['arma']}", "",
                         "La verdad era:",
                         f"Culpable: {escenario_actual['culpable']}",
                         f"Lugar:    {escenario_actual['lugar']}",
                         f"Arma:     {escenario_actual['arma']}", "",
                         "El verdadero culpable ha escapado..."
                     ]
                 # Dibujar el texto calculado inmediatamente
                 y_offset = 100
                 for line in resultado_final:
                    is_title = "FELICIDADES" in line or "Oh no" in line
                    current_font = font_titulo if is_title else font_normal
                    color = GREEN if "FELICIDADES" in resultado_final[0] else RED if "Oh no" in resultado_final[0] else BLACK
                    draw_text(screen, line, current_font, color, pygame.Rect(50, y_offset, SCREEN_WIDTH - 100, 50))
                    y_offset += 40 if line else 50

                 pygame.display.flip() # Mostrar el resultado inmediatamente
                 pygame.time.wait(3000) # Pausa dramática
                 game_state = "GAME_OVER" # Cambiar estado


        elif game_state == "GAME_OVER":
            # ... (código de dibujo sin cambios, muestra resultado y botón de reinicio) ...
            y_offset = 100
            for line in resultado_final:
               is_title = "FELICIDADES" in line or "Oh no" in line
               current_font = font_titulo if is_title else font_normal
               color = GREEN if "FELICIDADES" in resultado_final[0] else RED if "Oh no" in resultado_final[0] else BLACK
               draw_text(screen, line, current_font, color, pygame.Rect(50, y_offset, SCREEN_WIDTH - 100, 50))
               y_offset += 40 if line else 50
            draw_button(screen, font_boton, button_play_again)

        # --- Actualizar Pantalla ---
        if game_state != "REVEAL": # Evitar doble flip
             pygame.display.flip()

        # --- Controlar FPS ---
        clock.tick(30)

    pygame.quit()
    sys.exit()

# --- Bucle Principal del Programa ---
if __name__ == "__main__":
    game_loop()