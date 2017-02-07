from pymongo import Connection
from pymongo.errors import ConnectionFailure

def main():
    """Connect to MongoDB"""
    try:
        c= Connection(host= "localhost", port= 27017)
    except ConnectionFailure, e:
        sys.stderr.write("Could not connect to MOngoDB: %s" %e)
        sys.exit(1)
    #get the database handle
    dbh= c["Dainas"]
    #checking if succesfully connected
    assert dbh.connection == c
    print "Successfully set up a db handle"

if __name__ == "__main__":
    main()

