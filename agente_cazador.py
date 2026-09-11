import json
import time

class AgenteCazadorTendencias:
    def __init__(self, presupuesto_diario_usd=5.0):
        self.presupuesto_diario = presupuesto_diario_usd
        self.paises_objetivo = ["Colombia", "México", "Perú", "Chile", "Ecuador"]
        
    def analizar_nicho_ganador(self, tema_o_nicho):
        print(f"🔍 [AGENTE CAZADOR] Rastreando tendencias para el nicho: '{tema_o_nicho}'...")
        time.sleep(1) # Simulación de rastreo en tiempo real
        
        # Estructura de salida optimizada para conectar con Hotmart y Meta Ads
        resultado_analisis = {
            "nicho": tema_o_nicho,
            "potencial_viral": "ALTO",
            "temperatura_estimada_hotmart": "45° - 80° (Ideal para afiliados)",
            "publico_objetivo": {
                "edades": "22 - 48 años",
                "paises": self.paises_objetivo,
                "intereses_clave": [f"Cursos de {tema_o_nicho}", "Emprendimiento", "Desarrollo Personal"]
            },
            "estrategia_contenido": {
                "angulo_organico_tiktok_yt": "Historias de impacto / Curiosidades de alto enganche",
                "angulo_ads_facebook": "Anuncio UGC realista enfocado en resolver un problema urgente",
                "presupuesto_testeo": f"${self.presupuesto_diario} USD/día"
            }
        }
        return resultado_analisis

# --- PRUEBA DEL MÓDULO 1 ---
if __name__ == "__main__":
    cazador = AgenteCazadorTendencias(presupuesto_diario_usd=5.0)
    
    # Probamos con un nicho de ejemplo
    ficha_tecnica = cazador.analizar_nicho_ganador("Educación Canina / Adiestramiento")
    print("\n✅ [FICHA TÉCNICA GENERADA PARA EL MÓDULO 2]:")
    print(json.dumps(ficha_tecnica, indent=4, ensure_ascii=False))