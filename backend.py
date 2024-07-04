from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import os
import random

class backend:
    def __init__(self):
        self.lista = ["XD"]
        self.dir = ""
        self.rutaCarpeta = ""

    #Funciones de botones
    def getLista(self):
        return self.lista

    def gettamañoLista(self):
        return len(self.lista) > 0
    
    def añadirLista(self, ruta):
        self.dir.append(ruta)
        direccion = ruta.split('/')
        nombreCancion = direccion.pop()
        self.lista.append(nombreCancion)
        
    def getCarpeta(self):
        return self.rutaCarpeta

    def selecionarCarpeta(self):
        #si la lista contiene archivos, se limpia y se agrega una nueva carpeta
        if self.gettamañoLista():
            self.lista.clear()
        #Ruta de la carpeta donde se almacenaran las canciones
        ruta = QFileDialog.getExistingDirectory()+"/"
        self.rutaCarpeta = ruta
        musica = []
        if ruta:
            # Filtrar archivos MP3 dentro de la carpeta seleccionada
            mp3_files = [file for file in os.listdir(ruta) if file.endswith(".mp3")]
            #Crea un string con la ruta de cada archivo mp3 y la añade a la lista
            for mp3_file in mp3_files:
                var = ""
                var= f"{ruta}{mp3_file}"
                musica.append(var)

        self.dir = musica
        playList = []
        #Simplifica la ruta a solo el nombre del archivo
        for music in musica:
            direccion = music.split('/')
            nombreCancion = direccion.pop()
            playList.append(nombreCancion)

        self.lista = playList
        print(self.rutaCarpeta)

    def revuelve(self):
        random.shuffle(self.dir)
        playList = []
        #Simplifica la ruta a solo el nombre del archivo
        for music in self.dir:
            direccion = music.split('/')
            nombreCancion = direccion.pop()
            playList.append(nombreCancion)

        self.lista = playList
