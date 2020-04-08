import re

import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json
from pandas.io.json import json_normalize


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


def main(text):
    return text_normalized(text)


if __name__ == '__main__':
    with open('data/train.json') as file:
        data = json.load(file)
    df = pd.DataFrame(json_normalize(data['intents']))
    print(df.head())
    MyText = text_normalized("Пора делать")
    tfidf_vectorizer = TfidfVectorizer()
    values = tfidf_vectorizer.fit_transform([MyText])

    future_names = tfidf_vectorizer.get_feature_names()
    print(pd.DataFrame(values.toarray(), columns= future_names))
