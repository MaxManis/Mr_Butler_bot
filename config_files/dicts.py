from aiogram import types
import config_files.config as config


def start_but():
    start_buttons = config.start_keys
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    return keyboard


def buttons_keyboard(buttons):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


ua_cities = ['Киев', 'Харьков', 'Одесса', 'Днепропетровск', 'Донецк', 'Запорожье', 'Львов', 'Кривой Рог',
             'Николаев', 'Мариуполь', 'Луганск', 'Винница', 'Макеевка', 'Херсон', 'Полтава', 'Чернигов',
             'Черкассы', 'Житомир', 'Сумы', 'Хмельницкий', 'Черновцы', 'Горловка', 'Ровно', 'Днепродзержинск', 'Кировоград']

ru_cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань',
             'Самара', 'Челябинск', 'Омск', 'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Пермь', 'Волгоград', 'Воронеж', 'Саратов',
             'Краснодар', 'Тольятти', 'Тюмень', 'Ижевск', 'Барнаул', 'Ульяновск', 'Иркутск', 'Владивосток', 'Ярославль', 'Хабаровск',
             'Махачкала', 'Оренбург', 'Томск', 'Новокузнецк', 'Кемерово', 'Астрахань', 'Рязань', 'Набережные Челны', 'Пенза', 'Липецк',
             'Тула', 'Киров', 'Чебоксары', 'Калининград', 'Курск', 'Улан-Удэ', 'Магнитогорск', 'Тверь', 'Иваново', 'Брянск',
             'Сочи', 'Белгород', 'Сургут']

eu_cities = ['Амстердам', 'Андорра-ла-Велья', 'Афины', 'Белград', 'Берлин', 'Берн', 'Братислава', 'Брюссель', 'Будапешт', 'Бухарест', 'Вадуц',
             'Валлетта', 'Варшава', 'Ватикан', 'Вена', 'Вильнюс', 'Дублин', 'Загреб', 'Киев', 'Кишинёв', 'Копенгаген', 'Лиссабон', 'Лондон',
             'Любляна', 'Люксембург', 'Мадрид', 'Минск', 'Монако', 'Москва', 'Осло', 'Париж', 'Подгорица', 'Прага', 'Рейкьявик',
             'Рига', 'Рим', 'Сан-Марино', 'Сараево', 'Скопье', 'София', 'Стокгольм', 'Таллин', 'Тирана', 'Хельсинки']

all_cities = ['Киев', 'Харьков', 'Одесса', 'Днепропетровск', 'Донецк', 'Запорожье', 'Львов', 'Кривой Рог',
             'Николаев', 'Мариуполь', 'Луганск', 'Винница', 'Макеевка', 'Херсон', 'Полтава', 'Чернигов',
             'Черкассы', 'Житомир', 'Сумы', 'Хмельницкий', 'Черновцы', 'Горловка', 'Ровно', 'Днепродзержинск', 'Кировоград', 'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань',
             'Самара', 'Челябинск', 'Омск', 'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Пермь', 'Волгоград', 'Воронеж', 'Саратов',
             'Краснодар', 'Тольятти', 'Тюмень', 'Ижевск', 'Барнаул', 'Ульяновск', 'Иркутск', 'Владивосток', 'Ярославль', 'Хабаровск',
             'Махачкала', 'Оренбург', 'Томск', 'Новокузнецк', 'Кемерово', 'Астрахань', 'Рязань', 'Набережные Челны', 'Пенза', 'Липецк',
             'Тула', 'Киров', 'Чебоксары', 'Калининград', 'Курск', 'Улан-Удэ', 'Магнитогорск', 'Тверь', 'Иваново', 'Брянск',
             'Сочи', 'Белгород', 'Сургут', 'Амстердам', 'Андорра-ла-Велья', 'Афины', 'Белград', 'Берлин', 'Берн', 'Братислава', 'Брюссель', 'Будапешт', 'Бухарест', 'Вадуц',
             'Валлетта', 'Варшава', 'Ватикан', 'Вена', 'Вильнюс', 'Дублин', 'Загреб', 'Киев', 'Кишинёв', 'Копенгаген', 'Лиссабон', 'Лондон',
             'Любляна', 'Люксембург', 'Мадрид', 'Минск', 'Монако', 'Москва', 'Осло', 'Париж', 'Подгорица', 'Прага', 'Рейкьявик',
             'Рига', 'Рим', 'Сан-Марино', 'Сараево', 'Скопье', 'София', 'Стокгольм', 'Таллин', 'Тирана', 'Хельсинки']

all_sports = ['Football', 'Tennis']  # , 'American-Football', 'Baseball', 'Basketball', 'Ice-Hockey', 'Esports'