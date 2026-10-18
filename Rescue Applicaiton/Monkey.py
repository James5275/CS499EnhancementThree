from RescueAnimal import rescueAnimal

class monkey(rescueAnimal):
    def __init__(self, name, species, tailLength, height, bodyLength, gender,
                    age, weight, acquisitionDate, acquisitionCountry, trainingStatus,
                    reserved, inServiceCountry):
        super().__init__(name, "monkey", gender, age, weight,
                    acquisitionDate, acquisitionCountry, trainingStatus, 
                    reserved, inServiceCountry)
        self.species = species
        self.tailLength = tailLength
        self.height = height
        self.bodyLength = bodyLength