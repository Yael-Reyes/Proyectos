import json
import os
import random
import difflib

# Cargar la base de datos desde un archivo JSON si existe, o crear una nueva
DB_FILE = "chatbot_data.json"

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as file:
        knowledge_base = json.load(file)
else:
    knowledge_base = {
        "intents": [
            {
                "tag": "hola",
                "responses": ["¡Hola!", "Buenos días!", "¿Cómo estás?"]
            },
            {
                "tag": "nombre",
                "responses": ["Soy un chatbot en desarrollo."]
            }
        ]
    }


def get_response(user_input):
    tags = [intent["tag"] for intent in knowledge_base["intents"]]
    closest_match = difflib.get_close_matches(user_input.lower(), tags, n=1, cutoff=0.5)

    if closest_match:
        for intent in knowledge_base["intents"]:
            if intent["tag"] == closest_match[0]:
                return random.choice(intent["responses"])

    new_response = input("No sé la respuesta. ¿Qué debería responder? ")
    knowledge_base["intents"].append({
        "tag": user_input.lower(),
        "responses": [new_response]
    })

    with open(DB_FILE, "w") as file:
        json.dump(knowledge_base, file, indent=4)

    return "Gracias por enseñarme. Ahora lo recordaré."


def run_chatbot():
    print("Hola, soy tu chatbot. Escribe 'salir' para terminar.")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            print("Proceso finalizado")
            break
        response = get_response(user_input)
        print("Chatbot:", response)


if __name__ == "__main__":
    run_chatbot()
