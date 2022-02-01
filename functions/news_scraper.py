import requests
from bs4 import BeautifulSoup
from google_trans_new import google_translator

translator = google_translator()


def get_news(category='https://www.bbc.com/news/technology'):
    all_news = []

    # url = 'https://www.bbc.com/news/technology'
    # url = 'https://www.bbc.com/news/science_and_environment'
    url = category

    headers = {
        "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/97.0.4692.71 Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    news = soup.find('ol', class_='gs-u-m0 gs-u-p0 lx-stream__feed qa-stream')\
        .find_all('li', class_='lx-stream__post-container')

    for i in news:
        try:
            new_title = i.find('article').find('header').find('div').find('h3').text

            new_text = i.find('article').find('div', class_='gs-u-mb+ gel-body-copy qa-post-body')\
                .find('div', class_='lx-stream-related-story').find('div', class_='gel-5/8@l').find('p').text

            new_link = i.find('article').find('div', class_='gs-u-mb+ gel-body-copy qa-post-body')\
                .find('div', class_='lx-stream-related-story').find('div', class_='gel-5/8@l').find('a').get("href")
        except:
            new_text = 'No text'
            new_link = 'No link'

        all_news.append(
            {
                'Title': translator.translate(str(new_title), lang_tgt='ru'),
                'Text': translator.translate(str(new_text), lang_tgt='ru'),
                'Link': 'https://www.bbc.com' + new_link
            }
        )

    return all_news
