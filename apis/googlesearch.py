from bs4 import BeautifulSoup
import requests, urllib.parse
import lxml

google_link_template = 'https://www.google.com/search?q='

# Extracting searches from Google search
def google_scrape(search, num_links=3):

    # Querying
    url = google_link_template + str(search)
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    response = requests.get(url, headers=headers).text

    # Processing query results
    soup = BeautifulSoup(response, 'lxml')
    scraped_links = []

    for container in soup.find_all('div', class_='tF2Cxc'):
        head_text = container.find('h3', class_='LC20lb DKV0Md').text
        head_link = container.a['href']
        scraped_links.append({'head_text': head_text,
                            'head_link': head_link})

        if len(scraped_links) == num_links:
            break
    
    return scraped_links

def print_scraped_links(search, num_links=3):
    links = google_scrape(search, num_links)
    for link in links:
        print(link['head_text'])
        print(link['head_link'])
        print('--------------------------------------------------')
