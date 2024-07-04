from PyQt5.QtWidgets import QListWidget, QSizePolicy, QApplication
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QSlider, QListWidget, QLineEdit, QAction, QColorDialog
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtCore import QSize, Qt, QUrl, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import os
import subprocess
from tkinter import messagebox
from pytube import *
from interfazReproductor import interfazReproductor
import json
import emoji

class interfazBuscador(interfazReproductor):
    def __init__(self, ventana):
        super().__init__(ventana)
        with open('config.json', 'r') as f:
            self.config = json.load(f)
            colorBuscar = self.config.get('C. Btn. Buscar', '#4CAF50')
            colorDescargar = self.config.get('C. Btn. Descargar', '#2196F3')
            colorBarraBusqueda = self.config.get('C. Barra Busqueda', '#e7e7e7')
            colorLista = self.config.get('C. Lista', '#2B3444')
            colorObjLista = self.config.get('C. Objeto Lista', '#06090B')
            colorHover = self.config.get('C. Sombreado', '#70122A')

        #Buscador de musica:        
        self.entrada = QLineEdit(ventana)
        self.entrada.setGeometry(450, 60, 305, 30)
        self.entrada.setStyleSheet(f"""
                                    background-color: {colorBarraBusqueda};
                                    border: 1px solid #ccc;
                                    border-radius: 10px;
                                    padding-left: 25px; 
                                    font-size: 12px; """)
        self.entrada.addAction(QIcon("_internal/search.png"), QLineEdit.LeadingPosition)
        self.entrada.setPlaceholderText("Buscar...")
        self.entrada.returnPressed.connect(self.buscar)
        
        self.btnDescarga = QPushButton(ventana)
        self.btnDescarga.setGeometry(450, 405, 135, 20)
        self.btnDescarga.setText("Descargar")
        self.btnDescarga.setStyleSheet(f"""
                                        background-color: {colorDescargar}; 
                                        color: black;
                                        border: none;
                                        border-radius: 5px;
                                        font-size: 12px;
                                        font-weight: bold;""")
        self.btnDescarga.clicked.connect(self.descargar)

        self.btnBuscar = QPushButton(ventana)
        self.btnBuscar.setGeometry(620, 405, 135, 20)
        self.btnBuscar.setText("Buscar")
        self.btnBuscar.setStyleSheet(f"""background-color: {colorBuscar}; 
            color: black; 
            border: none;
            border-radius: 5px; 
            font-size: 12px;
            font-weight: bold;""")
        self.btnBuscar.clicked.connect(self.buscar)

        self.videos = QListWidget(ventana)
        self.videos.setGeometry(460, 115, 285, 265)
        self.videos.setStyleSheet(f"""
            QListWidget{{
                background-color: {colorLista};
                border: none;
                border-radius: 20px;
                padding: 10%;
            }}
            QListWidget::item {{
                background-color: {colorObjLista};
                color: #FAEEEF;
                font-size: 5px;
                font-weight: bold;
                border-radius: 8%;
                padding: 3px;
                margin: 2px;
                margin-left: 0px;
                margin-right: 10px;
                width: 35px;
                height: 25px;
            }}
            QListWidget::item:hover {{
                background-color: {colorHover};
                color: #FAEEEF;
            }}
        """)
        self.videos.itemDoubleClicked.connect(self.descargar)
        
    #Logica Buscador:
    def buscar(self):
        max = 10
        #limpia las listas de busquedas anteriores
        self.videos.clear()
        self.listaURL.clear()
        self.listaNombreVideo.clear()
        #raliza la busquda
        s = Search(self.entrada.text())
        count = 0
        for v in s.results:
            #solo mostrara 10 resultados por busqueda
            if count >= max:
                break
            #se añaden los resultados a las listas
            self.videos.addItem(v.title)
            self.listaURL.append(v.watch_url)
            self.listaNombreVideo.append(v.title)
            count += 1
            
    def descargar(self):
        #la musica seleccionada en la lista se almacena en una variable
        #if self.indice == None:
            #messagebox.showwarning(
                    #"Advertencia", "No seleccionaste ninguna cancion para descargar"
                #)
            
        self.indice = self.videos.currentRow().__index__()
        #se obtiene los datos de la musica seleccionada
        yt = YouTube(self.listaURL[self.indice]) 
        #se establece un formato de nombre para que no existan errores de guardado
        nombreCancion = yt.title
        nombreCancion = emoji.replace_emoji(nombreCancion, replace='')
        nombreCancion = nombreCancion.replace('/', '')
        nombreCancion = nombreCancion.replace('|', '-')
        nombreCancion = nombreCancion.replace(',', '#')
        nombreCancion = nombreCancion.replace('.', '_')
        nombreCancion = nombreCancion.replace('*', '')
        nombreCancion = nombreCancion +' '+ yt.author
        print(nombreCancion)

        #si no se ha seleccionado una ruta de descarga, se muestra una ventana emergente
        if not self.obj.getCarpeta():
                messagebox.showwarning(
                    "Advertencia", "Primero selecciona una ruta para descargar las canciones."
                )
        else:
            #se obtiene la ruta seleccionada
            self.ruta = self.obj.getCarpeta()

            # Se obtiene el audio de mayor calidad disponible
            audio_streams = yt.streams.filter(only_audio=True)
            audio_stream = audio_streams.first()
            # se procede con la descarga
            audio_stream.download(output_path= self.ruta, filename=f"{nombreCancion}.{audio_stream.subtype}")
            print(nombreCancion + " descargada correctamente")

            #la descarga se hace en formato mp4 porque es el formato por default de descarga en pytube
            #por lo que se utiliza ffmpeg para realizar la conversion de formatos de mp4 a mp3 y asi lograr
            #que sea un formato legible para el reproductor
            self.convertir(f"{self.ruta}/{nombreCancion}.mp4", f"{self.ruta}/{nombreCancion}.mp3")

    def convertir(self, video, ruta):
        #Comando para la conversion de mp4 a mp3
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", video,
            "-vn",
            "-acodec", "libmp3lame",
            "-ab", "192k",
            "-ar", "44100",
            "-y",
            ruta
        ]
        try:
            #Se ejecuta el comando de ffmpeg
            subprocess.run(ffmpeg_cmd, check=True)
            #se elimina el archivo mp4
            os.remove(video)
            
            #se añade el archivo mp3 a la lista de reproduccion
            self.obj.añadirLista(ruta)
            self.playlist.addItem(self.obj.lista[len(self.obj.lista)-1])
            #confirmacion de que enefecto ya tienes tu rola lista 
            print("Ya chingaste")
        except subprocess.CalledProcessError as e:
            #Fallo. pq? no se xd
            print("Fallo")


    