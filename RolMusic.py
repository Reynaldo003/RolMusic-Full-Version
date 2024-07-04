#Esta es una sgunda version del reproductor de musica con pyqt5
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QSlider, QListWidget, QLineEdit, QAction, QColorDialog
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtCore import QSize, Qt, QUrl, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from backend import backend
from tkinter import messagebox
import os
import subprocess
from pytube import *

class MiVentana(QMainWindow):
        def __init__(self):
            super().__init__()
        # Acción para la opción de sugerencias
            sugerencias_action = QAction('Sugerencias', self)
            sugerencias_action.setStatusTip('Enviar sugerencias')
            sugerencias_action.triggered.connect(self.mostrarSugerencias)

            # Acción para la opción de customización del diseño
            customizacion_action = QAction('Customización del diseño', self)
            customizacion_action.setStatusTip('Personalizar el diseño de la aplicación')
            customizacion_action.triggered.connect(self.mostrarCustomizacion)

            # Creamos la barra de menú
            menubar = self.menuBar()
            menubar.setStyleSheet("""
                                QMenuBar {
                                    background-color: #2B3444;
                                    color: white;
                                    padding: 5px; }
                            
                                QMenuBar::item:selected {
                                    background-color: #70122A;
                                    color: #FAEEEF;
                                    border-radius: 5px;}""")
            
            archivo_menu = menubar.addMenu('&Contacto')
            archivo_menu.addAction(sugerencias_action)

            # Creamos un menú adicional
            opciones_menu = menubar.addMenu('&Opciones')
            opciones_menu.addAction(customizacion_action)

        def mostrarSugerencias(self):
            # Método para mostrar las sugerencias (aquí puedes implementar la lógica para mostrar la ventana de sugerencias)
            print('Mostrando la ventana de sugerencias...')

        def mostrarCustomizacion(self):
            # Método para mostrar la customización del diseño (aquí puedes implementar la lógica para mostrar la ventana de customización)
            # Método para mostrar la ventana emergente con opciones de apariencia
            color = QColorDialog.getColor()
            if color.isValid():
                print('Color seleccionado:', color.name())

                self.videos.setStyleSheet(f"""QListWidget{{
                                            background-color: {color.name()};
                                            border: none;
                                            border-radius: 20px;
                                            padding: 10%;
                                            }}

                                        QListWidget::item {{
                                            background-color: #06090B;
                                            color: #8DB1DE;
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
                                            background-color: #70122A;
                                            color: #FAEEEF;}}""")

        #Enlaces de creador:
        def gitPagina(self):
            QDesktopServices.openUrl(QUrl("https://github.com/Reynaldo003"))

        def donaPagina(self):
            print("Paypal")

        def soporte(self):
            print("Crack")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = backend()
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())

