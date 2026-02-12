import telebot
import os

# ትክክለኛው ቶከን
API_TOKEN = '8530081968:AAFg4PPaTkLkX2U8iJSJ8hwaQWd89Xkt1vw'
ADMIN_ID = 8596054746

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም አቤል! ቦቱ አሁን በ Render ላይ በትክክል እየሰራ ነው።")

@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    bot.reply_to(message, "መልዕክትዎ ደርሶናል!")
    bot.send_message(ADMIN_ID, f"መልዕክት ከ: @{message.from_user.username}\n\n{message.text}")

bot.infinity_polling()
