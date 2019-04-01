import azure.cosmos as cosmos
import azure.cosmos.cosmos_client as cosmos_client
import json
import random

def randListElem(inList):
    """ Return a random element from a list supplied as a parameter """
    retVal = inList[random.randint(0, len(inList)-1 )]
    return(retVal)

def watchLiveTelevisionChannel():
    """ Return a random watchLiveTV document as a dictionary """
    channelNames = ['BBC1', 'BBC2', 'ITV1', 'Channel 4', 'BBC News', 'Sky Sports 1',
                     'Sky Sports 2']
    minutesViewed = random.randint(1, 121)
    channelName = randListElem(channelNames)
    intType = 'Watch live TV'
    wltvc = {   "channelName" : channelName,
                "minutesViewed" : minutesViewed,
                "type" : intType}
    return wltvc

def purchaseFoodBeverage():
    """ Return a random food or beverage purchase as a dictionary """
    foodItems = ['hotdog', 'veggie meat pie', 'crisps', 'meat and potato pie', 'peanuts'
                ]
    drinkItems = ['tea', 'Bovril', 'Hot Chocolate', 'Fanta', 'Diet Coke', 'Pepsi',
                'Coffee', 'bottled water']
    fbTypes = ['food', 'beverage']
    fbPrices = {"hotdog" : 0.45, "veggie meat pie" : 0.55, "crisps" : 0.25,
                "meat and potato pie" : 0.5, "peanuts" : 0.21 , "tea" : 0.10, 
                "Bovril" : 0.15, "Hot Chocolate" : 0.15, "Fanta" : 0.2,
                "Diet Coke" : 0.2, "Pepsi" : 0.2, "Coffee" : 0.12, 
                "bottled water" : 0.18 }
    
    fbType = randListElem(fbTypes)
    if fbType == 'food':
        fbItem = randListElem(foodItems)
        fbUnitPrice = fbPrices[fbItem]
        fbQuantity = random.randint(1, 12)
        
    elif fbType == 'beverage':
        fbItem = randListElem(drinkItems)
        fbUnitPrice = fbPrices[fbItem]
        fbQuantity = random.randint(1, 12)

    fbTotalPrice = fbQuantity * fbUnitPrice
    return(
            {"type" : fbType,
             "item" : fbItem,
             "unitPrice" : fbUnitPrice,
             "quantity" : fbQuantity,
             "totalPrice" : fbTotalPrice }
    )

def viewMap():
    """ Return a random map viewing event as a dict""" 
    return(
        {"type" : "viewMap",
         "minutesViewed" : random.randint(1, 25) }
    )
if __name__ == "__main__":

    # get the access key and endpoint and set up the client
    with open('config.json', 'r') as f:
        config = json.load(f)
    client = cosmos_client.CosmosClient(config['endPoint'], 
                                {'masterKey':    config['key']})

    databaseID = 'EntertainmentDatabase'
    collectionID = 'CustomCollection'
    database_link = 'dbs/' + databaseID
    collection_link = database_link + '/colls/' + collectionID
    NofDocsToCreate = 1000
   
    for cnt in range(NofDocsToCreate +1):
        # Create a random entertainment event instance and persist it to Cosmos
        entTypes = ["viewMap", "beverage", "food", "Watch live TV"]
        entInstType = randListElem(entTypes)
        if entInstType == "viewMap":
            entInst = viewMap()
        elif entInstType == "food" or entInstType == "beverage":
            entInst = purchaseFoodBeverage()
        else:
            entInst = watchLiveTelevisionChannel()

        client.CreateItem(collection_link, entInst)
        print('.', end = '')
        
    print("\nWritten {0} items into {1} collection".format(cnt, collectionID))