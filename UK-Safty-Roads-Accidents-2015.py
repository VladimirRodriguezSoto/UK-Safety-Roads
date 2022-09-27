import csv,sqlite3
from typing import Set
from unicodedata import decimal

# Creacion de la base de datos
conexion=sqlite3.connect("accidentes.db")
cursor=conexion.cursor()

# Eliminacion de tablas 
cursor.execute("DROP TABLE IF EXISTS TipoVehiculo")
cursor.execute("DROP TABLE IF EXISTS Accidente")
cursor.execute("DROP TABLE IF EXISTS MedianaAccidentes")
cursor.execute("DROP TABLE IF EXISTS Vehiculo")

# Creacion tablas
cursor.execute(""" 
    CREATE TABLE TipoVehiculo (
    Codigo INTERGER,
    Etiqueta TEXT)
    """)
    

cursor.execute(""" 
    CREATE TABLE Accidente (
    AccidenteIndex text,
    Severidad interger)
    """)

cursor.execute(""" 
    CREATE TABLE Vehiculo (
    Codigo text NOT NULL,
    TipoVehiculo interger NOT NULL)
    """)

cursor.execute(""" 
    CREATE TABLE MedianaAccidentes (
    TipoVehiculo text,
    Codigo interger,
    Severidad interger)
    """)   


# Introducir los datos a las tablas
# Tabla de tipo de vehiculos
with open('Python/SQL/Safty-Road-Accidents/datasets/vehicle_types.csv','r') as archivo1:
    for fila in archivo1:
        if fila!=1:
            cursor.execute('INSERT INTO Tipovehiculo VALUES(?,?)',fila.split(","))
    cursor.execute(''' DELETE FROM TipoVehiculo WHERE Codigo="code" ''')        
            

# Tabla de Vehiculos
with open('Python/SQL/Safty-Road-Accidents/datasets/Vehicles_2015.csv','r') as archivo2:
    for fila in archivo2:
        cursor.execute('INSERT INTO Vehiculo VALUES(?,?)',(fila.split(",")[0],fila.split(',')[2]))
    cursor.execute('DELETE FROM Vehiculo WHERE Codigo="Accident_Index"')   


# Tabla Accidente
with open('Python/SQL/Safty-Road-Accidents/datasets/Accidents_2015.csv','r') as archivo3:
    for fila in archivo3:
        cursor.execute('INSERT INTO Accidente VALUES(?,?)',(fila.split(',')[0],fila.split(',')[6]))
cursor.execute('DELETE FROM Accidente WHERE AccidenteIndex="Accident_Index"')   

# Union donde coinciden los indices de accidente y el tipo de veihiculo
# ---- Esto para obtener la severidad y tipos de vehiculo.
instruccion=cursor.execute(''' Select  Accidente.Severidad , TipoVehiculo.Etiqueta, TipoVehiculo.Codigo FROM Accidente
JOIN Vehiculo ON Accidente.AccidenteIndex=Vehiculo.Codigo
JOIN TipoVehiculo ON Vehiculo.TipoVehiculo=TipoVehiculo.Codigo
''')
lista=instruccion.fetchall()
for elemento in lista:
    cursor.execute(''' INSERT INTO MedianaAccidentes VALUES (?,?,?)''',(elemento[1],elemento[2],elemento[0]))


# Severidad y total de accidentes por tipo de vehiculo
lista=cursor.execute('''SELECT Codigo FROM TipoVehiculo''').fetchall()

def accidentes_Tipo_Vehiculo_Severeidad(n:list):
    for element in n:
        total_accidentes=cursor.execute('''SELECT TipoVehiculo FROM MedianaAccidentes WHERE Codigo={}'''.format(element[0])).fetchall()
        promedio=cursor.execute('''SELECT TipoVehiculo, AVG(Severidad) FROM MedianaAccidentes WHERE Codigo={}'''.format(element[0])).fetchone()
        print("*************************************************")
        print("Tipo de Vehiculo:",promedio[0],"Promedio de severidad:",promedio[1],'\n'+"Total de Accidentes",len(total_accidentes))
        print("*************************************************")
    

accidentes_Tipo_Vehiculo_Severeidad(lista)

conexion.commit()
cursor.close()