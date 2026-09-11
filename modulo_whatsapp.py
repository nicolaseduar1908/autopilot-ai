import os
from flask import Blueprint, request, jsonify

whatsapp_bp = Blueprint('whatsapp_bp', __name__)

@whatsapp_bp.route('/webhook_whatsapp', methods=['POST'])
def webhook_whatsapp():
    """
    Recibe los mensajes de los clientes que llegan desde Facebook Ads, 
    Instagram Ads o TikTok Ads a WhatsApp, y responde con una personalidad 
    amigable, empática y experta en cierre de ventas.
    """
    datos = request.get_json() or {}
    mensaje_cliente = datos.get("mensaje", "")
    nombre_cliente = datos.get("nombre", "amigo")
    origen_anuncio = datos.get("origen", "redes sociales") # Puede ser Facebook Ads, Instagram Ads o TikTok Ads

    # Personalidad del Agente de Ventas adaptada a pauta multicanal
    prompt_agente = f"""
    Eres un asesor comercial experto, pero actúas como un amigo cercano, amigable, con muy buen ánimo y energía positiva.
    Estás chateando por WhatsApp con {nombre_cliente}, quien llegó interesado por un anuncio en {origen_anuncio}.
    
    Reglas estrictas:
    1. NO menciones la palabra Hotmart, plataformas de pago técnicas, ni suenes como un robot corporativo.
    2. Escucha su problema, muéstrale empatía genuina y dale ánimos de que sí puede lograr lo que busca.
    3. Si notas que el cliente ya está convencido o pregunta cómo adquirir el programa/curso, entrégale el enlace de forma natural y cálida.
    4. Usa un tono humano, cercano (puedes usar algún emoji ocasional de forma amigable) y mantén los mensajes cortos, propios de WhatsApp.
    
    Mensaje actual del cliente: "{mensaje_cliente}"
    """

    # Respuesta simulada inicial del agente integrando el origen
    respuesta_generada = f"¡Hola {nombre_cliente}! Qué alegría saludarte. Vi que nos escribiste a través de nuestro anuncio en {origen_anuncio}. Oye, te entiendo perfectamente, a mí también me pasaba al principio, pero créeme que con el método correcto vas a ver un cambio total. ¡Vamos con toda! ¿Tienes alguna duda de cómo empezamos?"

    return jsonify({
        "status": "éxito",
        "canal": "WhatsApp Business",
        "origen_lead": origen_anuncio,
        "cliente": nombre_cliente,
        "mensaje_recibido": mensaje_cliente,
        "respuesta_agente": respuesta_generada,
        "fase_embudo": "generando_confianza"
    }), 200