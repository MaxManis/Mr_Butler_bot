import requests
import config_files.config as config
import functions.interesting_api as interesting_api


def get_weather(city_ru):
    city = interesting_api.translate_ru_to_en(city_ru)
    app_id = config.ow_appid
    print(city)
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={app_id}&units=metric'
    res = requests.get(url)
    data = res.json()
    if data['cod'] == '404':
        city = city_ru
        print(city)
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={app_id}&units=metric'
        res = requests.get(url)
        data = res.json()
    try:
        conditions = interesting_api.translate_en_to_ru(data['weather'][0]['description'])
        temper = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        if conditions == 'clear sky':
            conditions = 'чистое небо'
        elif conditions == 'few clouds':
            conditions = 'несколько облаков'
        elif conditions == 'scattered clouds':
            conditions = 'рассеянные облака'
        elif conditions == 'broken clouds':
            conditions = 'разбитые облака'
        elif conditions == 'shower rain':
            conditions = 'ливень'
        elif conditions == 'rain':
            conditions = 'дождь'
        elif conditions == 'thunderstorm':
            conditions = 'гроза'
        elif conditions == 'snow':
            conditions = 'снег'
        elif conditions == 'light snow':
            conditions = 'легкий снег'
        info = f'<b>В городе {city_ru} сейчас {conditions}.</b>\n' \
               f'<u>Температура: {temper}℃</u>\n' \
               f'Минимальная температура: {temp_min}℃\n' \
               f'Максимальная температура: {temp_max}℃\n'
        return info
    except:
        return 'None'

