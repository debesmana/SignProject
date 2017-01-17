import scrappy #scrappy is a library that helps write web crawlers

class poemSpider(scrappy.Spider):
    name = "poem" #identifies the crawler (This must be unique in the project)

    def requests(self):
        #where the crawler will look. At the moment only in one page
        urls = [
        'http://www.dainuskapis.lv/katalogs/1.-Par-dziesmam-un-dziedasanu'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            #what page is being read by crawler

    def parse(self,response):
        

tester = open("Test.txt", "w")

for i in :
    tester.write(str(i) + "\n")

tester.close()
