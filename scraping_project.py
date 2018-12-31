# Python 3 practice
# This script grabs data from http://quotes.toscrape.com
# and generates a guessing game.

import requests
from bs4 import BeautifulSoup
from random import choice


def went_to_college(desc):
	went_to_college = any([word == "University" or "College" for word in desc])
	if went_to_college is True:
		return f"This person went to college or university."
	return f"This person did not go to college or university."

def make_hints(author, about_soup):
	hints = []
	# First , last name initials
	hints.append(f"This person's first name begins with the letter '{author[0]}'")
	last_ini = [ char for char in author[1:-1] if char.isupper()] # Iterate string backwards, return first uppercase letter
	hints.append(f"This person's first name begins with the letter '{last_ini}'")

	# Birthday and Birthplace
	birthday = about_soup.find(class_="author-born-date")
	birthplace = birthday.find_next_sibling()
	hints.append(f"This person was born on {birthday.get_text()}, {birthplace.get_text()}.")

	# Schooling
	desc = about_soup.find(class_="author-description").get_text()
	hints.append(went_to_college(desc))

	return hints

def give_hint(hints):
	hint = choice(hints)
	return hint

def update_hint_list(hint, hints):
	hints.remove(hint)
	return hints

#----------------------------------------------------------------


url = "http://quotes.toscrape.com"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

#Variables for looping
again = "Y"

# Get quote, author, about URL
quote = soup.find(class_="text")

while again != "N":

	# Get quote, author, about URL
	author = quote.find_next_sibling().find(class_="author")
	about_url = url + author.find_next_sibling()["href"]

	#Getting the about
	about_req = requests.get(about_url)
	about_soup = BeautifulSoup(about_req.text, "html.parser")

	# Make hints with the above info
	hints = make_hints(author.get_text(), about_soup)

	# Game start
	guess = input("Who said this?\n" + quote.get_text() + "Take a guess!(You have 4 chances.) \n\n")
	chance = 4
	while chance is not 0 and again == "Y":
		if guess == author.get_text():
			print("Congrats! You got it!")
			break
		else:
			hint = give_hint(hints)
			print("Not quite. Here's a hint.\n" + hint)
			guess = input("Guess again.\n\n")
			hints = update_hint_list(hint, hints)
			chance -= 1

		if chance == 0:
			print(f"No more chances left! The answer : {author.get_text()}.  ")

	# Point to the next set of elements
	again = input("Do you want to play again? Y/N\n\n ").upper()
	quote = quote.find_parent().find_next_sibling().find(class_="text")
