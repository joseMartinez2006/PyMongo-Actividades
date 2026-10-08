import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri)

db = client["dbemp"]
emp = db["emp"]


def insertar_empleado():
    print("\n========== INSERTAR EMPLEADO ==========")

    empno = int(input("Número de empleado: "))
    ename = input("Nombre: ").upper()
    job = input("Puesto: ").upper()
    mgr_input = input("Número del jefe (Enter si no tiene): ")
    mgr = int(mgr_input) if mgr_input else None

    hiredate_input = input("Fecha de contratación (YYYY-MM-DD): ")
    hiredate = datetime.strptime(hiredate_input, "%Y-%m-%d")

    sal = float(input("Salario: "))

    comm_input = input("Comisión (Enter si no tiene): ")
    comm = float(comm_input) if comm_input else None

    deptno = int(input("Número de departamento: "))
    dname = input("Nombre del departamento: ").upper()
    loc = input("Ubicación: ").upper()

    empleado = {
        "empno": empno,
        "ename": ename,
        "job": job,
        "mgr": mgr,
        "hiredate": hiredate,
        "sal": sal,
        "comm": comm,
        "dept": {
            "deptno": deptno,
            "dname": dname,
            "loc": loc
        }
    }

    resultado = emp.insert_one(empleado)

    print("\nEmpleado insertado correctamente.")
    print("ID:", resultado.inserted_id)


def consultar_empleados():
    print("\n========== EMPLEADOS ==========")

    empleados = emp.find().sort("empno", 1)

    for empleado in empleados:
        print(f"\nNúmero: {empleado['empno']}")
        print(f"Nombre: {empleado['ename']}")
        print(f"Puesto: {empleado['job']}")
        print(f"Jefe: {empleado['mgr']}")
        print(f"Fecha contratación: {empleado['hiredate'].strftime('%Y-%m-%d')}")
        print(f"Salario: {empleado['sal']}")
        print(f"Comisión: {empleado['comm']}")
        print(f"Departamento: {empleado['dept']['deptno']}")
        print(f"Nombre departamento: {empleado['dept']['dname']}")
        print(f"Ubicación: {empleado['dept']['loc']}")
        print("--------------------------------")


def actualizar_empleado():
    print("\n========== ACTUALIZAR EMPLEADO ==========")

    empno = int(input("Número del empleado a actualizar: "))

    empleado = emp.find_one({"empno": empno})

    if empleado is None:
        print("\nNo se encontró el empleado.")
        return

    print("\nDeja vacío un campo si no deseas modificarlo.")

    ename = input(f"Nombre [{empleado['ename']}]: ")
    job = input(f"Puesto [{empleado['job']}]: ")
    sal = input(f"Salario [{empleado['sal']}]: ")

    cambios = {}

    if ename:
        cambios["ename"] = ename.upper()

    if job:
        cambios["job"] = job.upper()

    if sal:
        cambios["sal"] = float(sal)

    dept_name = input(
        f"Nombre departamento [{empleado['dept']['dname']}]: "
    )

    dept_loc = input(
        f"Ubicación [{empleado['dept']['loc']}]: "
    )

    if dept_name:
        cambios["dept.dname"] = dept_name.upper()

    if dept_loc:
        cambios["dept.loc"] = dept_loc.upper()

    if not cambios:
        print("\nNo se realizaron cambios.")
        return

    resultado = emp.update_one(
        {"empno": empno},
        {"$set": cambios}
    )

    if resultado.modified_count > 0:
        print("\nEmpleado actualizado correctamente.")
    else:
        print("\nNo hubo cambios.")


def eliminar_empleado():
    print("\n========== ELIMINAR EMPLEADO ==========")

    empno = int(input("Número del empleado a eliminar: "))

    empleado = emp.find_one({"empno": empno})

    if empleado is None:
        print("\nNo se encontró el empleado.")
        return

    print(f"\nEmpleado encontrado: {empleado['ename']}")
    confirmacion = input("¿Deseas eliminarlo? (s/n): ").lower()

    if confirmacion == "s":
        resultado = emp.delete_one({"empno": empno})

        if resultado.deleted_count > 0:
            print("\nEmpleado eliminado correctamente.")
        else:
            print("\nNo se pudo eliminar el empleado.")
    else:
        print("\nOperación cancelada.")


def menu():
    while True:
        print("\n========================================")
        print("          CRUD - MODELADO EMBEDDING")
        print("========================================")
        print("1. Insertar empleado")
        print("2. Consultar empleados")
        print("3. Actualizar empleado")
        print("4. Eliminar empleado")
        print("5. Salir")
        print("========================================")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            insertar_empleado()

        elif opcion == "2":
            consultar_empleados()

        elif opcion == "3":
            actualizar_empleado()

        elif opcion == "4":
            eliminar_empleado()

        elif opcion == "5":
            print("\nPrograma terminado.")
            break

        else:
            print("\nOpción no válida.")


try:
    menu()
finally:
    client.close()