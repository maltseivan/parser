import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import re


URL = 'https://habr.com/ru/search/?q=big%20data&target_type=posts&order=relevance'
HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Mobile Safari/537.36', 'accept': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find_all('a', class_='tm-article-snippet__title-link')


    for elem in link:
        text = []
        link_href_attr = elem.get("href")
        urlink = 'https://habr.com' + link_href_attr

        def get_html(urlink, params=None):
            r_content = requests.get(urlink, headers=HEADERS, params=params)
            return r_content

        def get_content_text(html):
            soup = BeautifulSoup(html, 'html.parser')
            chapter = soup.find('h1', class_='tm-article-snippet__title tm-article-snippet__title_h1').find_all("span")
            text_p = soup.find('div', class_="tm-article-body")
                
            for elem in chapter:
                chapter_text = elem.text
                text.append(chapter_text)

            for elem in text_p:
                elem_text = elem.text
                text.append(elem_text)

                valu = ""
                vale = " "

                while valu in text:
                    text.remove(valu)

                while vale in text:
                    text.remove(vale)


            name_chapter = re.sub("[$|@|&|:|/|!|?|;|%|#|$|^|*|)|(|-|_|]","",text[0])

            name = name_chapter + '.json'
            with open(name, 'w', encoding='utf-8') as file:
                json.dump(text, file, indent=3, ensure_ascii=False)

            pprint(name)

            

        def parse_text():
            result_text = get_html(urlink)
            if result_text.status_code == 200:
                get_content_text(result_text.text)
            else:
                print('Не могу получить страницу!')

        parse_text();


def parse():
    result = get_html(URL)
    if result.status_code == 200:
        get_content(result.text)
    else:
        print('Не могу получить страницу!')


parse();