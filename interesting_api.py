import requests
import json
import random
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink


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
    res = json.loads(response.text)
    return res['joke']


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
