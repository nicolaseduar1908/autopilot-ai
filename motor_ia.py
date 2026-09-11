import os
import json

class MotorIA:
    def __init__(self):
        # Aquí configuraremos la llave de la API (OpenAI o Anthropic)
        self.api_key = os.getenv("OPENAI_API_KEY", "TU_API_KEY_AQUI")
        
    def consultar_ia_estrategica(self, prompt_sistema, prompt_usuario):
        """
        Función central para conectarse con la IA y generar contenido real.
        Por ahora simula la respuesta inteligente lista para conectar con la API real.
        """
        print(f"🤖 [MOTOR IA] Procesando solicitud con IA...")
        
        # Simulación de respuesta inteligente de IA orientada a conversión
        if "nicho" in prompt_usuario.lower():
            return {
                "estado": "generado_por_ia",
                "analisis_real": f"Tendencia detectada con alta demanda en LATAM para el nicho consultado. Oportunidad de ROAS x3 en Meta Ads."
            }
        else:
            return {
                "estado": "generado_por_ia",
                "guion_ia": "Gancho agresivo de 3 segundos + Historia de transformación + Llamado a la acción irresistible."
            }

# --- PRUEBA DEL MÓDULO 3 ---
if __name__ == "__main__":
    ia = MotorIA()
    respuesta = ia.consultar_ia_estrategica("Eres un experto en marketing", "Analiza el nicho de repostería saludable")
    print(json.dumps(respuesta, indent=4, ensure_ascii=False))