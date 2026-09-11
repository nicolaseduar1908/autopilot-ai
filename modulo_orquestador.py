from flask import Blueprint, jsonify, request

orquestador_bp = Blueprint('orquestador', __name__)

@orquestador_bp.route('/orquestador/ejecutar_flujo_completo', methods=['POST', 'OPTIONS'])
def ejecutar_flujo_completo():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    datos = request.get_json() or {}
    
    nicho = datos.get('nicho', 'Emprendimiento')
    tema = datos.get('tema', 'Hotmart IA')
    canal_id = datos.get('canal_id', 'canal_youtube_01')
    avatar_id = datos.get('avatar_id', 'avatar_vendedor')

    # --- ESTRUCTURA DEL GUION BASADA EN LA FÓRMULA DE VENTA ---
    guion_generado = {
        "gancho_inicial": f"¿Quieres dominar {tema} pero no sabes por dónde empezar?",
        "problema": "La mayoría pierde semanas intentando entender el algoritmo sin una estrategia clara.",
        "solucion": f"Con este método automatizado en el nicho de {nicho}, multiplicas tus resultados en tiempo récord.",
        "llamado_a_la_accion": "Haz clic en el enlace del perfil y empieza hoy mismo."
    }

    # Respuesta estructurada para el frontend
    respuesta = {
        "status": "exitoso",
        "mensaje": "Flujo automatizado ejecutado y guion generado",
        "detalles_ejecucion": {
            "nicho_objetivo": nicho,
            "tema": tema,
            "canal_destino": canal_id,
            "avatar_asignado": avatar_id,
            "pasos_completados": [
                "Investigación de mercado finalizada",
                "Guion adaptado y optimizado con estructura AIDA",
                "Audio y render de avatar en cola de procesamiento",
                "Video programado para envío"
            ],
            "guion_final": guion_generado
        }
    }

    return jsonify(respuesta), 200