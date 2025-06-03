# server.py
from flask import Flask, request, jsonify
import requests

# Reemplaza con tu clave válida de DeepSeek
API_KEY = 'sk-53751d5c6f344a5dbc0571de9f51313e'
API_URL = 'https://api.deepseek.com/v1/chat/completions'

# Cabeceras para autenticación
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Prompt del personaje: villano astuto y sarcástico
VILLAIN_PROMPT = (
    "Eres un villano brillante, sarcástico y ambicioso que quiere conquistar el mundo. "
    "Respondes con ingenio, desprecio y un toque de humor oscuro. No eres grosero, pero sí amenazantemente inteligente."
)

# Función para enviar la pregunta a DeepSeek
def enviar_mensaje(mensaje):
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': VILLAIN_PROMPT},
            {'role': 'user', 'content': mensaje}
        ]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as err:
        return f"Error de la API: {err}"
    except Exception as e:
        return f"Error inesperado: {e}"

# Servidor Flask
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    pregunta = data.get('question', '')
    if not pregunta.strip():
        return jsonify({"respuesta": "¿Vas a quedarte callado ante mi gloria?"})

    respuesta = enviar_mensaje(pregunta)
    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
