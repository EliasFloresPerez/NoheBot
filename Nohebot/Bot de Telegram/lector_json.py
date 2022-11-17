import json
from WspUnemi import *
from BaseMySql import *
import re

def Cambiar_nombre_materia(frase):
    new_frase =  frase.split('-')
    
    codigo_materia =  new_frase[0]
    
    #Codigo feo
    codigo_materia = codigo_materia.split(" ")
    codigo_materia = list(map(lambda x : x.capitalize() , codigo_materia))
    codigo = ""
    
    for i in codigo_materia:
        
        try:
            if i[0] != "":
                
                codigo += i[0]
            else:
                
                codigo += i
        except:
            pass
    
    #print(codigo)
    try :
        codigo += "_"+new_frase[-2].strip()+new_frase[-3].strip()
    except:
        pass
    #print(codigo," -> ",new_frase[0])

    
    return codigo,new_frase[0]

def CambiarNombreTarea(frase,Codmateria):

    Nombre_Completo = frase
    frase =  frase.split('-')
    aux = ""
    try:
        if len(frase[1].split(' ')) > 1:
            aux = frase[1].split(' ')
            
            frase = aux[0][0]+aux[1][0]+aux[2][0]+frase[0]
        else:
            frase = frase[1][0] + frase[0]
        
    except:
        frase = frase[0]
    frase = Codmateria+"-"+frase

    #print(frase)
    return frase,Nombre_Completo


#Dios sabes que el codigo que veras a continuacion es una aberracion
#Pero creeme que puse en una balanza mi salud mental y ella peso mas
def Transformar_fecha(Oracion):
    Fecha = []
    meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
    cadena = ""
    
    oracion_split = Oracion.split(' ')
    #print("oracion : ",Oracion)
    
    if len(oracion_split) != 7:
        oracion_split.pop(0)
        
        
   

    Fecha.append(oracion_split[5][:-1])
    Fecha.append(str(meses.index(oracion_split[3])+1))
    Fecha.append(oracion_split[1])
    Fecha.append(oracion_split[-1])

    cadena = Fecha[0]+"-"+Fecha[1]+"-"+Fecha[2]
    
    
    s = re.sub(r'[^0-9:]', '', Fecha[3])

    cadena,s = Fecha_numero(cadena,s)
    return cadena,s

def Fecha_numero(fecha,hora = "0:0"):
    #print("antigua fecha: ",fecha,hora)
    fecha =  fecha.split('-')
    hora  =  hora.split(':')
    a = []
    b = []
    for i in fecha:
        a.append(int(i))
    for i in hora:
        b.append(int(i))
    
    fecha = str(a[0])+"-"+str(a[1])+"-"+str(a[2])
    hora = str(b[0])+":"+str(b[1])
    #print("Nueva fecha: ",fecha,hora)
    return fecha,hora

class Lector_json:
    Nombre  =""
    Usuario = ""
    Archivo = ""
    Diccionario = ""
    Estudiante = ""

    def __init__(self,archivo):
        self.Archivo = archivo
        
        self.AbrirJson()

        if(self.Verificar_Ususario()): #La funcion retornar una valor booleaneo
            self.Recoger_datos()
            database.Guardar()
            
        else:
            print("Usuario no registrado")

    def AbrirJson(self):
        
        
        
        self.Nombre = self.Archivo["Nombre"]
        self.Usuario = self.Archivo["Usuario"]
        self.Diccionario = self.Archivo["Eventos"]
        
            
    
    def Verificar_Ususario(self):
        self.Estudiante =  database.Retornar_Estudiante("Where e.Usuario = '{}'".format(self.Usuario))
        if self.Estudiante != [] :
            return True
        return False


    def Recoger_datos(self):
        
        cod = ""
        nombre = ""
        cod_tarea = ""
        nom_tarea = ""
        fecha_tarea = ""
        hora = ""
        enlace = ""
        for i in self.Diccionario:
            cod,nombre =  Cambiar_nombre_materia(i)
            #En esta parte apareceran las materias
            database.Insertar_Asignatura(cod,nombre)

            for j in self.Diccionario[i]:
                cod_tarea ,nom_tarea= CambiarNombreTarea(j,cod)
                enlace = self.Diccionario[i][j]["Link"]

                if self.Diccionario[i][j]["Tipo Actividad"] == "Tarea":
                    try:
                        fecha_tarea,hora = Transformar_fecha(self.Diccionario[i][j]["Fecha de entrega"])
                    except:
                        fecha_tarea,hora = "2006-6-6","0:0"


                elif self.Diccionario[i][j]["Tipo Actividad"] == "Cuestionario":
                    try:

                        fecha_tarea,hora  = Transformar_fecha(self.Diccionario[i][j]["Estado"])
                    except:
                        try:
                            
                            fecha_tarea,hora  = Transformar_fecha(self.Diccionario[i][j]["Fecha Cierre"])

                        except:
                            fecha_tarea,hora = "2006-6-6","0:0"
                        
            
                elif self.Diccionario[i][j]["Tipo Actividad"] == "Foro":
                    try :
                        print("Foro : ",self.Diccionario[i][j])
                        fecha_tarea,hora  = Transformar_fecha(self.Diccionario[i][j]["Fecha Cierre"])
                    except:
                        fecha_tarea,hora = "2006-6-6","0:0"

                database.Insertar_Tarea(cod_tarea,nom_tarea,cod,"2006-2-6",fecha_tarea,hora,enlace)
                self.Verificar_Tarea(cod_tarea,self.Diccionario[i][j])
                
    
    def Verificar_Tarea(self,CodigoTarea,dic):
        
        Valor_enviado = 1

        if dic["Tipo Actividad"] == "Tarea":

            try:
                if dic["Archivos enviados"] != "-":
                    Valor_enviado = 0
            except:
                pass
            
            
        elif dic["Tipo Actividad"] == "Cuestionario":

            try:
                dic["Estado"]
                Valor_enviado = 0
            except:
                pass

        elif dic["Tipo Actividad"] == "Foro":
            if dic["Realizado"] != "No entregado":
                Valor_enviado = 0


        #print("insertando : ",self.Usuario,CodigoTarea,Valor_enviado)
        database.Insertar_Lista_Estudiante_Tarea(self.Usuario,CodigoTarea,Valor_enviado)

       


