import os
import google.generativeai as genai
from flask import Blueprint, jsonify, request

orquestador_bp = Blueprint('orquestador', __name__)

# Configuración de la API Key de Gemini desde Render
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
  genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')


# --- RUTA PRINCIPAL QUE LLAMA MAKE (/api/comando) ---
@orquestador_bp.route('/api/comando', methods=['POST', 'OPTIONS'])
def comando():
  if request.method == 'OPTIONS':
    return jsonify({'status': 'ok'}), 200

  try:
    datos = request.get_json() or {}

    # Captura el mensaje enviado desde FlutterFlow / Make
    texto_usuario = (
        datos.get('comando') or datos.get('texto') or datos.get('mensaje', '')
    )

    if not texto_usuario:
      return (
          jsonify(
              {'respuesta': 'No recibí ninguna consulta. Inténtalo de nuevo.'}
          ),
          400,
      )

    # Genera la respuesta real con la IA de Gemini
    response = model.generate_content(texto_usuario)
    respuesta_ia = response.text

    return jsonify({'respuesta': respuesta_ia}), 200

  except Exception as e:
    print(f'Error al procesar con Gemini: {e}')
    return (
        jsonify({
            'respuesta': 'Ocurrió un error en el servidor al consultar con la IA.'
        }),
        500,
    )


# --- RUTA SECUNDARIA (FLUJO COMPLETO) ---
@orquestador_bp.route(
    '/orquestador/ejecutar_flujo_completo', methods=['POST', 'OPTIONS']
)
def ejecutar_flujo_completo():
  if request.method == 'OPTIONS':
    return jsonify({'status': 'ok'}), 200

  datos = request.get_json() or {}

  nicho = datos.get('nicho', 'Emprendimiento')
  tema = datos.get('tema', 'Hotmart IA')
  canal_id = datos.get('canal_id', 'canal_youtube_01')
  avatar_id = datos.get('avatar_id', 'avatar_vendedor')

  try:
    prompt = f'Crea un guion corto de venta AIDA para un video sobre {tema} en el nicho de {nicho}.'
    response = model.generate_content(prompt)
    guion_final = response.text
  except Exception:
    guion_final = (
        f'¿Quieres dominar {tema} en {nicho}? Multiplica tus resultados hoy.'
    )

  respuesta = {
      'status': 'exitoso',
      'mensaje': 'Flujo automatizado ejecutado y guion generado con IA',
      'detalles_ejecucion': {
          'nicho_objetivo': nicho,
          'tema': tema,
          'canal_destino': canal_id,
          'avatar_asignado': avatar_id,
          'guion_final': guion_final,
      },
  }

  return jsonify(respuesta), 200