import requests

class ModuloCanva:
    def __init__(self):
        print("[CANVA] Módulo de diseño inicializado correctamente.")

    def crear_grafico_campaña(self, titulo_campaña, nicho):
        print(f"[CANVA] Generando gráfico para el nicho '{nicho}' con el título: '{titulo_campaña}'")
        return {
            "estado": "exito",
            "url_imagen": "https://placeholder.com/diseno_campaña.png"
        }

if __name__ == "__main__":
    canva = ModuloCanva()
    canva.crear_grafico_campaña("Cómo organizar tu presupuesto", "Finanzas Personales")