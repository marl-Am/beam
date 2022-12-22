from random import randrange
import time
from flask import Flask, render_template
from dotenv import load_dotenv
import os
import requests
import json
import re

# get rid of '<.*?>'
CLEANR = re.compile('<.*?>')

app = Flask(__name__, template_folder='templates')

websites_visited = set()


def configure():
    # Load environment variables from the .env file
    load_dotenv()


@app.route('/')
def get_article():
    """
    Gets one random article by invoking the News API and returns it to the index.html.
    """
    url = ('https://newsapi.org/v2/everything?' +
           'q=science OR technology&' +
           'sortBy=relevancy&' +
           'language=en&' +
           'apiKey=' + os.getenv('NEWS_API_KEY'))

    time.sleep(1)
    response = requests.get(url)

    if response.status_code == 200:
        results = json.loads(response.text.encode())
        post = results["articles"]
        # total_results = results["totalResults"]

        # random Integer from 0 to total_results inclusive, # randrange(total_results)
        random_article = randrange(100)

        source = post[random_article]['source']['name']
        title = post[random_article]['title']

        # the news api wrongly has html tags in the article's text description, this removes it
        clean_description = re.sub(
            CLEANR, '', post[random_article]['description'])
        description = clean_description

        link = post[random_article]['url']

        article = {
            'source': source,
            'title': title,
            'description': description,
            'link': link
        }
        websites_visited.add(source)
    else:
        article = {
            'source': 'Source is currently unavailable.',
            'title': 'Title is currently unavailable.',
            'description': 'Description is currently unavailable.',
            'link': '#'
        }
    return render_template('index.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)
