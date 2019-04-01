import azure.cosmos as cosmos
import azure.cosmos.cosmos_client as cosmos_client
import json
 
with open('config.json', 'r') as f:
    config = json.load(f)
 
client = cosmos_client.CosmosClient(config['endPoint'],{'masterKey': config['key']})
databaseID =   'FinancialDatabase'
collectionID = 'PeopleCollection'
 
try:
    db = client.CreateDatabase({ 'id': databaseID} )
except Exception as ex:
    if type(ex) == cosmos.errors.HTTPFailure and ex.status_code == 409:
        # database already exists
        db = client.ReadDatabase('dbs/' + databaseID )
    else:
        print("we had a problem creating database")
        raise ex
 
print('Database self link is: {}'.format(db['_self']))
 
options = {
                'offerEnableRUPerMinuteThroughput': True,
                'offerVersion': "V2",
                'offerThroughput': 1000
}
 
try:
    collection = client.CreateContainer(db['_self'], { 'id': collectionID }, options)
except Exception as ex:
    if type(ex) == cosmos.errors.HTTPFailure and ex.status_code == 409:
        # collection already exists
        collection = client.ReadContainer('dbs/' + databaseID + '/colls/' + collectionID ) 
    else:
        print("we had a problem creating collection")
        raise ex
 
print('Collection self link for {} is: {}'.format(collectionID, collection['_self']))

