import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")  # o variable que te haya dado DeepSeek
API_BASE = os.getenv("DEEPSEEK_API_BASE")  # ej: "https://api.deepseek.com/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def generate_response(user_input, conversation_history=[]):
    # Agregar el mensaje del usuario a la conversación
    conversation_history.append({"role": "user", "content": user_input})

    # Mensaje del sistema con instrucciones
    system_prompt = {
        "role": "system",
        "content": (
            "Eres un asistente educativo inteligente. "
            "Tu función es enseñar de forma ética. "
            "No des respuestas directamente en ejercicios prácticos; guía al usuario. "
            "Explica la teoría, da ejemplos, y compara con el concepto. "
            "Si el tema es teórico, proporciona una tarea breve para comprobar el aprendizaje. "
            "Aprende el estilo de aprendizaje del usuario y adáptate a él con el tiempo."
            "Debes de dar respuestas con una estrucutra constante para que el alumno se acople bien a el contenido."
"
        )
    }

    # Construir el payload para la petición
    data = {
        "model": "deepseek-chat",  # Cambia esto al modelo que use DeepSeek
        "messages": [system_prompt] + conversation_history,
        "temperature": 0.7,
        "max_tokens": 600
    }

    try:
        response = requests.post(f"{API_BASE}/chat/completions", headers=HEADERS, json=data)
        response.raise_for_status()
        result = response.json()
        message = result["choices"][0]["message"]["content"]
        # Guardar la respuesta del asistente en la conversación
        conversation_history.append({"role": "assistant", "content": message})
        return message, conversation_history
    except requests.exceptions.RequestException as e:
        return f"Error en la llamada a la API: {e}", conversation_history

def run_chat():
    print("🎓 Bienvenido a tu tutor educativo. ¿Qué quieres aprender hoy?")
    conversation_history = []

    while True:
        user_input = input("\nTú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("📚 Sesión terminada. ¡Sigue aprendiendo!")
            break

        response, conversation_history = generate_response(user_input, conversation_history)
        print(f"\n🤖 Tutor: {response}")

if __name__ == "__main__":
    run_chat()
    
