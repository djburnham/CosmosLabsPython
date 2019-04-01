import azure.cosmos as cosmos
import azure.cosmos.cosmos_client as cosmos_client
import json

class Student:
    def __init__(self, firstName = None, lastName = None, clubs = None):
        self.firstName = firstName
        self.lastName = lastName
        self.clubs = clubs

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
  
    queryStr = """SELECT s.firstName, s.lastName, s.clubs FROM students s 
                   WHERE s.enrollmentYear = 2018"""

    resultSet = client.QueryItems(collection_link, queryStr)
    
    studentList = []
    for res in resultSet:
        newStudent = Student(res['firstName'], res['lastName'], res['clubs'])
        studentList.append(newStudent)
        print(newStudent.firstName, newStudent.lastName + ' activities = ', end = '')
        for act in newStudent.clubs:
            print(act + ", ", end = '')
        print()

    print("done")
