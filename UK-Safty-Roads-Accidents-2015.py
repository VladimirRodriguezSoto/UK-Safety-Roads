import csv,sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Creacion de la base de datos
conexion=sqlite3.connect("accidentes.db")
cursor=conexion.cursor()

# Eliminacion de tablas 
cursor.execute("DROP TABLE IF EXISTS TipoVehiculo")
cursor.execute("DROP TABLE IF EXISTS Accidente")
cursor.execute("DROP TABLE IF EXISTS MedianaAccidentes")
cursor.execute("DROP TABLE IF EXISTS Vehiculo")
cursor.execute("DROP TABLE IF EXISTS Resultados")

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
# -----------
instruccion=cursor.execute('''CREATE TABLE Resultados (
    TipoVehiculo text,
    PromedioSeverirad float,
    TotalAccidentes interger
) ''')
# ----------
def accidentes_Tipo_Vehiculo_Severeidad(n:list):
    for element in n:
        total_accidentes=cursor.execute('''SELECT TipoVehiculo FROM MedianaAccidentes WHERE Codigo={}'''.format(element[0])).fetchall()
        promedio=cursor.execute('''SELECT TipoVehiculo, AVG(Severidad) FROM MedianaAccidentes WHERE Codigo={}'''.format(element[0])).fetchone()
        print("*************************************************")
        print("Tipo de Vehiculo:",promedio[0],"Promedio de severidad:",promedio[1],'\n'+"Total de Accidentes",len(total_accidentes))
        cursor.execute('''INSERT INTO Resultados VALUES (?,?,?)''',(promedio[0],promedio[1],len(total_accidentes)))

accidentes_Tipo_Vehiculo_Severeidad(lista)
instruccion=cursor.execute(''' SELECT * FROM Resultados''').fetchall()
conexion.commit()
cursor.close()

# Conversion a dataframe  para plotear 
df=pd.DataFrame(instruccion)
df.columns=["Tipo de Vehiculo","Promedio de Severidad","Total de Accidentes"]

# PLOTS
fig,axes=plt.subplots(2,1,figsize=(23,10))
sns.barplot(ax=axes[0],x="Promedio de Severidad",y="Tipo de Vehiculo",data=df,palette="tab10")
axes[0].set_title("Promedio de Severidad - Tipo de Vehiculo")

sns.barplot(ax=axes[1],x="Total de Accidentes",y="Tipo de Vehiculo",data=df,palette="tab10")
axes[1].set_title("Total de Accidentes - Tipo de Vehiculo")
fig.savefig('box_plot.png')