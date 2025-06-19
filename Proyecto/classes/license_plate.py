
from dataclasses import dataclass, asdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from bson.objectid import ObjectId

@dataclass
class LicensePlate :
    
    code:str
    country:str
    yearOfIssue:int
    state:str
    owner:str
    motorcycleId:ObjectId = "-"
    
        
    def register (self, id:str):
        self.motorcycleId = ObjectId(id)
        
        
    def __str__(self):
        return (
            f"🔹 Code : {self.code}\n"
            f"🔹 Country : {self.country}\n"
            f"🔹 State : {self.state}\n"
            f"🔹 Owner : {self.owner}"
        )   
        
    def save(self, coll):
        return str(coll.insert_one(asdict(self)).inserted_id)
    
    