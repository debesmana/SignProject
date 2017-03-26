# coding=utf-8

import ast
from urllib2 import urlopen
from urllib2 import HTTPError
import re
import math
from bs4 import BeautifulSoup
from pymongo import MongoClient
#importing the libraries that will be used
#Beautiful soup can be found here : https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

#The lists used in the programm
url_list = []
daina_list = []
word_list = []

#keeps track of how many poems have been processed
counter = 0
counter_file = open("counter_file.txt", 'w')

#rounds up to nearest 10
def roundup(x):
    """Rounds a number up to the closest 10"""
    return int(math.ceil(x / 10.0)) * 10

#gets all the links to scrape
def get_links():
    """Scrapes the website for the next link"""
    #Gets all the links for the search "sun"
    SearchResultAmount = 30#905
    for x in range((roundup(SearchResultAmount)) / 10):
        url_list.append("http://www.dainuskapis.lv/meklet/%s/saule" % (int(x*10)))

#function to get daina
def get_daina(url):
    """Scrapes the web and returns daina object"""
    try:
        html = urlopen(url)
    except HTTPError as e:
        print e
        return None
        #checks if path provided is good
    try:
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        #turns the html into a bs object (makes it easier to read)
        daina = bsObj.findAll("", {"class" : "daina"})
        #finds all the daina objects in a web page
        for n in daina:
            daina_string = str(n)
            #turns html data into string
            daina_string = re.sub(ur"<[A-Za-z0-9\.\:\"\'\=\;\-\/ ]+>", "", daina_string)
            #regex to get rid of html elements
            daina_string = re.sub(ur"[0-9]+-[0-9]+", "", daina_string)
            #regex to get rid of numbering at begining of poem
            #print "start of n", daina_string
            #test if values are right
            daina_list.append(daina_string)
            
            #Writes to a counter file in case of internet crash so the programm can resume where it started 
            global counter
            counter += 1
            #print counter
            counter_file.write(str(counter) + "\n")

            #removes punctuation
            words = re.sub(ur"[\,\.\?\!\;\:]", "", daina_string)
            #gets seperate words
            words = re.split(ur'[ \n\t]+', words, flags=re.UNICODE)
            word_list.append(words)

    except AttributeError as e:
        print e
        return None
    
#writes to mongo
#def get_words(daina = []):
    """Splits poem into words and passes them into an array"""
    #word_list = str(daina)
    #word_list = re.split(ur'[\W\s]+', word_list, flags=re.UNICODE)
    #words = re.sub(r"<[\.\:\"\'\=\;\-\/\,\t ]+>", "", word_list)
    #regex to get rid of html elements
    #return word_list
def write_to_db(daina): 
    """Writes poems to db"""
    #setting up local mongoDB
    client = MongoClient()
    #if a database (or collection) with a certain name isn't found mongo creates a new one when the first document is inserted
    db = dainas.test
    collection = db.test_collection
    post = {"poem": daina}
    db.test_collection.insert(post)

#functions are called here
#def get_all_words(daina):

get_links()
for x in range(len(url_list)):
    get_daina(url_list[x])

for x in range(len(daina_list)): 
    print "poem %s" %(x), daina_list[x]

print word_list



counter_file.close()
#prints the poem
# TODO: write each daina object to mongoDB
