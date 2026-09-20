import os
import json
import subprocess
import requests
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from supabase import create_client, Client
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Importación defensiva de la librería oficial de ElevenLabs
try:
    from elevenlabs.client import ElevenLabs
except ImportError:
    ElevenLabs = None

# =========================================================
# MÓDULO DE CREACIÓN DE VIDEOS (HIPERREALISTAS Y 3D/4D)
# =========================================================
class CreadorVideoIA:
    def __init__(self):
        self.api_key_voz = os.getenv("ELEVENLABS_API_KEY")
        self.heygen_api_key = os.getenv("HEYGEN_API_KEY")
        
    def generar_video_hiperrealista(self, guion, producto_hotmart, voice_id="13db294466d0437599c222611e330541"):
        """
        Crea un video con un avatar hiperrealista mediante HeyGen API.
        Ideal para Hotmart, Facebook Ads y anuncios de impacto directo.
        """
        print(f"[{producto_hotmart}] Generando video hiperrealista en HeyGen...")
        
        if not self.heygen_api_key:
            print("⚠️ [HEYGEN] HEYGEN_API_KEY no detectada en las variables de entorno.")
            return {"status": "error", "mensaje": "HEYGEN_API_KEY no configurada"}

        url = "https://api.heygen.com/v2/video/generate"
        headers = {
            "X-Api-Key": self.heygen_api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": "Daisy-eInDoor-20220818",
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": guion or f"Hola, descubre el curso {producto_hotmart}.",
                        "voice_id": voice_id
                    }
                }
            ],
            "dimension": {
                "width": 1080,
                "height": 1920
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            data = response.json()
            print(f"✅ [HEYGEN] Respuesta recibida: {data}")
            return data
        except Exception as e:
            print(f"❌ [HEYGEN] Error al conectar con HeyGen: {e}")
            return {"status": "error", "mensaje": str(e)}

    def generar_video_animado(self, guion, estilo="3D_pelicula"):
        """
        Crea un video animado (Estilo 3D/4D, cinemático)
        Ideal para YouTube y TikTok con estrategias SEO.
        """
        print(f"Generando video animado con estilo: {estilo}...")
        video_url = f"https://ejemplo.com/video_animado_{estilo}.mp4"
        return video_url

    def generar_guion_organico(self, nicho, tema):
        return f"Guion orgánico optimizado para SEO sobre {nicho} - {tema}"

    def generar_guion_facebook_ads(self, curso, tema):
        return f"Guion de alto impacto para Facebook Ads sobre {curso} - {tema}"

    def procesar_campana_por_canal(self, canal, tipo_preferencia, guion, producto):
        """
        Selector inteligente: Define qué tipo de video se creará según el canal 
        que elijas en tu panel de control.
        """
        if tipo_preferencia == "hiperrealista":
            return self.generar_video_hiperrealista(guion, producto)
        elif tipo_preferencia == "animado":
            return self.generar_video_animado(guion, estilo="3D_cinematico")
        else:
            return self.generar_video_animado(guion)

# =========================================================
# IMPORTACIÓN DE MÓDULOS DEL PROYECTO (DEFENSIVO)
# =========================================================
try:
    from agente_cazador import AgenteCazadorTendencias
except ImportError:
    AgenteCazadorTendencias = None

try:
    from motor_ia import MotorIA
except ImportError:
    MotorIA = None

try:
    import modulo_canva
except ImportError:
    modulo_canva = None

# Importación de Blueprints / Módulos de Redes y Servicios
try:
    from modulo_hotmart import hotmart_bp
except ImportError:
    hotmart_bp = None

try:
    from modulo_youtube import youtube_bp
except ImportError:
    youtube_bp = None

try:
    from modulo_avatar_voz import avatar_voz_bp
except ImportError:
    avatar_voz_bp = None

try:
    from modulo_orquestador import orquestador_bp
except ImportError:
    orquestador_bp = None

try:
    from modulo_whatsapp import whatsapp_bp
except ImportError:
    whatsapp_bp = None

try:
    from modulo_redes import redes_bp
except ImportError:
    redes_bp = None

# =========================================================
# CONFIGURACIÓN DE FLASK Y CORS
# =========================================================
app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))
CORS(app, resources={r"/*": {"origins": "*"}})

# REGISTRO DE BLUEPRINTS
if hotmart_bp: app.register_blueprint(hotmart_bp, url_prefix='/hotmart')
if youtube_bp: app.register_blueprint(youtube_bp, url_prefix='/youtube')
if avatar_voz_bp: app.register_blueprint(avatar_voz_bp, url_prefix='/avatar_voz')
if orquestador_bp: app.register_blueprint(orquestador_bp, url_prefix='/orquestador')
if whatsapp_bp: app.register_blueprint(whatsapp_bp, url_prefix='/whatsapp')

if redes_bp:
    app.register_blueprint(redes_bp, url_prefix='/redes')
    print("✅ [MÓDULO REDES] Registrado correctamente.")
else:
    print("⚠️ [MÓDULO REDES] No se cargó modulo_redes.py (Opcional).")

# ---------------------------------------------------------
# CONFIGURACIÓN DE GEMINI IA OFICIAL
# ---------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("✅ [GEMINI] API Key configurada correctamente.")
    except Exception as e:
        print(f"⚠️ [GEMINI] Error al configurar API Key: {e}")
else:
    print("⚠️ [GEMINI] GEMINI_API_KEY no detectada en las variables de entorno.")

# ---------------------------------------------------------
# CONFIGURACIÓN DE ELEVENLABS IA
# ---------------------------------------------------------
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
elevenlabs_client = None

if ELEVENLABS_API_KEY and ElevenLabs:
    try:
        elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        print("✅ [ELEVENLABS] Cliente listo.")
    except Exception as e:
        print(f"⚠️ [ELEVENLABS] Error al inicializar: {e}")

# ---------------------------------------------------------
# CONFIGURACIÓN DE YOUTUBE Y SUPABASE
# ---------------------------------------------------------
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ [SUPABASE] Conexión establecida.")
    except Exception as e:
        print(f"⚠️ [SUPABASE] Error de conexión: {e}")
else:
    print("⚠️ [SUPABASE] SUPABASE_URL o SUPABASE_KEY no detectadas en variables de entorno.")

# ---------------------------------------------------------
# RUTAS DE LA APLICACIÓN
# ---------------------------------------------------------
@app.route('/', methods=['GET'])
def inicio():
    if os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory('static', 'index.html')
    return jsonify({"mensaje": "Servidor Flask activo", "status": "OK"}), 200

# ---------------------------------------------------------
# RUTA / GENERAR-VIDEO (CONECTADA DIRECTO CON FLUTTERFLOW)
# ---------------------------------------------------------
@app.route('/generar-video', methods=['POST', 'GET'])
@app.route('/generar-video/', methods=['POST', 'GET'])
def generar_video_flutterflow():
    if request.method == 'GET':
        return jsonify({"mensaje": "Endpoint /generar-video activo. Usa POST para enviar datos.", "status": "OK"}), 200
    try:
        datos = request.get_json() or {}
        prompt = datos.get("prompt", "") or datos.get("comando", "") or "Video de prueba automatizado"
        canal = datos.get("canal", "YouTube")
        preferencia = datos.get("preferencia", "animado")
        
        creador = CreadorVideoIA()
        resultado = creador.procesar_campana_por_canal(canal, preferencia, prompt, "Producto General")

        return jsonify({
            "status": "success",
            "mensaje": "Solicitud de video recibida correctamente",
            "prompt": prompt,
            "resultado": resultado
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500

# ---------------------------------------------------------
# PRUEBA RÁPIDA HEYGEN
# ---------------------------------------------------------
@app.route('/test-heygen', methods=['GET', 'POST'])
def test_heygen():
    creador = CreadorVideoIA()
    resultado = creador.generar_video_hiperrealista(
        guion="Hola, esta es una prueba desde Render conectando HeyGen.",
        producto_hotmart="Test HeyGen"
    )
    return jsonify(resultado), 200

@app.route('/webhook_hotmart', methods=['POST'])
def webhook_hotmart():
    try:
        datos = request.get_json() or {}
        comprador = datos.get("buyer", {}).get("name", "Cliente Desconocido")
        email = datos.get("buyer", {}).get("email", "sin_email@dominio.com")
        producto_nombre = datos.get("product", {}).get("name", "Producto Digital")
        precio = datos.get("price", {}).get("value", 0)
        moneda = datos.get("price", {}).get("currency_value", "USD")

        if supabase:
            try:
                registro_venta = {
                    "project_name": "Ventas_Hotmart_Log",
                    "current_step": f"Venta Aprobada: {producto_nombre}",
                    "summary": f"Comprador: {comprador} ({email}) | Valor: {precio} {moneda}",
                    "updated_at": datetime.now().isoformat()
                }
                supabase.table('project_memory').upsert(registro_venta).execute()
            except Exception as e:
                print(f"[-] Nota Supabase Venta: {e}")

        return jsonify({'status': 'recibido', 'mensaje': 'Venta registrada con éxito'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 400

@app.route('/memoria', methods=['GET'])
def obtener_memoria():
    return jsonify({
        'status': 'éxito',
        'mensaje': 'Servidor activo',
        'modulos_activos': {
            'hotmart': hotmart_bp is not None,
            'youtube': YOUTUBE_API_KEY is not None,
            'avatar_voz': avatar_voz_bp is not None,
            'orquestador': orquestador_bp is not None,
            'whatsapp': whatsapp_bp is not None,
            'elevenlabs': elevenlabs_client is not None,
            'heygen': os.getenv("HEYGEN_API_KEY") is not None,
            'redes': redes_bp is not None,
            'creador_video': True,
            'canva': modulo_canva is not None
        }
    }), 200

@app.route('/generar_campana', methods=['POST'])
def generar_campana():
    try:
        datos = request.get_json() or {}
        nicho = datos.get("nicho", "Educación Canina")
        tema_o_producto = datos.get("tema", "Ladridos Nocturnos")
        
        analisis = {}
        if AgenteCazadorTendencias:
            cazador = AgenteCazadorTendencias()
            analisis = cazador.analizar_nicho_ganador(nicho)
        
        creador = CreadorVideoIA()
        guion_organico = creador.generar_guion_organico(nicho, tema_o_producto)
        guion_ads = creador.generar_guion_facebook_ads(f"Curso de {nicho}", tema_o_producto)
        
        analisis_ia = "Motor IA no disponible"
        if MotorIA:
            ia = MotorIA()
            analisis_ia = ia.consultar_ia_estrategica("Experto en Tráfico", f"Analizar nicho {nicho}")
        
        return jsonify({
            "status": "éxito",
            "analisis_mercado": analisis,
            "estrategia_ia": analisis_ia,
            "video_organico_yt_tiktok": guion_organico,
            "anuncio_facebook_ads": guion_ads
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500

@app.route('/generar-video-canal', methods=['POST'])
def generar_video_canal():
    try:
        datos = request.get_json() or {}
        data_canal = datos.get('canal', 'YouTube')
        preferencia = datos.get('preferencia', 'animado')
        guion = datos.get('guion', 'Guion predeterminado')
        producto = datos.get('producto', 'Producto Digital')

        creador = CreadorVideoIA()
        url_video = creador.procesar_campana_por_canal(data_canal, preferencia, guion, producto)

        return jsonify({
            "status": "success",
            "mensaje": f"Video procesado para el canal {data_canal}",
            "resultado": url_video
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500

@app.route('/generar_audio_elevenlabs', methods=['POST'])
def generar_audio_elevenlabs():
    try:
        if not elevenlabs_client:
            return jsonify({'status': 'error', 'mensaje': 'Cliente de ElevenLabs no configurado'}), 500

        datos = request.get_json() or {}
        texto = datos.get("texto", "")
        nombre_archivo = datos.get("nombre_archivo", "narracion_generada.mp3")

        if not texto:
            return jsonify({'status': 'error', 'mensaje': 'El texto es obligatorio'}), 400

        try:
            audio_stream = elevenlabs_client.text_to_speech.convert(
                voice_id="pNInz6obpgDQGcFmaJgB",
                text=texto,
                model_id="eleven_multilingual_v2"
            )
        except AttributeError:
            audio_stream = elevenlabs_client.generate(
                text=texto,
                voice="Adam",
                model="eleven_multilingual_v2"
            )

        folder = app.static_folder or "static"
        os.makedirs(folder, exist_ok=True)
        ruta_salida = os.path.join(folder, nombre_archivo)
        
        with open(ruta_salida, "wb") as f:
            if isinstance(audio_stream, bytes):
                f.write(audio_stream)
            else:
                for chunk in audio_stream:
                    f.write(chunk)

        return jsonify({
            'status': 'éxito',
            'mensaje': 'Audio generado con éxito con ElevenLabs',
            'archivo_url': f"/{nombre_archivo}"
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500

# ---------------------------------------------------------
# RUTA / ENDPOINT DE CANVA
# ---------------------------------------------------------
@app.route('/canva/crear', methods=['POST'])
def generar_grafico_canva():
    try:
        if not modulo_canva:
            return jsonify({'status': 'error', 'mensaje': 'El módulo de Canva no se encuentra cargado'}), 500

        datos = request.get_json() or {}
        titulo = datos.get("titulo", "Campaña automatizada")
        nicho = datos.get("nicho", "Marketing")

        canva = modulo_canva.ModuloCanva()
        resultado = canva.crear_grafico_campaña(titulo, nicho)

        return jsonify({
            "status": "success",
            "mensaje": "Gráfico generado con Canva exitosamente",
            "detalle": resultado
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500

# ---------------------------------------------------------
# RUTAS ADICIONALES DE AUTOMATIZACIÓN (PROTEGIDAS PARA NUBE)
# ---------------------------------------------------------
@app.route('/crear_proyecto', methods=['POST'])
def crear_proyecto():
    try:
        datos = request.get_json() or {}
        nombre_proyecto = datos.get("nombre", "nuevo_proyecto")
        
        ruta_base = os.path.join(os.path.expanduser("~"), "Desktop", nombre_proyecto)
        try:
            os.makedirs(ruta_base, exist_ok=True)
            os.makedirs(os.path.join(ruta_base, "audios"), exist_ok=True)
            os.makedirs(os.path.join(ruta_base, "videos"), exist_ok=True)
            os.makedirs(os.path.join(ruta_base, "guiones"), exist_ok=True)
        except Exception as e_dir:
            print(f"[-] Nota carpetas locales: {e_dir}")
        
        if supabase:
            try:
                supabase.table('project_memory').upsert({
                    "project_name": nombre_proyecto,
                    "current_step": "Proyecto Creado",
                    "summary": f"Estructura registrada para {nombre_proyecto}",
                    "updated_at": datetime.now().isoformat()
                }).execute()
            except Exception as e:
                print(f"[-] Nota Supabase Proyecto: {e}")

        return jsonify({
            'status': 'éxito',
            'mensaje': f'Proyecto {nombre_proyecto} registrado correctamente',
            'ruta': ruta_base
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500

@app.route('/abrir_carpeta', methods=['POST'])
def abrir_carpeta():
    try:
        datos = request.get_json() or {}
        ruta = datos.get("ruta", "")
        if not ruta:
            ruta = os.path.expanduser("~")
            
        if os.path.exists(ruta):
            try:
                if hasattr(os, 'startfile'):
                    os.startfile(ruta)
                else:
                    subprocess.Popen(['xdg-open', ruta])
            except Exception as e_open:
                print(f"[-] Nota apertura carpeta: {e_open}")
            return jsonify({'status': 'éxito', 'mensaje': f'Ruta procesada: {ruta}'}), 200
        else:
            return jsonify({'status': 'error', 'mensaje': 'La ruta especificada no existe'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500

# ---------------------------------------------------------
# ENDPOINT PRINCIPAL (COMANDO GENERAL Y GEMINI)
# ---------------------------------------------------------
@app.route('/api/comando', methods=['POST'])
def ejecutar_comando():
    try:
        datos = request.get_json() or {}
        comando_texto = datos.get('comando', '').strip()
        comando_lower = comando_texto.lower()

        # 1. ACCIONES LOCALES (Solo si está ejecutándose localmente en Windows)
        if os.name == 'nt':
            try:
                if any(w in comando_lower for w in ["bloc de notas", "notepad"]):
                    subprocess.Popen(["notepad.exe"])
                    return jsonify({'respuesta': "Abriendo el Bloc de Notas..."}), 200

                elif any(w in comando_lower for w in ["calculadora", "calc"]):
                    subprocess.Popen(["calc.exe"])
                    return jsonify({'respuesta': "Abriendo la calculadora..."}), 200

                elif any(w in comando_lower for w in ["chrome", "navegador", "internet"]):
                    subprocess.Popen(["cmd", "/c", "start", "chrome"])
                    return jsonify({'respuesta': "Abriendo Google Chrome..."}), 200

                elif any(w in comando_lower for w in ["abrir carpeta", "explorador"]):
                    ruta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
                    if hasattr(os, 'startfile'):
                        os.startfile(ruta_escritorio)
                    return jsonify({'respuesta': "Abriendo el explorador de archivos..."}), 200
            except Exception as e_local:
                print(f"[-] Excepción acción local: {e_local}")

        # 2. PROMPT PARA GEMINI IA
        if GEMINI_API_KEY:
            prompt_sistema = (
                "Eres un asistente de IA útil, directo y conversacional. "
                "INSTRUCCIONES CLAVE DE RESPUESTA:\n"
                "- Si la pregunta del usuario es una duda directa, una operación matemática, un dato rápido o una conversación normal, "
                "responde de forma muy concisa, precisa y directa.\n"
                "- Solo si el usuario solicita explícitamente un guión, una estrategia de ventas, un plan de marketing o un contenido amplio, "
                "responde desplegando una estructura profesional paso a paso.\n\n"
                f"Consulta recibida: {comando_texto}"
            )

            modelos_compatibles = ['gemini-2.0-flash', 'gemini-1.5-flash']
            
            for nombre_modelo in modelos_compatibles:
                try:
                    model = genai.GenerativeModel(nombre_modelo)
                    response = model.generate_content(prompt_sistema)
                    if response and response.text:
                        return jsonify({'respuesta': response.text}), 200
                except Exception:
                    continue

        if any(w in comando_lower for w in ["hola", "buenas", "saludos"]):
            return jsonify({'respuesta': "¡Hola! 👋 ¿En qué te puedo colaborar hoy?"}), 200

        return jsonify({'respuesta': f"Entendí tu consulta sobre '{comando_texto}'."}), 200

    except Exception as e:
        return jsonify({'respuesta': f"Error interno del servidor: {str(e)}"}), 500

# ---------------------------------------------------------
# ARRANQUE DEL SERVIDOR FLASK
# ---------------------------------------------------------
if __name__ == '__main__':
    print("🚀 Servidor Controlador IA iniciado...")
    print("📍 Escuchando en http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)