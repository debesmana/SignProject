# -*- coding: utf-8 -*-
# utf-8 is a type of language encoding which covers the unicode character set. Latvian uses latin-extended a (if encoded correctly)
import pymongo #connecting to MongoDB
import getpass #mask raw_input for the password prompt
import os #allows access to files
import random

smallImage = []
mediumImage = []
largeImage = []
largeWords = [u"saule", u"tēvs", u"zeme", u"debesis", u"šodien", u"māte", u"diena", u"kungi", u"vainags", u"Jāņi", u"pērkons", u"lauks", u"brālis", u"māsa", u"diena", u"svešumā", u"druva", u"nakts", u"kumeļš", u"zirgs"] #words which the large signs are associated with

#local stuff for testing
USE_LOCAL = False
#mongodb authentication
if (not USE_LOCAL):
    user = raw_input("[?] Mongodb username: ")
    passw = getpass.getpass("[?] Mongodb password: ")

# Connection to Mongo DB
try:
    #setting up link to mongoDB
    if (USE_LOCAL):
        conn = pymongo.MongoClient('localhost', 27017)
    else:
        connURI = 'mongodb://%s:%s@mongoserver.almaulmane.com:27067/' % (user, passw)
        conn = pymongo.MongoClient(connURI)
    print "Connected to mongodb"
except pymongo.errors.ConnectionFailure, e:
    print "[!] Could not connect to MongoDB: %s" % e

#if a database (or collection) with a certain name isn't found mongo creates a new one when the first document is inserted
# Define mongoDB database
db = conn.poems

def get_images():
    for files in os.listdir("/Users/Alma/Documents/Processing/SignProject/Write to Mongo/Images/Images/Small"):
        smallImage.append(files)

    
    for files in os.listdir("/Users/Alma/Documents/Processing/SignProject/Write to Mongo/Images/Images/Medium"):
        mediumImage.append(files)

    
    for files in os.listdir("/Users/Alma/Documents/Processing/SignProject/Write to Mongo/Images/Images/Large"):
        largeImage.append(files)

def assign_image():
    #gets all words in db
    cursor = db.words.find({})
    #loops through all words in entry
    for document in cursor:
        #gets the word as string
        entry = document.get("word")
        #gets the tally
        size = document.get("tally")
        #if the word is a large word set size to large and image to the corresponding image number
        if entry in largeWords:
            db.words.update({"word": entry}, 
            {"$set": {"size": "large"}}, upsert = True)
            wordIndex = largeWords.index(entry)
            image = largeImage[wordIndex] 
            db.words.update({"word": entry},
            {"$set": {"image": str(image)}}, upsert = True)
            db.words.find()
        #else if the word is smaller or equal than 3 letters set size to small and image to random small image
        elif len(entry) <= 3:
            db.words.update({"word": entry}, 
            {"$set": {"size": "small"}}, upsert = True)
            image = random.choice(smallImage)
            db.words.update({"word": entry},
            {"$set": {"image": str(image)}}, upsert = True)
            db.words.find()
        #else if the word only appears once in db set size to small and image to random small image
        elif size == 1:
            db.words.update({"word": entry}, 
            {"$set": {"size": "small"}}, upsert = True)
            image = random.choice(smallImage)
            db.words.update({"word": entry},
            {"$set": {"image": str(image)}}, upsert = True)
            db.words.find()
        #if none of the above is true then set the size to medium and assign a random medium image
        else:
            db.words.update({"word": entry}, 
            {"$set": {"size": "medium"}}, upsert = True)
            image = random.choice(mediumImage)
            db.words.update({"word": entry},
            {"$set": {"image": str(image)}}, upsert = True)
            db.words.find()

get_images()
assign_image()

#closes the mongo connection
conn.close()
