# - *- coding: utf- 8 - *-
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram import Bot, types

from aiogram.utils.markdown import hbold, hunderline, hcode, hlink

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext

import config_files.dicts as dicts
import config_files.config as config
from config_files.my_states import TryMySets, WriteToOper, TasksToDo, WriteToUser, GoogTextTS, SportEvents

import functions.tasks_list as tasks_list
import functions.news_scraper as news_scraper
import functions.weather as weather
import functions.chatbot_talk as chatbot_talk
import functions.exchange_rate as exchange_rate
import functions.sqlite_db as sqlite_db
import functions.text_recognition as text_recognition
import functions.blackjack as blackjack
import functions.interesting_api as interesting_api
import functions.hotline as hotline
import functions.speech_recog as speech_recog
import functions.sport_events as sport_events

import random
import time
import json

bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

oper_id = config.oper_id
secret = config.secret

# bot.remove_webhook()
# sleep(1)
# bot.set_webhook(url=f"https://boston88.pythonanywhere.com/{secret}"


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    joined_users = sqlite_db.txt_db_set()
    print(joined_users)
    tasks_list.create_tasks_file(message.from_user.id)
    new_user_id = message.from_user.id
    check = sqlite_db.sql_check(new_user_id)

    if check is True:
        user_name = message.from_user.first_name
        await bot.send_sticker(message.chat.id, sqlite_db.open_sticker(5))
        await bot.send_message(message.from_user.id, f'Hello {user_name}!', reply_markup=dicts.start_but())
    elif check is False:
        # adding user id to txt db for msg sending
        sqlite_db.txt_db_add(joined_users, message.chat.id)
        # Share contact
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="📲Поделиться контактом📲", request_contact=True)
        keyboard.add(button_phone)
        await bot.send_message(message.from_user.id, 'Для продолжения работы с ботом нкжно зарегестрироваться!'
                                                     '\nОтправь мне свой контакт кнопкой ниже.', reply_markup=keyboard)


@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    if message.contact is not None:  # Если присланный объект contact не равен нулю
        res = sqlite_db.add_user(message)
        await bot.send_message(message.chat.id, f"🚹 Пользователь распознан как {res}")
        await bot.send_sticker(message.chat.id, sqlite_db.open_sticker(16))
        await start_command(message)
    else:
        await bot.send_message(message.chat.id, "Авторизация не удалась. \nПопробуйте еще раз!")
        await start_command(message)


@dp.message_handler(commands="admin")
async def help_command(message: types.Message):
    if str(message.from_user.id) in config.allowed_admin_users:
        await bot.send_message(message.chat.id, "Привет! Это панель админа с командами!\n"
                                                "/to_user - написать пользователю")
    else:
        await bot.send_message(message.chat.id, "Ая-яй, тебе сюда нельзя!")


@dp.message_handler(commands="help")
async def help_command(message: types.Message):
    await bot.send_message(message.chat.id, "Помощь...")


@dp.message_handler(commands="to_user", state='*')
async def to_user_command(message: types.Message):
    await bot.send_message(message.chat.id, "Введи ID пользователя, которому пишем")
    await WriteToUser.write_1.set()


@dp.message_handler(state=WriteToUser.write_1)
async def to_user_command_1(message: types.Message, state: FSMContext):
    ans = message.text
    await bot.send_message(message.chat.id, f"Введи сообщение для пользователя {ans}")
    await state.update_data(user_id=ans)
    await WriteToUser.write_2.set()


@dp.message_handler(state=WriteToUser.write_2)
async def to_user_command_2(message: types.Message, state: FSMContext):
    ans = message.text
    try:
        user_id = await state.get_data('user_id')
        await bot.send_message(user_id['user_id'], f"Сообщение от оператора бота: \n{ans}")
    except:
        await bot.send_message(message.chat.id, f"Сообщение НЕ доставлено.")
    await state.finish()


@dp.message_handler(content_types=[types.ContentType.VOICE])
async def voice_message_handler(message: types.Message):
    await bot.send_sticker(message.chat.id, sqlite_db.open_sticker(9))
    await bot.send_message(message.from_user.id, hcode('🕓Пожалуйста, подождите, я слушаю сообщение!'), parse_mode=types.ParseMode.HTML)
    file_path = f'{config.voice_rec_path}OGG_file-{message.chat.id}-{random.randint(146, 24357)}.ogg'
    await message.voice.download(file_path)  # .get_file()
    res = speech_recog.speech_rec(file_path, message.chat.id)
    await bot.send_message(message.from_user.id, hcode('🔊Результат распознавания аудио:'), parse_mode=types.ParseMode.HTML)
    await bot.send_message(message.from_user.id, res)


@dp.message_handler(Text(equals="GTTS"))
async def get_gtts(message: types.Message):
    res = interesting_api.google_text_to_speech(message.from_user.id)
    await bot.send_voice(message.from_user.id, open(res, "rb"))
    interesting_api.del_file_by_path(res)


@dp.message_handler(commands="sport", state='*')
async def get_sport(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери, пожалуйста, вид спорта!', reply_markup=dicts.buttons_keyboard(dicts.all_sports))
    await SportEvents.sport_1.set()


@dp.message_handler(state=SportEvents.sport_1)
async def get_sport(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Подожди, пожалуйста, клацаю каналы...")
    sport_type = message.text
    print(sport_type)
    res = sport_events.parse_sport_by_type(sport_type, message.from_user.id)
    with open(res, 'r', encoding='utf-8') as json_file:
        json_object = json.load(json_file)
        json_file.close()
    leagues = []
    for i in json_object:
        leagues.append(i)
    await bot.send_message(message.from_user.id, "Выбери лигу для отображения событий.", parse_mode=types.ParseMode.HTML,
                           reply_markup=dicts.buttons_keyboard(leagues))
    await state.update_data(sport_type=sport_type)
    await SportEvents.sport_2.set()


@dp.message_handler(state=SportEvents.sport_2)
async def get_sport(message: types.Message, state: FSMContext):
    ans = message.text
    await state.update_data(sport_league=ans)
    with open(f'{config.sport_json_path}json_sport_data-{str(message.from_user.id)}.json', 'r', encoding='utf-8') as json_file:
        json_object = json.load(json_file)
        json_file.close()
    mess = f'<b>{ans}:</b>\n'
    for y in json_object[ans]:
        print(y)
        if y["time"] != 'No data':
            mess += f'{y["team1"]} vs {y["team2"]} at {y["time"]}\n'
        else:
            mess += f'{y["team1"]} vs {y["team2"]} today!\n'
    await bot.send_message(message.from_user.id, mess, parse_mode=types.ParseMode.HTML,
                           reply_markup=dicts.start_but())
    await state.finish()


@dp.message_handler(Text(equals="💸Поиск на HotLine"), state=None)
async def get_state_1(message: types.Message):
    await bot.send_message(message.from_user.id, 'Отправь мне название продукта для поиска.')
    await TryMySets.set_1.set()


@dp.message_handler(state=TryMySets.set_1)
async def get_state_2(message: types.Message, state: FSMContext):
    if "@" in message.text:
        await bot.send_message(message.from_user.id, 'Напиши, пожалуйста корректное название')
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


@dp.message_handler(Text(equals="Список задачь"))
async def start_tasks_to(message: types.Message):
    buttons = ["Добавить задачу", "Посмотреть все задачи", "Удалить задачу"]
    await bot.send_message(message.from_user.id, 'Давай посмотрим на твои задачи!', reply_markup=dicts.buttons_keyboard(buttons))
    await TasksToDo.task_1.set()


@dp.message_handler(Text(equals=["Добавить задачу", "Посмотреть все задачи", "Удалить задачу"]), state=None)
async def start_tasks_to(message: types.Message):
    ans = message.text
    if ans == "Добавить задачу":
        await bot.send_message(message.from_user.id, 'Напиши текст новой задачи и мы ее добавим!')
        await TasksToDo.task_1.set()
    elif ans == "Посмотреть все задачи":
        content = tasks_list.read_tasks(message.from_user.id)
        count_tasks = len(content)
        res = f'<b>ВСЕГО ЗАДАЧЬ - {count_tasks}:</b>\n'
        for i in content:
            res += i + '\n'
        await bot.send_message(message.from_user.id, res, parse_mode=types.ParseMode.HTML, reply_markup=dicts.start_but())
    elif ans == "Удалить задачу":
        await bot.send_message(message.from_user.id, 'Введи ID задачи, которую нужно удалить!')
        await TasksToDo.task_2.set()


@dp.message_handler(state=TasksToDo.task_1)
async def start_tasks_to_1(message: types.Message, state: FSMContext):
    ans1 = message.text
    tasks_list.create_task(ans1, message.from_user.id)
    await state.update_data(answer_1=ans1)
    await bot.send_message(message.from_user.id, "Задача добавлена!", reply_markup=dicts.start_but())
    await state.reset_state()


@dp.message_handler(state=TasksToDo.task_2)
async def start_tasks_to_2(message: types.Message, state: FSMContext):
    count_tasks = len(tasks_list.read_tasks(message.from_user.id))
    if count_tasks == 0 or message.text == 0:
        return
    ans2 = message.text
    try:
        if int(ans2) > count_tasks:
            return
        tasks_list.del_tasks(ans2, message.from_user.id)
    except:
        await bot.send_message(message.from_user.id, "Введи цифру!", reply_markup=dicts.start_but())
        return
    await bot.send_message(message.from_user.id, "Задача удалена!", reply_markup=dicts.start_but())
    await state.update_data(answer_2=ans2)
    await state.finish()


@dp.message_handler(Text(equals="Написать оператору бота"), state='*')
async def write_to_oper_start(message: types.Message):
    sti = open(config.sticker_path + 'AnimatedSticker11.tgs', 'rb')
    await bot.send_sticker(message.chat.id, sti)
    await bot.send_message(message.from_user.id, 'Что-то не так!?\nНаписши свое сообщение оператору бота!')
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
    buttons = ["🪨Камень", "✂️Ножницы", "📄Бумага"]
    await bot.send_message(message.from_user.id, 'Отлично, давай сыграем!\nДелай свой выбор!\nРаз...Два...Три...',
                           reply_markup=dicts.buttons_keyboard(buttons))


@dp.message_handler(Text(equals=["🪨Камень", "✂️Ножницы", "📄Бумага"]))
async def stone_result(message: types.Message):
    ai = interesting_api.stone_paper()
    await bot.send_message(message.from_user.id, ai)
    player = message.text
    res = interesting_api.stone_paper_fight(ai, player)
    await bot.send_message(message.from_user.id, res, reply_markup=dicts.start_but())


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
    await bot.send_sticker(message.chat.id, sqlite_db.open_sticker(5))
    await bot.send_message(message.from_user.id, hcode('🕓Пожалуйста, подождите, я читаю текст!'), parse_mode=types.ParseMode.HTML)
    file_path = f'{config.text_rec_path}JPG-file-{message.chat.id}-{random.randint(165, 43267)}.jpg'
    await message.photo[-1].download(file_path)
    res = text_recognition.text_rec(file_path)
    await bot.send_message(message.from_user.id, hcode('✒️Результат распознавания текста:'), parse_mode=types.ParseMode.HTML)
    await bot.send_message(message.from_user.id, res, reply_markup=dicts.start_but())


@dp.message_handler(Text(equals="🃏BlackJack"))
async def start_blackjack(message: types.Message):
    await bot.send_message(message.from_user.id, 'ДОБРО ПОЖАЛОВАТЬ В BLACKJACK!')
    global dealer_hand, player_hand
    dealer_hand = blackjack.deal()
    player_hand = blackjack.deal()
    await bot.send_message(message.from_user.id, "Дилер показывает " +
                           hlink(str(dealer_hand[0]['value']), dealer_hand[0]['link']), parse_mode=types.ParseMode.HTML)
    await bot.send_message(message.from_user.id, "У вас " + hlink(str(player_hand[0]['value']), player_hand[0]['link']) +
                           ' and ' + hlink(str(player_hand[1]['value']), player_hand[1]['link']) + " с суммой " +
                           str(blackjack.total(player_hand)), parse_mode=types.ParseMode.HTML)
    blackjack.blackjack(dealer_hand, player_hand)
    buttons = ["♥️Взять", "♠️Открыть", "❌Выйти"]
    await bot.send_message(message.from_user.id, 'Что ты хочешь, Взять, Открыть, или Выйти: ', reply_markup=dicts.buttons_keyboard(buttons))


@dp.message_handler(Text(equals=["♥️Взять", "♠️Открыть", "❌Выйти"]))
async def play_blackjack(message: types.Message):
    if message.text == "♥️Взять":
        blackjack.hit(player_hand)
        while blackjack.total(dealer_hand) < 17:
            blackjack.hit(dealer_hand)
        await bot.send_message(message.from_user.id, blackjack.score(dealer_hand, player_hand), reply_markup=dicts.start_but())
    elif message.text == "♠️Открыть":
        while blackjack.total(dealer_hand) < 17:
            blackjack.hit(dealer_hand)
        await bot.send_message(message.from_user.id, blackjack.score(dealer_hand, player_hand), reply_markup=dicts.start_but())
    elif message.text == "❌Выйти":
        info = 'Пока!'
        await bot.send_message(message.from_user.id, info, reply_markup=dicts.start_but())


@dp.message_handler(Text(equals="⛅️Погода"))
async def get_weather(message: types.Message):
    buttons = ["🇺🇦Украина", "🇷🇺Россия", "🇪🇺Города Европы"]
    await bot.send_message(message.from_user.id, 'Выберете, пожалуйста, регион.', reply_markup=dicts.buttons_keyboard(buttons))


@dp.message_handler(Text(equals=["🇺🇦Украина", "🇷🇺Россия", "🇪🇺Города Европы"]))
async def choose_city(message: types.Message):
    if message.text == "🇺🇦Украина":
        await bot.send_message(message.from_user.id, 'Выбери город из списка!', reply_markup=dicts.buttons_keyboard(dicts.ua_cities))
    elif message.text == "🇷🇺Россия":
        await bot.send_message(message.from_user.id, 'Выбери город из списка!', reply_markup=dicts.buttons_keyboard(dicts.ru_cities))
    elif message.text == "🇪🇺Города Европы":
        await bot.send_message(message.from_user.id, 'Выбери город из списка!', reply_markup=dicts.buttons_keyboard(dicts.eu_cities))


@dp.message_handler(Text(equals=dicts.all_cities))
async def show_res_weather(message: types.Message):
    city_ru = message.text
    info = weather.get_weather(city_ru)
    await bot.send_message(message.from_user.id, info, parse_mode=types.ParseMode.HTML, reply_markup=dicts.start_but())


@dp.message_handler(Text(equals="📰Новости"))
async def choose_all_news(message: types.Message):
    buttons = ["🔬Science", "💻Tech", "🌎World"]
    await bot.send_message(message.from_user.id, 'Выбери категорию новостей!', reply_markup=dicts.buttons_keyboard(buttons))


@dp.message_handler(Text(equals=["🔬Science", "💻Tech", "🌎World"]))
async def get_news(message: types.Message):
    if message.text == "🔬Science":
        all_news = news_scraper.get_news('https://www.bbc.com/news/science_and_environment')
    elif message.text == "💻Tech":
        all_news = news_scraper.get_news()
    elif message.text == "🌎World":
        all_news = news_scraper.get_news('https://www.bbc.com/news/world')
    i = 0
    for p in range(1, 6):
        new = all_news[i]
        i += 1
        if new['Text'] == 'No text' or new['Text'] == 'Нет текста':
            continue
        news = f"{hbold(new['Title'])}\n" \
               f"{hunderline(new['Text'])}\n" \
               f"{hlink('Read more', new['Link'])}"
        await bot.send_message(message.from_user.id, news, parse_mode=types.ParseMode.HTML, reply_markup=dicts.start_but())
        time.sleep(1)


@dp.message_handler(Text(equals="💵Курс валют"))
async def get_rates_choose(message: types.Message):
    buttons = ["USD $", "EUR €", "UAH ₴", "RUB ₽"]
    await bot.send_message(message.from_user.id, 'Выберете, пожалуйста, валюту.', reply_markup=dicts.buttons_keyboard(buttons))


@dp.message_handler(Text(equals=["USD $", "EUR €", "UAH ₴", "RUB ₽"]))
async def get_rates(message: types.Message):
    result = exchange_rate.gey_rate(message.text[:message.text.find(' ')])
    await bot.send_message(message.from_user.id, result, parse_mode=types.ParseMode.HTML, reply_markup=dicts.start_but())


@dp.message_handler()
async def to_talk(message: types.Message):
    question = message.text
    response = chatbot_talk.ai_talk(question)
    await bot.send_message(message.from_user.id, response, reply_markup=dicts.start_but())


executor.start_polling(dp, skip_updates=True)
