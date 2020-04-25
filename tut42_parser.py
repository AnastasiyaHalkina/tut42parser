"""
Этот скрипт будет доставать статьи о науке с новостного сайта
https://42.tut.by/rubric/education/
"""

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://42.tut.by/rubric/{}/"


def get_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    return None


def get_data_page(text):
    soup = BeautifulSoup(text, "html.parser")
    articles = soup.select('div.news-entry.big.annoticed.time.ni')

    if len(articles) >= 1:
        articles_list = []
        for article in articles:
            art_data = {}
            url = article.find('a', class_='entry__link').get('href').strip()

            title = article.find('span', class_='entry-head').text.strip()

            date_public = article.find('span', class_='entry-time').find('span').text.strip()

            short_desc = article.find('span', class_="entry-note").text.strip()

            art_data['title'] = title
            art_data['url'] = url
            art_data['public'] = date_public
            art_data['description'] = short_desc

            articles_list.append(art_data)

        return articles_list
    else:
        return 'error'


def get_both_pages():
    pages_lst = ["education", "internet"]
    texts_lst = []

    for name in pages_lst:
        url = BASE_URL.format(name)
        text = get_page(url)
        texts_lst.append(text)
    return texts_lst


def main():
    texts_lst = get_both_pages()
    if texts_lst:
        try:
            text1, text2 = texts_lst
            result1, result2 = get_data_page(text1), get_data_page(text2)
        except:
            return "Ошибка извлечения данных. Возможно структура страницы была изменена"
        else:
            if result1 == 'error' or result2 == 'error':
                return "Ошибка. Возможно, контейнер, содержащий статьи, был переименован"
            return list(zip(result2, result1))[:10]
    else:
        return "Ошибка обращения к странице. Возможно страница временно недоступна"


if __name__ == "__main__":
    print(main())
