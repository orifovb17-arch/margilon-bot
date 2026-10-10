import os
from threading import Thread
from flask import Flask
import telebot

# --- 1. Render uchun Flask server ---
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlamoqda!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. Telegram bot kodi ---
TOKEN = "8787574332:AAFqmI0K_lYu8JFKuVUMqc8MU09Ves6kgOc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("ℹ️ Bot nimalar qila oladi?")
    btn2 = telebot.types.KeyboardButton("📩 Xabar / Yangilik yuborish")
    markup.add(btn1, btn2)
    
    bot.reply_to(message, "Assalomu alaykum! Marg'ilon 24/7 botiga xush kelibsiz!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "ℹ️ Bot nimalar qila oladi?":
        bot.send_message(message.chat.id, "Bu bot orqali 'Marg'ilon 24/7' kanaliga xabar va yangiliklar yuborishingiz mumkin.")
    elif message.text == "📩 Xabar / Yangilik yuborish":
        bot.send_message(message.chat.id, "Murojaatingizni yozib qoldiring, adminlar ko'rib chiqadi:")

# --- 3. Ishga tushirish ---
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()



