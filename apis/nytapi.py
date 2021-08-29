import requests
import os
from pprint import pprint
from bs4 import BeautifulSoup

# API documentation: https://developer.nytimes.com/docs/top-stories-product/1/overview
APIKEY = os.getenv('NYTIMES_APIKEY', '(apikey removed for github)')
SECTIONS = ['arts',
            'automobiles',
            'books',
            'business',
            'fashion',
            'food',
            'health',
            'home',
            'insider',
            'magazine',
            'movies',
            'nyregion',
            'obituaries',
            'opinion',
            'politics',
            'realestate',
            'science',
            'sports',
            'sundayreview',
            'technology',
            'theater',
            't-magazine',
            'travel',
            'upshot',
            'us',
            'world']

# Top articles from a section
def top_articles_in_section(section, num_articles=3):
    """
    Returns a list of stories with their title, published date, media, abstract, and url as dictionary keys.
    {'title': ..., 
    'pub_date':...,
    'media':...,
    'abstract':...,
    'url':...}
    """
    query_url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={APIKEY}"
    r = requests.get(query_url)
    query_data = r.json()['results']

    def process_results(data):
        """
        Processes data from API to return a list of dictionaries of articles' title, created date, abstract, and url.
        """
        articles = []

        # Title, Date, Abstract, URL
        for article in data:
            processed_article = {'title': article['title'],
                        'pub_date': article['created_date'].split('T')[0],
                        'abstract': article['abstract'],
                        'url': article['url']
            }
            if article['multimedia'] != None:
                processed_article['media'] = article['multimedia'][0]['url']
            else:
                processed_article['media'] = 'None'
            articles.append(processed_article)

            if len(articles) >= num_articles:
                return articles

    return process_results(query_data)


def print_top_articles(section, num_articles=3):
    """
    Prints results from top_articles_in_section in readable form.
    """
    if section not in SECTIONS:
        print('Invalid section.')
        return
    articles = top_articles_in_section(section, num_articles)

    # Title, Published Date, URL
    for article in articles:
        print(article['title'])
        print('Published Date: ' + article['pub_date'])
        print()
        print(article['abstract'])
        print('More at: ' + article['url'])
        print('------------------------------------------------------------------------------------------------')



# Article Search:
def search_articles(query, num_articles=3, sort="relevance"):
    """
    Returns a list of articles with their headline, published date, abstract, lead paragraph, and url as dictionary keys.
    """
    # sort = 'relevance'/'newest'/'oldest'
    # page = '0' <0-100>
    query_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?" \
                f"q={query}" \
                f"&api-key={APIKEY}" \
                f"&sort={sort}"
    r = requests.get(query_url)
    query_data = r.json()['response']['docs']

    def process_results(data):
        """
        Processes data from API to return a list of dictionaries of articles' title, created date, abstract, and url.
        """
        articles = []

        # Title, Published date, Abstract, Lead paragraph, URL
        for article in data:
            processed_article = {'title': article['headline']['main'],
                        'pub_date': article['pub_date'].split('T')[0],
                        'abstract': article['abstract'],
                        'lead_paragraph': article['lead_paragraph'],
                        'url': article['web_url']
            }
            articles.append(processed_article)

            if len(articles) >= num_articles:
                return articles

    articles = process_results(query_data)

    def scrape_image(articles):

        for article in articles:
            html_text = requests.get(article['url']).text
            soup = BeautifulSoup(html_text, 'lxml')
            pic_tag = soup.find_all('img')

            if pic_tag == None:
                article['media'] = 'None'
                continue

            for pic in pic_tag:
                if 'src=' in str(pic):
                    pic = str(pic).split('src="')[1].split('"')[0].replace('amp;', '')
                    if 'static01.nyt' in str(pic):
                        article['media'] = str(pic)
                        break
            
        return articles

    if articles == None:
        return None
    
    return scrape_image(articles)

def print_searched_articles(query, num_articles=3, sort="relevance"):
    """
    Prints results from search_articles in readable form.
    """
    articles = search_articles(query, num_articles, sort)
    if articles == None:
        print("No articles found.")
        return

    # Title, Published date, Abstract, Lead paragraph, URL
    for article in articles:
        print(article['title'])
        print('Published Date: ' + article['pub_date'])
        print()
        print('ABSTRACT: ')
        print(article['abstract'])
        print('LEAD PARAGRAPH:')
        print(article['lead_paragraph'])
        print()
        print('More at: ' + article['url'])
        print('------------------------------------------------------------------------------------------------')
