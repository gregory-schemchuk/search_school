import string
from nltk import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
#from sklearn.metrics.pairwise import cosine_similarity
import operator
import numpy as np
import math


def normalize():
    minVal = 0
    maxVal = 0
    for i in range(100):
        with open(f'../hw_4/{i}_lemm_tf_idf.txt', 'r', encoding='utf-8') as f:
            for k in f.read().split('\n'):
                if len(k.split()) > 1:
                    if float(k.split()[2]) < minVal:
                        minVal = float(k.split()[2])
                    if float(k.split()[2]) > maxVal:
                        maxVal = float(k.split()[2])
    return minVal, maxVal

def doVectorMatrix(min, max):
    mtx = []
    idfs = {}
    for i in range(100):
        vector = []
        with open(f'../hw_4/{i}_lemm_tf_idf.txt', 'r', encoding='utf-8') as f:
            for k in f.read().split('\n'):
                if len(k.split()) > 1:
                    vector.append( (float(k.split()[2]) - min) / (max - min) )
                    if i == 0:
                        idfs[k.split()[0].rstrip(':')] = float(k.split()[1])
        mtx.append(vector)
    return mtx, idfs

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
    lemmasRet = []
    for line in open("lemmas_bin.txt", "r", encoding='utf-8'):
        if line not in lines_seen:
            lemmasRet.append(line)
            lines_seen.add(line)
    return lemmasRet

def lemmatizeStr(findStr):
    tokens = tokenize(findStr)
    # lemma: form1,form2
    lemmas = lemmatize(tokens)
    return lemmas

def vectorizeNewStr(newStr, lemmas, idfs):
    tfs = {}
    for lem in lemmas:
        count = 0
        for form in lem.split()[1].split(','):
            count += newStr.count(form)
        tfs[lem.split()[0].rstrip(':')] = count
    vector = []
    for lemma, idf in idfs.items():
        if lemma in tfs:
            vector.append(tfs[lemma] * idf)
        else:
            vector.append(0)
    print("VECTOR: ", vector)
    return vector

def cosine_similarity(v1,v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    if math.sqrt(sumxx*sumyy) == 0:
        return 0
    return sumxy/math.sqrt(sumxx*sumyy)

def findFirstNSimmilars(n, vector, mtx):
    simm = {}
    retVal = []
    i = 0
    for vec in mtx:
        #v1 = np.array(vector).reshape(-1, 1)
        #v2 = np.array(vec).reshape(-1, 1)
        simm[i] = cosine_similarity(vector, vec)
        i = i + 1
    sorted_simm = sorted(simm.items(), key=operator.itemgetter(1), reverse=True)
    sorted_simm = list(sorted_simm)
    print("OUT: ", sorted_simm[0], sorted_simm[1], sorted_simm[2], sorted_simm[3], sorted_simm[4])
    for i in range(n):
        retVal.append(sorted_simm[i][0])
    return retVal

def retLinksById(ids):
    links = []
    with open(f'../hw_1/links.txt', 'r', encoding='utf-8') as f:
        alls = f.read().split('\n')
    for i in ids:
        links.append(alls[i])
        print("LINK: ", alls[i])
    return links

def main(findStr, N):
    minVal, maxVal = normalize()
    mtx, idfs = doVectorMatrix(minVal, maxVal)
    lemmas = lemmatizeStr(findStr)
    newVector = vectorizeNewStr(findStr, lemmas, idfs)
    simmilars = findFirstNSimmilars(N, newVector, mtx)
    links = retLinksById(simmilars)


if __name__ == '__main__':
    findStr = 'edit old words typo'
    N = 5
    main(findStr, N)