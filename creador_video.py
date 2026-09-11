import json

class CreadorVideoIA:
    def __init__(self):
        self.estilo_voz_organico = "Emotiva / Suspenso / Narrador Profundo"
        self.estilo_voz_ads = "Avatar UGC Realista / Entusiasta y Persuasivo"

    def generar_guion_organico(self, nicho, tema_especifico):
        """Genera guion optimizado para algortimos de YouTube Shorts y TikTok"""
        guion = {
            "plataforma": "YouTube Shorts / TikTok",
            "tipo_contenido": "Orgánico Viral",
            "nicho": nicho,
            "seo_metadata": {
                "titulo_viral": f"¡Lo que NUNCA te contaron sobre {tema_especifico}! 😱",
                "hashtags": [f"#{nicho.replace(' ', '')}", "#DatosCuriosos", "#Viral", "#Historias"],
                "descripcion": f"Descubre la verdad detrás de {tema_especifico}. Suscríbete para más historias increíbles."
            },
            "estructura_video": {
                "gancho_0_3_seg": f"¿Sabías que el 99% de las personas comete este grave error con {tema_especifico}?",
                "desarrollo_historia": "Tensión dramática, cambio de tomas rápido cada 2 segundos y subtítulos resaltados en amarillo.",
                "llamado_accion_cta": "Guarda este video y síguenos para no perderte la parte 2."
            },
            "instrucciones_ia_visual": "Imágenes sombrías estilo cómic/ilustración 3D, iluminaciones contrastadas y música de piano/suspenso de fondo."
        }
        return guion

    def generar_guion_facebook_ads(self, producto_hotmart, problema_principal):
        """Genera guion con estructura AIDA para conversión y ventas en Hotmart"""
        guion = {
            "plataforma": "Facebook Ads / Meta",
            "tipo_contenido": "Anuncio de Venta Directa",
            "producto": producto_hotmart,
            "estructura_aida": {
                "atencion": f"Si tienes problemas con {problema_principal}, detén este video un segundo...",
                "interes": f"Cientos de personas ya están resolviendo esto desde casa con este método paso a paso.",
                "deseo": "Muestra de pantalla por dentro del curso, certificados y resultados reales sin salir de casa.",
                "accion_cta": "Toca el botón de abajo ahora mismo y accede con el 50% de descuento solo por hoy."
            },
            "formato_visual": "Avatar UGC hiperrealista hablando directo a la cámara con subtítulos limpios y tomas del producto."
        }
        return guion

# --- PRUEBA DEL MÓDULO 2 ---
if __name__ == "__main__":
    creador = CreadorVideoIA()
    
    # 1. Ejemplo para canal orgánico (YouTube / TikTok)
    guion_organico = creador.generar_guion_organico("Educación Canina", "los ladridos nocturnos")
    print("✅ [GUION ORGANICO GENERADO]:")
    print(json.dumps(guion_organico, indent=4, ensure_ascii=False))
    
    # 2. Ejemplo para Facebook Ads (Hotmart)
    guion_ads = creador.generar_guion_facebook_ads("Curso de Adiestramiento Canino", "perros que muerden los muebles")
    print("\n✅ [GUION FACEBOOK ADS GENERADO]:")
    print(json.dumps(guion_ads, indent=4, ensure_ascii=False))