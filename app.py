from flask import Flask, request, jsonify
import sqlite3 as sql
import json

app = Flask(__name__)

def modifyParameter(param):
    newParam = param.replace(',',' ')
    paramList = newParam.split()
    return paramList

def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

@app.route('/api/products')
@app.route('/api/products/count')
def GetProducts():
    
    condition = ""
    order_by = ""
    #status OK
    if('status' in request.args):      
        status = str(request.args.get('status'))
        list_status = modifyParameter(status)
        c = "status IN "
        c_in = ""
        for st in list_status:
            c_in += "'"+st+"',"
        
        if(condition == ""):
            condition = " WHERE " +(c+"("+c_in)[:-1]+")"
        else:
            condition = " AND " +(c+"("+c_in)[:-1]+")"

    #fields OK
    if('fields' in request.args): 
        fields = ""     
        fieldsParam = str(request.args.get('fields'))
        if(fieldsParam == 'all'):
            fields = "*"
        else:
            list_fields = modifyParameter(fieldsParam)
            for field in list_fields:
                fields += field + ","

            fields = fields[:-1]

    #locked OK
    if('locked' in request.args):      
        locked = request.args.get('locked')
                   
        if(condition == ""):
            condition = " WHERE locked = " + "'"  + locked + "'"              
        else:
            condition += " AND locked = " + "'"  + locked + "'"
        
    #deleted OK
    if('deleted' in request.args):      
        deleted = request.args.get('deleted')
                   
        if(condition == ""):
            condition = " WHERE deleted = " + "'"  + deleted + "'"              
        else:
            condition += " AND deleted = " + "'"  + deleted + "'"

    #completed OK
    if('completed' in request.args):      
        completed = request.args.get('completed')
                   
        if(condition == ""):
            condition = " WHERE completed = " + "'"  + completed + "'"              
        else:
            condition += " AND completed = " + "'"  + completed + "'"

    #product_type OK
    if('product_type' in request.args):
        product_type = str(request.args.get('product_type'))
        c = "product_type = '"+product_type+"'"
 
        if(condition == ""):
            condition = " WHERE " + c
        else:
            condition += " AND " + c

    #order_name OK
    if('order_name' in request.args):
        order_name = str(request.args.get('order_name'))
        c = "order_name = '#"+order_name+"'"
 
        if(condition == ""):
            condition = " WHERE " + c
        else:
            condition += " AND " + c

    #variant_name OK
    if('variant_name' in request.args):
        variant_name = str(request.args.get('variant_name'))
        c = "variant_name = '"+variant_name+"'"
 
        if(condition == ""):
            condition = " WHERE " + c
        else:
            condition += " AND " + c

    #order by OK
    if('order_by' in request.args):
        param = str(request.args.get('order_by'))
        order_by = " ORDER BY " + param
    
    # Querys by diferents end points
    #-------------------------------------------------------------------------------------------
    if(request.path == "/api/products"):
        print(condition)
        try:
            connection = sql.connect("mock_server.db")
            connection.row_factory = dict_factory
            cursor = connection.cursor()
            cursor.execute("""SELECT """ + fields + """ 
                              FROM products """ 
                              + condition + " "
                              + order_by
                              )

            results = cursor.fetchall()
                        
        except:
            connection.rollback()
        
        finally:
            connection.close() 
            return jsonify(results)
            
    elif(request.path == "/api/products/count"):
        
        try:
            connection = sql.connect("mock_server.db")
            connection.row_factory = dict_factory
            cursor = connection.cursor()
            cursor.execute("""SELECT COUNT(*) as count,
                                     COUNT(*) as total
                              FROM products"""
                              + condition)
                              
            results = cursor.fetchall()
                        
        except:
            connection.rollback()
        
        finally:
            connection.close() 
            return jsonify(results)
    #-------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(port = 3000, debug = True)