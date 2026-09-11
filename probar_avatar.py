import requests

url = "http://127.0.0.1:5000/avatar_voz/generar_media"

datos_prueba = {
    "avatar_id": "avatar_2",
    "guion": "El secreto del éxito financiero no es ganar más, sino administrar mejor lo que ya recibes hoy."
}

try:
    respuesta = requests.post(url, json=datos_prueba)
    print(" Status de la prueba:", respuesta.status_code)
    print(" Respuesta del Servidor:")
    print(respuesta.json())
except Exception as e:
    print(" Error probando avatar y voz:", e)