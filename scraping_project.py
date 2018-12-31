# Python 3 practice
# This script grabs data from http://quotes.toscrape.com
# and generates a guessing game.

import requests

url = "http://quotes.toscrape.com"
req = requests.get(url)
print(req.text)