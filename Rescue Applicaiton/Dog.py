from RescueAnimal import rescueAnimal

class dog(rescueAnimal):
    def __init__(self, name, breed, gender, age, weight, acquisitionDate,
                 acquisitionCountry, trainingStatus, reserved,
                 inserviceCountry):
        super().__init__(name, "dog", gender, age, weight, acquisitionDate,
                 acquisitionCountry, trainingStatus, reserved,
                 inserviceCountry)
        self.breed = breed