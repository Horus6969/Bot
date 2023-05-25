import telebot
from telebot import types
from config import keys, TOKEN
from extensions import ConvertionException, СurrencyConverter

bot = telebot.TeleBot(TOKEN)


def convert_markup(quote=None):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    buttons = []

    for v in keys.keys():
        if v != quote:
            buttons.append(types.KeyboardButton(v.capitalize()))
    markup.add(*buttons)

    return markup


@bot.message_handler(commands=['start', 'help'])
def help(message:telebot.types.Message):
    text = 'Для начала конвертации введите команду: /convert\n\
Список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def values(message:telebot.types.Message):
    text = 'Выберите валюту, из которой конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=convert_markup())
    bot.register_next_step_handler(message, quote_handler)


def quote_handler(message:telebot.types.Message):
    quote = message.text.strip().lower()
    text = 'Выберите валюту, в которую конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=convert_markup(quote))
    bot.register_next_step_handler(message, base_handler, quote)


def base_handler(message:telebot.types.Message, quote):
    base = message.text.strip().lower()
    text = 'Введите количество конвертируемой валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, quote, base)


def amount_handler(message:telebot.types.Message, quote, base):
    amount = message.text.strip()
    try:
        total_base, rate = СurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Результат конвертации {amount} {quote} в {base} - {total_base} {keys[base]}\n\
Курс {quote} к {base} - {rate} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()