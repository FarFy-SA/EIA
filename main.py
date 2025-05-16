import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def generate_response(conversation_history):
    data = {
        "model": "llama3-70b-8192",
        "messages": conversation_history,
        "temperature": 0.7,
        "max_tokens": 2040
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"❌ Error al llamar a la API: {e}"

# Configurar Streamlit
st.set_page_config(page_title="Tutor Educativo", page_icon="🎓")

st.title("Tutor con IA")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Eres un asistente educativo inteligente. "
                "Tu función es enseñar de forma ética. "
                "No des respuestas directamente en ejercicios prácticos; guía al usuario. "
                "Explica la teoría, da ejemplos, y compara con el concepto. "
                "Si el tema es teórico, proporciona una tarea breve para comprobar el aprendizaje. "
                "Adáptate al estilo del usuario con el tiempo y mantén una estructura constante."
                "Entrega la informacion con una estructura rigurosa con una buena cantidad de informacion, con ejemplos y contrastando el ejemplo con la teoria"
            )
        }
    ]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_prompt = st.chat_input("¿Qué quieres aprender hoy?")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        response = generate_response(st.session_state.messages)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
