#Request to scrap websites using beautifulsoup and requests?:q!
import pickle 

import requests
from bs4 import BeautifulSoup


url_mov_bas = 'https://en.wikipedia.org'
url_year = '/wiki/Tamil_films_of_200'
base_url_list = []
movie_dict = {}
keywords_list = ['violence','crime']

for yy in range(9):
	base_url = url_mov_bas + url_year + str(yy)
	base_url_list.append(base_url)

try:
	dbfile = open('TamMoviePickle', 'rb')
	db = pickle.load(dbfile)
	dbfile = open('TamMoviePickle2000', 'rb')
	db.update(pickle.load(dbfile))
	
except:
	db = False

if not db:
	while len(base_url_list):
		print(base_url_list," <- Not empty proceeding to try all in list")
		for base_url in base_url_list:
			# Test URL base_url = "https://assets.digitalocean.com/articles/eng_python/beautiful-soup/mockturtle.html"
			print(base_url)
			try:
				page = requests.get(base_url)
				movie_dict[base_url] = []
				if page.status_code == 200:
					print("Good for -> {}".format(base_url))
					soup = BeautifulSoup(page.text,'html.parser')
					#td_soup = soup.find_all('i')
					for itag in soup.find_all('i'):
						if itag.parent.name == 'td':
							a_tag = itag.find('a')
							if a_tag:
								movie_dict[base_url].append(a_tag['href'])

					# Remove the Link from base_url lists
					print(base_url,' Successfully parsed (?) Removing from list')
					base_url_list.remove(base_url)
					print(base_url_list, " <- List after removal")
					# print(pretty_soup)
			except:
				print('Oops Couldn\'t fetch this time. Will try in next attempt')
				# Else Pass for this case and try again until all links were done
				pass
else:
	print("File already exists in DB")
	movie_dict = db.copy()

if not db:
	dbfile = open('TamMoviePickle2000', 'ab')
	pickle.dump(movie_dict, dbfile)
	dbfile.close() 

searched_movies = set()
total = 0
print("List of Tamil year movies:")
for x in sorted(movie_dict.keys()):
	total += len(movie_dict[x])
	print(x)
print("Total movies wiki content: " , total)
input()

for key in sorted(movie_dict.keys()):
	print("Going through ",key)
	for movie_link in movie_dict[key]:
		movie_url = url_mov_bas + movie_link
		page = requests.get(movie_url)
		if page.status_code == 200:
			for keyword in keywords_list:
				if keyword in page.text.lower(): 
					print("Matched with words you wanted! --> {0} movie {1}".format(keyword[0],movie_link) )
					searched_movies.add(movie_link)


print("Here is the list of searched movies:")
print(searched_movies)
