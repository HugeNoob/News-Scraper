import requests
from pprint import pprint

# API documentation: https://free-docs.newscatcherapi.com/?python#introduction
APIKEY = '5fdd297fefmsh88f9044b379b43dp164c0ajsn59d56efcf332'

# Article Search
def search_articles(query, num_articles=3):
    """
    Searches exact phrases in article body.
    """
    url = "https://free-news.p.rapidapi.com/v1/search"
    double_quoted_query = '"' + query + '"'

    querystring = {"q":f'{double_quoted_query}', 
                    "lang":"en",
                    "page":"1",
                    "page_size":f'{num_articles}'}

    headers = {
        'x-rapidapi-key': f'{APIKEY}',
        'x-rapidapi-host': "free-news.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    query_data = response.json()['articles']
    
    def process_results(data):
        """
        Processes data from API to return a list of dictionaries of articles' title, created date, and url.
        """
        articles = []

        # Title, Publication Date, Media, Abstract, and URL
        for article in data:
            processed_article = {'title': article['title'],
                                'pub_date': article['published_date'],
                                'media': article['media'],
                                'abstract': article['summary'],
                                'url': article['link']
            }
            articles.append(processed_article)
        return articles

    return process_results(query_data)

def print_searched_articles(query, num_articles=3):
    """
    Prints results from search_articles in readable form.
    """
    articles = search_articles(query, num_articles)
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

