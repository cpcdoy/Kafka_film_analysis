import tmdbsimple as tmdb
import numpy as np
from kafka import KafkaConsumer
import json

tmdb.API_KEY = '6130738744e761b316bcdb464c23e5ea'
movie = tmdb.Movies(603)
response = movie.info()
reviews = movie.reviews()

class Review(json.JSONEncoder):
    def __init__(self, author, id, content):
        self.author = author
        self.id = id
        self.content = content

class Movie(json.JSONEncoder):
    def __init__(self, id, title, release_date, popularity, revenue, budget, genre_list, review_list):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.popularity = popularity
        self.revenue = revenue
        self.budget = budget
        self.genre_list = genre_list
        self.review_list = review_list

movie_list = []
review_list = []
genre_list = []

for i in range(100):
    movie = tmdb.Movies(i)
    try:
        reponse = movie.info()
        reviews = movie.reviews()
        if (len(reviews["results"])):
            genre_list = []
            for g in movie.genres:
                genre_list.append(g["name"])

            for r in reviews["results"]:
                review_list.append(r["content"])

            movie_list.append(Movie(i, movie.title, movie.release_date, movie.popularity, movie.revenue, movie.budget, genre_list, review_list))

            genre_list = []
            review_list = []
    except:
        print(i)
        pass

json_string = json.dumps([m.__dict__ for m in movie_list])
with open('data/movie_data.json', 'w') as outfile:
    #json.dump(json_string, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
    json.dump(json_string, outfile)

data = json.loads(open('data/movie_data.json').read())
jsonmovies = json.loads(data)
for m in jsonmovies:
    print(m["title"])
