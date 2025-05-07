iimport streamlit as st
from duckduckgo_search import DDGS
import openai

openai.api_key = "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"

def buscar_en_web(pregunta, max_resultados=5):
    with DDGS() as ddgs:
        resultados = ddgs.text(pregunta, max_results=max_resultados)
        textos = [r['body'] for r in resultados if 'body' in r]
        return "\n\n".join(textos)

def explicar_como_profesor(pregunta, contenido_web):
    prompt = f"""
Eres un profesor experto y paciente. Explica claramente el tema: "{pregunta}" usando la información a continuación.
Agrega ejemplos si es posible. Sé pedagógico, claro y ordenado.

Contenido extraído de la web:
{contenido_web}
"""
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return respuesta.choices[0].message.content.strip()


st.title("Tutor IA con Búsqueda Web")
st.write("Haz una pregunta y te enseñaremos con información real de la web.")

pregunta = st.text_input("¿Qué quieres aprender hoy?")
if st.button("Buscar y enseñar"):
    if openai.api_key == "sk-ESCRIBE_TU_CLAVE_AQUI":
        st.error("❌ Por favor, reemplaza la clave en el código con tu API Key de OpenAI.")
    elif pregunta:
        with st.spinner("Buscando información real en la web..."):
            textos = buscar_en_web(pregunta)
        with st.spinner("Creando explicación clara como un profesor..."):
            explicacion = explicar_como_profesor(pregunta, textos)
        st.success("✅ Aquí tienes tu clase:")
        st.write(explicacion)
