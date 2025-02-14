![Logo](/img/logo.png)  ![Titulo](/img/titulo.png) 

# GranaBus. Bus Schedule Bot for Granada

## Introduction

This project is a Telegram bot designed to provide real-time bus schedules for interurban routes in Granada, Spain. Initially conceived as a learning exercise to gain experience with APIs, it has evolved into a functional and potentially useful tool for residents and visitors of Granada.

## Features

- **Real-Time Bus Schedules**: Retrieve up-to-date bus arrival times for interurban routes.
- **Bus Stop Search**: Search for bus stops by name, regardless of case sensitivity or accentuation.
- **Location Sharing**: Receive the geographical location of a selected bus stop.

## Deployment

The bot is deployed using [Railway](https://railway.app/), a platform that facilitates seamless deployment of applications. This project is my first experience using Railway to deploy an application to the cloud. Although I have followed the steps carefully, since it is my first attempt, you might encounter some errors or configurations that still need adjustment. 


## Usage

🔗 You can find the bot in this link [ t.me/GranaBusBot](t.me/GranaBusBot) 

1. **Start the Bot**: Initiate a conversation with the bot by sending the `/start` command.
2. **Help Command**: Use the `/help` command to receive instructions on how to interact with the bot.
3. **View Available Nuclei**: Send the `/paradas` command to view a list of available nuclei (areas).
4. **Select a Nucleus**: Type the name of a nucleus to see the bus stops within that area.
5. **Get Bus Schedules**: Enter the name of a bus stop to receive the upcoming bus schedules and the location of the stop.

**Note**: Ensure that bus stop names are entered with correct accents (e.g., "Río de Monachil" instead of "Rio de Monachil"). The bot is designed to handle both uppercase and lowercase inputs.

## Legal and Data Usage

This bot utilizes data from the [Consorcio de Transporte Metropolitano del Área de Granada](https://api.ctan.es/doc/#api-Paradas-ObtieneServiciosPorParada). The data is publicly accessible and used in accordance with the terms and conditions outlined by the API provider. Users are advised that this bot does not provide schedules for urban buses within Granada city, as those services are managed by a different entity, [Transportes Rober](https://www.transportesrober.com/informacio/contacto.htm).

## Disclaimer

This project was developed for educational purposes to gain experience in API integration and bot development. While it has been tested and functions as intended, users should verify critical information through official channels when necessary.

---

## Usage example

| Screenshot 1 | Screenshot 2 | Screenshot 3 | Screenshot 4 |
|--------------|--------------|--------------|--------------|
| ![Image 1](/img/start.jpg) | ![Image 2](/img/help.jpg) | ![Image 3](/img/paradas.jpg) | ![Image 4](/img/ejemplo-ortografia.jpg) |


---

# GranaBus. Bot de Horarios de Autobuses para Granada

## Introducción

Este proyecto es un bot de Telegram diseñado para proporcionar horarios de autobuses interurbanos en tiempo real en Granada, España. Inicialmente concebido como un ejercicio de aprendizaje para ganar experiencia con APIs, ha evolucionado hasta convertirse en una herramienta funcional y potencialmente útil para residentes y visitantes de Granada.

## Características

- **Horarios de Autobuses en Tiempo Real**: Obtén los horarios actualizados de llegada de autobuses para rutas interurbanas.
- **Búsqueda de Paradas**: Busca paradas de autobús por nombre, sin importar mayúsculas, minúsculas o acentuación.
- **Compartir Ubicación**: Recibe la ubicación geográfica de una parada de autobús seleccionada.

## Despliegue

El bot está desplegado utilizando [Railway](https://railway.app/), una plataforma que facilita el despliegue sin problemas de aplicaciones. Este proyecto es mi primera experiencia utilizando Railway para el despliegue de una aplicación en la nube. Aunque he seguido los pasos cuidadosamente, dado que es mi primer intento, es posible que encuentres algunos errores o configuraciones que aún necesiten ajuste.


## Uso

🔗 Puedes encontrar el bot en este link [ t.me/GranaBusBot](t.me/GranaBusBot) 

1. **Iniciar el Bot**: Inicia una conversación con el bot enviando el comando `/start`.
2. **Comando de Ayuda**: Utiliza el comando `/help` para recibir instrucciones sobre cómo interactuar con el bot.
3. **Ver Núcleos Disponibles**: Envía el comando `/paradas` para ver una lista de núcleos (áreas) disponibles.
4. **Seleccionar un Núcleo**: Escribe el nombre de un núcleo para ver las paradas de autobús en esa área.
5. **Obtener Horarios de Autobuses**: Ingresa el nombre de una parada de autobús para recibir los próximos horarios y la ubicación de la parada.

**Nota**: Asegúrate de ingresar los nombres de las paradas con las tildes correctas (por ejemplo, "Río de Monachil" en lugar de "Rio de Monachil"). El bot está diseñado para manejar entradas en mayúsculas y minúsculas.

## Aspectos Legales y Uso de Datos

Este bot utiliza datos del [Consorcio de Transporte Metropolitano del Área de Granada](https://api.ctan.es/doc/#api-Paradas-ObtieneServiciosPorParada). Los datos son de acceso público y se utilizan de acuerdo con los términos y condiciones establecidos por el proveedor de la API. Se informa a los usuarios que este bot no proporciona horarios para los autobuses urbanos dentro de la ciudad de Granada, ya que esos servicios son gestionados por otra entidad, [Transportes Rober](https://www.transportesrober.com/informacio/contacto.htm).

## Responsabilidad

Este proyecto fue desarrollado con fines educativos para ganar experiencia en la integración de APIs y desarrollo de bots. Aunque ha sido probado y funciona según lo previsto, los usuarios deben verificar información crítica a través de los canales oficiales cuando sea necesario.

### Autora:
Blanca Girón