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

quote = soup.find(class_="text").get_text() # Quote only, no other information
#print(quote)

author = soup.find(class_="author").get_text() 
#print(author)

about_url = url+soup.find(class_="author").find_next_sibling()["href"]
#print(about_url)

# First initial
hint_1 = f"This person's first name begins with the letter '{author[0]}'"
#print(hint_1)

# Last name initial
last_ini = [ char for char in author[1:-1] if char.isupper()] # Iterate string backwards, return first uppercase letter
hint_2 = f"This person's first name begins with the letter '{last_ini}'"


#Getting the about
about_req = requests.get(about_url)
about_soup = BeautifulSoup(about_req.text, "html.parser")

# Birthday and Birthplace
birthday = about_soup.find(class_="author-born-date")
# need get_text() later

birthplace = birthday.find_next_sibling()
#print(hint_3_birthplace.get_text())

hint_3 = f"This person was born on {birthday.get_text()}, {birthplace.get_text()}."

# Schooling
hint_4 = about_soup.find(class_="author-description").get_text()
#print(type(hint_4))
went_to_college = any([word == "University" or "College" for word in hint_4])
if went_to_college is True:
	print(f"This person went to college or university.")
else:
	print(f"This person did not go to college or university.")

