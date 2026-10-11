import telebot
from threading import Thread
import os

# --- 1. Flask веб-сервер для поддержки работы 24/7 ---
from flask import Flask
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. Код Telegram-бота ---
TOKEN = "8787574332:AAFqmI0K_1Yu8JFKuVMqc8M" # Ваш токен
ADMIN_ID = 8492433312                       # Ваш Telegram ID

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("ℹ️ Bot nimalar qila oladi?")
    btn2 = telebot.types.KeyboardButton("📩 Xabar / Yangilik yuborish")
    markup.add(btn1, btn2)
    
    bot.reply_to(message, "Assalomu alaykum! Marg'ilon 24/7 botiga xush kelibsiz!", reply_markup=markup)

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'voice'])
def handle_all_messages(message):
    # Если сообщение пришло от обычного пользователя (не от админа)
    if message.from_user.id
 






