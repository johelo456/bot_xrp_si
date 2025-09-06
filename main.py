import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests
from openai import OpenAI
from flask import Flask

# Importar configuración
from config import TELEGRAM_TOKEN, OPENAI_API_KEY

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if not TELEGRAM_TOKEN:
    print("Error: Token de Telegram no configurado")
    exit()

# Configurar OpenAI
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Estado de conversación
conversaciones = {}

# Obtener precio de XRP
def get_xrp_price():
    try:
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT', timeout=10)
        data = response.json()
        return float(data['price'])
    except:
        return None

# Sistema de diálogo inteligente
async def manejar_dialogo(update: Update, context: ContextTypes.DEFAULT_TYPE, mensaje: str):
    user_id = update.effective_user.id
    mensaje = mensaje.lower()
    
    # Palabras clave para diferentes intenciones
    saludos = ['hola', 'hi', 'hello', 'buenas', 'saludos']
    despedidas = ['adiós', 'bye', 'chao', 'nos vemos', 'hasta luego']
    emociones = ['cómo estás', 'qué tal', 'cómo te sientes']
    agradecimientos = ['gracias', 'thanks', 'thank you', 'te lo agradezco']
    
    if any(palabra in mensaje for palabra in saludos):
        return "¡Hola! 👋 Soy tu asistente de XRP. ¿En qué puedo ayudarte hoy?"
    
    elif any(palabra in mensaje for palabra in despedidas):
        return "¡Hasta luego! 😊 Recuerda que estoy aquí para ayudarte con XRP y criptomonedas."
    
    elif any(palabra in mensaje for palabra in emociones):
        return "¡Estoy excelente! 💙 Listo para ayudarte con análisis de XRP y inversiones."
    
    elif any(palabra in mensaje for palabra in agradecimientos):
        return "¡De nada! 😊 Estoy aquí para ayudarte. ¿Necesitas algo más sobre XRP?"
    
    elif 'qué puedes hacer' in mensaje or 'qué haces' in mensaje:
        return "Puedo ayudarte con: 📊 Precio de XRP, 📈 Análisis técnico, 🔔 Alertas, 💰 Inversiones hasta 200K COP, y conversar contigo sobre cripto."
    
    elif 'nombre' in mensaje:
        return "Soy XRP Assistant, tu experto en criptomonedas y especialmente en XRP. 😊"
    
    elif 'ayuda' in mensaje:
        return "Puedo ayudarte con: /price, /analysis, /news, /alerts, /portfolio. También podemos conversar sobre cripto."
    
    # Si no coincide con nada específico, usar OpenAI para respuesta conversacional
    if client:
        try:
            respuesta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente amable de criptomonedas especializado en XRP. Responde de forma conversacional y útil."},
                    {"role": "user", "content": mensaje}
                ],
                max_tokens=150
            )
            return respuesta.choices[0].message.content
        except:
            pass
    
    # Respuesta por defecto
    respuestas_default = [
        "Interesante pregunta sobre cripto. ¿Te gustaría saber el precio actual de XRP?",
        "Buena consulta. ¿Quieres que analice XRP para tu inversión?",
        "Puedo ayudarte mejor con comandos como /price o /analysis. ¿Qué necesitas?",
        "Como asistente de XRP, puedo darte precios, análisis y recomendaciones. ¿En qué te ayudo?"
    ]
    return random.choice(respuestas_default)

# Comando /start mejorado
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = f"""
¡Hola {user.first_name}! 👋 Soy tu asistente especializado en XRP.

💬 *Puedo conversar contigo* sobre:
• Precios y análisis de XRP
• Inversiones en cripto (80K-200K COP)
• Noticias del mercado
• Estrategias de trading

📋 *Comandos disponibles:*
/price - Precio actual de XRP
/analysis - Análisis técnico completo  
/news - Últimas noticias
/alerts - Configurar alertas
/portfolio - Tu portafolio

💡 *También puedes escribirme libremente* como:
• "Hola, ¿cómo estás?"
• "¿Qué me recomiendas para invertir?"
• "Cuéntame sobre XRP"
• "¿Cómo va el mercado?"

*¡Estoy aquí para ayudarte!* 🚀
"""
    
    keyboard = [
        [KeyboardButton("💰 Precio XRP"), KeyboardButton("📊 Análisis")],
        [KeyboardButton("💬 Conversar"), KeyboardButton("❓ Ayuda")],
        [KeyboardButton("📰 Noticias"), KeyboardButton("🔔 Alertas")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

# Manejar todos los mensajes de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    # Comandos de botones
    if text == "💰 Precio XRP":
        precio = get_xrp_price()
        if precio:
            precio_cop = precio * 3900
            await update.message.reply_text(f"💰 *XRP:* {precio:.4f} USD\n*≈* {precio_cop:,.0f} COP", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ No pude obtener el precio ahora.")
    
    elif text == "📊 Análisis":
        await update.message.reply_text("🔍 *Analizando XRP...*", parse_mode='Markdown')
        precio = get_xrp_price()
        if precio:
            analisis = f"""
📊 *Análisis Rápido de XRP*

• *Precio:* {precio:.4f} USD
• *Tendencia:* {'📈 Alcista' if precio > 0.58 else '📉 Bajista'}
• *Recomendación:* {'✅ Buena compra' if precio < 0.6 else ⚠️ Esperar'}

*Para inversiones de 80K-200K COP:* 
XRP es buena opción. También considera ADA o MATIC.
"""
            await update.message.reply_text(analisis, parse_mode='Markdown')
    
    elif text == "💬 Conversar":
        await update.message.reply_text("💬 ¡Claro! Puedes preguntarme sobre:\n• Precios de cripto\n• Estrategias de inversión\n• Noticias del mercado\n• Análisis técnico\n\n¿En qué te ayudo?")
    
    elif text == "📰 Noticias":
        await update.message.reply_text("📰 *Últimas de XRP:*\n\n• Ripple sigue creciendo\n• Nuevas asociaciones bancarias\n• Mercado estable esta semana", parse_mode='Markdown')
    
    elif text == "🔔 Alertas":
        await update.message.reply_text("🔔 *Alertas de Precio:*\n\nConfigura alertas con:\n`alertar a 3000 COP`\n`alertar a 0.75 USD`", parse_mode='Markdown')
    
    elif text == "❓ Ayuda":
        await start(update, context)
    
    else:
        # Diálogo inteligente
        respuesta = await manejar_dialogo(update, context, text)
        await update.message.reply_text(respuesta)

# Comandos tradicionales
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    precio = get_xrp_price()
    if precio:
        precio_cop = precio * 3900
        await update.message.reply_text(f"💎 *Precio XRP:*\n\n{precio:.4f} USD\n{precio_cop:,.0f} COP\n\n💡 ¿Quieres análisis? Usa /analysis", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Error obteniendo precio.")

async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 *Analizando XRP...*", parse_mode='Markdown')
    # Tu código de análisis aquí

# Configuración Flask para Render
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 XRP Bot está funcionando!"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Para webhook futuro
    return "OK"

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("analysis", analysis))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Bot iniciado con diálogo inteligente!")
    print("💬 Ahora puede conversar con usuarios")
    
    # Para Render.com, usar webhook o polling
    try:
        application.run_polling()
    except:
        # Fallback para Render
        app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()