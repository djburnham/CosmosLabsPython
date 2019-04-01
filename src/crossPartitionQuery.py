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

    databaseID = "UniversityDatabase";
    collectionID = "StudentCollection"
    database_link = 'dbs/' + databaseID
    collection_link = database_link + '/colls/' + collectionID

    queryStr = """ SELECT s.firstName, s.lastName, s.enrollmentYear,
                   s.projectedGraduationYear
                   FROM students s
                   WHERE s.projectedGraduationYear < 2020
                   """

    options = {'maxItemCount': 10, 'continuation': True, 
                'enableCrossPartitionQuery': True }
    resultSet = client.QueryItems(collection_link, queryStr, options)
    
    while True:
        result_block = resultSet.fetch_next_block()
        if result_block:
            for res in result_block:
                print(res)

            print("=======Page-Break========")
        else:
             break