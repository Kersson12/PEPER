# Chatbot Villano Sarcástico con DeepSeek y Flask

Este proyecto consiste en el desarrollo de un chatbot conversacional con una personalidad de villano sarcástico y astuto. La implementación se realiza utilizando Python, el microframework Flask para el backend del servidor y la API de DeepSeek como motor de inteligencia artificial para la generación de respuestas. El objetivo es crear una experiencia de usuario única donde el chatbot interactúa con ingenio, desprecio y un toque de humor oscuro.

## Tabla de Contenidos

1.  [Requisitos](https://www.google.com/search?q=%231-requisitos)
2.  [Estructura del Proyecto](https://www.google.com/search?q=%232-estructura-del-proyecto)
3.  [Configuración del Entorno](https://www.google.com/search?q=%233-configuraci%C3%B3n-del-entorno)
      * [Paso 1: Crear el Directorio del Proyecto](https://www.google.com/search?q=%23paso-1-crear-el-directorio-del-proyecto)
      * [Paso 2: Crear y Activar el Entorno Virtual](https://www.google.com/search?q=%23paso-2-crear-y-activar-el-entorno-virtual)
      * [Paso 3: Instalar Dependencias](https://www.google.com/search?q=%23paso-3-instalar-dependencias)
4.  [Desarrollo del Servidor (`server.py`)](https://www.google.com/search?q=%234-desarrollo-del-servidor-serverpy)
      * [Configuración de la API Key](https://www.google.com/search?q=%23configuraci%C3%B3n-de-la-api-key)
      * [Definición del Prompt del Personaje](https://www.google.com/search?q=%23definici%C3%B3n-del-prompt-del-personaje)
      * [Función para Enviar Mensajes a DeepSeek](https://www.google.com/search?q=%23funci%C3%B3n-para-enviar-mensajes-a-deepseek)
      * [Configuración de la Ruta del Chat](https://www.google.com/search?q=%23configuraci%C3%B3n-de-la-ruta-del-chat)
      * [Ejecución del Servidor](https://www.google.com/search?q=%23ejecuci%C3%B3n-del-servidor)
5.  [Ejecución del Chatbot](https://www.google.com/search?q=%235-ejecuci%C3%B3n-del-chatbot)
6.  [Interacción con el Chatbot](https://www.google.com/search?q=%236-interacci%C3%B3n-con-el-chatbot)
7.  [Consideraciones Adicionales](https://www.google.com/search?q=%237-consideraciones-adicionales)

-----

## 1\. Requisitos

Antes de iniciar el montaje, asegúrese de tener instalados los siguientes elementos en su sistema:

  * **Python 3.x**: Se recomienda utilizar la versión más reciente de Python 3 para asegurar la compatibilidad con las librerías.
  * **Conexión a Internet**: Necesaria para la instalación de dependencias y la comunicación con la API de DeepSeek.
  * **Clave de API de DeepSeek**: Deberá obtener una clave válida de la plataforma DeepSeek para autenticar las solicitudes a su API.

## 2\. Estructura del Proyecto

La estructura del proyecto es sencilla y se organiza de la siguiente manera:

```
PepperFinal/
├── venv/                 # Entorno virtual de Python
├── server.py             # Script principal del servidor Flask y lógica del chatbot
├── .gitignore            # (Opcional) Archivo para ignorar venv en control de versiones
└── readme.md             # Este archivo de documentación
```

La imagen 2.jpeg muestra la estructura de la carpeta `PepperFinal` después de la creación del entorno virtual (`venv`) y el archivo `server.py`. La imagen 1.jpeg proporciona una vista general de la ubicación de la carpeta `PepperFinal` dentro de `Documentos`.

## 3\. Configuración del Entorno

Siga estos pasos para configurar el entorno de desarrollo.

### Paso 1: Crear el Directorio del Proyecto

Primero, cree la carpeta principal para el proyecto. En este caso, la ruta sugerida es:

```bash
mkdir ~/Documentos/PepperFinal
cd ~/Documentos/PepperFinal
```

### Paso 2: Crear y Activar el Entorno Virtual

Es crucial utilizar un entorno virtual para gestionar las dependencias del proyecto de forma aislada.

1.  **Crear el entorno virtual:**

    ```bash
    python3 -m venv venv
    ```

    Esto creará una carpeta `venv` dentro de su directorio `PepperFinal`.

2.  **Activar el entorno virtual:**

      * **En Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
      * **En Windows (Command Prompt):**
        ```bash
        venv\Scripts\activate.bat
        ```
      * **En Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```

    Verá `(venv)` al inicio de su línea de comandos, lo que indica que el entorno virtual está activo.

### Paso 3: Instalar Dependencias

Con el entorno virtual activado, instale las librerías necesarias:

```bash
pip install Flask requests
```

  * `Flask`: El microframework web para Python.
  * `requests`: Librería HTTP para realizar solicitudes a la API de DeepSeek.

## 4\. Desarrollo del Servidor (`server.py`)

Cree un archivo llamado `server.py` dentro de la carpeta `PepperFinal` y añada el siguiente código:

```python
from flask import Flask, request, jsonify
import requests

# Reemplaza con tu clave válida de DeepSeek
API_KEY = 'sk-53751d5c6f344a5dbc0571de9f51313e' # Sustituir con la clave real obtenida de DeepSeek
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
        response.raise_for_status() # Lanza una excepción para errores HTTP
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

```

### Configuración de la API Key

**Es fundamental reemplazar `'sk-53751d5c6f344a5dbc0571de9f51313e'` con su clave de API real de DeepSeek.** Sin una clave válida, la comunicación con la API fallará.

### Definición del Prompt del Personaje

El `VILLAIN_PROMPT` es una parte crucial de este proyecto, ya que define la personalidad del chatbot. Se ha diseñado cuidadosamente para instruir a la IA a adoptar un rol de villano sarcástico, inteligente y ambicioso. Esta técnica es conocida como "ingeniería de *prompts*" y permite guiar el comportamiento de los modelos de lenguaje.

### Función para Enviar Mensajes a DeepSeek

La función `enviar_mensaje` se encarga de formatear la solicitud de manera que DeepSeek comprenda tanto el mensaje del usuario como el contexto de la personalidad del villano. Maneja la comunicación con la API y los posibles errores.

### Configuración de la Ruta del Chat

La aplicación Flask define una ruta `/chat` que escucha peticiones `POST`. Cuando una petición llega a esta ruta, extrae la pregunta del usuario del cuerpo JSON, la envía a la API de DeepSeek a través de la función `enviar_mensaje` y devuelve la respuesta obtenida, también en formato JSON.

### Ejecución del Servidor

El bloque `if __name__ == '__main__':` asegura que el servidor se inicie solo cuando el script se ejecuta directamente. El servidor escuchará en todas las interfaces de red disponibles (`0.0.0.0`) en el puerto `5000`.

## 5\. Ejecución del Chatbot

Con el entorno virtual activado y el archivo `server.py` creado, puede iniciar el servidor:

```bash
python server.py
```

Una vez ejecutado el comando, verá mensajes en la terminal indicando que Flask está iniciando el servidor en `http://0.0.0.0:5000/`. La imagen 3.jpeg muestra una terminal donde se han ejecutado comandos relacionados con el proyecto, lo que simula un entorno de ejecución.

## 6\. Interacción con el Chatbot

Para interactuar con el chatbot, puede utilizar herramientas como `curl`, Postman, Insomnia o cualquier cliente HTTP. Deberá enviar una solicitud `POST` a la URL `http://localhost:5000/chat` (o la dirección IP de su servidor si lo está ejecutando en otra máquina) con un cuerpo JSON que contenga la pregunta.

**Ejemplo de solicitud `POST` utilizando `curl`:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"question": "¿Cuál es tu plan para conquistar el mundo?"}' http://localhost:5000/chat
```

**Ejemplo de respuesta esperada (el contenido exacto variará según la IA):**

```json
{"respuesta": "Mi plan, patético mortal, es tan infalible que hasta mencionarlo es una pérdida de mi valioso tiempo. ¡La dominación es inevitable!"}
```

Si envía una pregunta vacía, la respuesta será sarcástica:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"question": ""}' http://localhost:5000/chat
```

**Respuesta:**

```json
{"respuesta": "¿Vas a quedarte callado ante mi gloria?"}
```

## 7\. Consideraciones Adicionales

  * **Seguridad:** Para un entorno de producción, es crucial gestionar la `API_KEY` de forma segura, por ejemplo, utilizando variables de entorno en lugar de codificarla directamente en el script.
  * **Manejo de Errores:** Aunque se incluye un manejo básico de errores, un sistema más robusto debería implementar un registro (logging) más detallado y respuestas de error más informativas para el cliente.
  * **Escalabilidad:** Para aplicaciones con alto tráfico, se deberían considerar soluciones de despliegue más avanzadas (como Gunicorn/Nginx o Docker) para Flask y estrategias de gestión de concurrencia.
  * **Personalización:** El `VILLAIN_PROMPT` puede ser ajustado para refinar la personalidad del chatbot o para cambiarla completamente a otro arquetipo.
  * **Documentación Adicional:** Para una comprensión más profunda sobre la preparación de documentos técnicos, se puede consultar el formato IEEE disponible en `Formato presentacion documentos IEEE ES.pdf`[cite: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14].
