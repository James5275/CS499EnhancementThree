#James Ehrle

from database import Database
from getpass import getpass
import os
from starterAnimals import StarterAnimals
from pymongo.errors import PyMongoError
from pathlib import Path
from dotenv import load_dotenv


from Dog import dog
from Monkey import monkey

#loading the .env file that holds the username and password
envPath = Path(__file__).resolve().parent / ".env"
load_dotenv(envPath)

#creating a driver class
class driver:

    #setting up for the monkey species that are allowed
    monkeySpecies = ["capuchin", "guenon", "macaque", "marmoset", "tamarin", "squirrel monkey"]

    #setting up inital state of the lists and initializing them
    def __init__(self):
        
        # Setting up the animalList that will house all of the animals
        self.database = Database()

        # Seed only when the animals collection is empty
        if self.database.animals.count_documents({}) == 0:
            self.database.seedAnimals(StarterAnimals())

        self.animalList = []

    def displayMenu(self):
                print("\n\n")
                print("\t\t\t\tRescue Animal System Menu")
                print("[1] Intake a new dog")
                print("[2] Intake a new monkey")
                print("[3] Reserve an animal")
                print("[4] Print a list of all dogs")
                print("[5] Print a list of all monkeys")
                print("[6] Print a list of all animals that are not reserved")
                print("[q] Quit application")
                print()

    def getUserChoice(self):
            #defining all of the valid options
            options = ['1', '2', '3', '4', '5', '6', 'q']

            while True: 

                self.displayMenu()

                #Getting input and making it lowercase and stripped of whitespace
                choice = input("Enter a menu selection: ").strip().lower()

                if choice in options:
                    return choice
                else: 
                    print("Invalid Choice. Enter valid option")

    def intakeNewDog(self):
        name = input("What is the dog's name?").strip().lower()
        #changing to searching the animalList by animalType
        for animal in self.animalList: 
            if animal.animalType == 'dog' and animal.name.strip().lower() == name:
                print("\nthis dog is already in our system\n")
                updateStatus = input("Would you like to update the training status? (yes or no): ").strip().lower()
                
                if updateStatus == "yes":
                    status = input("What is the new training status?: ").strip().lower()
                    self.database.updateTrainingStatus(animal, status)
                    print(f"{animal.name} status has been updated to {status}")
                return

        breed = input("What is " + name + "'s breed? \n").strip().lower()
        gender = input("What is " + name + "'s gender? \n").strip().lower()
        age = input("What is " + name + "'s age? \n").strip().lower()
        weight = input("What is " + name + "'s weight \n").strip().lower()
        acquisitionDate = input("What is " + name + "'s acquisition date? \n").strip().lower()
        acquisitionCountry = input("What is " + name + "'s acquisition country \n").strip().lower()
        trainingStatus = input("What is " + name + "'s training status \n").strip().lower()
    
        while True:
            booleanInput = input("Is " + name + " reserved? (true or false) \n").strip().lower()
            if booleanInput == "true":
                reserved = True
                break
            elif booleanInput == "false":
                reserved = False
                break
            else:
                print("please enter true or false for resered status \n")  
                
        inServiceCountry = input("What is " + name + "'s in service country \n")

        # Create the dog object
        newAnimal = dog(name,breed,gender,age,weight,acquisitionDate,acquisitionCountry,
            trainingStatus,reserved,inServiceCountry,)

        # Save the dog to MongoDB
        self.database.addAnimal(newAnimal)

        # Add the saved dog to the current program's list
        self.animalList.append(newAnimal)

        print(f"Thank you for adding {name}.")

    def intakeNewMonkey(self):
        self.animalList = self.database.loadAnimals()
        name = input("What is the Monkey's name? \n").strip().lower()

        #changing to searching the animalList by animalType
        for animal in self.animalList:
            if animal.animalType == 'monkey' and animal.name.strip().lower() == name:
                print("\nthis monkey is already in our system\n")
                updateStatus = input("Would you like to update the training status? (yes or no): ").strip().lower()
                
                if updateStatus == "yes":
                    status = input("What is the new training status?: ").strip().lower()
                    self.database.updateTrainingStatus(animal, status)
                    print(f"{animal.name} status has been updated to {status}")
                return

        while True:
            species = input("What is " + name + "'s" + " species \n").strip().lower()
            if species in self.monkeySpecies:
                break
            else:
                print("please enter correct Species \n")

        tailLength = input("What is " + name + "'s" + " tail Length \n").strip().lower()
        height = input("What is " + name + "'s" + " height \n").strip().lower()
        bodyLength = input("What is " + name + "'s" + " body length \n").strip().lower()
        gender = input("What is " + name + "'s gender? \n").strip().lower()
        age = input("What is " + name + "'s age? \n").strip().lower()
        weight = input("What is " + name + "'s weight \n").strip().lower()
        acquisitionDate = input("What is " + name + "'s acquisition date? \n").strip().lower()
        acquisitionCountry = input("What is " + name + "'s acquisition country \n").strip().lower()
        trainingStatus = input("What is " + name + "'s training status \n").strip().lower()
    
        while True:
            booleanInput = input("Is " + name + " reserved? (true or false) \n").strip().lower()
            if booleanInput == "true":
                reserved = True
                break
            elif booleanInput == "false":
                reserved = False
                break
            else:
                print("please enter true or false for resered status \n")  
                
        inServiceCountry = input("What is " + name + "'s in service country \n")

        newAnimal = monkey(name,species,tailLength,height,bodyLength,gender,
            age,weight,acquisitionDate,acquisitionCountry,trainingStatus,
            reserved,inServiceCountry,
        )

        # Save to MongoDB first
        self.database.addAnimal(newAnimal)

        # Add the saved monkey to the current list
        self.animalList.append(newAnimal)

        print(f"Thank you for adding {name}.")

    def reserveAnimal(self):

        while True:
            animalType = input("What animal type would you like to reserve? \n").strip().lower()

            if animalType == "dog":
                country = input("\nwhat is the service country? \n").strip().lower()
                foundAnimal = False
                for animal in self.animalList:
                    if (animal.animalType == animalType and animal.inServiceCountry.strip().lower() == country and
                        not animal.reserved and animal.trainingStatus.strip().lower() == "in service"):
                        
                        foundAnimal = True
                        print(f"\n{animal.name} is availiable. \n")
                        
                        while True:
                            newReserved = input("Would you like to reserve this dog? (yes or no) \n").strip().lower()
                            if newReserved == 'yes':
                                if self.database.reserveAnimal(animal):
                                    print(f"You have reserved {animal.name}.")
                                else:
                                    print("Unable to reserve this animal. Please try again.")
                                return
                            elif newReserved == 'no':
                                print("Okay, Ill take you back to the main menu")
                                return
                            else:
                                print("please enter yes or no")
                if not foundAnimal:
                    print("no dogs matching that discription")   

                break


            elif animalType == "monkey":
                country = input("\nwhat is the service country? \n").strip().lower()
                for animal in self.animalList:
                    if (animal.animalType == animalType and animal.inServiceCountry.strip().lower() == country and
                        not animal.reserved and animal.trainingStatus.strip().lower() == "in service"):

                        foundAnimal = True
                        print(f"\n{animal.name} is availiable. \n")
                        
                        while True:
                            newReserved = input("Would you like to reserve this monkey? (yes or no) \n").strip().lower()
                            if newReserved == 'yes':
                                if self.database.reserveAnimal(animal):
                                    print(f"You have reserved {animal.name}.")
                                else:
                                    print("Unable to reserve this animal. Please try again.")
                                return
                            elif newReserved == 'no':
                                print("Okay, Ill take you back to the main menu")
                                return
                            else:
                                print("please enter yes or no")
                if not foundAnimal:
                    print("no monkey matching that discription")   

                break

    def printAnimal(self, userChoice):

        if userChoice == '4':
            print("\nList of all dogs:")
            for animal in self.animalList:
                if animal.animalType == "dog":
                    print(f"{animal.name} - Training Status: {animal.trainingStatus}, "
                    f"Acquisition Country: {animal.acquisitionCountry}, "
                    f"In service location: {animal.inServiceCountry}, "
                    f"reserved: {str(animal.reserved).lower()} \n")

        elif userChoice == '5':
            print("\nList of all monkeys:")
            for animal in self.animalList:
                if animal.animalType == 'monkey':
                    print(f"{animal.name} - Training Status: {animal.trainingStatus}, "
                    f"Acquisition Country: {animal.acquisitionCountry}, "
                    f"In service location: {animal.inServiceCountry}, "
                    f"reserved: {str(animal.reserved).lower()} \n")
                    
        elif userChoice == '6':
            print("\nList of all animials avaliable:")
            print("Monkey:")
            for animal in self.animalList:
                if animal.animalType == 'monkey':
                    if not animal.reserved:
                        print(animal.name)
            print("\nDog: ")
            for animal in self.animalList:
                if animal.animalType == 'dog':
                    if not animal.reserved:
                        print(animal.name)

    def login(self):
        print("+++++LOGIN++++++")

        #this will allow user 3 attempts to logging in 
        for trys in range(3):
            username = input('Username: ').strip()
            user_password = input('Password: ')

            if (username == os.getenv("UserName") and user_password == os.getenv("PassWord")):
                print ('Login successful!')
                return True

            remaining = 2 - trys

            print(f"Incorrect Usernname or Password." 
            f"You have {remaining} trys left")
        
        print("Too many failed logins, Good Bye.")
        return False

    def main(self):
            
            self.animalList = self.database.loadAnimals()
            # while loop to display menu/getting user input 
            while True: 
                #getting user input
                userChoice = self.getUserChoice()

                if userChoice == '1': #Adding a New Dog
                    self.intakeNewDog()

                elif userChoice == '2': #Adding a New Monkey 
                    self.intakeNewMonkey()

                elif userChoice == '3': #Reserving an Animal
                    self.reserveAnimal()

                elif userChoice in ('4', '5', '6'): #Printing list of all dogs
                    self.printAnimal(userChoice)

                elif userChoice == 'q': #quiting the menu/program
                    print("goodbye!")
                    break 
            

if __name__ == "__main__":

    #if login comes back true it will go to main otherwise 
    #terminate the program
    if driver().login():
        driver().main()


