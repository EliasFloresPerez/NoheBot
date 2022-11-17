import sqlite3


db = "base_de_datos.db"

def db_connect(db_path = db):
    conexion=sqlite3.connect(db,check_same_thread=False)
    return conexion

def Insertar_Estudiante(user,con,nom,idc,):
    
    try :
        sql = """
            INSERT INTO Estudiantes (Usuario,Contrasena,Nombre,Id_chat)
            VALUES (?,?,?,?)"""
        cur.execute(sql, (user,con,nom,idc))
        
    except:
        print("Error ya existe")
        return -1
    
    return cur.lastrowid


def Insertar_Tarea(cod_tarea,nombre,cod_materia,fecha,hora):
    
    try :
        sql = """
            INSERT INTO Tarea (Codigo_Tarea,Nombre_Tarea,Codigo_Materia,Fecha,Hora)
            VALUES (?,?,?,?,?)"""
        cur.execute(sql, (cod_tarea,nombre,cod_materia,fecha,hora))
        
    except:
       
        #Actualizamos si ya existe
        cur.execute("UPDATE Tarea SET Fecha = '{0}', Hora = '{1}' WHERE Codigo_Tarea = '{2}'".format(fecha,hora,cod_tarea))

        
        return -1
    return cur.lastrowid

def Insertar_Materia(cod_materia,nombre):
    
    try :
        sql = """
            INSERT INTO Materia (Codigo_Materia,Nombre_Materia)
            VALUES (?,?)"""
        cur.execute(sql, (cod_materia,nombre))
        
    except:
        
        return -1
    return cur.lastrowid

def Insertar_Lista(usu,cod,env):
    
    try :
        cur.execute("SELECT * FROM Lista_de_tareas  WHERE Usuario = '{0}' and Codigo_Tarea == '{1}' ".format(usu,cod))
        resultados = cur.fetchall()
        
        if resultados == []:
            sql = """
                INSERT INTO Lista_de_tareas (Usuario,Codigo_Tarea,Enviado)
                VALUES (?,?,?)"""
            cur.execute(sql, (usu,cod,env))
        else:
        
            cur.execute("UPDATE Lista_de_tareas SET Enviado = {0} WHERE Usuario = '{1}' and Codigo_Tarea = '{2}'".format(env,usu,cod))

        
    except:
        
        return -1
    return cur.lastrowid

def Retornar_Credenciales(orden):
    cur.execute("SELECT e.Usuario,e.Contrasena,e.Id_chat FROM Estudiantes e {0}".format(orden))
    resultados = cur.fetchall()
    
    if len(resultados) > 0:
            return resultados
    else:
        return []

def Retornar_Estudiante(orden):
    cur.execute("SELECT e.Usuario,e.Nombre, e.Id_chat FROM Estudiantes e {0}".format(orden))
    resultados = cur.fetchall()
    
    if len(resultados) > 0:
            return resultados
    else:
        return []


def Retornar_Materias(user):
    orden = """
    SELECT m.Nombre_Materia from Estudiantes e  
    JOIN Lista_de_Tareas  tl 
    ON e.Usuario = tl.Usuario and tl.Usuario = '{0}'
    JOIN Tarea t
    ON t.Codigo_Tarea =  tl.Codigo_Tarea
    JOIN Materia m 
    ON m.Codigo_materia = t.Codigo_materia
    Group by m.Codigo_materia
    
    """.format(user)

    cur.execute(orden)

    resultados = cur.fetchall()
    
    if len(resultados) > 0:
            return resultados
    else:
        return []   
    

def Retornar_Estudiantes_Tareas(user,env,codigoMatera = ""):
    orden = """
    SELECT e.Nombre,e.Id_chat,m.Nombre_Materia,t.Nombre_Tarea, t.Fecha , t.Hora from Estudiantes e  
    JOIN Lista_de_Tareas  tl 
    ON e.Usuario = tl.Usuario and tl.Usuario = '{0}'  and tl.Enviado = '{1}'
    JOIN Tarea t
    ON t.Codigo_Tarea =  tl.Codigo_Tarea
    JOIN Materia m 
    ON m.Codigo_materia = t.Codigo_materia
    
    """.format(user,env)

    
    if codigoMatera != "":
        #Si quiere de una materia en especifico
        orden += """and m.Nombre_Materia = '{0}'""".format(codigoMatera)
        #print(orden)


    cur.execute(orden)

    resultados = cur.fetchall()
    
    if len(resultados) > 0:
            return resultados
    else:
        return []

def Tarea_Especifica(user,env,nombre_materia,nombre_tarea):
    orden = """
    SELECT e.Nombre,e.Id_chat,m.Nombre_Materia,t.Nombre_Tarea, t.Fecha , t.Hora from Estudiantes e  
    JOIN Lista_de_Tareas  tl 
    ON e.Usuario = tl.Usuario and tl.Usuario = '{0}'
    JOIN Tarea t
    ON t.Codigo_Tarea =  tl.Codigo_Tarea and t.Nombre_Tarea = '{1}'
    JOIN Materia m 
    ON m.Codigo_materia = t.Codigo_materia and m.Nombre_Materia = '{2}'
    
    """.format(user,nombre_tarea,nombre_materia)
    cur.execute(orden)

    resultados = cur.fetchall()
    
    if len(resultados) > 0:
            return resultados
    else:
        return []

con = db_connect()
cur = con.cursor()



'''var = Tarea_Especifica("afloresp3",0,"SISTEMAS OPERATIVOS ","S1-TAREA_1")

for i in var:
    print(i,'\n')'''

