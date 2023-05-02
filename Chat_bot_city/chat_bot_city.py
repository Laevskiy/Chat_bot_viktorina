import telebot
from telebot import types
import random
import pymongo
from pymongo import MongoClient

bot = telebot.TeleBot('5804607290:AAEMw4PJCiY3dFuFqYKR2CCTg2pqM63EXu0')

uri = "mongodb+srv://laevskiy91:Pass123@cluster0.yufpwcz.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["City_data_Base"]
collections = db['Cantry_cities']

global a
a = 0
global b
b = 0
global res
res = []
res_01 = collections.find({})

for i in res_01:
    res.append(i)

def podskazka():
    sp_podskazok = []
    v = len(res)-1
    sp_num = [a]
    while len(sp_num) != 3:
        u = random.randint(0,v)
        if u not in sp_num:
            sp_num.append(u)

    for i in sp_num:
        sp_podskazok.append(res[i]['city'])

    return sp_podskazok


def make_but(list):
    list_btn = []

    for i in list:
        btn = types.InlineKeyboardButton(text=i, callback_data=i)
        list_btn.append(btn)
    return list_btn


@ bot.message_handler(commands=['игра'])
def game_main(message):
    ansver = bot.send_message(message.chat.id, f"Назовите столицу {res[a]['country']} ")
    pds = podskazka()
    bot.send_message(message.chat.id, f"Подсказка {pds[0]},{pds[1]} или {pds[2]} ")
    pds_but = make_but(pds)
    keyboard = types.InlineKeyboardMarkup()

    for i in pds_but:
        keyboard.row(i)

    bot.send_message(message.chat.id, f"Назовите столицу {res[a]['country']}", reply_markup=keyboard)
    bot.register_next_step_handler(ansver, proverka_cities)

def proverka_cities(message) :

    global b
    global a
    if message.text == res[a]['city']:
        b = b + 1
        bot.send_message(message.chat.id, f" {message.text}, да Это верно. Так держать ")
    else:
        bot.send_message(message.chat.id, f"Увы")
    if a < len(res)-1:
        a = a + 1
        game_main(message)
    else:
        bot.send_message(message.chat.id, f"Игра окончена. Количество ваших баллов: {b}")
        a = 0
        b = 0


@ bot.callback_query_handler(func=lambda callback:True)
def callback_game (callback):
    global b
    global a
    if callback.data == res[a]['city']:
        bot.send_message(callback.message.chat.id, "Верный ответ")

    else:
        bot.send_message(callback.message.chat.id, "Ошибка")

    if a < len(res)-1:
        a = a + 1
        game_main(callback.message)
    else:
        bot.send_message(callback.message.chat.id, f"Игра окончена. Количество ваших баллов: {b}")
        a = 0
        b = 0

bot.polling(non_stop=True)