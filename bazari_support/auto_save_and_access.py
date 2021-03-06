import anvil.server
anvil.server.connect("NCQHRMRGTCNNGLUUUUKQIM2M-LHKZF6QGOHJTJ32F")

import csv
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import base64
from selenium import webdriver

from datetime import datetime, timezone
import random
from anvil.tables import app_tables

@anvil.server.callable
def uplink_scrape_data(url, slides, spanish_name, source_name):
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
        price=price_box.text.strip().replace('$', '') if price_box else 0 # In case of "Out of stock".      print(name)

        # Scrape picture.
        article_image=article.find('div', {'class': 'article__image'})
        picture_src=article_image.find('a', {'class': 'thumb-link'}).img['src']
        urllib.request.urlretrieve(picture_src, name)

        with open(name, 'rb') as img_file:
          picture="data:image/png;base64,"+base64.b64encode(img_file.read()).decode('utf-8')

        data.append((name, price, picture))
        check_names.append(check_name)
        time.sleep(1)

  print("...\n...\n[IN PROGRESS] Writing data to database. Please wait...")
  # Writing data to database.
  category=app_tables.categories.get(spanish_name=spanish_name)
  source=app_tables.sources.get(source_name=source_name)
  unit=app_tables.units.get(unit_name='piece')

  for article in data:
    print("Writing to database article " + str(data.index(article) + 1) + "/" + str(len(data)) + "...")

    name, price, picture=article

    app_tables.products.add_row(
      name=name,
      unit_price=round(float(price), 2),
      picture_b64=picture if picture else 'data:image/png;base64,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',
      sku=random.randint(100000,999999),
      category=[category],
      source=source,
      unit=unit,
      moq=1,
      increment=1,
      created=datetime.now(timezone.utc),
      disabled=False
    )
    
  print("[DONE] Finish scraping " + str(slides) + " pages of '" + url + "' (Total: " + str(len(data)) + " articles).")

anvil.server.wait_forever()
