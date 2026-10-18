#this is the list of animals that were in the list so they will fill the database
#to start then changes can be made on the local database
from Dog import dog
from Monkey import monkey


def StarterAnimals():
    return [
            dog("spot", "German Shepherd", "male", "1", "25.6", "05-12-2019",
                "United States", "in service", False, "England"),
            dog("rex", "Great Dane", "male", "3", "35.2", "02-03-2020",
                "United States", "in service", False, "United States"),
            dog("bella", "Chihuahua", "female", "4", "25.6", "12-12-2019",
                "Canada", "in service", True, "Canada"),
                

            monkey("Bobo", "Capuchin", "22", "30", "35", "male", "4", "55",
                    "07-27-2019", "United States", "in service", False, "england"),
            monkey("George", "Macaque", "20", "26", "32", "male", "1", "54",
                    "04-27-2020", "United States", "in service", False, "United States"),
            monkey("Stella", "Marmoset", "24", "28", "36", "female", "2", "45",
                    "07-19-2021", "Canada", "In service", True, "Canada"),
    ]
