import os
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

# Bases de datos y colecciones
db_embedding = client["dbemp"]
emp_embedding = db_embedding["emp"]

db_linking = client["dbscott"]
emp_linking = db_linking["emp"]
dept_linking = db_linking["dept"]

def insertar_empleado():
    print("\n========== INSERTAR EMPLEADO - EMBEDDING ==========")

    empno = int(input("Número de empleado: "))

    if emp_embedding.find_one({"empno": empno}):
        print("Ya existe un empleado con ese número.")
        return

    ename = input("Nombre: ").upper()
    job = input("Puesto: ").upper()

    mgr_input = input("Número del jefe (Enter si no tiene): ")
    mgr = int(mgr_input) if mgr_input else None

    hiredate = datetime.strptime(
        input("Fecha de contratación (YYYY-MM-DD): "),
        "%Y-%m-%d"
    )

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

    resultado = emp_embedding.insert_one(empleado)

    print("Empleado insertado correctamente.")
    print("ID:", resultado.inserted_id)


def consultar_empleados():
    print("\n========== EMPLEADOS - EMBEDDING ==========")

    empleados = emp_embedding.find().sort("empno", 1)

    for empleado in empleados:
        dept = empleado["dept"]

        print(f"\nNúmero: {empleado['empno']}")
        print(f"Nombre: {empleado['ename']}")
        print(f"Puesto: {empleado['job']}")
        print(f"Jefe: {empleado.get('mgr')}")
        print(f"Fecha contratación: {empleado['hiredate'].strftime('%Y-%m-%d')}")
        print(f"Salario: {empleado['sal']}")
        print(f"Comisión: {empleado.get('comm')}")
        print(f"Departamento: {dept['deptno']}")
        print(f"Nombre departamento: {dept['dname']}")
        print(f"Ubicación: {dept['loc']}")
        print("--------------------------------")


def actualizar_empleado():
    print("\n========== ACTUALIZAR EMPLEADO - EMBEDDING ==========")

    empno = int(input("Número del empleado a actualizar: "))
    empleado = emp_embedding.find_one({"empno": empno})

    if empleado is None:
        print("No se encontró el empleado.")
        return

    print("Deja vacío un campo si no deseas modificarlo.")

    ename = input(f"Nombre [{empleado['ename']}]: ")
    job = input(f"Puesto [{empleado['job']}]: ")
    sal = input(f"Salario [{empleado['sal']}]: ")

    dept_name = input(
        f"Nombre departamento [{empleado['dept']['dname']}]: "
    )
    dept_loc = input(
        f"Ubicación [{empleado['dept']['loc']}]: "
    )

    cambios = {}

    if ename:
        cambios["ename"] = ename.upper()

    if job:
        cambios["job"] = job.upper()

    if sal:
        cambios["sal"] = float(sal)

    if dept_name:
        cambios["dept.dname"] = dept_name.upper()

    if dept_loc:
        cambios["dept.loc"] = dept_loc.upper()

    if not cambios:
        print("No se realizaron cambios.")
        return

    resultado = emp_embedding.update_one(
        {"empno": empno},
        {"$set": cambios}
    )

    if resultado.modified_count > 0:
        print("Empleado actualizado correctamente.")
    else:
        print("No hubo cambios.")


def eliminar_empleado():
    print("\n========== ELIMINAR EMPLEADO - EMBEDDING ==========")

    empno = int(input("Número del empleado a eliminar: "))
    empleado = emp_embedding.find_one({"empno": empno})

    if empleado is None:
        print("No se encontró el empleado.")
        return

    print(f"Empleado encontrado: {empleado['ename']}")
    confirmacion = input("¿Deseas eliminarlo? (s/n): ").lower()

    if confirmacion == "s":
        emp_embedding.delete_one({"empno": empno})
        print("Empleado eliminado correctamente.")
    else:
        print("Operación cancelada.")

def buscar_empleados_embedding():
    print("\n========== BUSCAR EMPLEADOS - EMBEDDING ==========")

    nombre = input("Nombre del empleado a buscar: ").upper()

    empleados = emp_embedding.find({"ename": nombre}).sort("empno", 1)

    encontrados = 0

    for empleado in empleados:
        dept = empleado["dept"]

        print(f"\nNúmero: {empleado['empno']}")
        print(f"Nombre: {empleado['ename']}")
        print(f"Puesto: {empleado['job']}")
        print(f"Salario: {empleado['sal']}")
        print(f"Departamento: {dept['deptno']}")
        print(f"Nombre departamento: {dept['dname']}")
        print(f"Ubicación: {dept['loc']}")
        print("--------------------------------")

        encontrados += 1

    if encontrados == 0:
        print("No se encontraron empleados con ese nombre.")


def contar_empleados_embedding():
    print("\n========== CONTAR EMPLEADOS - EMBEDDING ==========")

    puesto = input("Puesto para filtrar: ").upper()

    cantidad = emp_embedding.count_documents({"job": puesto})

    print("Cantidad de empleados:", cantidad)

def menu_embedding():
    while True:
        print("\n========== CRUD - MODELADO EMBEDDING ==========")
        print("1. Insertar empleado")
        print("2. Consultar empleados")
        print("3. Actualizar empleado")
        print("4. Eliminar empleado")
        print("5. Buscar empleados")
        print("6. Contar empleados por puesto")
        print("7. Volver al menú principal")

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
            buscar_empleados_embedding()
        elif opcion == "6":
            contar_empleados_embedding()
        elif opcion == "7":
            break
        else:
            print("Opción no válida.")

def insertar_empleado_linking():
    print("\n========== INSERTAR EMPLEADO - LINKING ==========")

    empno = int(input("Número de empleado: "))

    if emp_linking.find_one({"empno": empno}):
        print("Ya existe un empleado con ese número.")
        return

    ename = input("Nombre: ").upper()
    job = input("Puesto: ").upper()

    mgr_input = input("Número del jefe (Enter si no tiene): ")
    mgr = int(mgr_input) if mgr_input else None

    hiredate = datetime.strptime(
        input("Fecha de contratación (YYYY-MM-DD): "),
        "%Y-%m-%d"
    )

    sal = float(input("Salario: "))

    comm_input = input("Comisión (Enter si no tiene): ")
    comm = float(comm_input) if comm_input else None

    deptno = int(input("Número de departamento: "))

    if not dept_linking.find_one({"deptno": deptno}):
        print("El departamento no existe.")
        return

    empleado = {
        "empno": empno,
        "ename": ename,
        "job": job,
        "mgr": mgr,
        "hiredate": hiredate,
        "sal": sal,
        "comm": comm,
        "deptno": deptno
    }

    resultado = emp_linking.insert_one(empleado)

    print("Empleado insertado correctamente.")
    print("ID:", resultado.inserted_id)

def consultar_empleados_linking():
    print("\n========== EMPLEADOS - LINKING ==========")

    pipeline = [
        {
            "$lookup": {
                "from": "dept",
                "localField": "deptno",
                "foreignField": "deptno",
                "as": "departamento"
            }
        },
        {"$sort": {"empno": 1}}
    ]

    for empleado in emp_linking.aggregate(pipeline):
        print(f"\nNúmero: {empleado['empno']}")
        print(f"Nombre: {empleado['ename']}")
        print(f"Puesto: {empleado['job']}")
        print(f"Jefe: {empleado.get('mgr')}")

        hiredate = empleado.get("hiredate")
        if hiredate:
            print(f"Fecha contratación: {hiredate.strftime('%Y-%m-%d')}")

        print(f"Salario: {empleado['sal']}")
        print(f"Comisión: {empleado.get('comm')}")
        print(f"Número de departamento: {empleado['deptno']}")

        departamentos = empleado.get("departamento", [])

        if departamentos:
            dept = departamentos[0]
            print(f"Nombre departamento: {dept['dname']}")
            print(f"Ubicación: {dept['loc']}")
        else:
            print("Departamento no encontrado.")

        print("--------------------------------")


def actualizar_empleado_linking():
    print("\n========== ACTUALIZAR EMPLEADO - LINKING ==========")

    empno = int(input("Número del empleado a actualizar: "))
    empleado = emp_linking.find_one({"empno": empno})

    if empleado is None:
        print("No se encontró el empleado.")
        return

    print("Deja vacío un campo si no deseas modificarlo.")

    ename = input(f"Nombre [{empleado['ename']}]: ")
    job = input(f"Puesto [{empleado['job']}]: ")
    sal = input(f"Salario [{empleado['sal']}]: ")
    deptno_input = input(
        f"Número de departamento [{empleado['deptno']}]: "
    )

    cambios = {}

    if ename:
        cambios["ename"] = ename.upper()

    if job:
        cambios["job"] = job.upper()

    if sal:
        cambios["sal"] = float(sal)

    if deptno_input:
        deptno = int(deptno_input)

        if not dept_linking.find_one({"deptno": deptno}):
            print("El departamento no existe.")
            return

        cambios["deptno"] = deptno

    if not cambios:
        print("No se realizaron cambios.")
        return

    resultado = emp_linking.update_one(
        {"empno": empno},
        {"$set": cambios}
    )

    if resultado.modified_count > 0:
        print("Empleado actualizado correctamente.")
    else:
        print("No hubo cambios.")


def eliminar_empleado_linking():
    print("\n========== ELIMINAR EMPLEADO - LINKING ==========")

    empno = int(input("Número del empleado a eliminar: "))
    empleado = emp_linking.find_one({"empno": empno})

    if empleado is None:
        print("No se encontró el empleado.")
        return

    print(f"Empleado encontrado: {empleado['ename']}")
    confirmacion = input("¿Deseas eliminarlo? (s/n): ").lower()

    if confirmacion == "s":
        emp_linking.delete_one({"empno": empno})
        print("Empleado eliminado correctamente.")
    else:
        print("Operación cancelada.")

def buscar_empleados_linking():
    print("\n========== BUSCAR EMPLEADOS - LINKING ==========")

    nombre = input("Nombre del empleado a buscar: ").upper()

    pipeline = [
        {"$match": {"ename": nombre}},
        {
            "$lookup": {
                "from": "dept",
                "localField": "deptno",
                "foreignField": "deptno",
                "as": "departamento"
            }
        },
        {"$sort": {"empno": 1}}
    ]

    encontrados = 0

    for empleado in emp_linking.aggregate(pipeline):
        print(f"\nNúmero: {empleado['empno']}")
        print(f"Nombre: {empleado['ename']}")
        print(f"Puesto: {empleado['job']}")
        print(f"Salario: {empleado['sal']}")
        print(f"Número de departamento: {empleado['deptno']}")

        departamentos = empleado.get("departamento", [])

        if departamentos:
            dept = departamentos[0]
            print(f"Nombre departamento: {dept['dname']}")
            print(f"Ubicación: {dept['loc']}")
        else:
            print("Departamento no encontrado.")

        print("--------------------------------")
        encontrados += 1

    if encontrados == 0:
        print("No se encontraron empleados con ese nombre.")


def contar_empleados_linking():
    print("\n========== CONTAR EMPLEADOS - LINKING ==========")

    puesto = input("Puesto para filtrar: ").upper()

    cantidad = emp_linking.count_documents({"job": puesto})

    print("Cantidad de empleados:", cantidad)


def menu_linking():
    while True:
        print("\n========== CRUD - MODELADO LINKING ==========")
        print("1. Insertar empleado")
        print("2. Consultar empleados")
        print("3. Actualizar empleado")
        print("4. Eliminar empleado")
        print("5. Buscar empleados")
        print("6. Contar empleados por puesto")
        print("7. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            insertar_empleado_linking()
        elif opcion == "2":
            consultar_empleados_linking()
        elif opcion == "3":
            actualizar_empleado_linking()
        elif opcion == "4":
            eliminar_empleado_linking()
        elif opcion == "5":
            buscar_empleados_linking()
        elif opcion == "6":
            contar_empleados_linking()
        elif opcion == "7":
            break
        else:
            print("Opción no válida.")

def menu():
    while True:
        print("\n========================================")
        print("       CRUD DE MONGODB EN PYTHON")
        print("========================================")
        print("1. Modelado Embedding")
        print("2. Modelado Linking")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            menu_embedding()
        elif opcion == "2":
            menu_linking()
        elif opcion == "3":
            print("Programa terminado.")
            break
        else:
            print("Opción no válida.")


try:
    menu()
finally:
    client.close()