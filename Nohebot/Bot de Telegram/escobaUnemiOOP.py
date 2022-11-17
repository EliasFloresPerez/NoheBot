from bs4 import BeautifulSoup as bs
from requests import Session
import json 
import warnings 
warnings.filterwarnings("ignore")

class Preparativos:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.url = "https://pregradovirtual.unemi.edu.ec/login/index.php"
        self.jsonOutput = {}
        self.response = {}
        self.linksCalificaciones = []
        self.mainUrl = "https://pregradovirtual.unemi.edu.ec/my/"


    def login(self):
        self.session.verify = False
        site = self.session.get(self.url)
        bsContent = bs(site.content, "html.parser")
        token = bsContent.find("input", {"name":"logintoken"})["value"]
        loginToken = {"username":str(self.user), "password":str(self.password), "logintoken":token}

        
        print(self.session.post(self.url, loginToken))
        

    def formatter(self, keys, valores, curso, nombreActividad, json):
        if curso in json.keys():
            infoExtraJson = dict(zip(keys, valores))
            dictionary = {}
            dictionary[nombreActividad] = infoExtraJson
            json[curso].update(dictionary)
        else:
            infoExtraJson = dict(zip(keys, valores))
            dictionary = {}
            dictionary[nombreActividad] = infoExtraJson
            json[curso] = dictionary
    
        
class Escoba(Preparativos):
    def __init__(self, user, password):
        
        super().__init__(user, password)
        self.session = Session()
        self.login() #tambien puede estar dentro de cada funcion en caso de que existan problemas de logout
        self.linkGetter()
    
    def linkGetter(self):
        htmlMain = self.session.get(self.mainUrl)
        soup = bs(htmlMain.content, "lxml")
        links = soup.find_all("a", class_="list-group-item-action")
        for link in links:
            if "course" in link["href"]:
                htmlCurso = self.session.get(link["href"])
                soup = bs(htmlCurso.content, "lxml")
                linksCurso = soup.find_all("a", class_="list-group-item-action")
                for linkCalificaciones in linksCurso:
                    if "grade" in linkCalificaciones["href"]:
                        self.linksCalificaciones.append(linkCalificaciones["href"])
                    else:
                        pass
            else:
                pass
    

    def escoba(self,i  = 0):
        nombreUsuario = "" 
        for linkCalificaciones in self.linksCalificaciones:
            htmlCalificaciones = self.session.get(linkCalificaciones)
            soup = bs(htmlCalificaciones.content, "lxml")
            nombreMateria = soup.find("h1").get_text()
            nombreUsuario = soup.find("span", "usertext").get_text()

            if(i == 1):
                self.response["Nombre"] = nombreUsuario
                return self.response

            linksActividades = soup.find_all("a", class_="gradeitemheader")
            for link in linksActividades:
                alts = link.find_all("img", class_="itemicon")
                tipoActividad = alts[0]["alt"]
                linkActividad = link["href"]
                htmlActividad = self.session.get(linkActividad)
                soup = bs(htmlActividad.content, "html.parser")
                try :
                    nombreTarea = soup.find("h2").get_text()
                except :
                    print(self.response)
                    return self.response
                infoHead = ["Link", "Tipo Actividad"]
                infoData = [linkActividad, tipoActividad]
                try:
                    if tipoActividad == "Tarea":
                        infoExtraHead = soup.find_all("th", "c0")
                        infoExtraData = soup.find_all("td", "lastcol")
                        for head, data in zip(infoExtraHead, infoExtraData):
                            infoHead.append(head.get_text())
                            infoData.append(data.get_text())
                        self.formatter(infoHead, infoData, nombreMateria, nombreTarea, self.jsonOutput)
                    elif tipoActividad == "Cuestionario":
                        infoExtra = soup.find("div", "quizinfo")
                        filas = infoExtra.find_all("p")
                        if "cerró" in filas[1].get_text() or "cerró" in filas[0].get_text() :
                            fechaCierreTest = filas[1].get_text().split(",",1)[1]
                            infoExtraTestHead = soup.find_all("th", "header")
                            infoExtraTestData = soup.find_all("td", "cell")
                            for head, data in zip(infoExtraTestHead, infoExtraTestData):
                                infoHead.append(head.get_text())
                                infoData.append(data.get_text())
                            self.formatter(infoHead, infoData, nombreMateria, nombreTarea, self.jsonOutput)
                        elif "estará" in filas[1].get_text():
                            fechasAbreCierre = []
                            infoHead = ["Link", "Tipo Actividad", "Fecha Inicio", "Fecha Cierre"]
                            fechasAbreCierre.append(linkActividad)
                            fechasAbreCierre.append(tipoActividad)
                            
                            fechasAbreCierre.append(filas[1].get_text().split(",", 1)[1])
                            fechasAbreCierre.append(filas[2].get_text().split(",", 1)[1])
                            self.formatter(infoHead, fechasAbreCierre, nombreMateria, nombreTarea, self.jsonOutput)
                        else:
                            fechasAbreCierre = []
                            infoHead = ["Link", "Tipo Actividad", "Fecha Inicio", "Fecha Cierre"]
                            fechasAbreCierre.append(linkActividad)
                            fechasAbreCierre.append(tipoActividad)
                            
                            try:
                                fechasAbreCierre.append(filas[1].get_text().split(",", 1)[1])
                                fechasAbreCierre.append(filas[2].get_text().split(",", 1)[1])
                            except:
                                fechasAbreCierre.append(filas[1].get_text().split(",", 1)[0])
                                fechasAbreCierre.append(filas[2].get_text().split(",", 1)[0])
                            self.formatter(infoHead, fechasAbreCierre, nombreMateria, nombreTarea, self.jsonOutput)
                    elif tipoActividad == "Foro":
                        nombresForos = []
                        fechasHeader = ["Link", "Tipo Actividad", "statusTarea", "Realizado", "Fecha Inicio", "Fecha Fin"]
                        fechasInicioFin = []
                        posts = soup.find_all("div", class_="forumpost")
                        for post in posts:
                            nombresForos.append(post['aria-label'].split('por')[-1].strip())
                        fechaFinal = soup.find("div", "alert-block").get_text().split(",", 1)[1].strip()
                        if "no" in fechaFinal:
                            status = "Cerrado"
                        else:
                            status = "Abierto"
                        try:
                            fechaInicio = soup.find("time").get_text().split(",", 1)[1].strip()
                        except:
                            fechaInicio = soup.find("time").get_text().strip()
                        fechasInicioFin.append(linkActividad)
                        fechasInicioFin.append(tipoActividad)
                        fechasInicioFin.append(status)
                        if nombreUsuario in nombresForos:
                            fechasInicioFin.append("Entregado")
                        else:
                            fechasInicioFin.append("No entregado")
                        fechasInicioFin.append(fechaInicio)
                        fechasInicioFin.append(fechaFinal)

                        self.formatter(fechasHeader, fechasInicioFin, nombreMateria, nombreTarea, self.jsonOutput)
                        
                except:
                    print("dios mio santo no")



                    pass
        self.response["Nombre"] = nombreUsuario
        self.response["Usuario"] = self.user
        self.response["Eventos"] = self.jsonOutput
        return self.response

        

if (__name__ == "__main__"):
    escoba = Escoba("Cveraq", "Primavera2")
    output = escoba.escoba()
    with open("output.json", "w" ,encoding="utf-8") as file:
        jsonString = json.dump(output, file, ensure_ascii=False , indent=4)

