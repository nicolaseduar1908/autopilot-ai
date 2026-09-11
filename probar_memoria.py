import requests

url = "http://127.0.0.1:5000/memoria"
datos = {
    "nombre_proyecto": "IA_piloto_automatico",
    "paso_actual": "Conexion Supabase Completada",
    "resumen_contexto": "Memoria conectada y funcionando al 100%"
}

respuesta = requests.post(url, json=datos)
print("Respuesta del servidor:", respuesta.json())