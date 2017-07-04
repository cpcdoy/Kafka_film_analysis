import tmdbsimple as tmdb
import numpy as np
from kafka import KafkaConsumer

tmdb.API_KEY = '6130738744e761b316bcdb464c23e5ea'
movie = tmdb.Movies(603)
response = movie.info()
reviews = movie.reviews()

for i in range(100):
    movie = tmdb.Movies(i)
    try:
        reponse = movie.info()
        reviews = movie.reviews()
        if (len(reviews["results"])):
            #Get Title
            print(movie.title)

            #Get Release_date
            print(movie.release_date)

            print(movie.popularity)

            print(movie.revenue)

            print(movie.budget)
            #Get Genre list
            for g in movie.genres:
                #print(g["id"])
                print(g["name"])

            #Get Review list
            for r in reviews["results"]:
                print("Author : " + r["author"])
                print("ReviewId: " + r["id"])
                print("Content: " + r["content"])
    except:
        print(i)
        pass
