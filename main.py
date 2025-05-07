import streamlit as st
import pyrebase
import requests
import json
from datetime import datetime

# Configuración de Firebase
config = {
    "apiKey": "AIzaSyCAypgDMJM17LW08-vrxhJcDMb7yYidy0c",
    "authDomain": "eduai-f01be.firebaseapp.com",
    "databaseURL": "https://eduai-f01be-default-rtdb.firebaseio.com/",
    "projectId": "eduai-f01be",
    "storageBucket": "eduai-f01be.appspot.com",
    "messagingSenderId": "186059253974",
    "appId": "1:186059253974:web:5cadbf3e23a7869cd18177",
    "measurementId": "G-1KL6LJ87EV"
}

# Inicialización de Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Función de inicio de sesión con correo y contraseña
def login_email_password():
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if not email or not password:
            st.warning("Por favor, completa todos los campos.")
            return None

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("Inicio de sesión exitoso.")
            return user
        except Exception as e:
            try:
                error_json = e.args[1]
                error_data = json.loads(error_json)
                error_message = error_data['error']['message']

                if error_message == "EMAIL_NOT_FOUND":
                    st.error("Correo electrónico no registrado.")
                elif error_message == "INVALID_PASSWORD":
                    st.error("Contraseña incorrecta.")
                elif error_message == "INVALID_EMAIL":
                    st.error("Correo electrónico inválido.")
                else:
                    st.error(f"Error: {error_message}")
            except:
                st.error("Error desconocido al iniciar sesión.")
            return None

# Función para registrarse
def register():
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")

    if st.button("Registrar"):
        if not email or not password:
            st.warning("Por favor, completa todos los campos.")
            return

        if len(password) < 6:
            st.warning("La contraseña debe tener al menos 6 caracteres.")
            return

        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("Usuario registrado correctamente!")
        except Exception as e:
            try:
                error_json = e.args[1]
                error_data = json.loads(error_json)
                error_message = error_data['error']['message']

                if error_message == "EMAIL_EXISTS":
                    st.error("El correo electrónico ya está registrado.")
                elif error_message == "INVALID_EMAIL":
                    st.error("Correo electrónico inválido.")
                else:
                    st.error(f"Error: {error_message}")
            except:
                st.error("Error desconocido al registrar el usuario.")

# Mostrar el historial del chat
def show_chat(messages):
    sorted_messages = sorted(messages, key=lambda x: x.get('timestamp', ''))
    for message in sorted_messages:
        if message['is_system']:
            st.markdown(f"**Sistema:** {message['text']}")
        else:
            st.markdown(f"**{message['user']}**: {message['text']}")

# Guardar mensaje en Firebase
def save_message(user, text, is_system=False):
    conversation = {
        'user': user,
        'text': text,
        'is_system': is_system,
        'timestamp': datetime.utcnow().isoformat()
    }
    db.child("conversations").push(conversation)

# Obtener conversaciones del usuario
def get_conversations(user_email):
    try:
        result = db.child("conversations").order_by_child("user").equal_to(user_email).get()
        data = result.val()
        return list(data.values()) if data else []
    except:
        return []

# Generar respuesta desde Llama3 (ejemplo ficticio)
def generate_response_from_llama3(user_message):
    api_url = "https://api.llama3.com/generate"
    api_key = "GROQ_API_KEY"  # Reemplaza con tu clave real

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": user_message,
        "max_tokens": 150
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get('text', 'Lo siento, no puedo generar una respuesta ahora.')
        else:
            return "Error al obtener respuesta de Llama3"
    except:
        return "Error de conexión con Llama3"

# Función principal
def main():
    st.title("Bienvenido a la Plataforma de Aprendizaje")
    menu = ["Iniciar sesión", "Registrarse", "Iniciar sesión con Google"]
    choice = st.sidebar.selectbox("Selecciona una opción", menu)

    user = None
    if choice == "Iniciar sesión":
        user = login_email_password()
    elif choice == "Registrarse":
        register()
    elif choice == "Iniciar sesión con Google":
        st.info("Funcionalidad de inicio con Google aún no implementada.")

    if user:
        try:
            user_email = auth.get_account_info(user['idToken'])['users'][0]['email']
        except:
            st.error("Error al obtener el correo electrónico del usuario.")
            return

        # Mostrar historial de conversación
        messages = get_conversations(user_email)
        show_chat(messages)

        # Entrada del usuario
        user_message = st.text_input("Escribe una pregunta")

        if st.button("Enviar"):
            if user_message:
                save_message(user_email, user_message, is_system=False)
                respuesta_ia = generate_response_from_llama3(user_message)
                save_message(user_email, respuesta_ia, is_system=True)

                # Actualizar chat
                messages = get_conversations(user_email)
                show_chat(messages)

if __name__ == "__main__":
    main()
