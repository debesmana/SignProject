from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = MongoClient()
db = client.test_database
collection = db.text
hamletFile = open("hamlet.txt",'r')
#print hamletFile.read()
book = {}
book["title"] = "Hamlet"
book["text"] = hamletFile

collection.update(book,upsert=True)
