import telebot

# የአዲሱ ቦት (@Abeletechbot) ቶከን
API_TOKEN = '8530081968:AAFg4PPaTkLkX2U8iJSJ8hwaQWd89Xkt1vw'
# የአንተ መለያ (ID)
ADMIN_ID = 8596054746

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም አቤል! አዲሱ ቦት (@Abeletechbot) በትክክል ስራ ጀምሯል። ጥያቄዎን እዚህ ይጻፉ።")

@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    # ለደንበኛው የሚሰጥ ምላሽ
    bot.reply_to(message, "መልዕክትዎ ደርሶናል! በቅርቡ እንመለስልዎታለን።")
    # መልዕክቱን ወደ አንተ (አድሚኑ) መላክ
    bot.send_message(ADMIN_ID, f"አዲስ መልዕክት ከ: @{message.from_user.username}\n\nይዘት: {message.text}")

print("ቦቱ @Abeletechbot ስራ ጀምሯል...")
bot.infinity_polling()
