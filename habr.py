import requests
from bs4 import BeautifulSoup
import re

KEYWORDS = ['python', 'sql', 'orm', 'парсинг']
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
base_url = 'https://habr.com'
url = base_url + '/ru/all/'

response = requests.get(url, headers=HEADERS)
response.raise_for_status()
text = response.text

soup = BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')

for article in articles:
    tags = article.find_all(class_="tm-article-snippet__hubs-item")
    tags = set(re.sub(r'\*', '', tag.text.lower()).strip() for tag in tags)

    article_preview_body = article.find_all(class_="article-formatted-body")
    article_preview_body = set(block.text.lower().strip() for block in article_preview_body)

    href = article.find('h2').find('a').attrs['href']
    link = base_url + href
    title = article.find('h2').find('span').text.lower().strip()
    date = article.find('time').attrs['title']
    count = 0

    for word in KEYWORDS:

        if (word in tags or word in ' '.join(article_preview_body) + title) and count == 0:
            print('{} - {} - {}'.format(date, title, link))
            count += 1
            break
        elif (word not in tags or word not in ' '.join(article_preview_body) + title) and count == 0:
            response = requests.get(link, headers=HEADERS)
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, features='html.parser')
            article_body = soup.find(class_="article-formatted-body").find_all('p')
            article_body = set(block.text.lower().strip() for block in article_body)

            for word in KEYWORDS:
                if word in ' '.join(article_body) and count == 0:
                    print('{} - {} - {}'.format(date, title, link))
                    count += 1
