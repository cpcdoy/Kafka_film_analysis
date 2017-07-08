import json, sys, re
sys.path.insert(0, '../1_film_dumper')
from film_dumper import *
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from textblob import TextBlob
from kafka import KafkaConsumer

class DumpedMovie():
    def __init__(self, jsonstring):
        self.__dict__ = jsonstring


def word_feats(words):
    return dict([(word, True) for word in words])

def analyze_from_jsonfile(path):
    data = json.loads(open(path).read())
    movies_json_string = json.loads(data)
    analyze_from_jsonstring(movies_json_string)

def analyze_from_jsonliststring(movies_json_string):
    movies = []
    for mjs in movies_json_string:
        movies.append(DumpedMovie(mjs))

    for m in movies:
        movie_popularity = 0
        for r in m.review_list:
            b = TextBlob(r)
            for s in b.sentences:
                word_count = len(s.words)
                if (word_count != 0):
                    movie_popularity += (s.polarity / word_count)
        print(m.title + "--> nb_reviews: " + str(len(m.review_list)) + ", popularity: " + str(movie_popularity))
        m.analyzed_popularity = movie_popularity
        json_str_dump = json.dumps(m.__dict__)
        #producer.send('test', key=b'film', value=json_str_dump.encode('ascii'))

def analyze_from_jsonstring(mjs, producer):
    m = DumpedMovie(mjs)
    movie_popularity = 0
    for r in m.review_list:
        b = TextBlob(r)
        for s in b.sentences:
            word_count = len(s.words)
            if (word_count != 0):
                movie_popularity += (s.polarity / word_count)
    print(m.title + "--> nb_reviews: " + str(len(m.review_list)) + ", popularity: " + str(movie_popularity))
    m.analyzed_popularity = movie_popularity
    json_str_dump = json.dumps(m.__dict__)
    producer.send('popularity', key=b'film', value=json_str_dump.encode('ascii'))

#analyze_from_jsonlistfile('../1_film_dumper/data/movie_data.json')
consumer = KafkaConsumer('test', group_id='kafka-streaming-example', bootstrap_servers=['localhost:9092'])
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

for message in consumer:
    consumer.commit()
    json_movie = json.loads(message.value.decode("utf-8"))
    analyze_from_jsonstring(json_movie, producer)
