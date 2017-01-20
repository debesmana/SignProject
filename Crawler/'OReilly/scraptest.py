from urllib2 import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup
#importing the libraries that will be used
#Beautiful soup can be found here : https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

#function to get html element (in this case h1)
def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
        #checks if path provided is good
    try:
        bsObj = BeautifulSoup(html.read())
        #turns the html into a bs object (makes it easier to read)
        title = bsObj.html.body.h1
        #sets title to be the h1 of the html page
    except AttributeError as e:
        return None
        #checks if there actually is a h1 tag
    return title

title = getTitle("http://www.pythonscraping.com/pages/page1.html")
#The website being scraped (looked at)

if title == None:
    print("Title could not befound")
else:
    print(title)
    #prints title
