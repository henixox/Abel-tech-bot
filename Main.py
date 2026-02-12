import telebot
import re

# መረጃዎችህ
TELEGRAM_TOKEN = '8530081968:AAFg4PPaTkLkX2U8iJSJ8hwaQWd89Xkt1vw'
ADMIN_ID = 8596054746

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# መጥፎ ቃላት ዝርዝር (እዚህ ጋር የሚከለከሉ ቃላትን መጨመር ትችላለህ)
BANNED_WORDS = ["ወሲብ", "sex", "porn", "ጋላቢ", "ቂጥ", "ብድ"] 

user_data = {}

# --- የግሩፕ ጥበቃ (Group Guard) ---

@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
def group_guard(message):
    # 1. ሊንክ ካለ ማጥፋት
    if re.search(r'http[s]?://|t\.me/|www\.', message.text.lower()) if message.text else False:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f"⚠️ @{message.from_user.username} ሊንክ መላክ የተከለከለ ነው!")
        return

    # 2. ጸያፍ ቃላት ካሉ ማጥፋት
    if message.text:
        for word in BANNED_WORDS:
            if word in message.text.lower():
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, "🚫 ጸያፍ ቃላት መጠቀም የተከለከለ ነው!")
                break

# --- የጥገና ትዕዛዝ (በግል ብቻ የሚሰራ) ---

@bot.message_handler(commands=['start'], func=lambda message: message.chat.type == 'private')
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    msg = bot.send_message(chat_id, "እንኳን ወደ Abel Tech የጥገና ቦት በደህና መጡ! 🛠\n\n**1️⃣ የዕቃው ዓይነት ምንድነው?**")
    bot.register_next_step_handler(msg, process_item_step)

def process_item_step(message):
    chat_id = message.chat.id
    user_data[chat_id]['item'] = message.text
    msg = bot.send_message(chat_id, "**2️⃣ ያሉበት አካባቢ (ሰፈር) የት ነው?**")
    bot.register_next_step_handler(msg, process_location_step)

def process_location_step(message):
    chat_id = message.chat.id
    user_data[chat_id]['location'] = message.text
    msg = bot.send_message(chat_id, "**3️⃣ ስልክ ቁጥርዎን ያስገቡ?**")
    bot.register_next_step_handler(msg, process_phone_step)

def process_phone_step(message):
    chat_id = message.chat.id
    user_data[chat_id]['phone'] = message.text
    msg = bot.send_message(chat_id, "**4️⃣ ፎቶ ወይም ቪዲዬ እዚህ ያሥቀምጡልኝ፦**\n(ከሌለዎት 'የለኝም' ይበሉ)")
    bot.register_next_step_handler(msg, process_media_step)

def process_media_step(message):
    chat_id = message.chat.id
    data = user_data[chat_id]
    summary = (
        "📩 **አዲስ ትዕዛዝ ደርሶሃል!**\n"
        f"👤 ደንበኛ: {message.from_user.first_name} (@{message.from_user.username})\n"
        f"🛠 ዕቃ: {data['item']}\n"
        f"📍 ቦታ: {data['location']}\n"
        f"📞 ስልክ: {data['phone']}"
    )
    bot.send_message(ADMIN_ID, summary)
    if message.content_type in ['photo', 'video']:
        bot.copy_message(ADMIN_ID, chat_id, message.message_id)
    bot.send_message(chat_id, "በጣም እናመሰግናለን! መረጃው ደርሶናል። 📞")

print("🛡 ቦቱ ግሩፕ ለመጠበቅና ትዕዛዝ ለመቀበል ዝግጁ ነው!")
bot.infinity_polling()
