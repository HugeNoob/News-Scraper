from flask import Flask, render_template, request
from apis import nytapi, guardianapi, newsapi, newscatcher

app = Flask(__name__)
 


@app.route('/')
def Index():
    nyt_article_list = nytapi.top_articles_in_section("home", 4)
    guardian_article_list = guardianapi.top_articles_in_section("search", 6)
    newsapi_article_list = newsapi.top_articles_in_section("general", 8)
    all_articles = {'nyt': nyt_article_list,
                    'guardian': guardian_article_list,
                    'newsapi1': newsapi_article_list[:4],
                    'newsapi2': newsapi_article_list[4:]
    }
    return render_template('index.html', context = all_articles)

@app.route('/business')
def business():
    nyt_article_list = nytapi.top_articles_in_section("business", 4)
    guardian_article_list = guardianapi.top_articles_in_section("business", 6)
    newsapi_article_list = newsapi.top_articles_in_section("business", 8)
    all_articles = {'nyt': nyt_article_list,
                    'guardian': guardian_article_list,
                    'newsapi1': newsapi_article_list[:4],
                    'newsapi2': newsapi_article_list[4:]
    }
    return render_template('business.html', context = all_articles)

@app.route('/health')
def health():
    nyt_article_list = nytapi.top_articles_in_section("health", 4)
    guardian_article_list = guardianapi.top_articles_in_section("healthcare-network", 6)
    newsapi_article_list = newsapi.top_articles_in_section("health", 8)
    all_articles = {'nyt': nyt_article_list,
                    'guardian': guardian_article_list,
                    'newsapi1': newsapi_article_list[:4],
                    'newsapi2': newsapi_article_list[4:]
    }
    return render_template('health.html', context = all_articles)

@app.route('/science')
def science():
    nyt_article_list = nytapi.top_articles_in_section("science", 4)
    guardian_article_list = guardianapi.top_articles_in_section("science", 6)
    newsapi_article_list = newsapi.top_articles_in_section("science", 8)
    all_articles = {'nyt': nyt_article_list,
                    'guardian': guardian_article_list,
                    'newsapi1': newsapi_article_list[:4],
                    'newsapi2': newsapi_article_list[4:]
    }
    return render_template('science.html', context = all_articles)

@app.route('/sports')
def sports():
    nyt_article_list = nytapi.top_articles_in_section("sports", 4)
    guardian_article_list = guardianapi.top_articles_in_section("sport", 6)
    newsapi_article_list = newsapi.top_articles_in_section("sports", 8)
    all_articles = {'nyt': nyt_article_list,
                    'guardian': guardian_article_list,
                    'newsapi1': newsapi_article_list[:4],
                    'newsapi2': newsapi_article_list[4:]
    }
    return render_template('sports.html', context = all_articles)

@app.route('/tech')
def tech():
    nyt_article_list = nytapi.top_articles_in_section("technology", 4)
    guardian_article_list = guardianapi.top_articles_in_section("technology", 6)
    newsapi_article_list = newsapi.top_articles_in_section("technology", 8)
    all_articles = {'nyt': nyt_article_list,
                    'guardian': guardian_article_list,
                    'newsapi1': newsapi_article_list[:4],
                    'newsapi2': newsapi_article_list[4:]
    }
    return render_template('tech.html', context = all_articles)

@app.route('/search', methods=["POST"])
def search():
    query = str(request.form.get('query'))
    nyt_article_list = nytapi.search_articles(query, 4)
    guardian_article_list = guardianapi.search_articles(query, 6)
    newsapi_article_list = newsapi.search_articles(query, 6)
    all_articles = {'nyt': nyt_article_list,
                    'guardian': guardian_article_list,
                    'newsapi1': newsapi_article_list,
    }
    return render_template('search.html', context = all_articles, query_str = query)

    

if __name__ == "__main__":
    app.run()