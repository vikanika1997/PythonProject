import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите: \n <имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n Увидеть список всех доступных валют: /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values (message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values=message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        base, quote, amount = values
        total_quote = CryptoConverter.convert(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_quote}'
        bot.send.message(message.chat.id, text)

bot.polling()