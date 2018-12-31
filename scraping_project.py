# Python 3 practice
# This script grabs data from http://quotes.toscrape.com
# and generates a guessing game.

import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com"
req = requests.get(url)
#print(req.text)

soup = BeautifulSoup(req.text, "html.parser")
#print(soup)

data_1 = soup.find(class_="quote").get_text()
print(data_1)