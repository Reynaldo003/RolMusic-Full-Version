from PyQt5.QtWidgets import QListWidget, QSizePolicy, QApplication
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QSlider, QListWidget, QLineEdit, QAction, QColorDialog
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtCore import QSize, Qt, QUrl, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from tkinter import messagebox
from backend import backend
from interfazCompartida import interfazCompartida
import json
import random

class interfazReproductor(interfazCompartida):

    obj = backend()

    def __init__(self, ventana):
        super().__init__(ventana)
        self.play = QMediaPlayer()
        self.play.setVolume(50)
        self.play.positionChanged.connect(self.segundos)
        self.play.mediaStatusChanged.connect(self.terminoCancion)
        self.indice = None
        self.maximo = 0
        self.ruta = ""

        with open('config.json', 'r') as f:
            self.config = json.load(f)
            anterior = self.config.get('anterior', 'internal/anterior1.svg')
            carpeta = self.config.get('carpeta', 'internal/carpeta1.svg')
            mutear = self.config.get('mutear', 'internal/mute1.svg')
            pausa = self.config.get('pausa', '_internal/pausa1.svg')
            play = self.config.get('play', '_internal/play1.svg')
            ruido = self.config.get('ruido', '_internal/ruido1.svg')
            siguiente = self.config.get('siguiente', '_internal/siguiente1.svg')
            aleatorio = self.config.get('aleatorio', '_internal/aleatorio1.svg')
            colorSlider = self.config.get('C. Lista', '#2B3444')
            colorPerilla = self.config.get('C. Sombreado', '#70122A')

        #Elementos de la interfaz grafica (Botones, Listas, Sliders, Etiquetas, imagenes)
        self.btnCarp = QPushButton(ventana)
        self.btnCarp.setGeometry(90, 450, 45, 45)
        self.btnCarp.setIcon(QIcon(carpeta))
        self.btnCarp.setIconSize(QSize(45, 45))
        self.btnCarp.setStyleSheet("""border-radius: 100%""")
        self.btnCarp.clicked.connect(self.llenarLista)

        self.btnAnt = QPushButton(ventana)
        self.btnAnt.setGeometry(140, 440, 65, 65)
        self.btnAnt.setIcon(QIcon(anterior))
        self.btnAnt.setIconSize(QSize(65, 65))
        self.btnAnt.setStyleSheet("""border: none;
                                   border-radius: 100%""")
        self.btnAnt.clicked.connect(self.anterior)

        self.btnSig = QPushButton(ventana)
        self.btnSig.setGeometry(280, 440, 65, 65)
        self.btnSig.setIcon(QIcon(siguiente))
        self.btnSig.setIconSize(QSize(65, 65))
        self.btnSig.setStyleSheet("""border: none;
                                   border-radius: 100%""")
        self.btnSig.clicked.connect(self.siguiente)

        self.btnAlatorio = QPushButton(ventana)
        self.btnAlatorio.setGeometry(350, 450, 45, 45)
        self.btnAlatorio.setIcon(QIcon(aleatorio))
        self.btnAlatorio.setIconSize(QSize(45, 45))
        self.btnAlatorio.setStyleSheet("""border: none;
                                   border-radius: 100%""")
        self.btnAlatorio.clicked.connect(self.revolver)

        self.btnPausa = QPushButton(ventana)
        self.btnPausa.setGeometry(210, 440, 65, 65)
        self.btnPausa.setIcon(QIcon(pausa) )
        self.btnPausa.setIconSize(QSize(65, 65))
        self.btnPausa.setStyleSheet("""border: none;
                                   border-radius: 100%""")
        self.btnPausa.clicked.connect(self.pausa)

        self.btnRepro = QPushButton(ventana)
        self.btnRepro.setGeometry(210, 440, 65, 65)
        self.btnRepro.setIcon(QIcon(play) )
        self.btnRepro.setIconSize(QSize(65, 65))
        self.btnRepro.setStyleSheet("""border: none;
                                   border-radius: 100%""")
        self.btnRepro.clicked.connect(self.repr)
        
        self.btnMutear = QPushButton(ventana)
        self.btnMutear.setGeometry(30, 335, 45, 45)
        self.btnMutear.setIcon(QIcon(mutear) )
        self.btnMutear.setIconSize(QSize(45, 45))
        self.btnMutear.setStyleSheet("""border: none;
                                    border-radius: 100%""")
        self.btnMutear.clicked.connect(self.silenciar)

        self.btnMaxVol = QPushButton(ventana)
        self.btnMaxVol.setGeometry(30, 60, 45, 45)
        self.btnMaxVol.setIcon(QIcon(ruido) )
        self.btnMaxVol.setIconSize(QSize(45, 45))
        self.btnMaxVol.setStyleSheet("""border: none;
                                   border-radius: 100%""")
        self.btnMaxVol.clicked.connect(self.volMax)

        self.sliderVol = QSlider(Qt.Orientation.Vertical, ventana)
        self.sliderVol.setGeometry(45,120, 12, 200)
        self.sliderVol.setMinimum(0)
        self.sliderVol.setMaximum(100)
        self.sliderVol.setValue(50)
        self.sliderVol.setStyleSheet(f"""
            QSlider::groove:vertical {{
                background: {colorSlider};
                width: 10px;
                border-radius: 5px;
            }}
            
            QSlider::handle:vertical {{
                background: {colorPerilla};
                height: 10px;
                border-radius: 5px;
            }}
        """)
        self.sliderVol.valueChanged.connect(self.volumen)

        self.sliderTiem = QSlider(Qt.Orientation.Horizontal, ventana)
        self.sliderTiem.setGeometry(130, 410, 225, 12)
        self.sliderTiem.setMinimum(0)
        self.sliderTiem.setValue(0)
        self.sliderTiem.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: {colorSlider};
                height: 12px;
                border-radius: 6px;
            }}
            
            QSlider::handle:horizontal {{
                background: {colorPerilla};
                width: 12px;
                height: 12px;
                border-radius: 6px;
            }}
        """)
        self.sliderTiem.setTickInterval(1000)
        self.sliderTiem.sliderMoved.connect(self.duracion)

        self.playlist.itemDoubleClicked.connect(self.repr)
        
        #Tiempo de reproduccion
        self.etqTiempoPos = QLabel(ventana)
        self.etqTiempoPos.setGeometry(90, 405, 30, 20)
        self.etqTiempoPos.setStyleSheet("color: white;")
        self.etqTiempoPos.setText("00:00")

        #Duracion de la cancion
        self.etqTiempoDur = QLabel(ventana)
        self.etqTiempoDur.setGeometry(365, 405, 30, 20)
        self.etqTiempoDur.setStyleSheet("color: white;")
        self.etqTiempoDur.setText("00:00")
        self.index = 0

    def repr(self):
        #Se obtiene la ruta de la cancion seleccionada por el mouse o presionando el boton
        #E inicia la reproduccion de la misma
        if len(self.obj.dir) == 0:
            messagebox.showwarning(
                "Advertencia", "No seleccionaste una carpeta con canciones"
            )
        else:
            if self.play.state() == self.play.State.PausedState and self.playlist.selectedItems():
                self.play.play()
                self.btnRepro.hide()
                self.btnPausa.show()
            else:
                self.maximo = len(self.obj.dir)
                self.play.setMedia(QMediaContent(QUrl.fromLocalFile(self.obj.dir[self.playlist.currentRow().__index__()])))
                self.index = self.playlist.currentRow().__index__()
                self.play.play()
                self.btnRepro.hide()
                self.btnPausa.show()

    def revolver(self):
        self.obj.revuelve()

        if self.obj.gettamañoLista():
            self.playlist.clear()
        #Se añade la lista al elemento visual
        self.playlist.addItems(self.obj.getLista())

    def llenarLista(self):
        #Si existe una reproduccion se detiene para que no suene mientra se eligen nuevas canciones
        print("entro")
        if self.play.state() == 1:
            self.play.stop()
        #Cuadro de dialogo que selecciona los archivos mp3
        self.obj.selecionarCarpeta()

        #Se establece la ruta de guardado de archivos mp3
        self.ruta = self.obj.getCarpeta()
        print(self.ruta)
        if not self.ruta:
            return
        else:
            self.ruta = list(self.ruta)[0]
        #Si ya existen canciones en la lista de reproduccion se eliminan y añaden la nueva seleccion
        if self.obj.gettamañoLista():
            self.playlist.clear()
        #Se añade la lista al elemento visual
        self.playlist.addItems(self.obj.getLista())

    def siguiente(self):
        self.maximo = len(self.obj.dir)
        self.index = self.index + 1
        if not self.obj.dir:
            return
        elif self.index == self.maximo:
            self.index = 0
            self.play.setMedia(QMediaContent(QUrl.fromLocalFile(self.obj.dir[self.index])))
        elif self.index <= self.maximo:
            self.play.setMedia(QMediaContent(QUrl.fromLocalFile(self.obj.dir[self.index])))
        self.play.play()

    def anterior(self):
        self.index = self.index - 1
        if not self.obj.dir:
            return
        elif self.index <= -1:
            self.index = len(self.obj.dir)-1
            self.play.setMedia(QMediaContent(QUrl.fromLocalFile(self.obj.dir[self.index])))
        else:
            self.play.setMedia(QMediaContent(QUrl.fromLocalFile(self.obj.dir[self.index])))
        self.play.play()

    def pausa(self):
        #Si existe una reproduccion se pausa la cancion
        if self.play.state() == self.play.State.PlayingState:
            self.play.pause()
            self.btnRepro.show()
            self.btnPausa.hide()

    def terminoCancion(self, estado):
        #Verifica si la reproduccion de un archivo mp3 termino y pasa a la siguiente cancion en la lista
        if estado == QMediaPlayer.MediaStatus.EndOfMedia:
            self.siguiente()

    def volumen(self, valor):
        #Slider del volumen
        self.play.setVolume(valor)

    def duracion(self, valor):
        #Slider de la duracion de la cancion
        self.play.setPosition(valor)

    def segundos(self, seg):
        #Tiempo actual de reproduccion
        self.sliderTiem.setValue(seg)
        self.sliderTiem.setMaximum(self.play.duration())
        minutes = seg / 60000
        seconds = (seg / 1000) % 60
        self.etqTiempoPos.setText(f"{int(minutes):02d}:{int(seconds):02d}")

        #Tiempo total de la duracion de la cancion
        duracion = self.play.duration()
        segundos = duracion // 1000  # Convertir la duración a segundos
        duracion = QTime(0, (segundos // 60) % 60, segundos % 60)
        self.etqTiempoDur.setText(duracion.toString("mm:ss"))

    def silenciar(self):
        self.sliderVol.setValue(0)

    def volMax(self):
        self.sliderVol.setValue(100)