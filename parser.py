import requests
from bs4 import BeautifulSoup
import json

URL = 'https://habr.com/ru/company/first/blog/653781/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36', 'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    chapter = soup.find('h1', class_='tm-article-snippet__title tm-article-snippet__title_h1').find_all("span")
    text_p = soup.find('div', class_="tm-article-body")

    text = []

    for elem in chapter:
        chapter_text = elem.text
        text.append(chapter_text)

    for elem in text_p:
        elem_text = elem.text
        text.append(elem_text)

    name_replace = text[0]
    name_new = "".join(c for c in name_replace if c.isalpha())
    name = name_new + '.json'

    valu = ""
    vale = " "

    while valu in text:
        text.remove(valu)

    while vale in text:
        text.remove(vale)

    with open(name, 'w', encoding='utf-8') as file:
        json.dump(text, file, indent=3, ensure_ascii=False)

    #for item in text:
    #    print(item)

def parse():
    result = get_html(URL)
    if result.status_code == 200:
        get_content(result.text)
    else:
        print('Не могу получить страницу!')

parse();
