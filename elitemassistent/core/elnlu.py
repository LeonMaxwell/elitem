import re

import nltk
import pandas as pd
import pymorphy2
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

nltk.download('punkt')
nltk.download('stopwords')
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


def processing_bow(query, records):
    print("---====Метод мешка слов====---")
    method = 'similarity_bow'
    cv = CountVectorizer()
    X = cv.fit_transform(records['lemmatized_about_service']).toarray()
    print("Полученое трансформированое значение: ")
    print(X)
    print()
    df_bow = pd.DataFrame(X, columns=cv.get_feature_names())
    print("Результат представление микросервисов используя метод мешок слов: ")
    print(df_bow)
    print()
    question_bow = cv.transform([query]).toarray()
    print("Представление нормализированного запроса используя метод мешка слов: ")
    print(question_bow)
    print()
    return compare_processing(question_bow, df_bow, records, method)


def processing_tfidf(query, records):
    print("---====Метод TF-IDF====---")
    method = 'similarity_tfidf'
    tfidf = TfidfVectorizer()
    X = tfidf.fit_transform(records['lemmatized_about_service']).toarray()
    df_tfidf = pd.DataFrame(X, columns=tfidf.get_feature_names())
    print("Обработка данных микрсоервисов используя метод TF-IDF: ")
    print(df_tfidf)
    print()
    query_tfidf = tfidf.transform([query]).toarray()
    print("Обработка данных микрсоервисов используя метод TF-IDF: ")
    print(query_tfidf)
    print()
    return compare_processing(query_tfidf, df_tfidf, records, method)


def compare_processing(proc_query, proc_records, records, name_method):
    threshold = 0.2
    cosine_value = 1 - pairwise_distances(proc_records, proc_query, metric='cosine')
    records[name_method] = cosine_value
    print(records)
    df_simi = pd.DataFrame(records, columns=['lemmatized_about_service', name_method])
    df_simi_sort = df_simi.sort_values(by=name_method, ascending=False)
    df_threshold = df_simi_sort[df_simi_sort[name_method] > threshold]
    if df_threshold.empty:
        result_compare = 'Такого сервиса не существует'
    else:
        index_value = cosine_value.argmax()
        result_compare = records['name_service'][index_value]
    return result_compare


def main(text, data_micros):
    question_lemma = text_normalized(text)
    df = pd.DataFrame(data_micros)
    df['lemmatized_about_service'] = df['about_service'].apply(text_normalized)
    print("Обработка таблицы: ")
    print(df['lemmatized_about_service'])
    print("")
    method_result_bow = processing_bow(question_lemma, df)
    method_result_tfidf = processing_tfidf(question_lemma, df)
    return method_result_bow
