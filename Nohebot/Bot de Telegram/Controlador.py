from asyncio import sleep
from datetime import date
from datetime import datetime
from BaseMySql import  *
import os
import time
import random

import queue
import threading

import  lector_json as L
from WspUnemi import *
from escobaUnemiOOP import *
from Seguridad import Encriptar,Desencriptar

Libros = ["📕","📗","📘","📙","📔","📒","📓"]
Tipos_t = ["🔻","⚠","📝","❌"]

     
#que = queue.Queue()
def llenar_base(orden = "",chat_id = ""):
    inicio = time.time()
    th = []
    qu = []
    contador = 0

    mensaje = ""
    contr = ""
    lista = database.Retornar_Credenciales(orden)
    
    if lista == []:
        bot.Enviar_mensaje(chat_id,"<b>No se encuentra registrado con nosotros</b>")
        return
    print("Alguien esta usando escoba ,",lista[0][0])
    for i in lista:
        
        qu.append(queue.Queue())

        contr = Desencriptar(i[1])
  
        try:
            
            thr = threading.Thread(target = lambda q, arg1,arg2 : q.put(Escoba(arg1,arg2).escoba()), args = (qu[contador],i[0],contr))
        except:
            mensaje = "No haga enojar al bot"
            bot.Enviar_mensaje(lista[contador][2],mensaje)
            return
        thr.start()
        th.append(thr)
        contador += 1
    
    #print(th)
    for i in th:
        i.join()
        #print("Termino")
    
    contador = 0;
    for i in qu:
        
        fin = time.time()
        mensaje = "<i>\nProceso terminado \nTiempo total : </i><b>{} Segundos 🕚 </b>".format(round(fin-inicio,2))
        var = i.get()
        
        if var != {}:
            
            L.Lector_json(var)
            
        else :
            
            mensaje = "<i>\nUn proceso rompio la escoba...</i>"

        bot.Enviar_mensaje(lista[contador][2],mensaje)
        contador += 1
        pass

    #print("El proceso  tardo  : ",fin-inicio)
    database.Guardar()

#Controlador de la hora
def Verificador_Hora():
    d = ""
    hora = ""
    while(True):
        d = datetime.now()
        hora = d.strftime('%H:%M')
        d =  d.strftime('%Y-%d-%m')
         
        print("Dia : ",d,"Hora :",hora)
        if(hora == hora):
            #Pedimos a todos los estudiantes
            Estudiantes =  database.Retornar_Estudiante("")
            for i in Estudiantes:
                print(i[2])
                #Hilar(i[2])
                pass
        


        time.sleep(3600)
    
#Hilo
def Hilo():
    th = threading.Thread(target = Verificador_Hora, args = ())
    th.start()
    
def FechaHoy():
    fecha = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M')
    return L.Fecha_numero(fecha,hora)
   
def Condicion_Fecha(tipo,fecha_tarea):
    
    fecha , hora =  FechaHoy()
    fechahoy =  datetime.strptime(fecha, '%Y-%m-%d') 
    fecha_t =  datetime.strptime(fecha_tarea, '%Y-%m-%d')
    diferencia = fecha_t - fechahoy
    fecha_error = datetime.strptime("2006-6-6", '%Y-%m-%d') 

    if tipo == 0:

        if  diferencia.days >= 0:
            return True

    if tipo == 1:

        if fecha ==  fecha_tarea:
            return True
    
    if tipo == 2:
        
        if diferencia.days <= 7  and diferencia.days > 0:
            return True

    if tipo == 3:
        if fecha_error ==  fecha_tarea:
            return True
    
    return False

def Leer_Estudiantes(usuario = "",hoy = 0,materia_esp = 0):
    Lista_Estudiantes = 0
    Lista_Tareas = 0
    Mensaje = ""
    Copia = ""
    fecha , hora =  FechaHoy()
    contador = 0
    Materias = ""
    Materias = []
    Lista_Tareas = []

    try:
        Lista_Estudiantes = database.Retornar_Estudiante("WHERE e.Usuario = '{}'".format(usuario))
        
        Estudiante = Lista_Estudiantes[0]

        Materias =  database.Retornar_Materias(Estudiante[0])
        

        Lista_Tareas = database.Retornar_Estudiantes_Tareas(Estudiante[0],1,Materias[materia_esp][0])

    except :
        #print(Materias,Lista_Tareas)
        print("Error : MATERIAS NO EXISTEN EN ESTE ESTUDIANTE ",usuario)
        pass
    
    #print("XD",Materias)
    if Materias == []:
        
        return -1,-1

    
    tipo = Tipos_t[hoy]
    #Creamos el mensaje
    Mensaje = "\n<b>{0} Pagina {1} de  {2}: </b>".format(tipo,materia_esp+1,len(Materias))
    Mensaje +="\n<b>Buenas 👋 {0}</b>\n<b>Fecha de hoy  : {1}</b>".format(Estudiante[1],fecha)
    Mensaje += "\n<b>🔴 Tareas no enviadas aun</b>"

    #Si el mensaje es con respecto al dia
    if hoy == 1:
        Mensaje += "\n\n<b><u> ⏰ QUE SE PRESENTAN HOY </u></b>📍"
    elif hoy == 2:
        Mensaje += "\n\n<b><u>QUE SE PRESENTAN EN MENOS DE 7 DIAS </u></b>🧩 "
    elif hoy == 3:
        Mensaje += "\n\n<b><u>QUE SE DESCONOCE LA FECHA A PRESENTAR  </u></b>"

    Mensaje += "\n\nMateria -<u><b>{0}</b></u>-".format(Materias[materia_esp][0])


    #Variables utiles
    Copia = Mensaje
    contador = 0

    
    #Vamos guardando las tareas 
    for j in Lista_Tareas:
        
        if Condicion_Fecha(hoy,j[5]):
            contador += 1
            #Solo entrara si no ha sido enviada y es el mismo dia
            Mensaje += "\n\n{0}]{1}|<i>{2}</i>|".format(contador,Libros[random.randint(0,6)],j[3]) 
       
            

    
    if Copia == Mensaje:
        Mensaje += "\n\n<i><b>Felicidades parece que no tienes actividades</b></i>";
    
    
    return Mensaje,contador

def Leer_Tarea(user,env,nombre_m,nombre_t):
    
    usuario= database.Retornar_Estudiante("Where e.Chat_id = '{}'".format(user))
    
    Tarea = database.Tarea_Especifica(usuario[0][0],env,nombre_m,nombre_t)
    
    mensaje = "\n<b>Nombre :</b> <i>{}</i>".format(Tarea[0][3])
    mensaje += "\n<b>Fecha maxima de entrega:</b> <i>{}</i>".format(Tarea[0][5])
    mensaje += "\n<b>Enlace :</b> <i>{}</i>".format(Tarea[0][7])
    return Tarea[0][1],mensaje

def Hilar(chatid):
    
    aid =  "Where e.Chat_id = '{}'".format(chatid)
    
    th = threading.Thread(target = lambda x,y: llenar_base(x,y), args = (aid,chatid))
    th.start()
    return th



if __name__ == "__main__":
    #Leer_Estudiantes("afloresp3",0,0)
    Hilar(1521172028)
    pass

    
   