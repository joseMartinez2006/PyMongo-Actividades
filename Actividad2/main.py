import os
from dotenv import load_dotenv
from pymongo import MongoClient
import queries

load_dotenv()

uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError("No se encontró MONGODB_URI en el archivo .env")

def mostrar_resultados(resultados):
    if not resultados:
        print("\nNo se encontraron resultados.")
        return

    print(f"\nTotal de resultados: {len(resultados)}")

    for resultado in resultados:
        for campo, valor in resultado.items():
            nombre = campo.replace("_", " ").capitalize()

            if isinstance(valor, dict):
                if "name" in valor and len(valor) == 1:
                    valor = valor["name"]
                else:
                    valor = ", ".join(
                        f"{clave}: {dato}"
                        for clave, dato in valor.items()
                    )

            print(f"{nombre}: {valor}")

        print("--------------------------------")

def mostrar_resultados_especiales(numero, resultados):
    if numero == 16:
        for resultado in resultados:
            print(f"\nContinente: {resultado['continent']}")

            for auto in resultado["cars"]:
                print(f"Descripción: {auto['description']}")
                print(f"MPG: {auto['mpg']}")
                print("--------------------------------")

    elif numero == 23:
        if not resultados:
            print("\nNo se encontraron resultados.")
            return

        resultado = resultados[0]

        print("\nAutomóviles por continente:")
        for dato in resultado["carsByContinent"]:
            print(f"Continente: {dato['_id']}")
            print(f"Cantidad: {dato['cars']}")
            print("--------------------------------")

        print("\nAutomóviles por cilindros:")
        for dato in resultado["carsByCylinders"]:
            print(f"Cilindros: {dato['_id']}")
            print(f"Cantidad: {dato['cars']}")
            print("--------------------------------")

        print("\nEstadísticas globales de MPG:")
        for dato in resultado["globalMpg"]:
            print(f"Mínimo: {dato['min']}")
            print(f"Máximo: {dato['max']}")
            print(f"Promedio: {dato['average']}")
            print("--------------------------------")

def main():
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)

    try:
        client.admin.command("ping")
        db = client["BDAutos"]

        print("Conexión con MongoDB exitosa.")
        print("Base de datos:", db.name)
        print("Automóviles registrados:", db.cars.count_documents({}))

        while True:
            print("\n========== MENU BDAutos ==========")
            print("1-25. Ejecutar una consulta")
            print("0. Salir")
            opcion = input("Selecciona una consulta (0-25): ").strip()

            if opcion == "0":
                print("Programa finalizado.")
                break

            if not opcion.isdigit() or not 1 <= int(opcion) <= 25:
                print("Opción no válida. Elige un número del 0 al 25.")
                continue

            numero = int(opcion)
            funcion = getattr(queries, f"consulta_{numero}")

            try:
                resultados = funcion(db)
                print(f"\n========== CONSULTA {numero} ==========")

                if numero in (16, 23):
                    mostrar_resultados_especiales(numero, resultados)
                else:
                    mostrar_resultados(resultados)

            except Exception as error:
                print(f"Error al ejecutar la consulta {numero}: {error}")

    except Exception as error:
        print("Error de conexión:", error)

    finally:
        client.close()

if __name__ == "__main__":
    main()