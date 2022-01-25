from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram import Bot, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
import config
import news_scraper

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    start_buttons = ["Погода", "Новости", "Товары"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.from_user.id, 'Hello!', reply_markup=keyboard)


@dp.message_handler(Text(equals="Новости"))
async def get_all_news(message: types.Message):
    start_buttons = ["Science", "Tech", "World"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await bot.send_message(message.from_user.id, 'Choose news category please!', reply_markup=keyboard)


@dp.message_handler(Text(equals=["Science", "Tech", "World"]))
async def get_all_news(message: types.Message):
    if message.text == "Science":
        all_news = news_scraper.get_news('https://www.bbc.com/news/science_and_environment')
    elif message.text == "Tech":
        all_news = news_scraper.get_news()
    elif message.text == "World":
        all_news = news_scraper.get_news('https://www.bbc.com/news/world')
    i = 0
    for p in range(1, 11):
        new = all_news[i]
        i += 1
        news = f"{hbold(new['Title'])}\n" \
               f"{hunderline(new['Text'])}\n" \
               f"{hlink('Read more', new['Link'])}"
        await bot.send_message(message.from_user.id, news, parse_mode=types.ParseMode.HTML)




executor.start_polling(dp, skip_updates=True)
