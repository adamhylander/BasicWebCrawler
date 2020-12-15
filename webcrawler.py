from bs4 import BeautifulSoup
import requests
import random

#This is the first website we use for the crawl.
website = 'https://www.d-sektionen.se'

source = requests.get(website).text

#BeautifulSoup is a python library that is meant for pulling data from either a
#HTML or XML file. BeautifulSoup allowed us to filter out every link from all of the
#a tags from each visited website. 
soup = BeautifulSoup(source, 'lxml')

#Here is the method that gets every single a tag. Although we only want the href.
#We filter out the href in the for loop below.
href_tags = soup.find_all('a', href=True)

#extractedLinks is an empty list that is meant for gathering all the links from the
#first website we gathered.
extractedLinks = []

#This is a variable that is needed to keep track of how many websites we have visited
amountOfWebsites = 0;

checkSites = []

#Here we go through all the links gather from the soup.find_all method. 
for links in href_tags:
	#We chose to stick only keep the links that are either http and https. This is because
	#a lot of the links we gather from soup.find_all can look like /contacts/ or #settings
	#and those links keep you on the same website
	if(links.get('href').split(":")[0] == "http" or links.get('href').split(":")[0] == "https"):
		#This condition checks to see if the link isn't just the same website. 
		if(links.get('href').split("/")[2] == website.split("/")[2] or links.get('href').split("/")[2] == website.split("www.")[1]):
			continue
		else:
			#This makes sure so we don't get any duplicates in our list
			if links.get('href') not in extractedLinks:
				extractedLinks.append(links.get('href'))

#In order to properly see the tree structure for each site we divided it by a for loop.
for i in range(3):
	#In order to get more reliable test results we used random links from the first
	#website instead of just using i.e. the first three links. This means we can test
	#the same website multiple times and see if it works properly. 
	randomLink = random.randrange(len(extractedLinks))
	print("Tree for Website Number: " + str(i+1))
	amountOfWebsites = amountOfWebsites + 1
	print(website + " -> " + extractedLinks[randomLink])
	print
	#Here we add the website we first visited in to our list of visited websites.
	#It is important that this is in the for loop since it has to be reset for each
	#individual tree.
	visitedWebsites = [website.split("/")[2], website.split("www.")[1]]
	gen2 = []

	source1 = requests.get(extractedLinks[randomLink]).text
	soupGen1 = BeautifulSoup(source1, 'lxml')
	href_tagsGen1 = soupGen1.find_all('a', href=True)

	counter = 1;

	for links in href_tagsGen1:
		if(links.get('href').split(":")[0] == "http" or links.get('href').split(":")[0] == "https"):
			if(links.get('href').split("/")[2] == extractedLinks[randomLink].split("/")[2] or links.get('href').split("/")[2] in visitedWebsites):
				continue
			else:
				if links.get('href') not in gen2:
					gen2.append(links.get('href'))
					visitedWebsites.append(links.get('href').split("/")[2])
					#The following two if statements are so that we don't visit duplicate sites
					#This is easier to explain with an example. Lets say we visited the website
					#https://www.youtube.com/ then that will be added to our lists of visited websites.
					#However this won't prevent us from entering https://youtube.com/ which is the same
					#website! These two if statements add both https://youtube.com/ and
					#https://www.youtube.com/ to our list.
					if "www" in links.get('href').split("/")[2]:
						visitedWebsites.append(links.get('href').split("/")[2].split("www.")[1])
					if "www" not in links.get('href').split("/")[2]:
						visitedWebsites.append("www." + str(links.get('href').split("/")[2]))
					counter = counter + 1
					if counter > 3:
						break
	#This for loop prints the second generation of crawls.
	for x in gen2:
		print(extractedLinks[randomLink] + " -> " + x)
		amountOfWebsites = amountOfWebsites + 1

	print

	#Then we keep doing this same method, looping for each generation, until we get
	#three layers deep. This could be made in to a method however we did not find this
	#necessary as we aren't crawling that deep.
	for x in gen2:
		counterGen2 = 1;
		gen3 = []
		source2 = requests.get(x).text
		soupGen2 = BeautifulSoup(source2, 'lxml')
		href_tagsGen2 = soupGen2.find_all('a', href=True)

		for links in href_tagsGen2:
			if(links.get('href').split(":")[0] == "http"):
				if(links.get('href').split("/")[2] == x.split("/")[2] or links.get('href').split("/")[2] in visitedWebsites):
					continue
				else:
					if links.get('href') not in gen3:
						gen3.append(links.get('href'))
						visitedWebsites.append(links.get('href').split("/")[2])
						if "www" in links.get('href').split("/")[2]:
							visitedWebsites.append(links.get('href').split("/")[2].split("www.")[1])
						if "www" not in links.get('href').split("/")[2]:
							visitedWebsites.append("www." + str(links.get('href').split("/")[2]))
						counterGen2 = counterGen2 + 1
						if counterGen2 > 3:
							break
		
		for y in gen3:
			print(x + " -> " + y)
			amountOfWebsites = amountOfWebsites + 1

		print

		for y in gen3:
			counterGen3 = 1
			gen4 = []
			source3 = requests.get(y).text
			soupGen3 = BeautifulSoup(source3, 'lxml')
			href_tagsGen3 = soupGen3.find_all('a', href=True)

			for links in href_tagsGen3:
				if(links.get('href').split(":")[0] == "http" or links.get('href').split(":")[0] == "https"):
					if(links.get('href').split("/")[2] == x.split("/")[2] or links.get('href').split("/")[2] in visitedWebsites):
						continue
					else:
						if links.get('href') not in gen4:
							gen4.append(links.get('href'))
							visitedWebsites.append(links.get('href').split("/")[2])
							counterGen3 = counterGen3 + 1
							if counterGen3 > 3:
								break

			for z in gen4:
				print(y + " -> " + z)
				amountOfWebsites = amountOfWebsites + 1;

			print

	#Here we remove the link that we used in this for loop so we don't get the same link twice
	del extractedLinks[randomLink]

#As an extra we also added the counter which tells us how many sites we visited in total. 
#Note that this does not filter out duplicates in between the trees.
print("Amount of Websites visited: " + str(amountOfWebsites))
