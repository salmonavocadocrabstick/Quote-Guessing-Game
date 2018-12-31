# Python 3 practice
# This script grabs data from http://quotes.toscrape.com
# and generates a guessing game.

import requests
from bs4 import BeautifulSoup


def went_to_college(desc):
	went_to_college = any([word == "University" or "College" for word in desc])
	if went_to_college is True:
		return f"This person went to college or university."
	return f"This person did not go to college or university."


url = "http://quotes.toscrape.com"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

# Get quote, author, about URL
quote = soup.find(class_="text").get_text() 
author = soup.find(class_="author").get_text() 
about_url = url+soup.find(class_="author").find_next_sibling()["href"]


# First , last name initials
hint_1 = f"This person's first name begins with the letter '{author[0]}'"
last_ini = [ char for char in author[1:-1] if char.isupper()] # Iterate string backwards, return first uppercase letter
hint_2 = f"This person's first name begins with the letter '{last_ini}'"


#Getting the about
about_req = requests.get(about_url)
about_soup = BeautifulSoup(about_req.text, "html.parser")

# Birthday and Birthplace
birthday = about_soup.find(class_="author-born-date")
birthplace = birthday.find_next_sibling()
hint_3 = f"This person was born on {birthday.get_text()}, {birthplace.get_text()}."

# Schooling
desc = about_soup.find(class_="author-description").get_text()
hint_4 = went_to_college(desc)

#----------------------------------------------------------------

chance = 4
again = "Y"

guess = input("Who said this?\n" + quote + "Take a guess! \n\n")
while chance is not 0 and again == "Y":
	if guess == author:
		print("Congrats! You got it!")
		again = input("Play again? Y/N\n\n").upper()
	else:
		print("Not quite. Here's a hint.\n" + hint_1)
		guess = input("Guess again.\n\n")
		chance -= 1