import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Cargar claves
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_BASE = os.getenv("DEEPSEEK_API_BASE")

# Verificación
if not API_KEY or not API_BASE:
    st.error("❌ Las variables DEEPSEEK_API_KEY y DEEPSEEK_API_BASE no están configuradas.")
    st.stop()

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Inicializar conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función para enviar mensajes a la API
def ask_deepseek(messages):
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 600
    }
    try:
        response = requests.post(f"{API_BASE}/chat/completions", headers=HEADERS, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error al conectar con la API: {e}"

# Interfaz de chat
st.title("🎓 Tutor Educativo AI")
st.caption("Basado en DeepSeek API. Escribe tu duda sobre cualquier tema académico.")

# Entrada del usuario
user_input = st.chat_input("Escribe aquí...")

# Sistema educativo (mensaje base)
system_message = {
    "role": "system",
    "content": (
        "Eres un asistente educativo inteligente. "
        "Tu función es enseñar de forma ética. "
        "No des respuestas directamente en ejercicios prácticos; guía al usuario. "
        "Explica la teoría, da ejemplos, y compara con el concepto. "
        "Si el tema es teórico, proporciona una tarea breve para comprobar el aprendizaje. "
        "Aprende el estilo de aprendizaje del usuario y adáptate a él con el tiempo."
    )
}

# Mostrar historial del chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Si hay mensaje nuevo
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Insertar el mensaje del sistema al principio
    history = [system_message] + st.session_state.messages
    assistant_response = ask_deepseek(history)

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
