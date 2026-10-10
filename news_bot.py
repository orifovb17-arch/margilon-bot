import os
from threading import Thread
from flask import Flask
import telebot

# --- 1. Server Render uchun ---
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
ADMIN_ID = 8492433312  # Sizning Telegram ID ingiz
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("ℹ️ Bot nimalar qila oladi?")
    btn2 = telebot.types.KeyboardButton("📩 Xabar / Yangilik yuborish")
    markup.add(btn1, btn2)
    
    bot.reply_to(message, "Assalomu alaykum! Marg'ilon 24/7 botiga xush kelibsiz!", reply_markup=markup)

@bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'document'])
def handle_all_messages(message):
    # Agar xabar tugmalardan biri bo'lsa:
    if message.text and "nimalar qila oladi" in message.text:
        bot.send_message(message.chat.id, "Bu bot orqali 'Marg'ilon 24/7' kanaliga xabar va yangiliklar yuborishingiz mumkin.")
    elif message.text and ("Xabar" in message.text or "Yangilik" in message.text):
        bot.send_message(message.chat.id, "Murojaatingizni yozib qoldiring (tekst, rasm yoki video yuborishingiz mumkin):")
    else:
        # Xabarni adminga (sizga) yo'naltirish:
        user_info = f"📩 **Yangi murojaat keldi!**\n\nKimdan: @{message.from_user.username if message.from_user.username else 'Yashirin profil'}\nIsmi: {message.from_user.first_name}\nID: `{message.chat.id}`"
        
        bot.send_message(ADMIN_ID, user_info, parse_mode="Markdown")
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        
        # Foydalanuvchiga tasdiq xabari:
        bot.send_message(message.chat.id, "Xabaringiz adminga yetkazildi! Rahmat.")

# --- 3. Ishga tushirish ---
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()





