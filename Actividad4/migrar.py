import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

ATLAS_URI = os.getenv("MONGODB_URI")
ORIGEN_URI = "mongodb://localhost:27017/"
DESTINO_URI = "mongodb://localhost:27018/"
BASE_DATOS = "dbscott"

atlas = MongoClient(ATLAS_URI, serverSelectionTimeoutMS=10000)
origen = MongoClient(ORIGEN_URI, serverSelectionTimeoutMS=5000)
destino = MongoClient(DESTINO_URI, serverSelectionTimeoutMS=5000)

try:
    atlas.admin.command("ping")
    origen.admin.command("ping")
    destino.admin.command("ping")

    atlas_db = atlas[BASE_DATOS]
    origen_db = origen[BASE_DATOS]
    destino_db = destino[BASE_DATOS]

    # Cargar los datos de Atlas al contenedor de origen.
    for nombre in atlas_db.list_collection_names():
        documentos = list(atlas_db[nombre].find())
        origen_db[nombre].delete_many({})

        if documentos:
            origen_db[nombre].insert_many(documentos)

    print("Datos cargados en el contenedor de origen.")

    # Migrar las colecciones del origen al destino.
    for nombre in origen_db.list_collection_names():
        documentos = list(origen_db[nombre].find())
        destino_db[nombre].delete_many({})

        if documentos:
            destino_db[nombre].insert_many(documentos)

        print(f"{nombre}: {len(documentos)} documentos migrados.")

    # Verificar las cantidades en ambos contenedores.
    print("\nVerificacion de la migracion:")

    for nombre in origen_db.list_collection_names():
        cantidad_origen = origen_db[nombre].count_documents({})
        cantidad_destino = destino_db[nombre].count_documents({})

        print(
            f"{nombre}: origen={cantidad_origen}, "
            f"destino={cantidad_destino}"
        )

    print("\nProceso terminado.")

except Exception as error:
    print("Error durante el proceso:", error)

finally:
    atlas.close()
    origen.close()
    destino.close()