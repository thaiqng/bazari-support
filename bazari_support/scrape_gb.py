import csv
from datetime import datetime
import urllib.request
from bs4 import BeautifulSoup
import time
import base64

url=input('Enter the URL: ')
slides=int(input('Enter the number of pages in this URL: '))

if slides and slides > 0:
  slide=1 
else:
  slides=0
  slide=0

data=[]

while slide <= slides:
  # Get and parse HTML.
  quote_page=url + "#" + str(slide) if slide > 0 else url 
  page=urllib.request.urlopen(quote_page)
  soup=BeautifulSoup(page, 'html.parser')

  print("...\n...\n[IN PROGRESS] Scraping page " + str(slide) + "/" + str(slides) + " of '" + url + "'. Please wait...")
  slide += 1

  articles=soup.find_all('article', {'class': 'article article--secondary'})
  length=len(articles)
  for article in articles:
    print("Scraping article " + str(articles.index(article) + 1) + "/" + str(length) + "...")

    # Scrape name and price.
    article_body=article.find('div', {'class': 'article__body'})
    name=article_body.h6.a.text.strip()
    price=article_body.find('span', {'class': 'newPrice'}).text.strip().replace('$', '')

    # Scrape picture.
    article_image=article.find('div', {'class': 'article__image'})
    picture=article_image.find('a', {'class': 'thumb-link'}).img['src']
    urllib.request.urlretrieve(picture, name)

    with open(name, 'rb') as img_file:
      picture="data:image/png;base64,"+base64.b64encode(img_file.read()).decode('utf-8')

    data.append((name, price, picture))
    time.sleep(1)

print("[IN PROGRESS] Writing data to 'index.csv'. Please wait...")
# Open a csv file with append instead of erasing.
with open('index.csv', 'a') as csv_file:
  writer = csv.writer(csv_file)
  for name, price, picture in data:
    print("Writing to database article " + str(data.index(article) + 1) + "/" + str(length) + "...")
    writer.writerow([name, price, picture, datetime.now()])

print("[DONE] Finish scraping " + str(slides) + " pages of '" + url + "' (Total: " + str(length) + " items).")
