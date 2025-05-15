from fastapi import FastAPI, Request
from pydantic import BaseModel
from deepseek import DeepSeekClient
import uvicorn
import random

app = FastAPI()
client = DeepSeekClient(api_key="DEEPSEEK_API_KEY")  


user_memory = {}

class UserInput(BaseModel):
    user_id: str
    message: str

@app.post("/learn")
async def learn(input: UserInput):
    user_id = input.user_id
    message = input.message.strip()


    if user_id not in user_memory:
        user_memory[user_id] = {"history": []}


    user_memory[user_id]["history"].append({"role": "user", "content": message})

    history = user_memory[user_id]["history"][-5:]

    # Construye prompt para el modelo
    prompt = f"""
Eres un tutor educativo basado en inteligencia artificial. El usuario quiere aprender algo. 
Debes identificar el tema y el tipo de contenido (teoría, ejemplo, ejercicio) basado en lo que escribe.
Nunca des respuestas directas a ejercicios, solo pistas. Si es teoría, ofrece una tarea corta para comprobar aprendizaje.
Debes de dar respuestas con una estrucutra constante para que el alumno se acople bien a el contenido.

Entrada del usuario: "{message}"

Contexto previo: {[m['content'] for m in history if m['role'] == 'user']}
Responde de forma pedagógica, adaptada al nivel del usuario.
"""

     
    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Eres un tutor educativo inteligente, ético y paciente."},
            {"role": "user", "content": prompt}
        ]
    )

    respuesta = completion.choices[0].message.content

    # Guarda respuesta del bot en memoria
    user_memory[user_id]["history"].append({"role": "assistant", "content": respuesta})

    return {"respuesta": respuesta}
