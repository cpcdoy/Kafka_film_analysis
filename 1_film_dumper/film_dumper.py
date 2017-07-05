import tmdbsimple as tmdb
import numpy as np
from kafka import KafkaProducer
import json, sys

class Review(json.JSONEncoder):
    def __init__(self, author, id, content):
        self.author = author
        self.id = id
        self.content = content

class Movie(json.JSONEncoder):
    def __init__(self, id, title, release_date, popularity, revenue, budget, genre_list, review_list, analyzed_popularity):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.popularity = popularity
        self.revenue = revenue
        self.budget = budget
        self.genre_list = genre_list
        self.review_list = review_list
        self.analyzed_popularity = analyzed_popularity

def dumper(nb_movies):
    tmdb.API_KEY = '6130738744e761b316bcdb464c23e5ea'

    movie_list = []
    review_list = []
    genre_list = []
    nb_dumped_movies = 0
    i = 0

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    while nb_movies > nb_dumped_movies:
        movie = tmdb.Movies(i)
        try:
            reponse = movie.info()
            reviews = movie.reviews()
            if (len(reviews["results"])):
                print('Found review: ', i)
                nb_dumped_movies += 1
                print(nb_dumped_movies)
                genre_list = []
                for g in movie.genres:
                    genre_list.append(g["name"])

                for r in reviews["results"]:
                    review_list.append(r["content"])

                json_str_dump = json.dumps(Movie(i, movie.title, movie.release_date, movie.popularity, movie.revenue, movie.budget, genre_list,  review_list, -1).__dict__)
                producer.send('test', key=b'film', value=json_str_dump.encode('ascii'))

                genre_list = []
                review_list = []
        except:
            pass
        i += 1
    json_string = json.dumps([m.__dict__ for m in movie_list])
    return json_string

def write_movies_to_jsonfile(path, nb_movies):
    json_string = dumper(nb_movies)
    with open(path, 'r+') as outfile:
        json.dump(json_string, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

def main():
    if (len(sys.argv) > 1):
        if (sys.argv[1].isdigit()):
            write_movies_to_jsonfile('data/movie_data.json', int(sys.argv[1]))
    return

if __name__ == "__main__":
    main()



#data = json.loads(open('data/movie_data.json').read())
#Json list of movies
#jsonmovies = json.loads(data)
