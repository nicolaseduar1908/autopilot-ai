import requests

url = "http://127.0.0.1:5000/youtube/programar_subida"

# Prueba enviando contenido para el Canal B
datos_video = {
    "canal_id": "canal_b",
    "titulo": "5 Hábitos Financieros para el Éxito",
    "descripcion": "Aprende cómo organizar tus finanzas paso a paso con Inteligencia Artificial.",
    "tags": ["finanzas", "desarrollo_personal", "ia"]
}

try:
    respuesta = requests.post(url, json=datos_video)
    print(" Status de la prueba:", respuesta.status_code)
    print(" Respuesta del Servidor:")
    print(respuesta.json())
except Exception as e:
    print(" Error probando la programación:", e)