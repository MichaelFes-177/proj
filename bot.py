import telebot
import pyowm
import pyowm.exceptions
import time as tm
from telebot import types
from pyowm.exceptions import api_response_error
from config import BOT_TOKEN, OWM_TOKEN
from utils.weather import get_forecast
from utils.world_time import get_time
from utils.news import get_article
from utils.stocks import *
from utils.crypto_coins import *
from utils.translate import *
from googletrans import Translator

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
owm = pyowm.OWM(OWM_TOKEN)
trans = Translator()


@bot.message_handler(commands=['start'])
def command_start(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time', '/news')
	start_markup.row('/crypto', '/stocks', '/translate')
	bot.send_message(message.chat.id, "🤖 Бот запустился!\n⚙ Нажми  /help чтобы увидеть все функции")
	bot.send_message(message.from_user.id, "⌨️ Добавлена клавиатура", reply_markup=start_markup)


@bot.message_handler(commands=['hide'])
def command_hide(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, "⌨💤...", reply_markup=hide_markup)


@bot.message_handler(commands=['help'])
def command_help(message):
	bot.send_message(message.chat.id, "🤖 /start - display the keyboard\n"
									  "☁ /Погода\n"
									  "💎 /криптовалюта\n"
									  "⌛️ /Время\n"
									  "📰 /Новости\n"
									  "🔁 /Перевод")


@bot.message_handler(commands=['weather'])
def command_weather(message):
	sent = bot.send_message(message.chat.id, "🗺 Enter the City or Country\n🔍 In such format:  Toronto  or  japan")
	bot.register_next_step_handler(sent, send_forecast)


def send_forecast(message):
	try:
		get_forecast(message.text)
	except pyowm.exceptions.api_response_error.NotFoundError:
		bot.send_message(message.chat.id, "❌  Wrong place, check mistakes and try again!")
	forecast = get_forecast(message.text)
	bot.send_message(message.chat.id, forecast)


@bot.message_handler(commands=['world_time'])
def command_world_time(message):
	sent = bot.send_message(message.chat.id, "🗺 Введи название города\n🔍 например:  Moscow  или  china")
	bot.register_next_step_handler(sent, send_time)


def send_time(message):
	try:
		get_time(message.text)
	except IndexError:
		bot.send_message(message.chat.id, "❌ Wrong place, check mistakes and try again")
	time = get_time(message.text)
	bot.send_message(message.chat.id, time)


@bot.message_handler(commands=['news'])
def command_news(message):
	bot.send_message(message.chat.id, f"🆕 Latest BBC article:\n{get_article()}")
	bot.send_message(message.chat.id, get_article(), parse_mode='HTML')


@bot.message_handler(commands=['crypto'])
def command_crypto(message):
	coins_markup = types.InlineKeyboardMarkup(row_width=1)
	for key, value in coins.items():
		coins_markup.add(types.InlineKeyboardButton(text=key, callback_data=value))
	bot.send_message(message.chat.id, "📃 Choose the coin:", reply_markup=coins_markup)


@bot.message_handler(commands=['translate'])
def command_translate(message):
	trans_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	trans_markup.row('German', 'French', 'Spanish')
	trans_markup.row('Russian', 'Japanese', 'Polish')
	sent = bot.send_message(message.chat.id, "📃 Choose the language translate to", reply_markup=trans_markup)
	bot.register_next_step_handler(sent, get_input)


def get_input(message):
	if not any(message.text in item for item in languages):
		hide_markup = telebot.types.ReplyKeyboardRemove()
		bot.send_message(message.chat.id, "❌ Wrong language, choose from butons only", reply_markup=hide_markup) 
	else:
		sent = bot.send_message(message.chat.id, "🚩 Your language is " + message.text + "\n➡️ Enter the input")
		languages_switcher = {
			'Russian': send_rus_trans,
			'German': send_ger_trans,
			'Japanese': send_jap_trans,
			'Polish': send_pol_trans,
			'Spanish': send_spa_trans,
			'French': send_fra_trans
		}
	
		lang_response = languages_switcher.get(message.text)
		bot.register_next_step_handler(sent, lang_response)


def send_rus_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False) #Return to start keyboard
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time', '/news')
	start_markup.row('/crypto', '/stocks', '/translate')	
	bot.send_message(message.chat.id, to_ru(message.text), reply_markup=start_markup)


def send_ger_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time', '/news')
	start_markup.row('/crypto', '/stocks', '/translate')
	bot.send_message(message.chat.id, to_de(message.text), reply_markup=start_markup)


def send_jap_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time', '/news')
	start_markup.row('/crypto', '/stocks', '/translate')
	bot.send_message(message.chat.id, to_ja(message.text), reply_markup=start_markup)


def send_pol_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time', '/news')
	start_markup.row('/crypto', '/stocks', '/translate')	
	bot.send_message(message.chat.id, to_pl(message.text), reply_markup=start_markup)


def send_spa_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time', '/news')
	start_markup.row('/crypto', '/stocks', '/translate')	
	bot.send_message(message.chat.id, to_es(message.text), reply_markup=start_markup)

	
def send_fra_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/погода', '/время', '/новости')
	start_markup.row('/криптовалюта', '/перевод')
	bot.send_message(message.chat.id, to_fr(message.text), reply_markup=start_markup)

	
while True:
	try:
		bot.infinity_polling(True)
	except Exception:
		tm.sleep(1)
