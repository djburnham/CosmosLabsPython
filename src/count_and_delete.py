import azure.cosmos.cosmos_client as document_client
import json
import time

def main():
    with open('config_ordsurvey.json', 'r') as f:
        config = json.load(f)

    client = document_client.CosmosClient(config['endPoint'], {'masterKey': config['key']})
    databaseID = 'collectiontest'
    collectionID = 'sparkoverload'


    db_query = "select * from r where r.id = '{0}'".format(databaseID)
    db = list(client.QueryDatabases(db_query))[0]
    db_link = db['_self']

    coll_query = "select * from r where r.id = '{0}'".format(collectionID)
    coll = list(client.QueryContainers(db_link, coll_query))[0]
    coll_link = coll['_self']

    options = {} 
    options['enableCrossPartitionQuery'] = True
    options['maxItemCount'] = 20
    query = { 'query': 'SELECT VALUE COUNT(1) FROM server s' }  
    start_time = time.time()  
    docs = client.QueryItems(coll_link, query, options)
    docsInCollection = list(docs)[0]
    callTimeStr = "{0:.3f}".format( time.time() - start_time)
    print("There are {0} documents, count(1) call took {1} seconds.".format(docsInCollection, callTimeStr) )

    resp = input("Do you want to clear the collection ? (yes/N) ")
    if resp != 'yes':
        return

    # We are assuming that the collection is partitioned by /id
    query = { 'query': 'SELECT * FROM C ' }
    docs = client.QueryItems(coll_link, query, options)
    myDocs = list(docs)
    
    delcnt = 0
    for myDoc in myDocs:
        options['partitionKey'] = myDoc["id"]
        deletedDoc = client.DeleteItem( myDoc["_self"], options=options)
        delcnt += 1

    print('ends.. collection cleared, {0} documents deleted'.format(delcnt) )

if __name__ == '__main__':
    main()
