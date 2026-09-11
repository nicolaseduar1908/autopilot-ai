import os
from flask import Blueprint, jsonify, request

youtube_bp = Blueprint('youtube', __name__)

# Configuración base de canales gestionados por la IA
CANALES_CONFIG = {
    'canal_a': {
        'nombre': 'Canal A - Curiosidades y Tecnología',
        'nicho': 'Tecnología',
        'estilo_guion': 'Dinámico, rápido y con llamadas a la acción directas',
        'activo': True
    },
    'canal_b': {
        'nombre': 'Canal B - Desarrollo Personal y Finanzas',
        'nicho': 'Finanzas',
        'estilo_guion': 'Analítico, inspirador y enfocado en aportar valor',
        'activo': True
    }
}

@youtube_bp.route('/canales', methods=['GET'])
def listar_canales():
    """Retorna los canales registrados y su estado."""
    return jsonify({
        'status': 'exitoso',
        'canales_conectados': len(CANALES_CONFIG),
        'canales': CANALES_CONFIG
    }), 200

@youtube_bp.route('/programar_subida', methods=['POST'])
def programar_subida():
    """Recibe un video/guion y lo asigna al canal correspondiente."""
    datos = request.get_json() or {}
    canal_id = datos.get('canal_id', 'canal_a')
    titulo = datos.get('titulo', 'Video Automatizado IA')
    descripcion = datos.get('descripcion', 'Descripción generada automáticamente.')
    tags = datos.get('tags', ['ia', 'automatizacion'])

    if canal_id not in CANALES_CONFIG:
        return jsonify({'status': 'error', 'mensaje': f'El canal {canal_id} no está registrado.'}), 400

    info_canal = CANALES_CONFIG[canal_id]

    # Simulación de la subida vía API de YouTube
    resultado = {
        'status': 'exitoso',
        'mensaje': f'Video programado con éxito en {info_canal["nombre"]}',
        'detalles_publicacion': {
            'canal': info_canal['nombre'],
            'titulo_optimizado': f"[{info_canal['nicho']}] {titulo}",
            'descripcion': descripcion,
            'etiquetas': tags,
            'estado_publicacion': 'Programado'
        }
    }

    print(f"🎬 [YOUTUBE MULTICANAL] Video publicado en {info_canal['nombre']}: '{titulo}'")
    return jsonify(resultado), 200