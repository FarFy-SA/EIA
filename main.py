import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")  # Define esto en tu archivo .env
API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def generate_response(user_input, conversation_history=[]):
    conversation_history.append({"role": "user", "content": user_input})

    # Mensaje inicial del sistema
    system_prompt = {
        "role": "system",
        "content": (
            "Eres un asistente educativo inteligente. "
            "Tu función es enseñar de forma ética. "
            "No des respuestas directamente en ejercicios prácticos; guía al usuario. "
            "Explica la teoría, da ejemplos, y compara con el concepto. "
            "Si el tema es teórico, proporciona una tarea breve para comprobar el aprendizaje. "
            "Adáptate al estilo del usuario con el tiempo y mantén una estructura constante."
        )
    }

    data = {
        "model": "llama3-70b-8192",  # Puedes cambiar a mixtral-8x7b-32768, etc.
        "messages": [system_prompt] + conversation_history,
        "temperature": 0.7,
        "max_tokens": 600
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        result = response.json()
        message = result["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": message})
        return message, conversation_history
    except requests.exceptions.RequestException as e:
        return f"❌ Error en la llamada a la API: {e}", conversation_history

def run_chat():
    print("🎓 Bienvenido a tu tutor educativo gratuito con GROQ. ¿Qué quieres aprender hoy?")
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
