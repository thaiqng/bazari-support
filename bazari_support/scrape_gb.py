import csv
from datetime import datetime
import urllib.request
from selenium import webdriver
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
check_names=[]
redo = False

while slide <= slides:
  # Get and parse HTML.
  source=url + "#" + str(slide) if slide > 0 else url
  driver=webdriver.Chrome() # Only real browser driver is used to pass in fragment, not normal HTTP request module.
  driver.get(source)
  page=driver.page_source
  soup=BeautifulSoup(page, 'html.parser')
  articles=soup.find_all('article', {'class': 'article article--secondary'})

  print("...\n...\n[IN PROGRESS] Scraping page " + str(slide) + "/" + str(slides) + " of '" + url + "'. Please wait...")
  slide += 1
  if redo:
    time.sleep(4)
    redo = False
  else:
    time.sleep(2)

  # Check if the article is repeated. If yes, don't proceed and redo the page scrape.
  check_name=articles[0].find('h6').a.text.strip().replace("/", "x")
  if check_name in check_names:
    slide -= 1
    redo = True 
    print("Finding duplicated article " + "'" + check_name + "'" + ". Redo page " + str(slide) + ".")
  else:
    for article in articles:
      print("Scraping article " + str(articles.index(article) + 1) + "/" + str(len(articles)) + "...")

      # Scrape name and price.
      article_body=article.find('div', {'class': 'article__body'})
      name=article_body.h6.a.text.strip().replace("/", "x") # In case the name includes "/" like "c/u" or "5/250ml".
      price_box=article_body.find('span', {'class': 'newPrice'})
      price=price_box.text.strip().replace('$', '') if price_box else 0 # In case of "Out of stock".

      # Scrape picture.
      article_image=article.find('div', {'class': 'article__image'})
      picture=article_image.find('a', {'class': 'thumb-link'}).img['src']
      urllib.request.urlretrieve(picture, name)

      with open(name, 'rb') as img_file:
        picture="data:image/png;base64,"+base64.b64encode(img_file.read()).decode('utf-8')

      data.append((name, price, picture))
      check_names.append(check_name)
      time.sleep(1)

print("\n\n[IN PROGRESS] Writing data to 'index.csv'. Please wait...")
# Open a csv file with append instead of erasing.
with open('index.csv', 'a') as csv_file:
  writer = csv.writer(csv_file)
  
  for article in data:
    print("Writing to database article " + str(data.index(article) + 1) + "/" + str(len(data)) + "...")

    name, price, picture=article

    writer.writerow([name, price, picture, datetime.now()])

print("[DONE] Finish scraping " + str(slides) + " pages of '" + url + "' (Total: " + str(len(data)) + " items).")
