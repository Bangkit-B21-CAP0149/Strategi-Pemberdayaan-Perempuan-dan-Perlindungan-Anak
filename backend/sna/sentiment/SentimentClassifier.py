import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from string import punctuation
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle
from os import path
import numpy as np


base_dir = path.abspath(path.dirname(__file__))
tokenizer_pkl = path.join(base_dir, 'models/tokenizer.pickle')


class SentimentClassifier:
    def __init__(self):
        self.tokenizer = pickle.load(open(tokenizer_pkl, 'rb'))
        self.classifier = load_model(path.join(base_dir, 'models/Twitter_BiLSTM_CPU.h5'))

    def preprocess(self, tweet):
        ps = PorterStemmer()
        negation_list = ["arent", "isnt", "dont", "doesnt", "not", "cant", "couldnt", "werent",
                         "wont", "didnt", "never", "nothing", "nowhere", "noone", "none",
                         "hasnt", "hadnt", "shouldnt",
                         "wouldnt", "aint"]
        tweet = tweet.lower()
        tweet = re.sub('n[^A-Za-z ]t', 'nt', tweet)
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweet)
        tweet = re.sub('@[^\s]+', '', tweet)
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        tweet = word_tokenize(tweet)
        tweet_list = []
        negate = False
        for word in tweet:
            word = ps.stem(word)
            if word in negation_list:
                negate = True
            elif negate is True and word in list(punctuation):
                negate = False

            if negate and word not in negation_list:
                word = "not_" + word
            else:
                pass
            word = re.sub('[^A-Za-z_ ]+', '', word)
            if len(word) > 2 and word not in stopwords.words('english'):
                tweet_list.append(word)
        tweet_set = set(tweet_list)
        return " ".join(tweet_set)

    def predict(self, tweet):
        self.tokenizer.fit_on_texts(tweet)
        tweet = self.tokenizer.texts_to_sequences(tweet)
        tweet = pad_sequences(tweet, maxlen=200)
        prediction = self.classifier.predict(tweet)
        result = np.argmax(prediction, axis=1)
        return result
