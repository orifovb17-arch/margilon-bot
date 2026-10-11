import os
import telebot
from flask import Flask
from threading import Thread

# --- 1. Flask Server (Render o'chib qolmasligi uchun) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot status: Active & Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. Bot va Admin Sozlamalari ---
TOKEN = "8787574332:AAGPJOvCwdjKYt389GUQO_on4GENqTRKBhw"
ADMIN_ID = 8492433312  # Sizning Telegram ID ingiz

bot = telebot.TeleBot(TOKEN)

# --- 3. Tugmalar Menusi ---
def main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton("📩 Xabar / Yangilik yuborish")
    btn2 = telebot.types.KeyboardButton("ℹ️ Bot haqida")
    markup.add(btn1, btn2)
    return markup

def cancel_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("❌ Bekor qilish"))
    return markup

# User holatlarini saqlash
user_states = {}

# --- 4. Command Handlers (/start, /help) ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_states[message.chat.id] = None
    text = (
        f"Assalomu alaykum, {message.from_user.first_name}!\n"
        f"**Marg'ilon 24/7** rasmiy botiga xush kelibsiz.\n\n"
        f"Ushbu bot orqali siz yangiliklar, murojaat va takliflaringizni "
        f"kanal administratoriga zudlik bilan yuborishingiz mumkin."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_keyboard())

# --- 5. Text Handler (Tugmalar va Xabarlar) ---
@bot.message_handler(func=lambda msg: True, content_types=['text', 'photo', 'video', 'voice', 'document'])
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text

    # Bekor qilish tugmasi bosilsa
    if text == "❌ Bekor qilish":
        user_states[chat_id] = None
        bot.send_message(chat_id, "Amal bekor qilindi.", reply_markup=main_keyboard())
        return

    # "Bot haqida" tugmasi
    if text == "ℹ️ Bot haqida":
        info_text = (
            "🤖 **Marg'ilon 24/7 Bot**\n\n"
            "Bu bot orqali siz admin bilan bog'lanishingiz, shahrimizga oid "
            "yangiliklar va muammolarni yuborishingiz mumkin."
        )
        bot.send_message(chat_id, info_text, parse_mode="Markdown", reply_markup=main_keyboard())
        return

    # "Xabar yuborish" tugmasi
    if text == "📩 Xabar / Yangilik yuborish":
        user_states[chat_id] = "WAITING_FOR_MSG"
        bot.send_message(
            chat_id, 
            "Matn, rasm yoki videongizni yuboring. Adminlarimiz uni ko'rib chiqishadi.", 
            reply_markup=cancel_keyboard()
        )
        return

    # Foydalanuvchi xabar yuborish rejimida bo'lsa yoki shunchaki yozsa
    if user_states.get(chat_id) == "WAITING_FOR_MSG" or chat_id != ADMIN_ID:
        # Adminga xabarni forward / nusxa qilib yuborish
        try:
            bot.send_message(
                ADMIN_ID, 
                f"📥 **Yangi murojaat!**\n\n"
                f"👤 **Kimdan:** {message.from_user.first_name} (@{message.from_user.username or 'Mavjud emas'})\n"
                f"🆔 **ID:** `{chat_id}`",
                parse_mode="Markdown"
            )
            # Xabarning o'zini (rasm, matn, video barchasini) adminga nusxalaydi
            bot.copy_message(chat_id=ADMIN_ID, from_chat_id=chat_id, message_id=message.message_id)
            
            user_states[chat_id] = None
            bot.send_message(chat_id, "✅ Xabaringiz adminga yetkazildi! Rahmat.", reply_markup=main_keyboard())
        except Exception as e:
            bot.send_message(chat_id, "⚠️ Xabar yuborishda xatolik yuz berdi. Qayta urinib ko'ring.", reply_markup=main_keyboard())

# --- 6. Botni uzluksiz ishga tushirish ---
if __name__ == "__main__":
    keep_alive()
    # non_stop va timeout orqali xatolik bo'lsa ham bot to'xtab qolmaydi
    bot.infinity_polling(timeout=10, long_polling_timeout=5)


 






