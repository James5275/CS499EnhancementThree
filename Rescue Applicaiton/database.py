#Database to store and retrieve animals using MongoDB
import os
from pymongo import MongoClient

#imports from the differnt classes
from Dog import dog
from Monkey import monkey


class Database:
    def __init__(self):
        #Creates MondoDB client and allows 5 seconds to locate avaliable server
        self.client = MongoClient(
            os.getenv('MONGODB_URI', 'mongodb://localhost:27017'),
            serverSelectionTimeoutMS=5000,
        )

        try:
            # Verify that the MongoDb server is reachable
            self.client.admin.command('ping')

            # Select the correct Database
            self.db = self.client[os.getenv('MONGODB_DATABASE', 'rescue_animal_db')]
            
            #keeping one collection to store both animals
            self.animals = self.db['animals']

            # prevents duplicates within the same animal type
            self.animals.create_index([('animalType', 1), ('nameKey', 1)], unique=True)

        except Exception:
            #closes connection if database cant be setup
            self.client.close()
            raise
    

    #converts animal object into a dictionary for MongoDB
    def toDocument(self, animal):
        document = vars(animal).copy()
        document.pop('_id', None)
        document['nameKey'] = animal.name.strip().lower()
        return document

    #converts it back from MongoDB to the object to be used
    def fromDocument(self, document):
        common = [document[field] for field in (
            'gender', 'age', 'weight', 'acquisitionDate', 'acquisitionCountry',
            'trainingStatus', 'reserved', 'inServiceCountry')]
        if document['animalType'] == 'dog':
            animal = dog(document['name'], document['breed'], *common)
        elif document['animalType'] == 'monkey':
            animal = monkey(document['name'], document['species'],
                            document['tailLength'], document['height'],
                            document['bodyLength'], *common)
        else:
            raise ValueError('Unknown animalType in database')
        animal._id = document['_id']
        return animal

    def loadAnimals(self):
        #returns saved animals as objects
        return [self.fromDocument(doc) for doc in self.animals.find().sort('nameKey', 1)]

    def addAnimal(self, animal):
        #adds new animal to the database
        result = self.animals.insert_one(self.toDocument(animal))
        animal._id = result.inserted_id

    def seedAnimals(self, animals):
        #insters the starter anmimals without overriding the saved changes
        added = 0
        for animal in animals:
            document = self.toDocument(animal)
            result = self.animals.update_one({'animalType': document['animalType'], 'nameKey': document['nameKey']},
                {'$setOnInsert': document}, upsert=True,)
            added += result.upserted_id is not None
        return added

    def updateTrainingStatus(self, animal, status):
        result = self.animals.update_one({"_id": animal._id}, {"$set": {"trainingStatus": status}})
        #locating the current record using the MongoDB ID
        if result.matched_count != 1:
            raise ValueError("Animal not found in the database.")

        animal.trainingStatus = status

    def reserveAnimal(self, animal):
        result = self.animals.update_one({"_id": animal._id,"reserved": False,
                "trainingStatus": animal.trainingStatus,},{"$set": {"reserved": True}},)

        if result.modified_count == 1:
            animal.reserved = True
            return True

        return False

    def close(self):
        self.client.close()
