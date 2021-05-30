from nltk.corpus import stopwords
import nltk
import pandas as pd
import numpy as np
import re

nltk.download('stopwords')
nltk.download('punkt')
sw = stopwords.words('indonesian')


class Wordcloud:

    @staticmethod
    def preprocess_data(data):
        data = data.lower()
        data = data.replace('\\t', " ").replace('\\n', " ").replace('\\u', " ")\
            .replace('\\', "").replace('username', "").replace('-', " ")\
            .replace(',', " ").replace('rt', '')
        data = data.replace("http://", " ").replace("https://", " ")
        data = re.sub('([@#][A-Za-z0-9-_*.]+)', '', data)
        data = re.sub('[()]', '', data)
        data = re.sub(r'[^\w]', ' ', data)
        data = re.sub(r'\d+', '', data)
        data = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', data)
        data = [word.lower() for word in data.split() if word.lower() not in sw]
        return ' '.join(data)

    @staticmethod
    def clean_length(data):
        data = [i for i in data.split() if len(i) > 2]
        return ' '.join(data)

    @staticmethod
    def output_data(data, column):
        data = pd.DataFrame(data)
        data[column] = data[column].apply(Wordcloud.preprocess_data)
        data[column] = data[column].apply(Wordcloud.clean_length)
        result = data[column].str.split(expand=True).stack().value_counts()[:500].T.to_dict()
        return result
