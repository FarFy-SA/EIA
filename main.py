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
import streamlit as st
import streamlit_authenticator as stauth
import requests
import os

# ========== CONFIGURAR LOGIN ==========
NOMBRES = ['Ana Gómez', 'Luis Pérez']
USUARIOS = ['ana', 'luis']
CLAVES = stauth.Hasher(['123', '456']).generate()

authenticator = stauth.Authenticate(
    NOMBRES, USUARIOS, CLAVES,
    'cookie_tutor', 'random_signature_key', cookie_expiry_days=1
)

# ========== INICIO DE SESIÓN ==========
nombre, estado_autenticacion, usuario = authenticator.login("Iniciar sesión", "main")

if estado_autenticacion:
    authenticator.logout("Cerrar sesión", "sidebar")
    st.sidebar.success(f"Bienvenido, {nombre}")

    # ========== MÚLTIPLES CLASES ==========
    if 'clases' not in st.session_state:
        st.session_state.clases = {}

    clase = st.sidebar.selectbox("Selecciona una clase", list(st.session_state.clases.keys()) + ["+ Nueva clase"])

    if clase == "+ Nueva clase":
        nueva_clase = st.sidebar.text_input("Nombre de la nueva clase:")
        if st.sidebar.button("Crear clase") and nueva_clase:
            st.session_state.clases[nueva_clase] = []
            clase = nueva_clase

    if clase not in st.session_state.clases:
        st.session_state.clases[clase] = []

    historial = st.session_state.clases[clase]

    # ========== INTERFAZ PRINCIPAL ==========
    st.title("Tutor IA con Groq + LLaMA 3")

    pregunta = st.text_input("Haz una pregunta sobre lo que quieras aprender:")

    if st.button("Preguntar") and pregunta:
        with st.spinner("Pensando..."):
            try:
                respuesta = obtener_respuesta_groq(pregunta, historial)
                historial.append({"rol": "user", "contenido": pregunta})
                historial.append({"rol": "assistant", "contenido": respuesta})
            except Exception as e:
                st.error(f"Error: {e}")

    # Mostrar historial de conversación
    for msg in historial:
        if msg["rol"] == "user":
            st.markdown(f"**Tú:** {msg['contenido']}")
        else:
            st.markdown(f"**Tutor IA:** {msg['contenido']}")

elif estado_autenticacion is False:
    st.error("Usuario o contraseña incorrectos")
elif estado_autenticacion is None:
    st.warning("Por favor inicia sesión")

# ========== LLAMADA A GROQ API ==========
def obtener_respuesta_groq(pregunta, historial):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    mensajes = [{"role": "system", "content": "Eres un tutor que explica con claridad a estudiantes"}]
    for h in historial:
        mensajes.append({"role": h["rol"], "content": h["contenido"]})
    mensajes.append({"role": "user", "content": pregunta})

    body = {
        "model": "llama3-8b-8192",
        "messages": mensajes,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
