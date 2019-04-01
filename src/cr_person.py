import azure.cosmos as cosmos
import azure.cosmos.cosmos_client as cosmos_client
import json
from faker import Faker

def create_person():
    myfactory = Faker('en_GB')
    firstName = myfactory.first_name()
    lastName = myfactory.last_name()
    fullName = firstName + " " + lastName
    address = myfactory.address()
    phoneNumber = myfactory.phone_number()
    email = myfactory.email()
    job = myfactory.job()
    company = myfactory.company() + " " + myfactory.company_suffix()
    geo = myfactory.local_latlng(country_code="US", coords_only=False)
    return {
        'FirstName': firstName,
        'LastName':  lastName,
        'FullName': fullName,
        'Address': address,
        'PhoneNumber': phoneNumber,
        "EmailAddress" : email,
        "Profession" : job,
        "Company" : company,
        "CompanyAddress" : myfactory.address(),
        "HQLocation" : geo
    }

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

    personDoc = create_person()

    personResp = client.CreateItem(collection_link, personDoc)

    # Get the resource cost from response headers
    responseHeaders = client.last_response_headers  
    resourceUsage = responseHeaders['x-ms-request-charge']

    if personResp:
        print("Document created - Resource cost was {} RU's".format(resourceUsage))
    else:
        print("No document created")