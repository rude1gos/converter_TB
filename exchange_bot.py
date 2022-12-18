import telebot
from telebot import types
from config import keys, TOKEN
from extensions import Convertation, ConvertException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет, добро пожаловать в конвертер'
    bot.send_message(message.chat.id, text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    help = types.KeyboardButton('/help')
    values = types.KeyboardButton('/values')
    markup.add(help, values)
    bot.send_message(message.chat.id, 'Команды', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nСписок доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertException('Много/мало параметров')

        quote, base, amount = values
        total_base = Convertation.convert(quote, base, amount)
        new_price = total_base * float(amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {round(new_price, 2)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
