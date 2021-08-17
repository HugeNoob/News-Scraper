import requests
from pprint import pp, pprint

# API documentation: https://newsapi.org/docs/get-started#top-headlines
APIKEY='6845da88691f4be0b29abf74c1945fa1'
SECTIONS = ['business', 
            'entertainment', 
            'general', 
            'health', 
            'science', 
            'sports', 
            'technology']
COUNTRY_CODES = ['ae', 
                'ar', 
                'at', 
                'au', 
                'be', 
                'bg', 
                'br', 
                'ca', 
                'ch', 
                'cn', 
                'co', 
                'cu', 
                'cz', 
                'de', 
                'eg', 
                'fr', 
                'gb', 
                'gr',
                'hk',
                'hu',
                'id',
                'ie',
                'il',
                'in',
                'it',
                'jp',
                'kr',
                'lt',
                'lv',
                'ma',
                'mx',
                'my',
                'ng',
                'nl',
                'no',
                'nz',
                'ph',
                'pl',
                'pt',
                'ro',
                'rs',
                'ru',
                'sa',
                'se',
                'sg',
                'si',
                'sk',
                'th',
                'tr',
                'tw',
                'ua',
                'us',
                've',
                'za']

# Top articles
def top_articles_in_section(section, num_articles=3, country='us'):
    """
    Searches exact phrases in article body.
    """
    query_url = f'https://newsapi.org/v2/top-headlines?' \
                f'country={country}' \
                f'&category={section}' \
                f'&apiKey={APIKEY}' \


    r = requests.get(query_url)
    query_data = r.json()['articles']
    def process_results(data):
        """
        Processes data from API to return a list of dictionaries of articles' title, created date, and url.
        """
        articles = []

        # Title, Publication Date, Abstract, and URL
        for article in data:
            processed_article = {'title': article['title'],
                                'pub_date': article['publishedAt'].split('T')[0],
                                'media': article['urlToImage'],
                                'abstract': article['description'],
                                'url': article['url']
            }
            articles.append(processed_article)

            if len(articles) >= num_articles:
                return articles

    return process_results(query_data)

def print_top_articles(section, num_articles=3, country='sg'):
    """
    Prints results from top_articles_in_section in readable form.
    """
    if section not in SECTIONS:
        print('Invalid section.')
        return
    articles = top_articles_in_section(section, num_articles, country)

    # Title, Publication Date, Abstract, and URL
    for article in articles:
        print(article['title'])
        print('Published Date: ' + article['pub_date'])
        print()
        print('ABSTRACT:')
        print(article['abstract'])
        print()
        print('More at: ' + article['url'])
        print('------------------------------------------------------------------------------------------------')



# Article Search
def search_articles(query, num_articles=3, orderby='relevance'):
    """
    Searches exact phrases in article body.
    """
    query_url = f'https://newsapi.org/v2/everything?' \
                f'q={query}' \
                f'&sortBy={orderby}' \
                f'&apiKey={APIKEY}' \

    r = requests.get(query_url)

    query_data = r.json()['articles']
    def process_results(data):
        """
        Processes data from API to return a list of dictionaries of articles' title, created date, and url.
        """
        articles = []

        # Title, Publication Date, Media, Abstract, and URL
        for article in data:
            processed_article = {'title': article['title'],
                                'pub_date': article['publishedAt'].split('T')[0],
                                'media': article['urlToImage'],
                                'abstract': article['description'],
                                'url': article['url']
            }
            articles.append(processed_article)

            if len(articles) >= num_articles:
                return articles
    
    return process_results(query_data)

def print_searched_articles(query, num_articles=3, orderby='relevance'):
    """
    Prints results from search_stories in readable form.
    """
    articles = search_articles(query, num_articles, orderby)
    if articles == None:
        print("No articles found.")
        return

    # Title, Publication Date, Abstract, and URL
    for article in articles:
        print(article['title'])
        print('Published Date: ' + article['pub_date'])
        print()
        print('ABSTRACT:')
        print(article['abstract'])
        print()
        print('More at: ' + article['url'])
        print('------------------------------------------------------------------------------------------------')
