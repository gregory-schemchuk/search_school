from bs4 import BeautifulSoup
import requests
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from nltk.stem import WordNetLemmatizer


def doParse():
    all_text = ""
    f = open("links.txt")
    for url in f:
        # делаем запрос и получаем html
        html_text = requests.get(url).text
        # используем парсер lxml
        body = BeautifulSoup(html_text).find('body').text
        #body = BeautifulSoup(html_text).find('div', {"id": "global-wrap"}).get_text(" ")
        all_text = all_text + str(body).lower()
    with open("all_text.txt", "w", encoding='utf-8') as file:
        file.write(all_text)
    return all_text

def remove_chars_from_text(text, chars):
    return "".join([ch if ch not in chars else " " for ch in text])


def tokenize(text):
    #spec_chars = string.punctuation + '\n\xa0«»\t—…abcdefghijklmnopqrstuvwxyz↑©•–”→'
    spec_chars = string.punctuation + '\n\xa0«»\t—…↑©•–”→😍😍😘😊😉😙😁❤😃👍�🖕🏿🖕🏾🖕🏽🖕🏼🖕🏻🖕😇😌😄'
    text = remove_chars_from_text(text, spec_chars)
    text = remove_chars_from_text(text, string.digits)
    text_tokens = word_tokenize(text)
    # удалить дубли
    text_tokens = list(set(text_tokens))
    ordered_tokens = set()
    for word in text_tokens:
        if word not in ordered_tokens:
            ordered_tokens.add(word)
    #russian_stopwords = stopwords.words("russian")
    #text_tokens = [token.strip() for token in text_tokens if token not in russian_stopwords]
    with open("tokens.txt", "w", encoding='utf-8') as file:
        print(text_tokens, file=file, sep="\n")
    return text_tokens


def lemmatize(text_tokens):
    final_text = ""
    #for word in text_tokens:
    #    forms = []
    #    for p in morph.parse(word):
    #        if str(p.normal_form) not in forms:
    #            forms.append(str(p.normal_form))
    #    final_text = final_text + word + ": " + ' '.join(forms) + "\n"

    lemmatizer = WordNetLemmatizer()
    dict = {}
    i = 0
    for word in text_tokens:
        lemma = lemmatizer.lemmatize(word)

        if lemma in dict:
            if word not in dict[lemma]:
                dict[lemma].append(word)
        else:
            dict[lemma] = [word]

    for key, value in dict.items():
        final_text = final_text + key + ": "
        for v in value:
            final_text = final_text + v + ","
        final_text = final_text[:-1]
        final_text = final_text + "\n"

    with open("lemmas_bin.txt", "w", encoding='utf-8') as file:
        file.write(final_text)

    # удалить дубликаты
    lines_seen = set()
    outfile = open("lemmas.txt", "w", encoding='utf-8')
    for line in open("lemmas_bin.txt", "r", encoding='utf-8'):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()


if __name__ == '__main__':
    src_text = doParse()
    tokens = tokenize(src_text)
    lemmatize(tokens)
