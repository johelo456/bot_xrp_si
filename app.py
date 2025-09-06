# app.py - Archivo SEPARADO para Flask
from flask import Flask
import threading
import os

app = Flask(__name__)

# Variable para controlar si el bot ya está corriendo
bot_started = False

@app.route('/')
def home():
    return "🤖 XRP Bot está funcionando correctamente! 🚀"

@app.route('/health')
def health():
    return "✅ Bot saludable"

def start_bot():
    """Función para iniciar el bot en un hilo separado"""
    global bot_started
    if not bot_started:
        print("Iniciando bot de Telegram...")
        try:
            from main import main
            main()
        except Exception as e:
            print(f"Error iniciando bot: {e}")
        bot_started = True

# Iniciar el bot cuando la app se levante
if __name__ == '__main__':
    # Iniciar el bot en un hilo separado
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Iniciar Flask
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
