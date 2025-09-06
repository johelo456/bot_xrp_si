import os

# Leer tokens desde variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Verificar que los tokens estén disponibles
if not TELEGRAM_TOKEN:
    print("ERROR: No se encontró el token de Telegram (setea TELEGRAM_TOKEN)")
    
if not OPENAI_API_KEY:
    print("ERROR: No se encontró la API key de OpenAI (setea OPENAI_API_KEY)")
