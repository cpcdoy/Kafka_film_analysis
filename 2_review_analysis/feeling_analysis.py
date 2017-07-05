import json, sys, re
sys.path.insert(0, '../1_film_dumper')
from film_dumper import *
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

class DumpedMovie():
    def __init__(self, jsonstring):
        self.__dict__ = jsonstring


def word_feats(words):
    return dict([(word, True) for word in words])

data = json.loads(open('../1_film_dumper/data/movie_data.json').read())
movies_json_string = json.loads(data)
movies = []

for mjs in movies_json_string:
    movies.append(DumpedMovie(mjs))

neg_review_files = movie_reviews.fileids('neg')
pos_review_files = movie_reviews.fileids('pos')

neg_words = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in neg_review_files]
pos_words = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in pos_review_files]

train_data = neg_words + pos_words
classifier = NaiveBayesClassifier.train(train_data)

#p = classifier.prob_classify(word_feats('baaaaaaaad'))
#print(p.prob('pos'))

for m in movies:
    movie_popularity = 0
    for r in m.review_list:
        lines = r.splitlines()
        review_popularity = 0
        word_count = 0
        for l in lines:
            words = [w for w in re.split("\W", l.lower()) if w != ""]
            word_count += len(words)
            for w in words:
                p = classifier.prob_classify(word_feats(w))
                review_popularity += p.prob('pos')
                review_popularity -= p.prob('neg')
        review_popularity /= word_count
        movie_popularity += review_popularity
    print(m.title + "--> nb_reviews: " + str(len(m.review_list)) + ", popularity: " + str(movie_popularity))
    m.analyzed_popularity = movie_popularity
