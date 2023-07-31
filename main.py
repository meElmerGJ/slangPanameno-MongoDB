
import pymongo

database_name = 'slangPanameno'

client = pymongo.MongoClient('mongodb://localhost:27017')

db = client[database_name]

slangs = db['slangs']

if __name__ == '__main__':
    # Elmer es
    slangs.insert_one(
        {
            "name": "Elmer",
            "age": 23
        }
    )



