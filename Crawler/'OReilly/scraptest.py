# coding=utf-8

from urllib2 import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup
#importing the libraries that will be used
#Beautiful soup can be found here : https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

#function to get html element (in this case h1)
def getDaina(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print e
        return None
        #checks if path provided is good
    try:
        bsObj = BeautifulSoup(html.read(),'html.parser')
        #turns the html into a bs object (makes it easier to read)
        daina = bsObj.findAll("", {"class" : "daina"}).children
        #finds all daina objects 
        for n in daina:
            
            print "start of n",n
            #print dir(n)
        
    except AttributeError as e:
        print e
        return None
        #checks if there actually is a h1 tag
    return daina

poem = getDaina("http://www.dainuskapis.lv/katalogs/1.-Par-dziesmam-un-dziedasanu")
#The website being scraped (looked at)

'''if poem == None:
    print "poem could not be found"
else:
    print poem
    #prints the poem '''