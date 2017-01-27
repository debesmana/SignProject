# coding=utf-8

from urllib2 import urlopen
from urllib2 import HTTPError
import re
from bs4 import BeautifulSoup
#importing the libraries that will be used
#Beautiful soup can be found here : https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

#function to get html element (in this case h1)
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
            daina_string = re.sub(r"<[A-Za-z0-9\.\:\"\=\;\-\/ ]+>", "", daina_string)
            daina_string = re.sub(r"[0-9]+-[0-9]+", "", daina_string)
            print "start of n", daina_string
            #print dir(n)
            return daina_string

    except AttributeError as e:
        print e
        return None

poem = get_daina("http://www.dainuskapis.lv/katalogs/1.-Par-dziesmam-un-dziedasanu")
#The website being scraped (looked at)
# TODO: return each daina as seperate object
# TODO: write each daina object to mongoDB

'''if poem == None:
    print "poem could not be found"
else:
    print poem
    #prints the poem '''