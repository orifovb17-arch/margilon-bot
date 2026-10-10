
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
    # Agar xabar "Bot nimalar qila oladi?" tugmasi bo'lsa:
    if message.text and "nimalar qila oladi" in message.text:
        info_text = (
            "ℹ️ **\"Marg'ilon 24/7\" rasmiy murojaat boti!**\n\n"
            "Ushbu bot orqali siz:\n"
            "🔹 Marg'ilon va Farg'ona vodiysidagi tezkor xabar, voqea va hodisalarni yuborishingiz;\n"
            "🔹 Foto, video yoki audio murojaatlarni kanal adminlariga yetkazishingiz;\n"
            "🔹 Reklama va hamkorlik bo'yicha bog'lanishingiz mumkin.\n\n"
            "📩 *Xabaringiz maxfiyligi ta'minlanadi!*"
        )
        bot.send_message(message.chat.id, info_text, parse_mode="Markdown")
        
    # Agar xabar "Xabar / Yangilik yuborish" tugmasi bo'lsa:
    elif message.text and ("Xabar" in message.text or "Yangilik" in message.text):
        bot.send_message(message.chat.id, "Murojaatingizni yozib qoldiring (tekst, rasm yoki video yuborishingiz mumkin):")
        
    # Qolgan barcha xabarlar adminga yo'naltiriladi:
    else:
        user_info = (
            f"📩 **Yangi murojaat keldi!**\n\n"
            f"Kimdan: @{message.from_user.username if message.from_user.username else 'Yashirin profil'}\n"
            f"Ismi: {message.from_user.first_name}\n"
            f"ID: `{message.chat.id}`"
        )
        bot.send_message(ADMIN_ID, user_info, parse_mode="Markdown")
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        
        bot.send_message(message.chat.id, "Xabaringiz adminga yetkazildi! Rahmat.")

# --- 3. Ishga tushirish ---
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()





