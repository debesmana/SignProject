# coding=utf-8

from urllib2 import urlopen
from urllib2 import HTTPError
import re
from bs4 import BeautifulSoup
#importing the libraries that will be used
#Beautiful soup can be found here : https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

#gets all the links to scrape
# TODO: finish function
def get_links(original_url):
    """Scrapes the website for the next link"""
    try:
        html = urlopen(original_url)
    except HTTPError as e:
        print e
        return None
        #checks if the path provided works

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
            return daina_string

    except AttributeError as e:
        print e
        return None

def get_daina_info(url):
    """Scrapes the web and returns info from the daina object"""
    try:
        html = urlopen(url)
    except HTTPError as e:
        print e
        return None
        #checks if path provided is good
    try:
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        #turns the html into a bs object (makes it easier to read)
        info = bsObj.find("", {"class" : "dainaadvlinks"}).findAll("kategorija")
        #finds all the daina info objects in a web page
        for n in info:
            # TODO: add regular expression to remove <>
            info_string = str(n)
            #turns into data into string
            info_string = re.sub(r"<[A-Za-z0-9\.\:\"\=\;\-\/\?\"\+\% ]+>", "", info_string)
            #regex to get rid of html elements
            #daina_string = re.sub(r"[0-9]+-[0-9]+", "", daina_string)
            #regex to get rid of numbering at begining of poem
            print info_string
            #test if values are right
            return info_string

    except AttributeError as e:
        print e
        return None


poem = get_daina("http://www.dainuskapis.lv/katalogs/1.-Par-dziesmam-un-dziedasanu")
info = get_daina_info("http://www.dainuskapis.lv/katalogs/1.-Par-dziesmam-un-dziedasanu")
#The website being scraped (looked at)
# TODO: write each daina object to mongoDB

if poem is None:
    print "poem could not be found"
else:
    print poem
    #prints the poem
