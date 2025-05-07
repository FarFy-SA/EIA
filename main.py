import os
import streamlit as st
from duckduckgo_search import DDGS
from openai import OpenAI

# Inicializa cliente OpenAI desde variables de entorno
client = OpenAI()

# Función para buscar en internet usando DuckDuckGo
def buscar_informacion(pregunta):
    resultados = []
    with DDGS() as ddgs:
        for r in ddgs.text(pregunta, max_results=3):
            resultados.append(r["body"])
    return resultados

# Función para generar explicación con IA
def explicar_como_profesor(pregunta, textos):
    contexto = "\n\n".join(textos)
    prompt = f"""Eres un profesor experto. Usando solo la información a continuación, responde claramente a esta pregunta:
    
Pregunta: {pregunta}

Información:
{contexto}

Responde:"""

    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return respuesta.choices[0].message.content

# Interfaz de usuario con Streamlit
st.title("Tutor IA 📚")
st.write("Haz una pregunta y recibirás una explicación con datos actuales.")

pregunta = st.text_input("¿Qué tema quieres aprender?", "")

if pregunta:
    with st.spinner("Buscando información y generando respuesta..."):
        textos = buscar_informacion(pregunta)
        explicacion = explicar_como_profesor(pregunta, textos)
        st.markdown("### Explicación:")
        st.write(explicacion)
