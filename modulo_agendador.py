import os
import random
from datetime import datetime, timedelta
from supabase import create_client, Client

# Configuración de URL y Secret Key de Supabase
URL_SUPABASE = "https://edogknzbnipcwxcfvzuz.supabase.co"
KEY_SUPABASE = "sb_secret_VBCrdBeVEysr9GCsBT5JtA_3-ET5-wz"

supabase: Client = create_client(URL_SUPABASE, KEY_SUPABASE)

def aplicar_jitter_horario(hora_base_str):
    """Suma un jitter aleatorio de -5 a +12 minutos para evitar patrones de bots."""
    formato = "%H:%M"
    hora_dt = datetime.strptime(hora_base_str, formato)
    minutos_variacion = random.randint(-5, 12)
    hora_ajustada = hora_dt + timedelta(minutes=minutos_variacion)
    return hora_ajustada.strftime("%H:%M")

def procesar_cola_canales():
    print("🤖 [AGENDADOR IA] Escaneando canales activos en Supabase...\n")
    
    # Consultar la tabla de canales
    respuesta = supabase.table("canales").select("*").eq("estado", "activo").execute()
    canales = respuesta.data

    if not canales:
        print("⚠️ No se encontraron canales activos.")
        return

    for canal in canales:
        print(f"📌 Canal: {canal['nombre_canal']} ({canal['plataforma'].upper()})")
        print(f"🎭 Temática: {canal['tematica']}")
        
        horarios = canal.get("horarios_publicacion", [])
        print("⏰ Programando publicaciones con anti-bot (jitter)...")
        
        for hora in horarios:
            hora_humana = aplicar_jitter_horario(hora)
            print(f"  👉 Video programado para las {hora_humana} hrs (Hora base: {hora})")
        print("-" * 40)

if __name__ == "__main__":
    procesar_cola_canales()