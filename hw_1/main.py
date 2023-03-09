from bs4 import BeautifulSoup
import requests


def doParse():
    f = open("links.txt")
    i = 0
    for url in f:
        # делаем запрос и получаем html
        html_text = requests.get(url).text
        # используем парсер lxml
        body = BeautifulSoup(html_text).find('body')
        #print(body)

        file = open(str(i) + ".txt", "w", encoding='utf-8')
        file.write(str(body))
        file.close()

        with open("index.txt", "w") as file:
            file.write(url + " " + str(i))

        i = i + 1


if __name__ == '__main__':
    doParse()
