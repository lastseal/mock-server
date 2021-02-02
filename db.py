import json
import sqlite3
from datetime import datetime
db=sqlite3.connect('mock_server.db')

#------------------------------------------------------
# Este Script permite crear tablas en una base de datos sqlite3, transformando data de un archivo JSON a SQL.
# Se debe cambiar los datos de este script segun la tabla a crear y luego insertar:
# line 14 (json que se leera y guardara en base de datos)
# line 36 (tabla a crear)
# line 37 (tabla en donde se insertara la data)
#------------------------------------------------------

with open('products.json', encoding='utf-8-sig') as json_file:
    json_data = json.loads(json_file.read())
    
#Aim of this block is to get the list of the columns in the JSON file.
    columns = []
    column = []
    for data in json_data:
        column = list(data.keys())
        for col in column:
            if col not in columns:
                columns.append(col)
                                
#Here we get values of the columns in the JSON file in the right order.   
    value = []
    values = [] 
    for data in json_data:
        for i in columns:
            value.append(str(dict(data).get(i)))   
        values.append(list(value)) 
        value.clear()
        
#Time to generate the create and insert queries and apply it to the sqlite3 database       
    create_query = "create table products ({0})".format(" text,".join(columns))
    insert_query = "insert into products ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))  

    print("insert has started at " + str(datetime.now()))  
    c = db.cursor()   
    c.execute(create_query)
    c.executemany(insert_query , values)
    values.clear()
    db.commit()
    c.close()
    print("insert has completed at " + str(datetime.now()))