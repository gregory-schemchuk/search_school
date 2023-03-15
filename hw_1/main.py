from bs4 import BeautifulSoup
import requests


def doParse():
    f = open("links.txt")
    i = 0
    index = ""
    for url in f:
        # делаем запрос и получаем html
        html_text = requests.get(url).text
        # используем парсер lxml
        body = BeautifulSoup(html_text).find('body')
        #body = BeautifulSoup(html_text).find('div', {"id": "app"})
        #print(body)

        file = open(str(i) + ".txt", "w", encoding='utf-8')
        file.write(str(body))
        file.close()

        url = url.strip()
        index = index + url + " " + str(i) + "\n"

        i = i + 1

    with open("index.txt", "w", encoding='utf-8') as file:
        file.write(index)


if __name__ == '__main__':
    doParse()
