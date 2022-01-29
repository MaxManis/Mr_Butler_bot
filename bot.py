# - *- coding: utf- 8 - *-
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram import Bot, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import config
import news_scraper
import weather
import chatbot_talk
import exchange_rate
import sqlite_db
import text_recognition
import blackjack
import interesting_api

import random

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

oper_id = config.oper_id
secret = config.secret

# bot.remove_webhook()
# sleep(1)
# bot.set_webhook(url="https://boston88.pythonanywhere.com/{}".format(secret))

# main part of txt db for msg sending
joined_file = open("db/joined.txt", "r")
joinedUsers = set()
for line in joined_file:
    joinedUsers.add(line.strip())
joined_file.close()


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    new_user_id = message.from_user.id
    res = sqlite_db.sql_check(new_user_id)

    if res is True:
        start_buttons = config.start_keys
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        user_name = message.from_user.first_name
        await bot.send_message(message.from_user.id, f'Hello {user_name}!', reply_markup=keyboard)

    elif res is False:
        # TXT DataBase:
        # adding user id to txt db for msg sending
        if not str(message.chat.id) in joinedUsers:
            joined_file = open("db/joined.txt", 'a')
            joined_file.write(str(message.chat.id) + "\n")
            joinedUsers.add(message.chat.id)
        # Share contact
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="📲Поделиться контактом📲", request_contact=True)
        keyboard.add(button_phone)
        await bot.send_message(message.from_user.id, 'Need to reg pls!', reply_markup=keyboard)


@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    if message.contact is not None:  # Если присланный объект contact не равен нулю
        res = sqlite_db.add_user(message)
        keyboard = types.ReplyKeyboardRemove()
        await bot.send_message(message.chat.id, f"🚹 Пользователь распознан как {res}", reply_markup=keyboard)
        await start_command(message)
    else:
        await bot.send_message(message.chat.id, "Авторизация не удалась. \nПопробуйте еще раз!")
        await start_command(message)


@dp.message_handler(Text(equals="😁Daddy jokes"))
async def get_weather(message: types.Message):
    await bot.send_message(message.from_user.id, interesting_api.daddy_jokes())


@dp.message_handler(Text(equals="👽Rick and Morty"))
async def get_rick_morty(message: types.Message):
    await bot.send_message(message.from_user.id, interesting_api.get_morty(), parse_mode=types.ParseMode.HTML)


@dp.message_handler(Text(equals="✒️Распознавание текста"))
async def get_weather(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберете, пожалуйста, изображение на вашем устройстве.\n'
                                                 'Затем отправьте его мне)')


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    await bot.send_message(message.from_user.id, '🕓Please wait, Im reading your text!')
    file_path = f'files/test-{message.chat.id}.jpg'
    await message.photo[-1].download(file_path)
    res = text_recognition.text_rec(file_path)
    start_buttons = config.start_keys
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    co = ''
    for i in res:
        co += f'\n{i}'
    await bot.send_message(message.from_user.id, '✒️Результат распознавания текста:')
    await bot.send_message(message.from_user.id, co, reply_markup=keyboard)


@dp.message_handler(Text(equals="🃏BlackJack"))
async def start_blackjack(message: types.Message):
    await bot.send_message(message.from_user.id, 'WELCOME TO BLACKJACK!')
    global dealer_hand, player_hand
    dealer_hand = blackjack.deal()
    player_hand = blackjack.deal()
    await bot.send_message(message.from_user.id, "The dealer is showing a " +
                           hlink(str(dealer_hand[0]['value']), dealer_hand[0]['link']), parse_mode=types.ParseMode.HTML)
    await bot.send_message(message.from_user.id, "You have a " + hlink(str(player_hand[0]['value']), player_hand[0]['link']) +
                           ' and ' + hlink(str(player_hand[1]['value']), player_hand[1]['link']) + " for a total of " +
                           str(blackjack.total(player_hand)), parse_mode=types.ParseMode.HTML)
    blackjack.blackjack(dealer_hand, player_hand)
    start_buttons = ["♥️Hit", "♠️Stand", "❌Quit"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.from_user.id, 'Do you want to Hit, Stand, or Quit: ', reply_markup=keyboard)


@dp.message_handler(Text(equals=["♥️Hit", "♠️Stand", "❌Quit"]))
async def play_blackjack(message: types.Message):
    start_buttons = config.start_keys
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    if message.text == "♥️Hit":
        blackjack.hit(player_hand)
        while blackjack.total(dealer_hand) < 17:
            blackjack.hit(dealer_hand)
        await bot.send_message(message.from_user.id, blackjack.score(dealer_hand, player_hand), reply_markup=keyboard)
    elif message.text == "♠️Stand":
        while blackjack.total(dealer_hand) < 17:
            blackjack.hit(dealer_hand)
        await bot.send_message(message.from_user.id, blackjack.score(dealer_hand, player_hand), reply_markup=keyboard)
    elif message.text == "❌Quit":
        info = 'Bye!'
        await bot.send_message(message.from_user.id, info, reply_markup=keyboard)


@dp.message_handler(Text(equals="⛅️Погода"))
async def get_weather(message: types.Message):
    start_buttons = ["🇺🇦Украина", "🇷🇺Россия", "🇪🇺Города Европы"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.from_user.id, 'Выберете, пожалуйста, регион.', reply_markup=keyboard)


@dp.message_handler(Text(equals=["🇺🇦Украина", "🇷🇺Россия", "🇪🇺Города Европы"]))
async def choose_city(message: types.Message):
    if message.text == "🇺🇦Украина":
        ilk = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*config.ua_cities)
    elif message.text == "🇷🇺Россия":
        ilk = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*config.ru_cities)
    elif message.text == "🇪🇺Города Европы":
        ilk = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*config.eu_cities)
    await bot.send_message(message.from_user.id, 'Choose your city please!', reply_markup=ilk)


@dp.message_handler(Text(equals=config.all_cities))
async def show_res_weather(message: types.Message):
    city = message.text
    info = weather.get_weather(city)
    start_buttons = config.start_keys
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.from_user.id, info, parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.message_handler(Text(equals="📰Новости"))
async def choose_all_news(message: types.Message):
    start_buttons = ["🔬Science", "💻Tech", "🌎World"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.from_user.id, 'Choose news category please!', reply_markup=keyboard)


@dp.message_handler(Text(equals=["🔬Science", "💻Tech", "🌎World"]))
async def get_news(message: types.Message):
    if message.text == "🔬Science":
        all_news = news_scraper.get_news('https://www.bbc.com/news/science_and_environment')
    elif message.text == "💻Tech":
        all_news = news_scraper.get_news()
    elif message.text == "🌎World":
        all_news = news_scraper.get_news('https://www.bbc.com/news/world')

    start_buttons = config.start_keys
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    i = 0
    for p in range(1, 11):
        new = all_news[i]
        i += 1
        if new['Text'] == 'No text':
            continue
        news = f"{hbold(new['Title'])}\n" \
               f"{hunderline(new['Text'])}\n" \
               f"{hlink('Read more', new['Link'])}"
        await bot.send_message(message.from_user.id, news, parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.message_handler(Text(equals="💵Курс валют"))
async def get_rates_choose(message: types.Message):
    start_buttons = ["USD $", "EUR €", "UAH ₴", "RUB ₽"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.from_user.id, 'Выберете, пожалуйста, валюту.', reply_markup=keyboard)


@dp.message_handler(Text(equals=["USD $", "EUR €", "UAH ₴", "RUB ₽"]))
async def get_rates(message: types.Message):
    result = exchange_rate.gey_rate(message.text[:message.text.find(' ')])
    start_buttons = config.start_keys
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.from_user.id, result, parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.message_handler()
async def to_talk(message: types.Message):
    question = message.text
    response = chatbot_talk.ai_talk(question)
    await bot.send_message(message.from_user.id, response)


executor.start_polling(dp, skip_updates=True)
