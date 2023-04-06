from bs4 import BeautifulSoup
import string
from nltk import word_tokenize
import math
import ast


def remove_chars_from_text(text, chars):
    return "".join([ch if ch not in chars else " " for ch in text])


def tokenize(text):
    # spec_chars = string.punctuation + '\n\xa0«»\t—…abcdefghijklmnopqrstuvwxyz↑©•–”→'
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
    # russian_stopwords = stopwords.words("russian")
    # text_tokens = [token.strip() for token in text_tokens if token not in russian_stopwords]
    return text_tokens


def create_tf_dict(filename, termins):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    words_count = len(text.split())
    tf_dict = {}
    for k in termins:
        tf_dict[k] = [float(text.count(k) / words_count)]
    return tf_dict


def create_termin_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        src_text = f.read().lower()
        return tokenize(src_text)


def create_lemm_list():
    lemmas_dict = {}
    with open('../hw_2/lemmas.txt', 'r', encoding='utf-8') as f:
        lemmas = [k.split() for k in f.read().split('\n')]

    for k in range(100):
        with open(f'../hw_1/{k}.txt', 'r', encoding='utf-8') as f:
            file = f.read()
            file = BeautifulSoup(file).find('body').text

        for lem in lemmas:
            count = 0
            for form in lem[1].split(','):
                count += file.count(form)
            lemmas_dict[lem[0].rstrip(':')] = count

    idf = {}
    corpuses = []
    for i in range(100):
        with open(f'../hw_1/{i}.txt', 'r', encoding='utf-8') as f:
            file = f.read()
            corpuses.append(BeautifulSoup(file).find('body').text)

    for w in lemmas:
        print("start lemma: " + w[1])
        k = 0  # number of documents in the corpus that contain this word
        for i in range(100):
            file = corpuses[i]
            for form in w[1].split(','):
                if form in file.split():
                    k += 1
        if k == 0:
            idf[w[0].rstrip(':')] = 0
        else:
            idf[w[0].rstrip(':')] = math.log(100 / k, 10)

    for k in range(100):
        with open(f'../hw_1/{k}.txt', 'r', encoding='utf-8') as f:
            file = f.read()
            file = BeautifulSoup(file).find('body').text
        with open(f'{k}_lemm_tf_idf.txt', 'w', encoding='utf-8') as f:
            for x in lemmas_dict.keys():
                f.write(f'{x} {idf[x]} {idf[x] * (lemmas_dict[x] / len(file.split()))} \n')


def main():
    # lemmas
    #create_lemm_list()



    # default tf-idf
    all_tf_dict = []
    for file_num in range(100):
        filename = f'../hw_1/{file_num}.txt'
        termin_list = create_termin_list(filename)
        all_tf_dict.append(create_tf_dict(filename, termin_list))

    for number, tf_dict in enumerate(all_tf_dict):
        for word in tf_dict.keys():
            count = 0
            for dicti in all_tf_dict:
                if word in dicti.keys():
                    count += 1
            all_tf_dict[number][word].append(float(all_tf_dict[number][word][0] * math.log(100 / count, 10)))

        with open(f'{number}_tf-ifd.txt', 'w', encoding='utf-8') as f:
            for k in tf_dict.keys():
                f.write(f"{k} {tf_dict[k][0]} {tf_dict[k][1]}\n")


if __name__ == '__main__':
    main()
