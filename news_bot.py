import os
from flask import Flask
from threading import Thread
import telebot

# --- 1. Render uchun Flask serveri (Keep Alive) ---
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
    bot.reply_to(message, "Assalomu alaykum! Marg'ilon 24/7 botiga xush kelibsiz!")

# --- 3. Ishga tushirish ---
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()


