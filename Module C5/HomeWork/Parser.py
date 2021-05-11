import requests  # импортируем наш знакомый модуль
from bs4 import BeautifulSoup
import csv
import os
# import lxml.html
# from lxml import etree

URL = 'https://auto.ria.com/newauto/marka-skoda/'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
           'accept': '*/*'}
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
    # print(pagination)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='proposition_link')

    cars = []
    for item in items:
        title = item.find('div', class_='proposition_title')
        uah_price = item.find('span', class_='size16')
        region = item.find('div', class_='proposition_information')

        if uah_price:
            uah_price = uah_price.get_text()
        else:
            uah_price = 'Цену уточняйте'
        # price = item.find('div', class_='proposition_price')
        cars.append({
            'title': title.find('span', class_='link').get_text(strip=True) + ' ' +
                     title.find('div', class_ = 'proposition_equip size13').find_next('span', class_='link').get_text(strip=True),
            'link': 'https://auto.ria.com'+item.get('href'),
            'usd_price': item.find('span', class_='green bold size22').get_text(strip=True),
            'uah_price': uah_price,
            'city': region.find_next('span', class_='item region').get_text()

        })
    return cars


def save_file(items,path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка','Ссылка','Цена в $','Цена в грн','Город'])
        for item in items:
            writer.writerow([item['title'],item['link'],item['usd_price'],item['uah_price'],item['city']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count+1):
            print(f'Парсинг страницы {page} из {pages_count}')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars,FILE)
        print(len(cars))
        os.startfile(FILE)
    else:
        print('Error')


def main():
    base = 'https://ru.stackoverflow.com/'
    html = requests.get(base).content
    soap = BeautifulSoup(html, 'lxml')
    div = soap.find('div', id='question-mini-list')
    a = div.find_all('a', class_="question-hyperlink")

    for _ in a:
        print(_.getText())


if __name__ == '__main__':
    parse()

























# создадим объект ElementTree. Он возвращается функцией parse()
# tree = etree.parse('Welcome to Python.org.html',lxml.html.HTMLParser())  # попытаемся спарсить наш файл с помощью html парсера. Сам html - это то что мы скачали и поместили в папку из браузера.
# print(tree)
# ul = tree.findall(
#     '/body/div/div[3]/div/section/div[2]/div[2]/div/ul/li')  # помещаем в аргумент методу findall скопированный xpath. Здесь мы получим все элементы списка новостей. (Все заголовки и их даты)
# print(ul)
# # создаём цикл в котором мы будем выводить название каждого элемента из списка
# for li in ul:
#     a = li.find('a')  # в каждом элементе находим где хранится заголовок новости. У нас это тег <a>. Т.е. гиперссылка на которую нужно нажать, чтобы перейти на страницу с новостью. (Гиперссылки в html это всегда тэг <a>)
#     b = li.find('time')
#     print(a.text)  # из этого тега забираем текст - это и будет нашим названием
#     print(b.get('datetime'))

# tree = etree.parse('test.html', lxml.html.HTMLParser())
#
# text = tree.xpath('/html/body/tag1/tag2/text()')
#
# print(text[0])