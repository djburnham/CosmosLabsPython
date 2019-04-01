import pydocumentdb
import pydocumentdb.document_client as document_client
import random

def randcar():
    makes = ['Ford', 'Volvo', 'Austin', 'Triumph', 'Saab', 'Rolls-Royce']
    colours = ['red', 'blue', 'silver', 'brown', 'yellow', 'green', 'black', 'white']
    make = makes[ random.randint(1, len(makes)-1 )]
    colour = colours[ random.randint(1, len(colours)-1 )]
    cardict = { 'id' : make, 'Colour' : colour}
    return cardict



endpoint = 'https://ordsurveytest.documents.azure.com:443/'
key = 'ttpzHyHIqAO0mSzgCZxfCTnF16qK7adCqoxGvcECzGxge2GYqlSlkeOWhn3w7MmFsyfWpjhe0qiAkmBN4Yop3g=='

client = document_client.DocumentClient(endpoint, {'masterKey': key })
databaseID = 'collectiontest'
collectionID = 'baz'

db_query = "select * from r where r.id = '{0}'".format(databaseID)
db = list(client.QueryDatabases(db_query))[0]
db_link = db['_self']

coll_query = "select * from r where r.id = '{0}'".format(collectionID)
coll = list(client.QueryCollections(db_link, coll_query))[0]
coll_link = coll['_self']


for z in range(1000, 100000):
    rc = randcar()
    rc['id'] = rc['id'] + str(z)
    client.CreateDocument(coll_link, rc )
    if z%1000 == 0:
        print('.', end='', flush=True)

print("Done!")
