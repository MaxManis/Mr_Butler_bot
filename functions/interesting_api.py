import requests
import json
import random
import os
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from google_trans_new import google_translator
import config_files.config as config
from gtts import gTTS


def translate_ru_to_en(ru):
    input_ru = ru
    translator = google_translator()
    res = translator.translate(str(input_ru), lang_tgt='en')
    return res


def translate_en_to_ru(en):
    input_en = en
    translator = google_translator()
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
    ans = translate_en_to_ru(data[0]['answer'])
    res = translate_en_to_ru(data[0]['question'])
    print(res)
    print(ans)

    # ex = {'success': True, 'deck_id': 'srcgbpkbvjsc', 'cards': [{'code': '0C', 'image': 'https://deckofcardsapi.com/static/img/0C.png',
    # 'images': {'svg': 'https://deckofcardsapi.com/static/img/0C.svg', 'png': 'https://deckofcardsapi.com/static/img/0C.png'},
    # 'value': '10', 'suit': 'CLUBS'}], 'remaining': 51}
    # DIAMONDS, HEARTS, CLUBS, SPADES


def daddy_jokes():
    url = 'https://icanhazdadjoke.com/'
    response = requests.get(url, headers={'Accept': 'application/json'})
    res_1 = json.loads(response.text)
    res_2 = res_1['joke']
    translator = google_translator()
    res = translator.translate(str(res_2), lang_tgt='ru')
    return res


def post_track():
    url = 'https://api.parceltrack.ru/v1/trackings/get/SA145413132EE'
    response = requests.get(url, headers={'Accept': 'application/json',
                                          'Api-Key': config.track_api,
                                          'X-Requested-With': 'XMLHttpRequest'
                                          })
    res_1 = json.loads(response.text)
    return res_1


def just_do_txt_without_empty_lines_ha():
    file = open(f'{config.lib_path}dial.txt', 'r', encoding='utf-8')
    to = file.readlines()
    te = []
    for i in to:
        if i != '\n':
            te.append(i)
    with open(f'{config.lib_path}dial2.txt', 'w', encoding='utf-8') as file:
        for i in te:
            file.write(i)
    file.close()


def just_do_txt_without_empty_lines_2_bid_file():
    with open(f'{config.lib_path}dialogues.txt', 'r', encoding='utf-8') as file:
        content = file.readlines()
    data = []
    p = 0
    for i in content:
        if p == 0 and i != '':
            data.append(i.strip())
            p += 1
            continue
        elif p == 1 and i != '':
            data.append(i.strip())
            p += 1
            continue
        elif p == 2 and i != '':
            continue
        elif p == 2 and i == '':
            p = 0
            continue
    with open(f'{config.lib_path}dialogues2.txt', 'w', encoding='utf-8') as file:
        for i in data:
            file.write(i)
    file.close()


def google_text_to_speech(user_id):
    file = open(f'{config.lib_path}dial2.txt', 'r', encoding='utf-8')
    text = file.readlines()
    n = random.randint(1, len(text))
    ts = text[n]
    te = ts[ts.find('-')+2:]
    print(te)
    tts = gTTS(text=te, lang='ru')
    v_path = f'{config.voice_wav_abs_path}dial-{user_id}-gtts.mp3'
    tts.save(v_path)
    return v_path


def del_file_by_path(path):
    os.remove(path)


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
    res = f'<b>Имя: {name}</b>\n' \
          f'Статус: {status}\n' \
          f'Вид: {species}\n' \
          f'{hlink("Img", image)}'
    return res


def time_api(city='Kiev'):
    url = f'http://worldtimeapi.org/api/timezone/Europe/{city}'
    response = requests.get(url)
    src = response.json()
    date = src['datetime']
    time = src['datetime']
    res = [date[:date.find('T')],
           time[time.find('T')+1:time.find('.')]]
    return res


