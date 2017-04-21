# -*- coding: utf-8 -*-
# utf-8 is a type of language encoding which covers the unicode character set. Latvian uses latin-extended a (if encoded correctly)
# http://www.utf8-chartable.de/unicode-utf8-table.pl

from urllib2 import urlopen
from urllib2 import HTTPError
import re
import math
import string
from bs4 import BeautifulSoup
import pymongo
#importing the libraries that will be used
#Beautiful soup can be found here : https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

#The lists used in the programm
url_list = []
daina_list = []
word_list = []

#keeps track of how many poems have been processed
counter = 0
counter_file = open("counter_file.txt", 'w')

# Connection to Mongo DB
try:
    #setting up link to mongoDB
    #conn = pymongo.MongoClient('138.68.170.30', 27067)
    conn = pymongo.MongoClient('localhost', 27017) #Localhost to test if problem with server
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
 #if a database (or collection) with a certain name isn't found mongo creates a new one when the first document is inserted
# Define mongoDB database
db = conn.poems

#rounds up to nearest 10
def roundup(x):
    """Rounds a number up to the closest 10"""
    return int(math.ceil(x / 10.0)) * 10

#gets all the links to scrape
def get_links():
    """Scrapes the website for the next link"""
    #Gets all the links for the search "sun"
    SearchResultAmount = 5#905
    for x in range((roundup(SearchResultAmount)) / 10):
        url_list.append("http://www.dainuskapis.lv/meklet/%s/saule" % (int(x*10)))

#function to get daina
def write_to_counter():
    """Writes to a counter file in case of internet crash so the programm can resume where it started"""
    global counter
    counter += 1
    #print counter
    counter_file.write(str(counter) + "\n")

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
            try:
                daina_string.decode('utf-8')
                #print "string is UTF-8, length %d bytes" % len(daina_string)
            except UnicodeError:
                print "string is not UTF-8"
            #turns html data into string
            daina_string = re.sub(ur"<[A-Za-z0-9\.\:\"\'\=\;\-\/ \t]+>", "", daina_string)
            #regex to get rid of html elements
            daina_string = re.sub(ur"[0-9]+-[0-9]+", "", daina_string)
            #regex to get rid of numbering at begining of poem
            daina_string = re.sub(ur"[ \n\t+]", " ", daina_string)
            #regex to get rid of trailing white space, tabs and new lines
            #print "start of n", daina_string
            #test if values are right
            daina_list.append(daina_string)
            #Lists how far the code got in case of crash, internet failure etc.
            write_to_counter()
    except AttributeError as e:
        print e
        return None
def flatten_list(listOfLists):
    """Flatten a list of (lists of (lists of strings)) for any level 
    of nesting"""
    #http://stackoverflow.com/questions/17864466/flatten-a-list-of-strings-and-lists-of-strings-and-lists-in-python
    merged_list = []

    for i in listOfLists:
        # Only append if i is a basestring (superclass of string)
        if isinstance(i, basestring):
            merged_list.append(i)
        # Otherwise call this function recursively
        else:
            merged_list.extend(flatten_list(i))
    #print merged_list
    return merged_list

def get_all_words(text):
    word_list = []
    print len(text)
    for x in range(len(text)):
        temporary = []
        #regex to remove any punctuation
        text[x] = re.sub(u"[\,\.\"\:\;\-\?\!\(\)]", "",  text[x])
        #regex to split into words
        temporary = re.sub(u"(\b[^\s]+\b)", " ",  text[x]).split()
        #make everything lower case
        temporary = [x.lower() for x in temporary]
        #word_list = [x.strip(string.punctuation) for x in word_list] #doesn't remove punctuation from within a word
        word_list.append(temporary)
    print repr(word_list).decode("unicode-escape")
    return word_list
        

def write_daina_to_db(daina): 
    """Writes poems to db"""
    # Define the collection where dainas will be inserted
    posts = db.poems
    for poem in range(len(daina)):
        # Empty dictionary for storing poems
        data = {}
        data['daina'] = daina[poem]
        posts.insert(data)
        print data
    #print posts.count()
def write_words_to_db(wordList):
    # Define the collection where words will be inserted
    posts = db.words
    data = {}
    for x in range(len(wordList)):
        posts.find_and_modify({"word": wordList[x]}, {"$inc":{"count": 1}}, safe = True, new = True)
        #
        print data
#functions are called here

get_links()
for x in range(len(url_list)):
    get_daina(url_list[x])
for x in range(len(daina_list)): 
    #print "poem %s" %(x), daina_list[x] unflattened list
    #print "poem %s" %(x), repr(daina_list[x]) checing unicode 
    merged_daina_list = flatten_list(daina_list)
    #print "poem %s" %(x), merged_daina_list [x]
for x in range(len(word_list)):
    print "word %s" %(x), word_list[x]

#write_daina_to_db(merged_daina_list)
word_List = get_all_words(merged_daina_list)
#merged_word_list = flatten_list(word_List)
#print repr(word_List).decode("unicode-escape")
#print repr(merged_word_list).decode("unicode-escape")
#write_words_to_db(word_List)
counter_file.close()#files that are opened need to be closed
#prints the poem
# TODO: write each word to mongoDB
# TODO: write word sorting algorythm
