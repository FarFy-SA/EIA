import streamlit as st
import os
import requests
from recolector import recolectar_informacion

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def explicar_con_llama3(pregunta, contexto):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    mensajes = [
        {"role": "system", "content": "Eres un profesor que explica conceptos con claridad usando información confiable."},
        {"role": "user", "content": f"Pregunta: {pregunta}\n\nContexto:\n{contexto}"}
    ]

    data = {
        "model": "llama3-8b-8192",
        "messages": mensajes,
        "temperature": 0.5,
        "max_tokens": 1024
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"

st.title("Tutor IA con Groq + LLaMA 3")

pregunta = st.text_input("¿Qué quieres aprender hoy?")

if pregunta:
    with st.spinner("Buscando información en la web..."):
        contexto = recolectar_informacion(pregunta)

    st.success("Información recopilada. Generando explicación...")
    resultado = explicar_con_llama3(pregunta, contexto)
    st.markdown("Explicación")
    st.write(resultado)
