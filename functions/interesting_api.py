import requests
import json
import random
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from google_trans_new import google_translator
import config_files.config

translator = google_translator()


def translate_ru_to_en(ru):
    input_ru = ru
    res = translator.translate(str(input_ru), lang_tgt='en')
    return res


def translate_en_to_ru(en):
    input_en = en
    res = translator.translate(str(input_en), lang_tgt='ru')
    return res


def stone_paper():
    i = random.randint(1, 30)
    if i <= 10:
        res = '🪨Камень'
    elif i <= 20:
        res = '✂️Ножницы'
    elif i <= 30:
        res = '📄Бумага'
    return res


def stone_paper_fight(ai_res, player_res):
    ai = ai_res
    player = player_res
    # "🪨Камень", "✂️Ножницы", "📄Бумага"
    if player == '🪨Камень' and ai == '✂️Ножницы':
        res = 'Камень ломает ножницы\nТы победил!'
    elif player == '🪨Камень' and ai == '📄Бумага':
        res = 'Бумага кроет камень!\nТы проиграл!'
    elif player == '🪨Камень' and ai == '🪨Камень':
        res = "Камень против камня?\nХмм, это ничья!"
    elif player == '✂️Ножницы' and ai == '🪨Камень':
        res = 'Камень ломает ножницы\nТы проиграл!'
    elif player == '✂️Ножницы' and ai == '✂️Ножницы':
        res = "Ножницы против ножниц?\nХмм, это ничья!"
    elif player == '✂️Ножницы' and ai == '📄Бумага':
        res = 'Ножницы разрезают бумагу\nТы победил!'
    elif player == '📄Бумага' and ai == '🪨Камень':
        res = 'Бумага кроет камень!\nТы победил!'
    elif player == '📄Бумага' and ai == '✂️Ножницы':
        res = 'Ножницы разрезают бумагу\nТы проиграл!'
    elif player == '📄Бумага' and ai == '📄Бумага':
        res = "Бумага против бумаги?\nХмм, это ничья!"
    return res


def viktorina():
    url = 'http://jservice.io/api/random?count=1'

    response = requests.get(url)
    data = response.json()

    print(data[0]['question'])
    print(data[0]['answer'])
    print(data)


    # ex = {'success': True, 'deck_id': 'srcgbpkbvjsc', 'cards': [{'code': '0C', 'image': 'https://deckofcardsapi.com/static/img/0C.png',
    # 'images': {'svg': 'https://deckofcardsapi.com/static/img/0C.svg', 'png': 'https://deckofcardsapi.com/static/img/0C.png'},
    # 'value': '10', 'suit': 'CLUBS'}], 'remaining': 51}
    # DIAMONDS, HEARTS, CLUBS, SPADES


def daddy_jokes():
    url = 'https://icanhazdadjoke.com/'
    response = requests.get(url, headers={'Accept': 'application/json'})
    res_1 = json.loads(response.text)
    res_2 = res_1['joke']
    res = translator.translate(str(res_2), lang_tgt='ru')
    return res


def post_track():
    url = 'https://api.parceltrack.ru/v1/trackings/get/SA145413132EE'
    response = requests.get(url, headers={'Accept': 'application/json',
                                          'Api-Key': config_files.config.track_api,
                                          'X-Requested-With': 'XMLHttpRequest'
                                          })
    res_1 = json.loads(response.text)
    return res_1


def get_morty():
    url = 'https://rickandmortyapi.com/api/character'
    response = requests.get(url)
    data = response.json()
    id = data['info']['count']
    url_char = f'https://rickandmortyapi.com/api/character/{random.randint(1, id)}'
    response_char = requests.get(url_char)
    name = response_char.json()['name']
    status = response_char.json()['status']
    species = response_char.json()['species']
    image = response_char.json()['image']
    res = f'<b>Name: {name}</b>\n' \
          f'Status: {status}\n' \
          f'Species: {species}\n' \
          f'{hlink("Image", image)}'

    return res


