import azure.cosmos as cosmos
import azure.cosmos.cosmos_client as cosmos_client
import json
with open('config.json', 'r') as f:
    config = json.load(f)
client = cosmos_client.CosmosClient(config['endPoint'], 
                            {'masterKey':    config['key']})

databaseID = 'EntertainmentDatabase'
try:
    db = client.CreateDatabase({ 'id': databaseID} )
except Exception as ex:
    if type(ex) == cosmos.errors.HTTPFailure and ex.status_code == 409:
        # database already exists
        db = client.ReadDatabase('dbs/' + databaseID )
    else:
        print("we had a problem")
        raise ex

print('Database self link is: {}'.format(db['_self']))

print('ends..')