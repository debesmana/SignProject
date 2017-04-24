# -*- coding: utf-8 -*-
# utf-8 is a type of language encoding which covers the unicode character set. Latvian uses latin-extended a (if encoded correctly)
# http://www.utf8-chartable.de/unicode-utf8-table.pl  <-- For debugging

from urllib2 import urlopen #For the web scraping
from urllib2 import HTTPError #In case of problems connecting
import re #Regular Expressions
import math
import string #String operations (.upper & .lower)
from bs4 import BeautifulSoup #For getting rid of the garbage from the web
import pymongo #connecting to MongoDB
#importing the libraries that will be used
#Beautiful soup can be found here : https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

#The global lists used in the programm
url_list = []
daina_list = []
word_list = []

#keeps track of how many poems have been processed
#Useful if connnection gets interrupted
counter = 0
counter_file = open("counter_file.txt", 'w')

#local stuff for testing
USE_LOCAL = True
#mongodb authentication
if (not USE_LOCAL):
    user = raw_input("[?] Mongodb username: ")
    passw = getpass.getpass("[?] Mongodb password: ")

# Connection to Mongo DB
try:
    #setting up link to mongoDB
    if (USE_LOCAL):
        conn = pymongo.MongoClient('localhost', 27017)
    else:
        connURI = 'mongodb://%s:%s@mongoserver.almaulmane.com:27067/' % (user, passw)
        conn = pymongo.MongoClient(connURI)
    print "Connected to mongodb"
except pymongo.errors.ConnectionFailure, e:
    print "[!] Could not connect to MongoDB: %s" % e

#if a database (or collection) with a certain name isn't found mongo creates a new one when the first document is inserted
# Define mongoDB database
db = conn.poems

#rounds up to nearest 10. This is so all the poems from website are taken
def roundup(x):
    """Rounds a number up to the closest 10"""
    return int(math.ceil(x / 10.0)) * 10

#gets all the links to scrape
def get_links():
    """Scrapes the website for the next link"""
    #Gets all the links for the search "sun"
    #The links are always the same only the result page number changes
    SearchResultAmount = 10#905
    for x in range((roundup(SearchResultAmount)) / 10):
        url_list.append("http://www.dainuskapis.lv/meklet/%s/saule" % (int(x*10)))

#writes to counter in case of crash
def write_to_counter():
    """Writes to a counter file in case of internet crash so the programm can resume where it started"""
    global counter
    counter += 1
    #print counter
    counter_file.write(str(counter) + "\n")

#flattens list to avoid nested lists
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

#Scrapes the web for dainas and cleans up the html mess
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
            daina_string = re.sub(ur"[ \t+]", " ", daina_string)
            #regex to get rid of trailing white space and tabs
            daina_string = re.sub(ur"[\(\)\.\,\?\!\:\"\'\=\;\-\/]", "", daina_string)
            #regex to get rid of punctuation
            daina_string = re.sub(ur"  +", " | ", daina_string)
            #regex to get visibly show new space (for some inexplicable reason the html had it as multiple spaces)
            #print "start of n", daina_string
            #test if values are right
            daina_list.append(daina_string)
            #Lists how far the code got in case of crash, internet failure etc.
            write_to_counter()
    except AttributeError as e:
        print e
        return None
#Seperates out all the words into a list
def get_all_words(text):
    #print len(text)
    for x in range(len(text)):
        temporary = []
        #regex to remove any punctuation
        text[x] = re.sub(u"[\,\.\"\:\;\-\?\!\(\)]", "",  text[x])
        #make everything lower case
        temporary = re.sub(u"(\b[^\s]+\b)", " ",  text[x]).split()
        #make everything lower case
        temporary = [x.lower() for x in temporary]
        #word_list = [x.strip(string.punctuation) for x in word_list] #doesn't remove punctuation from within a word
        word_list.append(temporary)
    return word_list

#write the poems to the poem db
def write_daina_to_db(daina): 
    """Writes poems to db"""
    # Define the collection where dainas will be inserted
    posts = db.poems
    test = True
    #cleans collection for testing
    if test:
        db.poems.drop()
    for poem in range(len(daina)):
        # Empty dictionary for storing poems
        data = {}
        data['daina'] = daina[poem]
        posts.insert(data)
        #print data
    #print posts.count()
def write_words_to_db(words_list):
    # Define the collection where words will be inserted
    posts = db.words
    test = True
    #cleans collection for testing
    if test:
        db.words.drop()
    #print "word list is ", len(words_list)
    for x in range(len(words_list)):
        # Empty dictionary for storing poems
        db.words.update({"word": str(words_list[x])}, 
        {"$inc": {"tally": 1}}, upsert = True)
        db.words.find()
    print "posts in words db", posts.count()


#FUNCTIONS ARE CALLED HERE:
get_links()
for x in range(len(url_list)):
    get_daina(url_list[x])
#print daina_list
for x in range(len(daina_list)):
    #print "poem %s" %(x), daina_list[x] unflattened list
    #print "poem %s" %(x), repr(daina_list[x]) checking unicode
    merged_daina_list = flatten_list(daina_list)
    #print "poem %s" %(x), merged_daina_list[x]
    #unicode has to be checked in a for loop since python can't interpret list elements as unicode
words = get_all_words(merged_daina_list)
merged_words = flatten_list(words)
#print "words is", len(merged_words)
#for x in range(len(merged_words)):
    #print merged_words[x]
write_daina_to_db(merged_daina_list)
write_words_to_db(merged_words)


# TODO: write each word to mongoDB
# TODO: write word sorting algorithm
# TODO: tally words
# TODO: rewrite poems as word IDs