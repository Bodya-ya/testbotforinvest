import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from os import getenv
import json
import pandas as pd
import requests
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('agg')
from steps import STEPS
import time
load_dotenv()
token = getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

def load_data() -> dict:
    """Функция загрузки данных из json"""
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}


def save_data(data: dict):
    """Функция сохранения данных в json"""
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

user_data = load_data()
tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))
timeforinvest = lambda x: time.strftime("%d.%m.%Y", time.localtime(x))

@bot.message_handler(commands=["start"])
def start(message: Message):
    user_id = message.from_user.id
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("А ну-ка...")

    if str(user_id) not in user_data:
        user_data[str(user_id)] = "Назад⬅️"
        save_data(user_data)




    bot.send_message(
        chat_id=message.chat.id,
        text=f"Привет {message.from_user.username}!\nМоё имя ИнвестБот!\nЯ здесь чтобы помочь вам разобраться в мире инвестиций.\nСледить за акциями и избежать ошибок новичков.\nИзучайте последние новости и аналитику, делайте выгодные инвестиции и помните, что в мире инвестиций всегда есть место риску.\nНажимай кнопочку и я тебе всё объясню!",
        reply_markup=keyboard,
    )
def filter_start_choice(message: Message):
    keywords = ["А ну-ка..."]
    return message.text in keywords

def send_next_quest_step(user_id):
    current_step = user_data[str(user_id)]
    mesag, visor = STEPS[current_step]

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(*visor)
    bot.send_message(
        chat_id=user_id,
        text=mesag,
        reply_markup=keyboard,
    )


@bot.message_handler(func=filter_start_choice)
def handler_start_choices(message: Message):
    user_id = message.from_user.id
    current_choice = message.text

    if current_choice == "А ну-ка...":
        user_data[str(user_id)] = "Главноеменю"
        save_data(user_data)

    send_next_quest_step(user_id)

@bot.message_handler(content_types=["text"])
def handler_users_answers(message: Message):
    user_id = message.from_user.id
    current_step = user_data[str(user_id)]
    available_choices = STEPS[current_step][1]
    current_choice = message.text
    if message.text.lower() == 'назад⬅️':
        for location in STEPS.keys():
            if user_data[str(user_id)] in STEPS[location][1]:
                user_data[str(user_id)] = location
                save_data(user_data)
                send_next_quest_step(user_id)

    elif current_choice not in available_choices:
        bot.send_message(
            chat_id=user_id,
            text='выбери что-то из предложенного...',
        )
        return
    elif current_choice == "Яндекс🔴":
        with open(f"yandex{message.chat.id}.png", "wb+") as file:
            j = requests.get(
                'http://iss.moex.com/iss/engines/stock/markets/shares/securities/YNDX/candles.json?from=2024-01-01&till=2024-03-30&interval=24').json()
            data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
            frame = pd.DataFrame(data)
            f1 = plt.figure()
            plt.plot(list(frame['close']))
            plt.savefig(f"yandex{message.chat.id}.png")
            plt.clf()
            plt.cla()
            bot.send_photo(message.chat.id, file)
            bot.send_message(message.chat.id, (tconv(message.date)))
    elif current_choice == "ГазПром🔵":
        with open(f"gazprom{message.chat.id}.png", "wb+") as file:
            j = requests.get(
                'http://iss.moex.com/iss/engines/stock/markets/shares/securities/GAZP/candles.json?from=2024-01-01&till=2024-03-30&interval=24').json()
            data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
            frame = pd.DataFrame(data)
            f2 = plt.figure()
            plt.ioff()
            plt.plot(list(frame['close']))
            plt.savefig(f"gazprom{message.chat.id}.png")
            plt.clf()
            plt.cla()
            bot.send_photo(message.chat.id, file)
            bot.send_message(message.chat.id, (tconv(message.date)))
    elif current_choice == "Лукоил🔴":
        with open(f"luckoul{message.chat.id}.png", "wb+") as file:
            j = requests.get(
                'http://iss.moex.com/iss/engines/stock/markets/shares/securities/LKOH/candles.json?from=2024-01-01&till=2024-03-30&interval=24').json()
            data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
            frame = pd.DataFrame(data)
            f3 = plt.figure()
            plt.ioff()
            plt.plot(list(frame['close']))
            plt.savefig(f"luckoul{message.chat.id}.png")
            plt.clf()
            plt.cla()
            bot.send_photo(message.chat.id, file)
            bot.send_message(message.chat.id, (tconv(message.date)))
    elif current_choice == "Детский мир🔵":
        with open(f"kidworld{message.chat.id}.png", "wb+") as file:
            j = requests.get(
                'http://iss.moex.com/iss/engines/stock/markets/shares/securities/DSKY/candles.json?from=2024-01-01&till=2024-03-30&interval=24').json()
            data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
            frame = pd.DataFrame(data)
            f4 = plt.figure()
            plt.ioff()
            plt.plot(list(frame['close']))
            plt.savefig(f"kidworld{message.chat.id}.png")
            plt.clf()
            plt.cla()
            bot.send_photo(message.chat.id, file)
            bot.send_message(message.chat.id, (tconv(message.date)))
    elif current_choice == "Аэрофлот🔵":
        with open(f"airflot{message.chat.id}.png", "wb+") as file:
            j = requests.get(
                'http://iss.moex.com/iss/engines/stock/markets/shares/securities/AFLT/candles.json?from=2024-01-01&till=2024-03-30&interval=24').json()
            data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
            frame = pd.DataFrame(data)
            f5 = plt.figure()
            plt.plot(list(frame['close']))
            plt.savefig(f"airflot{message.chat.id}.png")
            plt.clf()
            plt.cla()
        
            bot.send_photo(message.chat.id, file)
            bot.send_message(message.chat.id, (tconv(message.date)))
    elif current_choice == "Сбербанк🟢":
        with open(f"sber{message.chat.id}.png", "wb+") as file:    
            j = requests.get(
                'http://iss.moex.com/iss/engines/stock/markets/shares/securities/SBER/candles.json?from=2024-01-01&till=2024-03-30&interval=24').json()
            data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
            frame = pd.DataFrame(data)
            f6 = plt.figure()
            plt.plot(list(frame['close']))
            plt.savefig(f"sber{message.chat.id}.png")
            plt.clf()
            plt.cla()
            bot.send_photo(message.chat.id, file)
            bot.send_message(message.chat.id, (tconv(message.date)))
    elif current_choice == "МТС🔴":
        with open(f"mts{message.chat.id}.png", "wb+") as file:    
            j = requests.get(
                'http://iss.moex.com/iss/engines/stock/markets/shares/securities/MTSS/candles.json?from=2024-01-01&till=2024-03-30&interval=24').json()
            data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
            frame = pd.DataFrame(data)
            f7 = plt.figure()
            plt.plot(list(frame['close']))
            plt.savefig(f"mts{message.chat.id}.png")
            plt.clf()
            plt.cla()
            bot.send_photo(message.chat.id, file)
            bot.send_message(message.chat.id, (tconv(message.date)))
    elif current_choice == "ПИК🟠":
        with open(f"pick{message.chat.id}.png", "wb+") as file:
            j = requests.get(
                'http://iss.moex.com/iss/engines/stock/markets/shares/securities/PIKK/candles.json?from=2024-01-01&till=2024-03-30&interval=24').json()
            data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
            frame = pd.DataFrame(data)
            f8 = plt.figure()
            plt.ioff()
            plt.plot(list(frame['close']))
            plt.savefig(f"pick{message.chat.id}.png", "wb+")
            plt.clf()
            plt.cla()
            bot.send_photo(message.chat.id, file)
            bot.send_message(message.chat.id, (tconv(message.date)))
    else:
        user_data[str(user_id)] = current_choice
        save_data(user_data)
        send_next_quest_step(user_id)

@bot.message_handler(func=lambda message: True)
def callback_worker(message):
    current_choice = message.text
    user_id = message.from_user.id

    user_data[str(user_id)] = current_choice
    save_data(user_data)
    send_next_quest_step(user_id)
if __name__ == "__main__":
    while True:
        try:
            bot.polling()
        except Exception as ex:
            pass