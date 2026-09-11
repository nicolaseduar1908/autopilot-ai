import requests

url = 'http://127.0.0.1:5000/webhook_hotmart'
datos_venta = {
    'event': 'PURCHASE_APPROVED',
    'data': {
        'buyer': {'name': 'Carlos Pérez', 'email': 'carlos.prueba@email.com'},
        'product': {'name': 'Curso de Marketing Digital'},
        'purchase': {'price': {'value': 47.00, 'currency_value': 'USD'}}
    }
}

res = requests.post(url, json=datos_venta)
print('Respuesta Hotmart:', res.json())
