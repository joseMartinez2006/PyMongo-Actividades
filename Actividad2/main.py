
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError("No se encontró MONGODB_URI en el archivo .env")

client = MongoClient(uri, serverSelectionTimeoutMS=10000)

try:
    client.admin.command("ping")
    db = client["BDAutos"]
    cars = db["cars"]

    print("Conexión con MongoDB exitosa.")
    print("Base de datos:", db.name)
    print("Colección:", cars.name)
    print("Automóviles registrados:", cars.count_documents({}))

except Exception as error:
    print("Error de conexión:", error)

finally:
    client.close()