import requests
from bs4 import *


def get_products(for_search):
    base_url = 'https://hotline.ua/sr/?q='
    search = for_search
    url = base_url + search.replace(' ', '%20')
    headers = requests.utils.default_headers()
    headers.update({
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    })

    print(url)
    response = requests.get(url, headers=headers)
    src = response.text

    soup = BeautifulSoup(src, "lxml")

    try:
        products = soup.find('div', class_='search-list__body').find_all('div', class_='list-item flex')

        products_list = []
        for product in products:
            item_pic = product.find('div', class_='list-item__photo').find('img').get('src')
            item_info = product.find('div', class_='list-item__info flex-column').find('a', class_='list-item__title text-md m_b-5')
            item_specs = product.find('div', class_='list-item__info flex-column').find('div', class_='list-item__specifications-text')
            item_price_1 = product.find('div', class_='list-item__value flex-column').find('span', class_='price__value')
            price_a_b = product.find('div', class_='list-item__value flex-column').find('div', class_='text-sm')
            item_url = product.find('div', class_='list-item__photo').find('a').get('href')
            item_price = str(item_price_1)
            price = item_price.replace('\xa0', ' ')
            if price_a_b is None:
                price_a_b = 'Нет данных'
            else:
                price_a_b = price_a_b.text.strip()
            products_list.append({
                'item_pic': 'https://hotline.ua' + item_pic,
                'item_info': item_info.text.strip(),
                'item_specs': item_specs.text.strip(),
                'item_price': price[price.find(';">')+3:price.find('</')] + ' грн',
                'price_a_b': price_a_b,
                'item_url': 'https://hotline.ua' + item_url
            })
    except AttributeError:
        print('No such products')
        products_list = []
        for i in range(1, 10):
            products_list.append({
                'item_pic': 'None',
                'item_info': 'None',
                'item_specs': 'None',
                'item_price': 'None',
                'price_a_b': 'None',
                'item_url': 'None'
            })

    return products_list

