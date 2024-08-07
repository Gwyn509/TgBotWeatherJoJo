import telebot
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
import os

EMOJI_CODE = {200: '⛈',
              201: '⛈',
              202: '⛈',
              210: '🌩',
              211: '🌩',
              212: '🌩',
              221: '🌩',
              230: '⛈',
              231: '⛈',
              232: '⛈',
              301: '🌧',
              302: '🌧',
              310: '🌧',
              311: '🌧',
              312: '🌧',
              313: '🌧',
              314: '🌧',
              321: '🌧',
              500: '🌧',
              501: '🌧',
              502: '🌧',
              503: '🌧',
              504: '🌧',
              511: '🌧',
              520: '🌧',
              521: '🌧',
              522: '🌧',
              531: '🌧',
              600: '🌨',
              601: '🌨',
              602: '🌨',
              611: '🌨',
              612: '🌨',
              613: '🌨',
              615: '🌨',
              616: '🌨',
              620: '🌨',
              621: '🌨',
              622: '🌨',
              701: '🌫',
              711: '🌫',
              721: '🌫',
              731: '🌫',
              741: '🌫',
              751: '🌫',
              761: '🌫',
              762: '🌫',
              771: '🌫',
              781: '🌫',
              800: '☀️',
              801: '🌤',
              802: '☁️',
              803: '☁️',
              804: '☁️'}

load_dotenv()
TOKEN_BOT = os.getenv("TOKEN")
TOKEN_WEATHER = '7d228e7dc45fc69e4b244b144839939b'
URL_WEATHER = 'https://api.openweathermap.org/data/2.5/weather'

bot = telebot.TeleBot(TOKEN_BOT)
KeyB = ReplyKeyboardMarkup(resize_keyboard = True)
KeyB.add(KeyboardButton("Получить погоду", request_location = True))
KeyB.add(KeyboardButton("О проекте"))

@bot.message_handler(commands=["start"])
def send_about(message):
  text = "Отправь мне своё местоположение"
  bot.send_message(message.chat.id, text, reply_markup = KeyB)

@bot.message_handler(regexp = "О проекте")
def send_welcome(message):
    text = '''Бот позволяет получить погоду в текущем местоположении!
Для получения погоды - отправь боту геопозицию.
Погода берется с сайта https://openweathermap.org.'''
    bot.send_message(message.chat.id, text, reply_markup=KeyB)

def get_weather(lat, lon):
    params = {
        "appid" : TOKEN_WEATHER,
        "lat" : lat,
        "lon" : lon,
        "units" : "metric",
        "lang" : "ru"
    }
    responce = requests.get(url = URL_WEATHER, params = params).json()
    emoji = EMOJI_CODE[responce ["weather"][0]["id"]]
    text = f'''🏙Погода в: {responce ["name"]}
{emoji} {responce ["weather"][0]["description"]}
🌡Температура {round(responce ["main"]["temp"])}{chr(8451)}
🌡Ощущается {round(responce ["main"]["temp"])}{chr(8451)}
💧Влажность {responce["main"]["humidity"]}
'''
    return text


@bot.message_handler(content_types=['location'])
def send_weather(message):
    lat = message.location.latitude
    lon = message.location.latitude
    result = get_weather(lat, lon)
    bot.send_message(message.chat.id, result, reply_markup=KeyB)

bot.infinity_polling()