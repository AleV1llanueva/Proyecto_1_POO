from dataclasses import dataclass, asdict
import os
import unittest
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from bson.objectid import ObjectId

from app import get_collection, update_collection
from classes.motorcycle import Motorcycle
from classes.license_plate import LicensePlate


URI = os.getenv("URI")

class TestMyModelo (unittest.TestCase):
    
    def setUp(self):
        #Conexion a mongoDB
        self.coll = get_collection(URI)
    
        #Instancias de prueba
        mTest = Motorcycle("YAMAHA", "YZ125", "Blue", "3954h94t", "Pedro")
        lpTest = LicensePlate("234HGD", "Honduras", 2020, "Comayagua", "Pedro")
    
        #Subir primer instancia
        self.mId = mTest.save(self.coll)
        lpTest.motorcycleId = self.mId
    
        #Subir segunda instancia y actualizar primera
        self.lpId = lpTest.save(self.coll)
        update_collection(self.mId, self.lpId, self.coll)
    
    def testExistInTheDatabase(self):
        
        #Existencia de la motocicleta en la base de datos
        filtro = {"_id": ObjectId(self.mId)}
        mTest = self.coll.find_one(filtro)
        self.assertTrue(mTest)
        
        #Existencia de la placa
        filtro = {"_id": ObjectId(self.lpId)}
        lpTest = self.coll.find_one(filtro)
        self.assertTrue(lpTest)
        
    def testSaveIds(self):
        
        #Recupera motocicleta
        filtro = {"_id": ObjectId(self.mId)}
        mTest = self.coll.find_one(filtro)
        
        #Recupera placa
        filtro = {"_id": ObjectId(self.lpId)}
        lpTest = self.coll.find_one(filtro)
        
        #Si existe la moto, verfique que se guardo correctamente el id de la placa
        if mTest:
            self.assertEqual(str(mTest["licensePlateId"]), str(self.lpId))
           
        #Si existe el placa, verifique que se guardo correctamente el id de la moto 
        if lpTest:
            self.assertEqual(str(lpTest["motorcycleId"]),str( self.mId))
            
    def tearDown(self):
        self.coll.delete_one({"_id": ObjectId(self.mId)})
        self.coll.delete_one({"_id": ObjectId(self.lpId)})
            
            
if __name__ == '__main__':
    unittest.main()