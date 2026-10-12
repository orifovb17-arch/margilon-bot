import os
import time
from threading import Thread
from flask import Flask
import telebot

# Telegram Bot Tokeningizni atrofdagi o'zgaruvchidan yoki to'g'ridan-to'g'ri oling
TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Render serverini uqlab qolmasligi uchun sodda veb-sahifa (Healthcheck)
@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!", 200

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Botingizning buyruq va buyruq ishlovchilari
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "Xush kelibsiz! @Margilon24_7 kanali rasmiy admin boti ishlamoqda. "
        "Murojaatingizni yuborishingiz mumkin."
    )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Xabaringiz qabul qilindi!")

# Botni xatosiz va uzluksiz ishga tushirish funksiyasi
def start_bot():
    while True:
        try:
            print("Eski seanslar va conflict'lar tozalanmoqda...")
            # 1. Conflict xatosini oldini olish uchun eski webhook va ulanishlarni tozalaymiz
            bot.remove_webhook(drop_pending_updates=True)
            time.sleep(1)
            
            print("Bot muvaffaqiyatli ishga tushdi!")
            # 2. Skip_pending_updates=True orqali eski toplanib qolgan xabarlardan tiqilib qolmaydi
            bot.infinity_polling(timeout=10, long_polling_timeout=5, skip_pending_updates=True)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}. Bot 5 sekunddan so'ng qayta ishga tushadi...")
            time.sleep(5)

if __name__ == "__main__":
    # Flask serverini alohida fonda (Thread) ishga tushiramiz
    server_thread = Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()

    # Botni cheksiz tsiklda ishga tushiramiz
    start_bot()



 






