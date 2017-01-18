from urllib2 import urlopen
from bs4 import BeautifulSoup
#importing the libraries that will be used
#Beautiful soup can be found here : https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

html = urlopen("http://www.pythonscraping.com/pages/page1.html")
#The website being scraped (looked at)
bsObj = BeautifulSoup(html.read())
#turns the html into a bs object (makes it easier to read)
print(bsObj.html.body.h1)
#fetches the html object called (in this case h1)
