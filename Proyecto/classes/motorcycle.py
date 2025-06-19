from dataclasses import dataclass, asdict
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

@dataclass
class Motorcycle:
    brand:str
    model:str
    color:str
    vin:str
    owner:str
    licensePlateId:str = "-"
        
    def hasA (self, id:str):
        self.licensePlateId = ObjectId(id)
        
    def __str__(self):
        return (
            f"🔹 Brand : {self.brand}\n"
            f"🔹 Model : {self.model}\n"
            f"🔹 Color : {self.color}\n"
            f"🔹 VIN : {self.vin}\n"
            f"🔹 Owner : {self.owner}"
        )   
        
    def save(self, coll):
        return str(coll.insert_one(asdict(self)).inserted_id)
    