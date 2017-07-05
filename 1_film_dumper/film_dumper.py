import tmdbsimple as tmdb
import numpy as np
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json, sys, getopt

#producer = KafkaProducer(bootstrap_servers=['192.168.0.30:9092'])

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
    def __init__(self, json_dict_string):
        self.__dict__ = json_dict_string

def dumper(nb_movies):
    tmdb.API_KEY = '6130738744e761b316bcdb464c23e5ea'

    movie_list = []
    review_list = []
    genre_list = []
    nb_of_dumped_movies = 0
    i = 10
    while nb_of_dumped_movies < nb_movies:
        movie = tmdb.Movies(i)
        try:
            reponse = movie.info()
            reviews = movie.reviews()
            if (len(reviews["results"])):
                nb_of_dumped_movies += 1
                print(nb_of_dumped_movies)
                genre_list = []
                for g in movie.genres:
                    genre_list.append(g["name"])

                for r in reviews["results"]:
                    review_list.append(r["content"])

                movie_list.append(Movie(i, movie.title, movie.release_date, movie.popularity, movie.revenue, movie.budget, genre_list, review_list))

                genre_list = []
                review_list = []
        except:
            pass
        i += 1
    json_string = json.dumps([m.__dict__ for m in movie_list])
    data = json.loads(json_string)
    for m in data:
        str_as_bytes = str.encode(m["title"])
        print(str_as_bytes)
    return json_string

def dump_and_write_movies_to_json(nb_movies):
    json_string = dumper(nb_movies)
    with open('data/movie_data.json', 'w') as outfile:
        json.dump(json_string, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

def load_movies_from_jsonfile(path):
    data = json.loads(open(path).read())
    jsonmovies = json.loads(data)
    for m in jsonmovies:
        print(m["title"])
    return jsonmovies

def main():
    if len(sys.argv) > 1:
        if sys.argv[1].isdigit():
            dump_and_write_movies_to_json(int(sys.argv[1]))

if __name__ == "__main__":
    main()
