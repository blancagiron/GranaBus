import os
import json
import requests
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, 
    CallbackContext, ConversationHandler
)

# Estados para la conversación
ELEGIR_NUCLEO = 1

# Cargar datos de paradas desde el archivo JSON
with open("paradas_granada.json", "r", encoding="utf-8") as file:
    paradas_data = json.load(file)

paradas_lista = paradas_data.get("paradas", [])

# Diccionarios
nucleos_dict = {}
paradas_dict = {}

for parada in paradas_lista:
    nombre_nucleo = parada["nucleo"].lower()
    nombre_parada = parada["nombre"].lower()
    id_parada = parada["idParada"]

    if nombre_nucleo not in nucleos_dict:
        nucleos_dict[nombre_nucleo] = []
    nucleos_dict[nombre_nucleo].append(nombre_parada)

    paradas_dict[nombre_parada] = id_parada

def obtener_horarios(id_parada):
    url = f"http://api.ctan.es/v1/Consorcios/3/paradas/{id_parada}/servicios"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data.get("servicios", [])
        except json.JSONDecodeError:
            return None
    return None

# Comandos del bot
async def start(update: Update, context: CallbackContext):
    with open("txt/welcome.txt", "r", encoding="utf-8") as file:
        mensaje = file.read()
    
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def help(update: Update, context: CallbackContext):
    with open("txt/help.txt", "r", encoding="utf-8") as file:
        mensaje = file.read()
    
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def paradas(update: Update, context: CallbackContext):
    mensaje = "🗺️ Núcleos disponibles:\n\n"
    for nucleo in nucleos_dict.keys():
        mensaje += f"- {nucleo.title()}\n"
    mensaje += "\nEscribe el nombre de un núcleo para ver sus paradas."
    await update.message.reply_text(mensaje)
    return ELEGIR_NUCLEO

async def elegir_nucleo(update: Update, context: CallbackContext):
    nombre_nucleo = update.message.text.lower()
    if nombre_nucleo in nucleos_dict:
        mensaje = f"📍 Paradas en *{nombre_nucleo.title()}*:\n\n"
        for parada in nucleos_dict[nombre_nucleo]:
            mensaje += f"- {parada.title()}\n"
        mensaje += "\nEscribe el nombre de una parada para ver los horarios."
        await update.message.reply_text(mensaje, parse_mode="Markdown")
    else:
        await update.message.reply_text("🚫 Núcleo no encontrado. Inténtalo de nuevo.")
    return ConversationHandler.END

async def handle_message(update: Update, context: CallbackContext):
    nombre_parada = update.message.text.lower()
    if nombre_parada in paradas_dict:
        id_parada = paradas_dict[nombre_parada]
        servicios = obtener_horarios(id_parada)
        if servicios:
            mensaje = f"🚌 Horarios para la parada *{nombre_parada.title()}*:\n"
            for servicio in servicios:
                hora = servicio.get("servicio", "Hora no disponible")
                linea = servicio.get("linea", "Desconocida")
                mensaje += f"🚍 Línea {linea}: {hora}\n"
            await update.message.reply_text(mensaje, parse_mode="Markdown")
        else:
            await update.message.reply_text("⏳ No hay horarios disponibles.")
    else:
        await update.message.reply_text("🚫 Parada no encontrada.")

# Flask para Webhooks
app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
URL = f"https://{os.getenv('RAILWAY_STATIC_URL')}/{TOKEN}"

# Create and initialize application
async def create_application():
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("paradas", paradas))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    await app.initialize()
    await app.start()
    await app.bot.set_webhook(url=URL)
    
    return app

# Create event loop and application
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
application = loop.run_until_complete(create_application())

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        
        async def process_update():
            await application.process_update(update)
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(process_update())
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
            
        return "ok"

@app.route("/")
def home():
    return "¡El bot está funcionando! 🚀"

if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))