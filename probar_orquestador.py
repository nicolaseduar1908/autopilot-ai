import requests

url = "http://127.0.0.1:5000/orquestador/ejecutar_flujo_completo"
payload = {
    "nicho": "Emprendimiento",
    "tema": "Hotmart IA",
    "canal_id": "canal_youtube_01",
    "avatar_id": "avatar_vendedor"
}

try:
    print("📡 Enviando petición al servidor backend...")
    respuesta = requests.post(url, json=payload)
    
    print(f"Status Code: {respuesta.status_code}")
    
    if respuesta.status_code == 200:
        print("\n🎉 ¡ÉXITO! Respuesta del Orquestador:")
        print(respuesta.json())
    else:
        print(f"\n⚠️ El servidor respondió con error {respuesta.status_code}:")
        print(respuesta.text)

except Exception as e:
    print(f"❌ Error de conexión: {e}")