# librebiras
import os
from dataclasses import dataclass, asdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from bson.objectid import ObjectId

from classes.motorcycle import Motorcycle
from classes.license_plate import LicensePlate

load_dotenv()

URI = os.getenv("URI") # URI:identificaor uniforme de recursos (como una URL para base de datos)


    
def get_collection(uri, db="demo_db", col="motorcycles_LicensePlates"):
    client = MongoClient (
        uri
        , Server_api = ServerApi("1")
        , tls = True #protocolo de seguridad
        , tlsAllowInvalidCertificates = True 
    )
    
    client.admin.command("ping") 
    
    return client[db][col] 

def update_collection(doc_id, id_relation, coll):
    
    #doc_id : id del elemento a buscar
    #id_relation : id que insertaremos
    
    filtro = {"_id": ObjectId(doc_id)}
    newValue = {"$set":{"licensePlateId": ObjectId(id_relation)}}
    
    result = coll.update_one(filtro, newValue)
    
    if result.matched_count > 0:
        print("Documento actualizado correctamente")
    else:
        print("No se encontro ningun documento con ese id")
    return result

def main() : 
    
    coll = get_collection(URI) #recolecta la coleccioh
    
    m = Motorcycle("Honda", "CRF250f" , "white", "12341JSOFD34", "Juan" )
    lp = LicensePlate("210HTR", "Honduras", 2017, "Intibuca", "Juanito")
    
    motorcycleId = m.save(coll)
    lp.register(motorcycleId)
    print("Este es el ID de la motocicleta: " + motorcycleId)
    
    licensePlateId = lp.save(coll)
    print("Este es el id de la placa: " + licensePlateId)
    update_collection(motorcycleId, licensePlateId, coll)
    
    
    
if __name__ == "__main__" : #ejecutar el main primero
    main()