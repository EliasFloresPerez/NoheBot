import pymysql

class DataBase:

    def __init__(self):
        
        self.connection = pymysql.connect(
            host='localhost',
            user = 'root',
            password = '',
            db = 'nohebot'
        )
        self.cursor =  self.connection.cursor()
        

    #Funciones que ingresan datos en la BD
    def Insertar_Estudiante(self,usu,contra,nom,cid,num=None):
        sql = "Insert into Estudiante(Usuario,Contrasenia,Nombre,Chat_id,Numero) Values (%s,%s,%s,%s,%s)"
        val = (usu,contra,nom,cid,num)

        try:
            self.cursor.execute(sql,val)
            self.connection.commit()
            
        except Exception as e:
            print("Error al insertar un estudiante ")
            return -1

    def Insertar_Asignatura(self,id_c,nom,carr = None):
        sql = "Insert into Asignatura(id_asignatura,Nombre,Carrera) Values (%s,%s,%s)"
        val = (id_c,nom,carr)

        try:
            self.cursor.execute(sql,val)
            self.connection.commit()
            
        except Exception as e:
            #print("Error al insertar una asignatura ")
            return -1

    def Insertar_Lista_Estudiante_Tarea(self,usu,cod,env):
        sql = "SELECT * FROM estudiante_has_tareas_entregar  WHERE Usuario = %s and Tarea_id = %s "
        val = (usu,cod)
        self.cursor.execute(sql,val)
        resultado =  self.cursor.fetchall()
        
        try:
            if resultado == ():
                #Si no hay nada
            
                sql = "Insert into estudiante_has_tareas_entregar (Usuario,Tarea_id,Enviado) Values (%s,%s,%s)"
                val = (usu,cod,env)
                self.cursor.execute(sql,val)
            else:
                
                #Si hay algo
                sql = "Update  estudiante_has_tareas_entregar Set Enviado = %s Where Usuario = %s and Tarea_id = %s"
                val = (env,usu,cod)
                self.cursor.execute(sql,val)
            self.connection.commit()
        except:

            print("Error desconocido ",val)
            pass
     
    def Insertar_Tarea(self,cod_tarea,nombre,cod_materia,fecha_ini,fecha_fin,hora = None,enlace = None):
        sql = ""
        val = ""
        try:
            sql = """
            Insert into Tareas_Entregar
            (Id_tarea, Nombre, Asignatura_id, Fecha_inicio, Fecha_fin, Hora, Enlace)
            Values(%s,%s,%s,%s,%s,%s,%s)
            """
            val = (cod_tarea,nombre,cod_materia,fecha_ini,fecha_fin,hora,enlace)
            self.cursor.execute(sql,val)
        except:
            #print("Hizo update",fecha_ini,fecha_fin,hora,cod_tarea)
            sql = """
            Update Tareas_Entregar 
            Set Fecha_inicio = %s , Fecha_fin = %s, Hora = %s
            Where Id_tarea = %s
            """
            val = (fecha_ini,fecha_fin,hora,cod_tarea)
            
            self.cursor.execute(sql,val)
        self.connection.commit()

    #Funciones que Devuelven Datos de la DB 

    def Retornar_Credenciales(self,orden):
        sql = """
        SELECT 
        e.Usuario,e.Contrasenia,e.Chat_id 
        FROM Estudiante e 
        {0}""".format(orden)
        self.cursor.execute(sql)
        resultados =  self.cursor.fetchall()
        
        if len(resultados) > 0:
                #Retorna una tupla
                return resultados
        else:
            return []

    def Retornar_Estudiante(self,orden):

        sql = """
        SELECT 
        e.Usuario, e.Nombre, e.Chat_id 
        FROM Estudiante e 
        {0}""".format(orden)

        self.cursor.execute(sql)

        resultados =  self.cursor.fetchall()
        
        if len(resultados) > 0:
                #Retorna una tupla
                
                return resultados
        else:
            return []

    def Retornar_Materias(self,user):
        orden = """
        SELECT m.Nombre 
        From Estudiante e  

        JOIN estudiante_has_tareas_entregar  tl
            ON e.Usuario = tl.Usuario and tl.Usuario = %s

        JOIN tareas_Entregar t
            ON t.Id_Tarea =  tl.Tarea_Id

        JOIN Asignatura m 
            ON m.id_asignatura = t.asignatura_id

        Group by m.id_asignatura
        
        """

        self.cursor.execute(orden,user)

        resultados = self.cursor.fetchall()
        
        if len(resultados) > 0:
            
            return resultados
        else:
            return [] 

    def Retornar_Estudiantes_Tareas(self,user,env,codigoMatera = ""):
        orden = """
        SELECT e.Nombre,e.Chat_id,m.Nombre,t.Nombre, t.Fecha_inicio ,t.Fecha_fin , t.Hora 
        from Estudiante e

        JOIN estudiante_has_tareas_entregar  tl 
            ON e.Usuario = tl.Usuario and tl.Usuario = %s  and tl.Enviado = %s

        JOIN tareas_Entregar t
            ON t.Id_Tarea =  tl.Tarea_id

        JOIN Asignatura m 
            ON m.id_asignatura = t.Asignatura_id
        
        """

        if codigoMatera != "":
            #Si quiere de una materia en especifico
            orden += """and m.Nombre = '{}'""".format(codigoMatera)
            #print(orden)

        values = (user,env)
        self.cursor.execute(orden,values)

        resultados = self.cursor.fetchall()
        
        if len(resultados) > 0:
            
            return resultados
        else:
            print(resultados)
            return []

    def Tarea_Especifica(self,user,env,nombre_materia,nombre_tarea):
        orden = """
        SELECT e.Nombre, e.Chat_id ,m.Nombre ,t.Nombre , t.Fecha_inicio , t.Fecha_fin, t.Hora ,t.enlace
        From Estudiante e  

        JOIN estudiante_has_tareas_entregar  tl 
            ON e.Usuario = tl.Usuario and tl.Usuario = %s

        JOIN tareas_Entregar t
            ON t.Id_tarea =  tl.Tarea_id and t.Nombre = %s

        JOIN Asignatura m 
            ON m.Id_asignatura = t.asignatura_id and m.Nombre = %s
        
        """
        values = (user,nombre_tarea,nombre_materia)

        self.cursor.execute(orden,values)

        resultados = self.cursor.fetchall()
        
        if len(resultados) > 0:
            print(resultados)
            return resultados
        else:
            return []


    #Funciones BD 

    def Guardar(self):
        self.connection.commit()
database =  DataBase()

