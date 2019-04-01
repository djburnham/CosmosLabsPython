import azure.cosmos as cosmos
import azure.cosmos.cosmos_client as cosmos_client
import json
from faker import Faker

if __name__ == "__main__":

    # get the access key and endpoint and set up the client
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # create a client and set up the database and collection links 
    client = cosmos_client.CosmosClient(config['endPoint'], 
                                {'masterKey':    config['key']})

    createdDocs = 10000
    databaseID = "FinancialDatabase";
    collectionID = "InvestorCollection"
    storedProcID = "bulkUpload"
    database_link = 'dbs/' + databaseID
    collection_link = database_link + '/colls/' + collectionID
    storedProc_link = collection_link + '/sprocs/' + storedProcID
    options = { "partitionKey": "contosofinancial" }

    # create some random documents with the faker module
    myFactory = Faker()
    newDocArr = []
    for cnt in range(createdDocs):
        newDoc = { "firstName": myFactory.first_name() ,
                   "lastName" : myFactory.last_name() ,
                   "company"  : "contosofinancial" 
                   }
        newDocArr.append(newDoc)

    while len(newDocArr) > 0:
        # render the json array of docs as a string we can't pass an array
        # to the stored procedure
        ndaStr = json.dumps(newDocArr)
        nDocsCreated = client.ExecuteStoredProcedure(storedProc_link, ndaStr , options)
        print("Just inserted {} documents".format(nDocsCreated))
        newDocArr = newDocArr[nDocsCreated :]
    
    print("done!")



