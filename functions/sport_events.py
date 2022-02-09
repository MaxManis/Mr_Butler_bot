from bs4 import BeautifulSoup
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
import sys
import config_files.config as config
import json


class Client(QWebEnginePage):
    def __init__(self, url):
        global app
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ""
        self.loadFinished.connect(self.on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def on_load_finished(self):
        self.html = self.toHtml(self.callable)
        print("Load Finished")

    def callable(self, data):
        self.html = data
        self.app.quit()


def get_sport_page_as_file(sport_type, user_id):
    url = f'https://1xbet.com/line/{sport_type}/'
    client_response = Client(url)
    time.sleep(3)
    with open(f'{config.sport_json_path}/index-{user_id}.html', 'w', encoding='utf-8') as file:
        file.write(client_response.html)
    res = client_response.html
    return res


def parse_sport_by_type(sport_type, user_id='01001'):
    get_sport_page_as_file(sport_type, user_id)
    with open(f'{config.sport_json_path}/index-{user_id}.html', 'r', encoding='utf-8') as file:
        src = file.read()
    # url = 'https://1xbet.com/line/Football/'
    # url = f'https://1xbet.com/line/{sport_type}/'
    # client_response = Client(url)
    # time.sleep(5)
    # src = client_response.html
    soup = BeautifulSoup(src, "lxml")
    res = []
    all_leagues = soup.find('div', id='maincontent').find('div', class_='game_content_line on_main live-content').find_all('div',{"data-name":"dashboard-champ-content"})
    for one_league in all_leagues:
        league = one_league.find('div', class_='fixed-heading').find('div', class_='c-events__name').find('a').text
        country = one_league.find('div', class_='fixed-heading').find('div', class_='c-events__item c-events__item_head').find('div').get('title')
        try:
            events = one_league.find_all('div', class_='c-events__item c-events__item_game') #   c-events__item c-events__item_game c-events__item--has-no-info
        except:
            events = one_league.find_all('div', class_='c-events__item c-events__item_game c-events__item--has-no-info')
        print('=========================================')
        print(country)
        print('-----------' + league + '-----------')
        for event in events:
            try:
                event_time = event.find('div', class_='c-events__time min').find('span').text
            except:
                event_time = 'No data'
            teams = event.find('a', class_='c-events__name').find('span', class_='c-events__teams').find_all('span', class_='c-events__team')
            team_list = []
            for team in teams:
                t1 = team.text
                team_list.append(t1)
            res.append({
                'league': league,
                'team1': team_list[0].strip(),
                'team2': team_list[1].strip(),
                'time': event_time
            })
            print(f'{team_list[0].strip()} vs {team_list[1].strip()} at {event_time}')
    json_path = res_to_json_try(res, user_id)
    print(json_path)
    return json_path


def res_to_json_try(res, user_id):
    print(res)
    leagues = []
    for i in res:
        league = i['league']
        if league not in leagues:
            leagues.append(league)
    c = 0
    mess = ""
    for i in res:
        if mess == "":
            mess += '{ "' + leagues[c] + '": ['
        elif mess != "" and i['league'] == leagues[c]:
            mess += ', '
        if i['league'] == leagues[c]:
            mess += '{"team1": ' + '"' + i["team1"] + '"' +\
                    ', "team2": ' + '"' + i["team2"] + '"' + \
                    ', "time": ' + '"' + i["time"] + '"}'
            continue
        elif i['league'] != leagues[c]:
            mess += ']'
            print(mess)
            c += 1
            print(c)
            mess += ', "' + leagues[c] + '": ['
            mess += '{"team1": ' + '"' + i["team1"] + '"' +\
                    ', "team2": ' + '"' + i["team2"] + '"' + \
                    ', "time": ' + '"' + i["time"] + '"}'
    mess += ']}'
    print(mess)
    json_1 = json.loads(mess)
    with open(f'{config.sport_json_path}json_sport_data-{str(user_id)}.json', 'w', encoding='utf-8') as outfile:
        json.dump(json_1, outfile, indent=4, ensure_ascii=False, sort_keys=False, separators=(', ', ': '))
    json_path = f'{config.sport_json_path}json_sport_data-{str(user_id)}.json'
    return json_path


def res_to_txt_try(res):
    leagues = []
    for i in res:
        league = i['league']
        if league not in leagues:
            leagues.append(league)
    count_league = len(leagues)
    print(leagues)
    print(count_league)
    c = 0
    mess = ''
    for i in res:
        if mess == '':
            mess += f'<b>{leagues[c]}:</b>\n'
        if i['league'] == leagues[c]:
            mess += f'{i["team1"]} vs {i["team2"]} at {i["time"]}\n'
            continue
        elif i['league'] != leagues[c]:
            with open(f'{config.functions_path}/sport.txt', 'a', encoding='utf-8') as file:
                file.write(mess)
            mess = ''
            c += 1
            print(c)
            mess += f'<b>{leagues[c]}:</b>\n'
            mess += f'{i["team1"]} vs {i["team2"]} at {i["time"]}\n'


def read_sport_file():
    with open(f'{config.functions_path}/sport.txt', 'r', encoding='utf-8') as file:
        src = file.read()
    return src




