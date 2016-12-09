from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import re

client = MongoClient()
db = client.test_database
collection = db.text
hamletFile = open("hamlet.txt",'r')
#print hamletFile.read()
#create new book and insert it
book = {}
book["title"] = "Hamlet"
book["text"] = hamletFile

try:
    collection.insert(book)
except:
    print("Document already exists")

#create new collection
collection = db.words
text = hamletFile.read().lower()
hamletFile.close()
# replaces anything that is not a lowercase letter, a space, or an apostrophe with a space:
text = re.sub('[^a-z\ \']+', " ", text)
words = list(text.split())
for i in range(0, len(words))
    word ={}
    word["word"] = words

    try:
        collection.insert(word)
    except:
        print("word already inserted")
