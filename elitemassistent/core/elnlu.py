import json
import re

import nltk
import pandas as pd
import pymorphy2
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

nltk.download('punkt')
morph = pymorphy2.MorphAnalyzer()


def stop_words(word):
    stop = stopwords.words('russian')
    if word in stop:
        return False
    else:
        return True


def text_normalized(text):
    text_lemmater = list()
    text = str(text).lower()
    spl_chr_tet = re.sub(r'[^ а-яa-z]', '', text)
    tokens = nltk.word_tokenize(spl_chr_tet)
    for word in tokens:
        if stop_words(word):
            text_lemmater.append(morph.parse(word)[0].normal_form)
    return " ".join(text_lemmater)


def main(text, data_micros):
    tfidf = TfidfVectorizer()
    cv = CountVectorizer()
    question_lemma = text_normalized(text)
    df = pd.DataFrame(data_micros)
    df['lemmatized_about_service'] = df['about_service'].apply(text_normalized)
    print(df.tail(15))
    X = cv.fit_transform(df['lemmatized_about_service']).toarray()
    features = cv.get_feature_names()
    df_bow = pd.DataFrame(X, columns=features)
    print(df_bow.head())
    question_bow = cv.transform([question_lemma]).toarray()
    print(question_bow)
    cosine_value = 1 - pairwise_distances(df_bow, question_bow, metric='cosine')
    print(cosine_value)
    df['similarity_bow'] = cosine_value
    df_simi = pd.DataFrame(df, columns=['lemmatized_about_service', 'similarity_bow'])
    df_simi_sort = df_simi.sort_values(by='similarity_bow', ascending=False)
    trash_hold = 0.2
    df_trash_hold = df_simi_sort[df_simi_sort['similarity_bow'] > trash_hold]
    print(df_trash_hold)
    if df_trash_hold.empty:
        response_itog = "Такого сервиса не существует"
    else:
        index_values = cosine_value.argmax()
        response_itog = df['name_service'][index_values]
    return response_itog


if __name__ == '__main__':
    res = list()
    itogList = list()
    patterns_normalize = list()
    tfidf_vectorizer = TfidfVectorizer()
    training = list()
    output = list()
    labels = list
    docs_y = list()

    with open('data/train.json') as file:
        data = json.load(file)

    df = pd.DataFrame(pd.json_normalize(data['intents']))
    print(df.head())

    MyText = text_normalized("пока")

    for itnr in df['patterns']:
        wrds = [text_normalized(wrds) for wrds in itnr]
        res.append(wrds)
        docs_y.append(df['tag'])

    itogList = sorted((item for sublist in res for item in sublist))
    print(itogList)
    labels = [label for label in df['tag']]
    labels = sorted(labels)
    print(labels)

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(res):
        bag = []

        wrds = [text_normalized(w) for w in doc]

        for w in itogList:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        out_row = out_empty[:]
        out_row[labels.index(docs_y[x][x])] = 1

        training.append(bag)
        output.append(out_row)

    print(training)
    print(output)

    values = tfidf_vectorizer.fit_transform(itogList)
    future_names = tfidf_vectorizer.get_feature_names()
    df_tfidf = pd.DataFrame(values.toarray(), columns=future_names)
    df_tfidf = df_tfidf.head()
    print(df_tfidf)

    tf = tfidf_vectorizer.transform([MyText]).toarray()
    cos = 1 - pairwise_distances(df_tfidf, tf, metric='cosine')
    print(tf)

    index_value = cos.argmax()
    print(index_value)
    print(df['responses'].loc[index_value])
