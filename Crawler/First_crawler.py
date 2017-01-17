def setAllURLs(self):
    pass

def getURL(self):
    with open("URL_list.txt", "w") as urls:
        currentURL= urls.readline()
    urls.close()
    return currentURL
    #returns URL to look in

def parseHTML(self, URL):
    pass
    #goes through URLs looks for html elements
    #returns JSON objects to test file

current = getURL()
parseHTML(current)
tester = open("Test.txt", "w")

for i in :
    tester.write(str(i) + "\n")

tester.close()
