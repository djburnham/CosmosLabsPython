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
    collectionID = "PeopleCollection"
    database_link = 'dbs/' + databaseID
    collection_link = database_link + '/colls/' + collectionID

    document_id = "example.document"
    document_link = collection_link + '/docs/' + document_id 

    doc = { "id": "example.document",
            "FirstName": "Example",
            "LastName": "Personage"}

    read_response = client.UpsertItem(collection_link, doc)
    if read_response:
        print("example.doc loaded ok"   )
    
    print("done !")