import telebot
from config import TOKEN, keys
from utils import CryptoConverter, ConvertionExseption, UserDB

bot = telebot.TeleBot(TOKEN)

db = UserDB()

@bot.message_handler(commands=['start','help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работать введите команду боту в следующем формате:\n<имя валюты> \
<в какую перевести> \
<количество переводимой валюты>\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message,text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message,text)


@bot.message_handler(commands=['set'])
def set_keyboard(message: telebot.types.Message):
    markup = telebot.types.InlineKeyboardMarkup()
    for key, val in keys.items():
        button = telebot.types.InlineKeyboardButton(text=key.capitalize(), callback_data=f'val1 {val}')
        markup.add(button)
    bot.send_message(chat_id=message.chat.id, text='Выберите валюту, из которой будем конвертировать',reply_markup=markup)

    markup = telebot.types.InlineKeyboardMarkup()
    for key, val in keys.items():
        button = telebot.types.InlineKeyboardButton(text=key.capitalize(), callback_data=f'val2 {val}')
        markup.add(button)
    bot.send_message(chat_id=message.chat.id, text='Выберите валюту, в которую конвертируем', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handler_query(call):
    t, st = call.data.split()
    user_id = call.message.chat.id
    if t == 'val1':
        db.change_from(user_id, st)

    if t == 'val2':
        db.change_to(user_id, st)

    pair = db.get_pair(user_id)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'Теперь конвертируем из {pair[0]} в {pair[1]}')



@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        pair = db.get_pair(message.chat.id)
        values = [*pair, message.text.strip()]

        if len(values) != 3:
            raise ConvertionExseption('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionExseption as e:
        bot.reply_to(message,f'Ошибка пользователя \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n {e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id,text)


bot.polling()



