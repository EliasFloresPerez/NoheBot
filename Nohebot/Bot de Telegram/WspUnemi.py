from importlib.metadata import entry_points
import requests
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext import ConversationHandler , CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply


from telegram import (ParseMode)

from Seguridad import Encriptar,Desencriptar
from BaseMySql import  *
from escobaUnemiOOP import *
import Controlador as c  


INPUT_TEXT = 0
class NoheBot:
	#Atributos
	if True:
		token = '5568451985:AAHIANb-W1Shq_qe8DIwB4jrLUi1LIXEglU'
	
	method = 'sendMessage'
	updater = Updater(token, use_context=True)
	
	def __init__(self):
		pass

	#Funciones de comandos
	def start(self,update: Update, context: CallbackContext):
		
		
		update.message.reply_text(
			"""\
				Escriba <b>/help</b> para conocer los comandos disponibles
			""",parse_mode=ParseMode.HTML)
		self.Botones_Teclado(update,context)
	def help(self,update: Update, context: CallbackContext):

		update.message.reply_text("""
		<b>Comandos disponibles  : </b>\
		\n<b>/Registrar</b> \
		\nINSTRUCCIONES : Digite el comando -> /Registrar seguido de su\
		usuario y contraseña del pregrado separado por un espacio
		\n<b>/Creditos</b> [Acerca de nostros]\
		

		""",parse_mode=ParseMode.HTML)


	#Filtros de tareas
	def Tareas(self,update: Update, context: CallbackContext,num = 0,boo = True,tipo = 0):
		
		aux =   database.Retornar_Estudiante("Where e.Chat_id = '{}'".format(update.message.chat_id))

		if aux == []:
			self.Enviar_mensaje(update.message.chat_id,"Para poder usar este comando primero debes registrarte")
			return 
		
		keyboard = [[InlineKeyboardButton(" ⬅ ", callback_data = "Anterior"),
		InlineKeyboardButton("  ❌  ", callback_data = "Cerrar"),
		InlineKeyboardButton(" ➡ ", callback_data = "Siguiente")],
		]
		
		reply_markup2 = InlineKeyboardMarkup(keyboard)

		
		mensaje,contador = c.Leer_Estudiantes(aux[0][0],tipo,num)

		if mensaje == -1 :
			self.Enviar_mensaje(update.message.chat_id,"No se encontraron materias y tareas aun...")
			return
		valor_num = -1
		
		#[InlineKeyboardButton(" {} ".format(i+1), callback_data = "numero")]
		for i in range(contador):
			if i % 5 == 0:
				valor_num += 1
				keyboard.insert(valor_num,[])
			keyboard[valor_num].append(InlineKeyboardButton(" {} ".format(i+1), callback_data = "Numero:{}".format(i+1)))
			#Creamos un boton para tareas en un maximo de 5 por array
		#print(keyboard)
		#print(mensaje)

		if mensaje == -1:
			reply_markup2 = InlineKeyboardMarkup([]) #Sacamos los botones
			mensaje = "<i>Aun no se encontraron tareas registradas...</i>"

		if boo :
			update.message.reply_text(mensaje,reply_markup=reply_markup2,parse_mode=ParseMode.HTML)
		else:
			try :
				update.edit_message_text(mensaje,reply_markup=reply_markup2,parse_mode=ParseMode.HTML)
			except:
				pass

	def TareasHoy(self,update: Update, context: CallbackContext):
		self.Tareas(update,context,0,True,1)

	def TareasSemana(self,update: Update, context: CallbackContext):
		self.Tareas(update,context,0,True,2)

	def TareasError(self,update: Update, context: CallbackContext):
		self.Tareas(update,context,0,True,3)
	#Recogedor de Tareas
	def Escoba(self,update: Update, context: CallbackContext):
		keyboard = [[InlineKeyboardButton("Comenzar ", callback_data = "Comenzar")],
		[InlineKeyboardButton("❌", callback_data = "Cerrar")]]
		
		reply_markup2 = InlineKeyboardMarkup(keyboard)

		
		update.message.reply_text('''
		\n⏫Puede tardar 1 minuto en recoger los datos 🕔 
		\n Aprete Comenzar para que el bot empiece  ✅
		\n🚨RECUERDE QUE ESTA ACCION CERRARA SU SESION EN EL PREGRADO Y EVITE ENTRAR HASTA QUE EL BOT TERMINE🚨
		''',reply_markup=reply_markup2)
		


	# Funcion coge usuario y contraseña llama a escoba unemi 
	def Registrar(self,update: Update, context: CallbackContext):
		mensaje  = update.message.text
		#print(mensaje)
		#context.bot.send_message(update.message.chat_id, "{}".format(update.message.chat_id), parse_mode=ParseMode.HTML)
		try:
			datos = mensaje[11:].split(' ')
			update.message.reply_text('''
							En proceso... ''')
			database.Guardar()
			print("Alguien se esta registrando")
			#print("Usuario :{0}, Contra : {1} ".format(datos[0],datos[1]))
			escoba = Escoba(datos[0],datos[1])
			escoba = escoba.escoba(1)
		except:
			update.message.reply_text('''
							Error digite Registar con sus datos alado ''')
			database.Guardar()
			return
		
		if escoba['Nombre']!= '':
			
			try:
				datos[1] =  Encriptar(datos[1])
				print(datos[1])
				if database.Insertar_Estudiante(datos[0],datos[1],escoba['Nombre'],update.message.chat_id) != -1:

					update.message.reply_text('''
							Registrado correctamente!" Bienvenido\
							\n \
							''')
					database.Guardar()
					
				else:
					0/0
			except:
				update.message.reply_text('''
						Usuario ya registrado...''')
		else:
			update.message.reply_text('''
					Error de inicio de secion\nUsuario o contraseña invalidas''')
			database.Guardar()
			
	#Mostrar los creditos
	def Creditos(self,update: Update, context: CallbackContext):
		#Botones inline
		# InlineKeyboardMarkup -> objeto que recibe un json o arreglo de arreglos
		# InlineKeyboardButton -> Objeto que como parametros recibe el nombre del boton y la url que redirecciona
		#recibe mas parametros segun la ocacion callbackcontext manda a llamar un comando de la clase handler
		# reply_markup = reply_markup2 -> Recibe un objeto de este tipo en el mensaje enviado para poner los botones 
		# abajo
		#keyboard ->Variable usada para guardar la lista de listas 
		keyboard = [
			[InlineKeyboardButton("Elias ", url = "https://www.instagram.com/elias_flores_perez/"),
			InlineKeyboardButton("Raul", url ="https://www.instagram.com/ranford56/" )],

			[InlineKeyboardButton("Melanie ", url = "https://instagram.com/melanieandradv?igshid=YmMyMTA2M2Y=" ),
			InlineKeyboardButton("Nohely ", url = "https://instagram.com/nohely_bodniza?igshid=YmMyMTA2M2Y=" )],

			[InlineKeyboardButton("Joseph ", url = "https://www.facebook.com/joseph.guashpaastudillo" ),
			InlineKeyboardButton("Joel ", url = "https://instagram.com/joelderkz?igshid=YmMyMTA2M2Y=" )],

			[InlineKeyboardButton(" YOUTUBE ▶ Phd Richar Ramirez  ", url = "https://www.youtube.com/channel/UCbXZ2RoQ2SNYZd1Jtx3V9fQ" )],
			[InlineKeyboardButton("❌", callback_data = "Cerrar")]
			]

		reply_markup2 = InlineKeyboardMarkup(keyboard)

		update.message.reply_text("""
		<b>Acerca de nosotros</b>
		.: <i>Elias   Flores  </i>       🐣 
		.: <i>Raul    Garcia  </i>       🐄	  
		.: <i>Nohely  Bodniza </i>   ⚖ 
		.: <i>Melanie Andrade </i>  🌈	  
		.: <i>Joseph  Guashpa </i>🃏	 
		.: <i>Joel    Arrobo  </i>       🇪🇸 
		Con la ayuda del Phd <u><b>RICHARD RAMIREZ ANORMALIZA</b></u>
		Agradecimientos a la Directora <u>Ing. Mirella</u> y a la FACI
		""",parse_mode=ParseMode.HTML,reply_markup=reply_markup2)
	
	#Para tratar con mensajes que no son comandos
	def unknown(self,update: Update, context: CallbackContext):

		
		update.message.reply_text(
			"Losiento '%s' no es un comando valido" % update.message.text)

	def unknown_text(self,update: Update, context: CallbackContext):

		if(update.message.text == 'Tareas' ):
			self.Tareas(update,context)
		elif update.message.text == 'Tareas Hoy':
			self.Tareas(update,context,0,True,1)
		elif update.message.text == 'Tareas Semana':
			self.Tareas(update,context,0,True,2)
		elif update.message.text == 'Escoba':
			self.Escoba(update,context)
		elif update.message.text =='Mostrar Menu ⬆':
			self.Botones_Teclado(update,context,1)
		elif update.message.text =='Ocultar Menu ⬇':
			self.Botones_Teclado(update,context,0)
		elif update.message.text =='Tareas Error':
			self.TareasError(update,context)
		else:
			update.message.reply_text(
				"Losiento no puedo reconocer este mensaje '%s'" % update.message.text)


	#Poder enviar mensajes a un cierto chat
	def Enviar_mensaje(self,chat_id,mensaje):
		response = requests.post(
			url='https://api.telegram.org/bot{0}/{1}'.format(self.token, self.method),
			data={'chat_id': chat_id, 'text':"{0}".format(mensaje),'parse_mode' : ParseMode.HTML}
		).json()

	#Funciones de los botones
	def Botones_basicos(self,update, context):
		query = update.callback_query
		query.answer()

		mensaje = query["data"]

		idc = query.message.chat_id #message.chat_id
		if mensaje == "Comenzar":
			
			c.Hilar(idc) 
			
			try:
				query.edit_message_text(text = "<i>Comenzando proceso...⏳⌛</i>",parse_mode=ParseMode.HTML)
			except:
				query.edit_message_text(text = "<i>Proceso abortado por activar escoba mas de una vez...⏳⌛</i>",parse_mode=ParseMode.HTML)
		elif mensaje == "Cerrar":
			update.callback_query.delete_message()


	def Botones_Movilidad(self,update, context):
		#Preguntar cual fue el boton
		#print(update.callback_query)
		query = update.callback_query
		query.answer()

		mensaje = query["data"]
		idc = query.message.chat_id #message.chat_id
		numero = query["message"]["text"].split(" ")
		tipo = numero[0]
		
		try :
			numero =  int(numero[2])
		except:
			numero = 0
		usuario =  database.Retornar_Estudiante("Where e.Chat_id = '{}'".format(idc))[0]
		
		Tipos_t = ["🔻","⚠","📝","❌"]
		tipo =  Tipos_t.index(tipo)

		total_materias = database.Retornar_Materias(usuario[0])
		total_materias = len(total_materias)
		

		if mensaje == "Siguiente":
			if numero > total_materias-1:
				numero = 0
			
			self.Tareas(query,context,numero,False,tipo)

		elif mensaje == "Anterior":
			numero -=2 
			if numero < 0 :
				numero = total_materias-1
			
			self.Tareas(query,context,numero,False,tipo)
		

	def Botones_Numeros(self,update, context):
		query = update.callback_query
		query.answer()
		
		mensaje = query["data"]
		mensaje = mensaje.split(":")[1]
		mensaje = int(mensaje)
		
		idc = query.message.chat_id #message.chat_id
		tarea = query["message"]["text"].split("|")
		tarea.pop(0)
		tareas = []

		materia = query["message"]["text"].split("-")
		#Mejorar
		for i in range(len(tarea)):
			if i % 2 == 0:
				tareas.append(tarea[i])

		#print(materia[3])
		idc,mensaje = c.Leer_Tarea(idc,1,materia[3],tareas[mensaje - 1])
		self.Enviar_mensaje(idc,mensaje)

	def Botones_Teclado(self,update, context,show = 0):
		keyboard = ""
		if(show == 1):
			keyboard = [['Tareas', 'Tareas Hoy'],['Tareas Semana','Tareas Error'],['Escoba'],['Ocultar Menu ⬇']]
		else:
			keyboard = [['Mostrar Menu ⬆']]
		reply_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True,resize_keyboard=True)
		message = "Ok "
		update.message.reply_text(message, reply_markup=reply_markup)
	
	def input_text(self,update: Update, context: CallbackContext):
		#No se que hace pero si lo borro se muere
		print("Hola",ConversationHandler)
		return ConversationHandler.END


	#Bucle del bot 
	def Iniciar(self):
		print("Iniciado")
		c.Hilo()
		
		#Comandos
		self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
		self.updater.dispatcher.add_handler(CommandHandler('help', self.help))
		self.updater.dispatcher.add_handler(CommandHandler('Registrar', self.Registrar))
		self.updater.dispatcher.add_handler(CommandHandler('Creditos', self.Creditos))
		
		self.updater.dispatcher.add_handler(CommandHandler('Tareas', self.Tareas))
		self.updater.dispatcher.add_handler(CommandHandler('TareasHoy', self.TareasHoy))
		self.updater.dispatcher.add_handler(CommandHandler('TareasSemana', self.TareasSemana))
		self.updater.dispatcher.add_handler(CommandHandler('TareasError', self.TareasError))
		self.updater.dispatcher.add_handler(CommandHandler('Escoba', self.Escoba))
		self.updater.dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))
		self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.unknown_text))

		#Respuestas de botones para
		self.updater.dispatcher.add_handler(ConversationHandler(
			entry_points = [
				
				CallbackQueryHandler(pattern =  'Cerrar' , callback =  self.Botones_basicos),
				CallbackQueryHandler(pattern =  'Comenzar' , callback =  self.Botones_basicos),
				CallbackQueryHandler(pattern =  'Anterior' , callback =  self.Botones_Movilidad),
				CallbackQueryHandler(pattern =  'Siguiente' , callback =  self.Botones_Movilidad),
				CallbackQueryHandler(pattern =  r'Numero:[0-9]*' , callback =  self.Botones_Numeros)
			],
			states = {
				INPUT_TEXT : [MessageHandler(Filters.text,self.input_text)]
			},
			fallbacks = []
		))

		
		#Bucle ""
		
		self.updater.start_polling()
		


bot = NoheBot()

if (__name__ == "__main__"):
	bot.Iniciar()
	


