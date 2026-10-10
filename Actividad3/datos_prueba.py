from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db_embedding = client["dbemp"]
emp_embedding = db_embedding["emp"]

db_linking = client["dbscott"]
emp_linking = db_linking["emp"]
dept_linking = db_linking["dept"]

departamentos = [
    {"deptno": 10, "dname": "ACCOUNTING", "loc": "NEW YORK"},
    {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"},
    {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"},
    {"deptno": 40, "dname": "OPERATIONS", "loc": "BOSTON"}
]

datos_empleados = [
    (7369, "SMITH", "CLERK", 7902, "1980-12-17", 800, None, 20),
    (7499, "ALLEN", "SALESMAN", 7698, "1981-02-20", 1600, 300, 30),
    (7521, "WARD", "SALESMAN", 7698, "1981-02-22", 1250, 500, 30),
    (7566, "JONES", "MANAGER", 7839, "1981-04-02", 2975, None, 20),
    (7654, "MARTIN", "SALESMAN", 7698, "1981-09-28", 1250, 1400, 30),
    (7698, "BLAKE", "MANAGER", 7839, "1981-05-01", 2850, None, 30),
    (7782, "CLARK", "MANAGER", 7839, "1981-06-09", 2450, None, 10),
    (7788, "SCOTT", "ANALYST", 7566, "1987-04-19", 3000, None, 20),
    (7839, "KING", "PRESIDENT", None, "1981-11-17", 5000, None, 10),
    (7844, "TURNER", "SALESMAN", 7698, "1981-09-08", 1500, 0, 30),
    (7876, "ADAMS", "CLERK", 7788, "1987-05-23", 1100, None, 20),
    (7900, "JAMES", "CLERK", 7698, "1981-12-03", 950, None, 30),
    (7902, "FORD", "ANALYST", 7566, "1981-12-03", 3000, None, 20),
    (7934, "MILLER", "CLERK", 7782, "1982-01-23", 1300, None, 10)
]

try:
    mapa_departamentos = {
        dept["deptno"]: dept for dept in departamentos
    }

    empleados_embedding = []
    empleados_linking = []

    for empno, ename, job, mgr, fecha, sal, comm, deptno in datos_empleados:
        empleado = {
            "empno": empno,
            "ename": ename,
            "job": job,
            "mgr": mgr,
            "hiredate": datetime.strptime(fecha, "%Y-%m-%d"),
            "sal": sal,
            "comm": comm
        }

        empleado_embedding = empleado.copy()
        empleado_embedding["dept"] = mapa_departamentos[deptno]
        empleados_embedding.append(empleado_embedding)

        empleado_linking = empleado.copy()
        empleado_linking["deptno"] = deptno
        empleados_linking.append(empleado_linking)

    # Reemplazar únicamente los datos de prueba de Docker.
    emp_embedding.delete_many({})
    emp_linking.delete_many({})
    dept_linking.delete_many({})

    emp_embedding.insert_many(empleados_embedding)
    dept_linking.insert_many(departamentos)
    emp_linking.insert_many(empleados_linking)

    print("Datos cargados correctamente en MongoDB Docker.")
    print("Empleados Embedding:", emp_embedding.count_documents({}))
    print("Empleados Linking:", emp_linking.count_documents({}))
    print("Departamentos Linking:", dept_linking.count_documents({}))

finally:
    client.close()