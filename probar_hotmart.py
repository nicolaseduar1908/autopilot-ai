import requests

url = "http://127.0.0.1:5000/hotmart/metricas_ventas"

try:
    respuesta = requests.get(url)
    print(" status de la prueba:", respuesta.status_code)
    print(" Respuesta del Servidor:")
    print(respuesta.json())
except Exception as e:
    print(" Error probando el endpoint:", e)