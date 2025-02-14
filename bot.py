import os
import json
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
import asyncio

ELEGIR_NUCLEO = 1

# Se cargan los datos desde el archivo JSON de paradas, este archivo se ha generado previamente con una petición a la API. 
# Se ha hecho así porque no he encontrado los ID de las paradas interurbanas, por lo que he necesitado hacer una petición a la API para obtenerlos.
# Se mapea porque para el usuario es más fácil buscar por nombre de parada que por ID.

with open("paradas_granada.json", "r", encoding="utf-8") as file:
    paradas_data = json.load(file)

paradas_lista = paradas_data.get("paradas", [])

nucleos_dict = {} # Diccionario para mapear núcleos con paradas
paradas_dict = {} # Diccionario para mapear paradas con ID

for parada in paradas_lista:
    nombre_nucleo = parada["nucleo"].lower()
    nombre_parada = parada["nombre"].lower()
    id_parada = parada["idParada"]
    if nombre_nucleo not in nucleos_dict:
        nucleos_dict[nombre_nucleo] = []
    nucleos_dict[nombre_nucleo].append(nombre_parada)
    paradas_dict[nombre_parada] = id_parada

def obtener_horarios(id_parada):
    url = f"http://api.ctan.es/v1/Consorcios/3/paradas/{id_parada}/servicios" # se obtienen servicios haciendo una petición a la API con el ID de la parada
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data.get("servicios", [])
        except:
            return None
    return None

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

# El comando /paradas sirve para que el usuario pueda ver las paradas, pero como hay muchas paradas, se le pide que elija un núcleo primero.
# Una vez que el usuario elige un núcleo, se le muestran las paradas de ese núcleo.
# Por eso se usa un ConversationHandler para manejar el estado de la conversación.
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


# Manejo de mensajes de texto que no sean comandos
async def handle_message(update: Update, context: CallbackContext):
    nombre_parada = update.message.text.lower()
    if nombre_parada in paradas_dict: # Si el nombre de la parada está en el diccionario de paradas, se obtienen los horarios
        id_parada = paradas_dict[nombre_parada]  # Se obtiene el ID de la parada
        servicios = obtener_horarios(id_parada) # Se obtienen los horarios

         # Buscar la latitud y longitud de la parada
        parada_info = next((p for p in paradas_lista if p["idParada"] == id_parada), None)

        if servicios:
            mensaje = f"🚌 Horarios para la parada *{nombre_parada.title()}*:\n"
            for servicio in servicios:
                hora = servicio.get("servicio", "Hora no disponible")
                linea = servicio.get("linea", "Desconocida")
                mensaje += f"🚍 Línea {linea}: {hora}\n"
            await update.message.reply_text(mensaje, parse_mode="Markdown")

            if parada_info:
                latitud = parada_info["latitud"]
                longitud = parada_info["longitud"]
                await update.message.reply_location(latitude=latitud, longitude=longitud)
            else:
                await update.message.reply_text("📍 Ubicación no disponible para esta parada.")
        else:
            await update.message.reply_text("⏳ No hay horarios disponibles.")
    else:
        await update.message.reply_text("🚫 Parada no encontrada.")

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
URL = f"https://{os.getenv('RAILWAY_STATIC_URL')}/{TOKEN}"

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Configuración del bot

application = Application.builder().token(TOKEN).build() # Se crea la aplicación del bot con el token
conv_handler = ConversationHandler( # manejar conversacion de paradas 
    entry_points=[CommandHandler("paradas", paradas)],
    states={ELEGIR_NUCLEO: [MessageHandler(filters.TEXT & ~filters.COMMAND, elegir_nucleo)]}, # Se espera mensaje que no sea comando
    fallbacks=[]
)
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help))
application.add_handler(conv_handler)
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

loop.run_until_complete(application.initialize())
loop.run_until_complete(application.start())
loop.run_until_complete(application.bot.set_webhook(url=URL))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        loop.run_until_complete(application.process_update(update))
        return "ok"

@app.route("/")
def home():
    return "¡El bot está funcionando! 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))