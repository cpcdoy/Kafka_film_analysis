import requests
from bs4 import BeautifulSoup as bs
import json

def get_review_page_urls(movie_url):
    review_url = movie_url + '/reviews'
    sp = bs(requests.get(review_url).content, "html.parser")
    review_page_urls = []
    review_page_container = sp.find('div', {"id" : "tn15content"}).find_all('table')[1]
    for page_url in review_page_container.find_all("a"):
        review_page_urls.append(movie_url + '/' + page_url.get("href"))
    return set(review_page_urls)

def review_filter(tag):
    return not(tag.has_attr('class')) and not(tag.has_attr('id')) and tag.find("h2")

def get_reviews_in_page(review_page_url):
    reviews = []
    sp = bs(requests.get(review_page_url).content, "html.parser")
    for review_container in sp.find_all('div'):
        if (review_filter(review_container)):
            content = review_container.find_next_sibling().get_text()
            reviews.append(content)
    return reviews

def get_movie_reviews(movie_url):
    review_page_urls = get_review_page_urls(movie_url)
    movie_reviews = []
    for review_page_url in review_page_urls:
        movie_reviews.extend(get_reviews_in_page(review_page_url))
    return movie_reviews


"""
movie_url = 'http://akas.imdb.com/title/tt0000001'
review_list = get_movie_reviews(movie_url)
print("number of reviews = " + str(len(review_list)))
reviews_in_json = json.dumps(review_list)
with open('data.json', 'w') as outfile:
    json.dump(reviews_in_json, outfile)
"""

