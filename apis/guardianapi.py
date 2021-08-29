import requests
from pprint import pprint
from bs4 import BeautifulSoup

# API documentation: https://open-platform.theguardian.com/documentation/
APIKEY = '(apikey removed for github)'
SECTIONS = ['about', 
            'animals-farmed',
            'artanddesign',
            'australia-news',
            'better-business',
            'books',
            'business',
            'business-to-business',
            'cardiff',
            'childrens-books-site',
            'cities',
            'commentisfree',
            'community',
            'crosswords',
            'culture',
            'culture-network',
            'culture-professionals-network',
            'edinburgh',
            'education',
            'enterprise-network',
            'environment',
            'extra',
            'fashion',
            'film',
            'food',
            'football',
            'games',
            'global-development',
            'global-development-professionals-network',
            'government-computing-network',
            'guardian-professional',
            'healthcare-network',
            'help',
            'higher-education-network',
            'housing-network',
            'inequality',
            'info',
            'jobsadvice',
            'katine',
            'law',
            'leeds',
            'lifeandstyle',
            'local',
            'local-government-network',
            'media',
            'media-network',
            'membership',
            'money',
            'music',
            'news',
            'politics',
            'public-leaders-network',
            'science',
            'search',
            'small-business-network',
            'social-care-network',
            'social-enterprise-network',
            'society',
            'society-professionals',
            'sport',
            'stage',
            'teacher-network',
            'technology',
            'theguardian',
            'theobserver',
            'travel',
            'travel/offers',
            'tv-and-radio',
            'uk-news',
            'us-news',
            'voluntary-sector-network',
            'weather',
            'women-in-leadership',
            'working-in-development',
            'world']

# Top articles from a section
def top_articles_in_section(section, num_articles=3):
    """
    Returns a list of articles with their title, published date, and url as dictionary keys.
    """
    query_url = f"http://content.guardianapis.com/{section}?" \
                f"api-key={APIKEY}" \

    r = requests.get(query_url)
    query_data = r.json()['response']['results']
    def process_results(data):
        """
        Processes data from API to return a list of dictionaries of articles' title, created date, and url.
        """
        articles = []
        for article in data:
            processed_article = {'title': article['webTitle'],
                                'pub_date': article['webPublicationDate'].split('T')[0],
                                'url': article['webUrl']
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
                    if 'i.guim.co.uk' in str(pic):
                        article['media'] = str(pic)
                        break
            
        return articles

    return scrape_image(articles)

def print_top_articles(section, num_articles=3):
    """
    Prints results from top_articles_in_section in readable form.
    """
    if section not in SECTIONS:
        print('Invalid section.')
        return
    articles = top_articles_in_section(section, num_articles)

    # Title, Publication Date, URL
    for article in articles:
        print(article['title'])
        print('Published Date: ' + article['pub_date'])
        print()
        print('More at: ' + article['url'])
        print('------------------------------------------------------------------------------------------------')


# Article Search
def search_articles(query, num_articles=3, orderby='relevance'):
    """
    Searches exact phrases in article body.
    """
    double_quoted_query = '"' + query + '"'
    query_fields = "body"
    query_url = f"https://content.guardianapis.com/search?" \
                f"api-key={APIKEY}" \
                f"&q={double_quoted_query}" \
                f"&query-fields={query_fields}" \
                f"&order-by={orderby}" \
                f"&show-fields=headline,byline,starRating,shortUrl"

    r = requests.get(query_url)
    query_data = r.json()['response']['results']
    def process_results(data):
        """
        Processes data from API to return a list of dictionaries of articles' title, created date, and url.
        """
        articles = []

        # Title, Publication date, URL
        for article in data:
            processed_article = {'title': article['fields']['headline'],
                                'pub_date': article['webPublicationDate'].split('T')[0],
                                'url': article['webUrl']
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
                    if 'i.guim.co.uk' in str(pic):
                        article['media'] = str(pic)
                        break
            
        return articles

    if articles == None:
        return None
    
    return scrape_image(articles)

def print_searched_articles(query, num_articles=3, orderby='relevance'):
    """
    Prints results from search_articles in readable form.
    """
    articles = search_articles(query, num_articles, orderby)
    if articles == None:
        print("No articles found.")
        return

    # Title, Publication date, URL
    for article in articles:
        print(article['title'])
        print('Published Date: ' + article['pub_date'])
        print()
        print('More at: ' + article['url'])
        print('------------------------------------------------------------------------------------------------')
