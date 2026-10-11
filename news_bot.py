import telebot
from threading import Thread
import os

# --- 1. Flask server (Render va UptimeRobot o'chib qolmasligi uchun) ---
from flask import Flask
app = Flask('')

@app.route('/')
def home():
    return "Bot status: Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. Telegram bot sozlamalari ---
TOKEN = "8787574332:AAGPJOvCwdjKYt389GUQO_on4GENqTRKBhw"
ADMIN_ID = 8492433312

bot = telebot.TeleBot(TOKEN)

# --- 3. Start va Help komandalari ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("ℹ️ Bot nimalar qila oladi?")
    btn2 = telebot.types.KeyboardButton("📩 Xabar / Yangilik yuborish")
    markup.add(btn1, btn2)
    
    bot.reply_to(message, "Assalomu alaykum! Marg'ilon 24/7 botiga xush kelibsiz!", reply_markup=markup)

# --- 4. Barcha xabarlarni adminga yo'naltirish (Forward) ---
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'voice'])
def handle_all_messages(message):
    # Agar xabar adminga (sizga) tegishli bo'lmasa:
    if message.from_user.id != ADMIN_ID:
        # Xabarni adminga forward qiladi
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        # Yozgan odamga javob qaytaradi
        bot.reply_to(message, "Xabaringiz adminga yetkazildi! Rahmat.")

# --- 5. Botni ishga tushirish ---
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

 






