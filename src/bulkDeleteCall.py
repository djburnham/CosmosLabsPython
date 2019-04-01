import azure.cosmos as cosmos
import azure.cosmos.cosmos_client as cosmos_client
import json

if __name__ == "__main__":

    # get the access key and endpoint and set up the client
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # create a client and set up the database and collection links 
    client = cosmos_client.CosmosClient(config['endPoint'], 
                                {'masterKey':    config['key']})

    databaseID = "FinancialDatabase";
    collectionID = "InvestorCollection"
    storedProcID = "bulkDelete"
    database_link = 'dbs/' + databaseID
    collection_link = database_link + '/colls/' + collectionID
    storedProc_link = collection_link + '/sprocs/' + storedProcID

    docsDeleted = {'continuation' : True, 'deleted' : 0 }

    options = { "partitionKey": "contosofinancial"}
    queryStr = "SELECT * FROM investors i WHERE i.company = 'contosofinancial'"
    while docsDeleted['continuation']:
        docsDeleted = client.ExecuteStoredProcedure(storedProc_link, queryStr , options)
        print("Number of documents deleted = {}".format(docsDeleted['deleted']) )
        
    print("done!")