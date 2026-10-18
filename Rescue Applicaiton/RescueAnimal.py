from datetime import date

class rescueAnimal:
    #initializing constructor for the core attributes for the animals
    def __init__ (self, name, animalType, gender, age, weight,
                    acquisitionDate, acquisitionCountry, trainingStatus, 
                    reserved, inServiceCountry):
        self.name = name
        self.animalType = animalType
        self.gender = gender
        self.age = age
        self.weight = weight
        self.acquisitionDate = acquisitionDate
        self.acquisitionCountry = acquisitionCountry
        self.trainingStatus = trainingStatus
        self.reserved = reserved
        self.inServiceCountry = inServiceCountry

