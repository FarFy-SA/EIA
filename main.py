import streamlit as st
import pyrebase
import requests  # Para hacer solicitudes HTTP

# Configuración de Firebase
config = {
    "apiKey": "AIzaSyCAypgDMJM17LW08-vrxhJcDMb7yYidy0c",
    "authDomain": "eduai-f01be.firebaseapp.com",
    "databaseURL": "https://eduai-f01be-default-rtdb.firebaseio.com/"
    "projectId": "eduai-f01be", 
    "storageBucket": "eduai-f01be.firebasestorage.app",  
    "messagingSenderId": "186059253974", 
    "appId": "1:186059253974:web:5cadbf3e23a7869cd18177",  
    "measurementId": "G-1KL6LJ87EV"  
}

# Inicialización de Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Función para iniciar sesión con Google
def login_google():
    auth_url = auth.get_redirect_url('https://yourapp.com')  # La URL de redirección para autenticar Google
    st.write(f"Inicia sesión con Google: [Haz clic aquí]({auth_url})")

# Función de inicio de sesión con correo y contraseña
def login_email_password():
    email = st.text_input("Correo electrónico", type="email")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar sesión"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success(f"Bienvenido {user['email']}")
            return user  # Retorna el usuario autenticado
        except:
            st.error("Error al iniciar sesión")

# Función para registrarse
def register():
    email = st.text_input("Correo electrónico", type="email")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Registrar"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("Usuario registrado correctamente!")
        except:
            st.error("Error al registrar el usuario")

# Función para mostrar el chat
def show_chat(messages):
    for message in messages:
        if message['user'] == 'system':
            st.markdown(f"**Sistema:** {message['text']}")
        else:
            st.markdown(f"**{message['user']}**: {message['text']}")

# Función para guardar un mensaje en Firebase
def save_message(user, text, is_system=False):
    db = firebase.database()
    conversation = {
        'user': user,
        'text': text,
        'is_system': is_system
    }
    db.child("conversations").push(conversation)

# Función para obtener las conversaciones de Firebase
def get_conversations(user_email):
    db = firebase.database()
    conversations = db.child("conversations").order_by_child("user").equal_to(user_email).get()
    return conversations.val() if conversations else []

# Función para obtener respuesta desde Llama3
def generate_response_from_llama3(user_message):
    # Suponiendo que Llama3 tiene un endpoint para hacer solicitudes.
    api_url = "https://api.llama3.com/generate"  # URL de ejemplo
    api_key = "GROQ_API_KEY"  # Reemplaza con tu clave de API de Llama3
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": user_message,
        "max_tokens": 150  
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json().get('text', 'Lo siento, no puedo generar una respuesta ahora.')
    else:
        return "Error al obtener respuesta de Llama3"

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
        login_google()

    if user:
        # Si el usuario ha iniciado sesión correctamente, mostrar el chat
        user_email = user['email']
        
        # Recuperar las conversaciones de Firebase
        messages = get_conversations(user_email)

        # Mostrar el historial del chat
        show_chat(messages)

        # Crear un campo para que el usuario escriba su mensaje
        user_message = st.text_input("Escribe una pregunta")

        if st.button("Enviar"):
            if user_message:
                # Guardamos el mensaje del usuario en Firebase
                save_message(user_email, user_message, is_system=False)

                # Obtener respuesta desde Llama3
                respuesta_ia = generate_response_from_llama3(user_message)
                save_message('system', respuesta_ia, is_system=True)

                # Recuperar nuevamente las conversaciones para mostrarlas
                messages = get_conversations(user_email)

                # Mostrar el historial actualizado
                show_chat(messages)

if __name__ == "__main__":
    main()
