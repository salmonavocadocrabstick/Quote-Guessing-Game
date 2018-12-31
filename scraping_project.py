# Python 3 practice
# This script grabs data from http://quotes.toscrape.com
# and generates a guessing game.

import requests
from bs4 import BeautifulSoup
from random import choice

def makeHints(author, about_soup):
	hints = []
	# First , last name initials
	hints.append(f"This person's first name begins with the letter '{author[0]}'")
	last_ini = [char for char in author[1:-1] if char.isupper()] # Iterate string backwards, return first uppercase letter
	hints.append(f"This person's last name begins with the letter '{last_ini[-1]}'")

	# Birthday and Birthplace
	birthday = about_soup.find(class_="author-born-date")
	birthplace = birthday.find_next_sibling()
	hints.append(f"This person was born on {birthday.get_text()}, {birthplace.get_text()}.")

	# Acheivment
	desc = str(about_soup.find(class_="author-description").get_text()).split('.')
	info = list(filter(lambda x : any(item == "His" or item =="Her" for item in x.split()), desc))
	if info == []:
		info = list(filter(lambda x : any(item == "He" or item =="She" for item in x.split()), desc))
	if info != []:
		hints.append(info[0])

	return hints

def giveHint(hints):
	if hints != []:
		hint = choice(hints)
	else:
		hint = "Oops! No more hints available for this person."
	return hint

def updateHintList(hint, hints):
	hints.remove(hint)
	return hints

def getUserInput(prompt, error_message):
	while True:
		try:
			guess = input(prompt)
		except Exception:
			print(error_message)
		else:
			return guess

#----------------------------------------------------------------


url = "http://quotes.toscrape.com"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

# #Variables for looping
again = "Y"
current = 2
next_page_url = "/page/"


# Get quote, author, about URL
quote = soup.find(class_="text")

while again == "Y":

	# Get quote, author, about URL
	author = quote.find_next_sibling().find(class_="author")
	about_url = url + author.find_next_sibling()["href"]

	#Getting the about
	about_req = requests.get(about_url)
	about_soup = BeautifulSoup(about_req.text, "html.parser")

	# Make hints with the above info
	hints = makeHints(author.get_text(), about_soup)

	# Game start
	print("Who said this?\n" + quote.get_text()) 
	guess = getUserInput("Take a guess!(You have 4 chances.) \n\n", "Alphabets only!")
	chance = 3
	while chance is not 0 and again == "Y":
		chance -= 1
		if guess == author.get_text():
			print("Congrats! You got it!")
			break
		else:
			hint = giveHint(hints)
			print("Not quite. Here's a hint.\n" + hint)
			#guess = input("Guess again.\n\n")
			guess = getUserInput("Guess again.\n\n", "Alphabets only!")
			hints = updateHintList(hint, hints)
		if chance <= 0:
			print(f"No more chances left! The answer : {author.get_text()}.  ")

		
	again = getUserInput("Do you want to play again? Y/N\n\n ", "Y or N only!").upper()
	# Check if we are at the end of the page, where a next button is available.
	# Point to the next set of elements
	try:
		quote = quote.find_parent().find_next_sibling().find(class_="text")
		print(quote.get_text())
	except AttributeError:
		next_page = url + next_page_url + str(current)
		#print(next_page)
		req = requests.get(next_page)
		#print(req.text)
		soup = BeautifulSoup(req.text, "html.parser")
		current += 1
		quote = soup.find(class_="text")
	finally:
		hints.clear()
		