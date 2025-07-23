import telebot
import webbrowser
from telebot import types



@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://iitu.edu.kz/ru/')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перети на сайт IITU')
    btn2 = types.KeyboardButton('Сетевая безопасность')
    btn3 = types.KeyboardButton('Компьютерные науки')
    btn4 = types.KeyboardButton('ПИ')
    btn5 = types.KeyboardButton('Data science')
    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4, btn5)


    file = open('./photo.jpeg', 'rb')
    bot.send_photo(message.chat.id, file)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Перети на сайт IITU':
        bot.send_message(message.chat.id, 'Вы перешли на сайт')
        webbrowser.open('https://iitu.edu.kz/ru/')

    elif message.text == 'Сетевая безопасность':
        bot.send_message(message.chat.id, 'Вы перешли на сайт')
        webbrowser.open('https://iitu.edu.kz/ru/articles/departments/computer-engineering/6b06303-сетевая-безопасность/')

    elif message.text == 'Компьютерные науки':
        bot.send_message(message.chat.id, 'Вы перешли на сайт')
        webbrowser.open('https://iitu.edu.kz/ru/articles/departments/matematiceskoe-komp_uternoe-modelirovanie/6b06101-компьютерные-науки/')
    
    elif message.text == 'ПИ':
        bot.send_message(message.chat.id, 'Вы перешли на сайт')
        webbrowser.open('https://iitu.edu.kz/ru/articles/departments/computer-engineering/6b06110-програмная-инженерия/')
    
    elif message.text == 'Data science':
        bot.send_message(message.chat.id, 'Вы перешли на сайт')
        webbrowser.open('https://iitu.edu.kz/ru/articles/departments/matematiceskoe-komp_uternoe-modelirovanie/6b06112-data-science/')
    


# @bot.message_handler(commands=['start'])
# def site(message):
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton('Перети на сайт IITU', url='https://iitu.edu.kz/ru/')
#     btn2 = types.InlineKeyboardButton('Сетевая безопасность', url='https://iitu.edu.kz/ru/articles/departments/computer-engineering/6b06303-сетевая-безопасность/')
#     btn3 = types.InlineKeyboardButton('Компьютерные науки', url='https://iitu.edu.kz/ru/articles/departments/matematiceskoe-komp_uternoe-modelirovanie/6b06101-компьютерные-науки/')
#     btn4 = types.InlineKeyboardButton('ПИ', url='https://iitu.edu.kz/ru/articles/departments/computer-engineering/6b06110-програмная-инженерия/')
#     btn5 = types.InlineKeyboardButton('Data science', url='https://iitu.edu.kz/ru/articles/departments/matematiceskoe-komp_uternoe-modelirovanie/6b06112-data-science/')
#     markup.row(btn1)
#     markup.row(btn2, btn3)
#     markup.row(btn4, btn5)
#     bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name}', reply_markup=markup)


@bot.message_handler()
def hi(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name}')
    elif message.text.lower() == "id":
        bot.reply_to(message, f'ID: {message.from_user.id}')
    elif message.text.lower() == "/start":
        bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name}')
    elif message.text.lower() == '417б':
        bot.send_message(message.chat.id, 'Этот кабинет находиться в корпусе Байзақ на 4 этаже')

bot.polling(non_stop=True)