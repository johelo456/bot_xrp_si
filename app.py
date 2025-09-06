from flask import Flask
import threading
import os
from main import main  # Importa tu función main

app = Flask(__name__)

# Variable para controlar si el bot ya está corriendo
bot_started = False

@app.route('/')
def home():
    return "🤖 XRP Bot está funcionando correctamente! 🚀"

def start_bot():
    """Función para iniciar el bot en un hilo separado"""
    global bot_started
    if not bot_started:
        print("Iniciando bot de Telegram...")
        try:
            main()
        except Exception as e:
            print(f"Error iniciando bot: {e}")
        bot_started = True

# Iniciar el bot cuando la app se levante
@app.before_first_request
def initialize():
    thread = threading.Thread(target=start_bot)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
