from dotenv import load_dotenv
import os
import telebot

load_dotenv()
api = os.getenv("MY_API_KEY")
bot = telebot.TeleBot(api)

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f"id: {message.from_user.id}")


bot.polling(none_stop=True)
