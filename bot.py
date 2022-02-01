# - *- coding: utf- 8 - *-
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram import Bot, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import config_files.dicts as dicts
import config_files.config as config
from config_files.my_states import TryMySets, WriteToOper

import functions.news_scraper as news_scraper
import functions.weather as weather
import functions.chatbot_talk as chatbot_talk
import functions.exchange_rate as exchange_rate
import functions.sqlite_db as sqlite_db
import functions.text_recognition as text_recognition
import functions.blackjack as blackjack
import functions.interesting_api as interesting_api
import functions.hotline as hotline

import random

bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

oper_id = config.oper_id
secret = config.secret

# bot.remove_webhook()
# sleep(1)
# bot.set_webhook(url="https://boston88.pythonanywhere.com/{}".format(secret))

# main part of txt db for msg sending
joined_file = open(config.db_path + "joined.txt", "r")
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
        sti = open(config.sticker_path + 'AnimatedSticker5.tgs', 'rb')
        await bot.send_sticker(message.chat.id, sti)
        await bot.send_message(message.from_user.id, f'Hello {user_name}!', reply_markup=keyboard)

    elif res is False:
        # TXT DataBase:
        # adding user id to txt db for msg sending
        if not str(message.chat.id) in joinedUsers:
            joined_file = open(config.db_path + "joined.txt", 'a')
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


@dp.message_handler(Text(equals="💸HotLine Search"), state=None)
async def get_state_1(message: types.Message):
    await bot.send_message(message.from_user.id, 'Send me a product name')
    await TryMySets.set_1.set()


@dp.message_handler(state=TryMySets.set_1)
async def get_state_2(message: types.Message, state: FSMContext):
    if "@" in message.text:
        await bot.send_message(message.from_user.id, 'Please write correct product name')
        return
    ans = message.text
    res = hotline.get_products(ans)
    i = 0
    for p in range(1, 6):
        all_info = res[i]
        if all_info['item_info'] == 'None':
            await bot.send_message(message.from_user.id, 'Некорректный запрос!\n'
                                                         'Попробуйте еще раз!')
            break
        prod = f"{hbold(all_info['item_info'])}\n" \
               f"{hlink(all_info['item_price'], all_info['item_pic'])}\n" \
               f"{all_info['price_a_b']}\n" \
               f"{all_info['item_specs']}\n" \
               f"{hlink('READ MORE', all_info['item_url'])}"
        await bot.send_message(message.from_user.id, prod, parse_mode=types.ParseMode.HTML)
        i += 1
    await state.update_data(answer_1=ans)
    await state.finish()


@dp.message_handler(Text(equals="Написать оператору бота"), state='*')
async def write_to_oper_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Написши свое сообщение оператору бота!')
    await WriteToOper.write_1.set()


@dp.message_handler(state=WriteToOper.write_1)
async def write_to_oper(message: types.Message, state: FSMContext):
    ans = message.text
    await bot.send_message(message.from_user.id, 'Сообщение оператору доставлено!')
    await bot.send_message(config.oper_id, f'Сообщение от пользователя {message.from_user.id}:\n' + ans)
    await state.update_data(answer_1=ans)
    await state.finish()


@dp.message_handler(Text(equals="🪨Камень-ножницы-бумага"))
async def stone_start(message: types.Message):
    start_buttons = ["🪨Камень", "✂️Ножницы", "📄Бумага"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.from_user.id, 'Отлично, давай сыграем!\nДелай свой выбор!\nРаз...Два...Три...',
                           reply_markup=keyboard)


@dp.message_handler(Text(equals=["🪨Камень", "✂️Ножницы", "📄Бумага"]))
async def stone_result(message: types.Message):
    start_buttons = config.start_keys
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    ai = interesting_api.stone_paper()
    await bot.send_message(message.from_user.id, ai)
    player = message.text
    res = interesting_api.stone_paper_fight(ai, player)
    await bot.send_message(message.from_user.id, res, reply_markup=keyboard)


@dp.message_handler(Text(equals="🥲Несмешные шутки"))
async def get_joke(message: types.Message):
    await bot.send_message(message.from_user.id, interesting_api.daddy_jokes())


@dp.message_handler(Text(equals="👽Rick and Morty"))
async def get_rick_morty(message: types.Message):
    await bot.send_message(message.from_user.id, interesting_api.get_morty(), parse_mode=types.ParseMode.HTML)


@dp.message_handler(Text(equals="✒️Распознавание текста"))
async def start_text_recognition(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберете, пожалуйста, изображение на вашем устройстве.\n'
                                                 'Затем отправьте его мне)')


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    await bot.send_message(message.from_user.id, hcode('🕓Please wait, Im reading your text!'), parse_mode=types.ParseMode.HTML)
    file_path = f'{config.text_rec_path}test-{message.chat.id}.jpg'
    await message.photo[-1].download(file_path)
    res = text_recognition.text_rec(file_path)
    start_buttons = config.start_keys
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.from_user.id, '✒️Результат распознавания текста:')
    await bot.send_message(message.from_user.id, res, reply_markup=keyboard)


@dp.message_handler(Text(equals="🃏BlackJack"))
async def start_blackjack(message: types.Message):
    await bot.send_message(message.from_user.id, 'ДОБРО ПОЖАЛОВАТЬ В BLACKJACK!')
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
        ilk = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*dicts.ua_cities)
    elif message.text == "🇷🇺Россия":
        ilk = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*dicts.ru_cities)
    elif message.text == "🇪🇺Города Европы":
        ilk = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*dicts.eu_cities)
    await bot.send_message(message.from_user.id, 'Choose your city please!', reply_markup=ilk)


@dp.message_handler(Text(equals=dicts.all_cities))
async def show_res_weather(message: types.Message):
    city_ru = message.text
    city_en = interesting_api.translate_ru_to_en(city_ru)
    info = weather.get_weather(city_en, city_ru)
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
    for p in range(1, 6):
        new = all_news[i]
        i += 1
        if new['Text'] == 'No text' or new['Text'] == 'Нет текста':
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
