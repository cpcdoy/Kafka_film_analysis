import json, sys, re
sys.path.insert(0, '../1_film_dumper')
from film_dumper import *
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from textblob import TextBlob

class DumpedMovie():
    def __init__(self, jsonstring):
        self.__dict__ = jsonstring


def word_feats(words):
    return dict([(word, True) for word in words])

def analyze_from_jsonfile(path):
    data = json.loads(open(path).read())
    movies_json_string = json.loads(data)
    movies = []

    for mjs in movies_json_string:
        movies.append(DumpedMovie(mjs))

    for m in movies:
        movie_popularity = 0
        for r in m.review_list:
            b = TextBlob(r)
            for s in b.sentences:
                movie_popularity += s.polarity
        print(m.title + "--> nb_reviews: " + str(len(m.review_list)) + ", popularity: " + str(movie_popularity))
        m.analyzed_popularity = movie_popularity

analyze_from_jsonfile('../1_film_dumper/data/movie_data.json')
