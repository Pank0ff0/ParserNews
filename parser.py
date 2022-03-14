from turtle import ht
import requests 
from bs4 import BeautifulSoup
import csv

CSV = 'news.csv'
HOST = 'https://www.m24.ru/'
URL = 'https://www.m24.ru/news'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params) 
    return r
    
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('p', class_= 'b-materials-list__title b-materials-list__title_news')
    news = []


    for  item in items:
        news.append(
            {
                'title':item.find('a').get_text(strip=True),
                'link':HOST + item.find('a').get('href'),
                'foto':HOST + item.find('i', class_ = 'b-materials-list__img').find('img').get('src')
            }
        )
    return news

def seve_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(['Новость', 'Ссылка на новость', 'Фото к новости'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['foto']])
            
            
def parser():
    html = get_html(URL)
    if html.status_code == 200:
        news = []
        news.extend(get_content(html.text))
        print('Страница спаршена')
        seve_doc(news, CSV)
        pass
    else:
        print('Error')
        
parser()