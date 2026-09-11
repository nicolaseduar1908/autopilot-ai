import os
import requests
from flask import Blueprint, request, jsonify

avatar_voz_bp = Blueprint('avatar_voz_bp', __name__)

# Configuración de APIs para Avatares y Voces
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "TU_ELEVENLABS_KEY")
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY", "TU_HEYGEN_KEY")
HEDRA_API_KEY = os.getenv("HEDRA_API_KEY", "TU_HEDRA_KEY")

# =========================================================
# 1. CANAL 1: MINISERIES / PELÍCULAS (AVATARES FOTORREALISTAS CON DIÁLOGO)
# =========================================================
@avatar_voz_bp.route('/generar_miniserie_pelicula', methods=['POST'])
def generar_miniserie_pelicula():
    """
    Genera episodios de miniseries donde los avatares actúan y hablan
    directamente en pantalla personaje por personaje (Sincronización de labios).
    """
    datos = request.get_json() or {}
    dialogos = datos.get("dialogos", [
        {"personaje": "Avatar_Femenino_1", "voz_id": "Voz_Actriz_1", "texto": "No vas a creer lo que descubrí en esa casa..."},
        {"personaje": "Avatar_Masculino_1", "voz_id": "Voz_Actor_1", "texto": "¿De qué estás hablando? Dijimos que jamás volveríamos allá."}
    ])
    estilo_visual = datos.get("estilo", "cinematografico_fantasia") # Basado en foto 2

    escenas_renderizadas = []
    
    for i, dialogo in enumerate(dialogos):
        # Simulación de renderizado por escena/personaje en la API de avatar fotorrealista
        escenas_renderizadas.append({
            "escena": i + 1,
            "personaje": dialogo.get("personaje"),
            "estilo": estilo_visual,
            "tipo_audio": "Sincronización labial (Lip-sync actuado)",
            "texto_hablado": dialogo.get("texto"),
            "status": "Escena renderizada con éxito"
        })

    return jsonify({
        "status": "éxito",
        "canal_destino": "Canal 1 - Miniseries & Películas IA",
        "estilo_visual": estilo_visual,
        "total_escenas": len(escenas_renderizadas),
        "escenas": escenas_renderizadas
    }), 200


# =========================================================
# 2. CANAL 2: NARRACIÓN Y ANIMACIONES (HISTORIAS / TERROR / REFLEXIÓN)
# =========================================================
@avatar_voz_bp.route('/generar_historia_narrada', methods=['POST'])
def generar_historia_narrada():
    """
    Genera videos con voz en off envolvente de narrador mientras en pantalla
    se muestran secuencias animadas, ilustradas o escenas de suspenso/motivación.
    """
    datos = request.get_json() or {}
    guion_historia = datos.get("guion", "Cuentan las leyendas del pueblo que a medianoche todo cambia...")
    categoria = datos.get("categoria", "terror_misterio") # terror, motivacion, superacion
    tipo_voz = datos.get("voz_narrador", "Voz_Profunda_Misteriosa")

    return jsonify({
        "status": "éxito",
        "canal_destino": "Canal 2 - Historias & Animaciones",
        "categoria": categoria,
        "audio": {
            "tipo": "Voz en Off (Narrador Ambiental)",
            "voz_utilizada": tipo_voz,
            "transcripcion": guion_historia
        },
        "visual": {
            "estilo": "Animado 2D / Ilustrado / Oscuro según tema",
            "secuencias_generadas": 5
        },
        "mensaje": "Video animado con narración listo para YouTube Shorts / TikTok"
    }), 200


# =========================================================
# 3. PUBLICIDAD HOTMART + FACEBOOK ADS (AVATAR ULTRA REALISTA UGC)
# =========================================================
@avatar_voz_bp.route('/generar_anuncio_hotmart', methods=['POST'])
def generar_anuncio_hotmart():
    """
    Genera un video publicitario de un avatar hiperrealista estilo persona real
    (como la foto 1) recomendando un producto digital de Hotmart.
    """
    datos = request.get_json() or {}
    producto = datos.get("producto", "Curso Online")
    guion_ventas = datos.get("guion_ventas", f"Si quieres aprender {producto}, este método cambió todo para mí...")
    
    return jsonify({
        "status": "éxito",
        "tipo": "Anuncio UGC para Facebook Ads / TikTok Ads",
        "avatar": "Fotorrealista Humano (Estilo Recomendación)",
        "producto_hotmart": producto,
        "guion_ejecutado": guion_ventas,
        "video_url": "https://api.avatar.ai/renders/anuncio_hotmart_ready.mp4"
    }), 200