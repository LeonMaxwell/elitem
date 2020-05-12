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


def treatment_intents(*args):
    pass


def main(text, data_micros):
    tfidf = TfidfVectorizer()
    cv = CountVectorizer()
    question_lemma = text_normalized(text)
    df = pd.DataFrame(data_micros)
    print(df)
    return df.head(10)


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
