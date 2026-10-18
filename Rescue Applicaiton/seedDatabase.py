from database import Database
from starter_animals import starter_animals
from pymongo.errors import PyMongoError


def main():
    database = None
    try:
        database = Database()
        added = database.seedAnimals(StarterAnimals())
        print(f'Added {added} starter animals to {database.db.name}.animals.')
        for animal in database.load_animals():
            print(f'{animal.name} | {animal.animalType} | {animal.trainingStatus} | reserved={animal.reserved}')
    except PyMongoError:
        print('Could not complete database setup. Check MongoDB is running and MONGODB_URI is correct.')
        raise SystemExit(1)
    finally:
        if database is not None:
            database.close()


if __name__ == '__main__':
    main()
