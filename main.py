import telebot

bot = telebot.TeleBot('7509082884:AAHom-IkjxOjp35zsaCRK5DR1vngsYyNiik')

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