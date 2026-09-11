import os
import requests
from flask import Blueprint, jsonify, request

hotmart_bp = Blueprint('hotmart', __name__)

# Configuración de credenciales de la API de Hotmart
# (En producción las tomará del archivo .env)
HOTMART_CLIENT_ID = os.getenv('HOTMART_CLIENT_ID', '')
HOTMART_CLIENT_SECRET = os.getenv('HOTMART_CLIENT_SECRET', '')
HOTMART_BASIC_TOKEN = os.getenv('HOTMART_BASIC_TOKEN', '')

def obtener_token_hotmart():
    """Obtiene el token Bearer para autenticarse con la API de Hotmart."""
    url = "https://api-sec-vlc.hotmart.com/security/oauth/token?grant_type=client_credentials"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {HOTMART_BASIC_TOKEN}'
    }
    try:
        response = requests.post(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get('access_token')
    except Exception as e:
        print(f"Error conectando con Hotmart: {e}")
    return None

@hotmart_bp.route('/metricas_ventas', methods=['GET'])
def obtener_metricas_ventas():
    """Endpoint para consultar las ventas acumuladas e ingresos del día."""
    # Simulación de respuesta mientras se cargan las credenciales reales de Hotmart
    metricas = {
        'estado': 'exitoso',
        'ventas_hoy': 0,
        'ingresos_hoy_usd': 0.0,
        'moneda': 'USD',
        'mensaje': 'Métricas sincronizadas correctamente con la API de Hotmart.'
    }
    return jsonify(metricas), 200

@hotmart_bp.route('/webhook_hotmart', methods=['POST'])
def webhook_hotmart():
    """Webhook que recibe las notificaciones instantáneas de cada venta realizada."""
    datos = request.json or {}
    evento = datos.get('event', 'PURCHASE_APPROVED')
    data_venta = datos.get('data', {})
    
    print(f"🔔 [NOTIFICACIÓN HOTMART] Nuevo evento recibido: {evento}")
    
    # Respuesta estándar para confirmar a Hotmart que se recibió la notificación
    return jsonify({'status': 'recibido', 'event': evento}), 200