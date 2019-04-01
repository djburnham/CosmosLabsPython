import azure.cosmos as cosmos
import azure.cosmos.cosmos_client as cosmos_client
import json
import random
from faker import Faker

DOCS_TO_CREATE = 10000

def create_tx():
    """Return a fake tx object - create factory myfactory outside call"""
    firstName = myfactory.first_name()
    lastName = myfactory.last_name()
    paidBy = firstName.lower() + lastName.lower()
    processed = myfactory.boolean(chance_of_getting_true=80)
    amount = myfactory.pydecimal(left_digits=4, right_digits=2, positive=True)
    costCentres = ['toys','computers', 'jewelery','automotive','outdoors','sports',
                    'garden', 'books', 'tools', 'grocery', 'industrial']
    costCenter = costCentres[random.randint(0,10)]

    return {
        'amount': float(amount), 
        'paidBy': paidBy,
        'processed':  processed,
        'costCenter': costCenter
    }

if __name__ == "__main__":
    myfactory = Faker('en_GB')
    txList = []

    print("Creating a list of 10,000 documents")
    for cnt in range(DOCS_TO_CREATE):
        txList.append(create_tx())
        if cnt%100 == 0 :
            print('.', end="")
    print('\nCreated a list of 10,000 documents.')

    # get the access key and endpoint and set up the client
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # create a client and set up the database and collection links 
    client = cosmos_client.CosmosClient(config['endPoint'], 
                                {'masterKey':    config['key']})

    databaseID = "FinancialDatabase";
    collectionID = "TransactionCollection"
    database_link = 'dbs/' + databaseID
    collection_link = database_link + '/colls/' + collectionID

    for cnt in range(DOCS_TO_CREATE):
        TxResp = client.CreateItem(collection_link, txList[cnt])
        if cnt%100 == 0 :
            print('.', end="")

    print('\nCreated 10,000 documents in the TransactionCollection')
