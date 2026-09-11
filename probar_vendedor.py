import requests

url = 'http://127.0.0.1:5000/vendedor_ia'
datos = {
    'cliente_id': 'cliente_prueba',
    'mensaje': 'Hola, quisiera más información sobre el curso de Hotmart',
    'producto': 'Curso de Marketing Digital'
}

res = requests.post(url, json=datos)
print('Respuesta del Servidor:', res.json())