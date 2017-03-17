# coding=utf-8

from urllib2 import urlopen
from urllib2 import HTTPError
import re
import math
from bs4 import BeautifulSoup
#importing the libraries that will be used
#Beautiful soup can be found here : https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

#All the URL for the scraper
url_list = []
daina_list = []

#rounds up to nearest 10
def roundup(x):
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
            # TODO: add regular expression to remove <>
            daina_string = str(n)
            #turns into data into string
            daina_string = re.sub(r"<[A-Za-z0-9\.\:\"\=\;\-\/ ]+>", "", daina_string)
            #regex to get rid of html elements
            daina_string = re.sub(r"[0-9]+-[0-9]+", "", daina_string)
            #regex to get rid of numbering at begining of poem
            #print "start of n", daina_string
            #test if values are right
            daina_list.append(daina_string)
    except AttributeError as e:
        print e
        return None
    
#functions are called here
get_links()
for x in range(len(url_list)):
    get_daina(url_list[x])

for x in range(len(daina_list)): 
    print "poem %s" %(x), daina_list[x]
#prints the poem
# TODO: write each daina object to mongoDB
