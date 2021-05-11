import telebot

TOKEN = '1868800073:AAFD2Ve6UnQ0jpgzAzBk657z9j2wvmXdca0'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f"Welcome, @{message.chat.username}")


@bot.message_handler(content_types=['photo'])
def picture_repeat(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')

bot.polling(none_stop=True)
