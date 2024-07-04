import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QStatusBar, QPushButton, QSlider, QListWidget, QLineEdit, QAction, QColorDialog
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtCore import QSize, Qt, QUrl, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
# Importar la clase ColorCustomizationWindow
from editarColor import cambiarColor
from agradecimientos import agradec
from tkinter import messagebox

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        # Reproductor
        self.setWindowTitle("RolMusic")
        self.setGeometry(100, 100, 785, 550)
        self.setFixedSize(800, 550)

        # Cargar el color de fondo desde el archivo JSON
        with open("config.json", "r") as f:
            self.config = json.load(f)
            colorFondoVentana = self.config.get("C. Fondo", "#3D4395")
            colorBarraMenu = self.config.get("C. Barra Menu", "#2B3444")
            colorLista = self.config.get('C. Lista', '#2B3444')
            colorObjLista = self.config.get('C. Objeto Lista', '#06090B')
            colorHover = self.config.get('C. Sombreado', '#70122A')

        self.setWindowIcon(QIcon("_internal/rolmusic.ico"))
        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {colorFondoVentana};
            }}
            QScrollBar:vertical {{
                border: 1px solid red;
                background: #2B3444;
                width: 10px;
                height: 15px;
                margin: 22px 0 22px 0;
            }}
            QScrollBar::handle:vertical {{
                background: #9B2B40;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #70122A;
            }}
            QScrollBar::add-line:vertical {{
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}
            QScrollBar::sub-line:vertical {{
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            QDialog {{
                background-color: {colorFondoVentana};
            }}
            QComboBox {{
                color: white;
                background-color: {colorLista}; 
                border: 1px solid #000000;
                border-radius: 5px; 
                padding: 3px 20px 3px 5px; 
                selection-background-color: {colorHover};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: {colorLista};
                border-left-style: solid;
                border-top-right-radius: 3px; 
                border-bottom-right-radius: 3px;
            }}
            QComboBox::hover {{
                background-color: {colorHover};
            }}

            QComboBox QAbstractItemView {{
                background-color: {colorObjLista};
                color: white; 
                selection-background-color: {colorHover};
            }}
            """
        )

        # Creamos la barra de menú
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {colorBarraMenu};
                color: white;
                padding: 5px; }}
        
            QMenuBar::item:selected {{
                background-color: {colorHover};
                color: #FAEEEF;
                border-radius: 5px;}}
            
            QMenu {{
                background-color: {colorLista};
            }}
            QMenu::item {{
                background-color: {colorLista};
                color: white;
                padding: 5px 20px;
                border-radius: 5px;
            }}
            QMenu::item:selected {{
                background-color: {colorHover};
                color: white;
            }}
                """)
        self.email = 'soporterolmusic@gmail.com'

        # Menu Apariencia
        apariencia = menubar.addMenu("&Apariencia")
        apariencia.addAction("Personalizar").triggered.connect(self.mostrarCustomizacion)

        # Menu Contribuir
        contribuir = menubar.addMenu("&Contribuir")
        contribuir.addAction("Agradecimientos").triggered.connect(self.mostrarAgradecimientos)
        contribuir.addAction("Contactame").triggered.connect(self.mostrarContacto)
        contribuir.addAction("Apoya el proyecto").triggered.connect(self.mostrarLinkDonacion)

        #Menu Acerca de
        acercaDe = menubar.addMenu("&Acerca de")
        acercaDe.addAction("v. 1.0.0")
        acercaDe.addAction("GitHub").triggered.connect(self.gitPagina)

        # Menu Ayuda
        ayuda = menubar.addMenu("&Ayuda")
        ayuda.addAction("Tutorial De Uso").triggered.connect(self.tutorial)

    def mostrarCustomizacion(self):
        ventanaCustomizacion = cambiarColor(self)
        ventanaCustomizacion.exec_()

    def mostrarContacto(self):
        # Mostrar cuadro de diálogo con información de contacto
        ventanaContac = QMessageBox(self)
        ventanaContac.setStyleSheet("""
            QMessageBox {
                background-color: #DD4254;
            }
            QMessageBox QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #43DE64;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 10px;
            }
        """)

        ventanaContac.setWindowTitle('Contactar para Sugerencias y Reportes de Errores')
        ventanaContac.setText('Puedes contactarme por correo electrónico para enviar sugerencias, reportes de errores u otras consultas.')
        ventanaContac.setInformativeText(f'Correo electrónico: {self.email}')
        ventanaContac.setIcon(QMessageBox.Information)
        ventanaContac.exec_()
        self.copiaPortapapeles()

    def copiaPortapapeles(self):
        # Copiar el correo electrónico al portapapeles
        copiaPorta = QApplication.clipboard()
        copiaPorta.setText(self.email)
        copiaCorreo= QMessageBox(self)
        copiaCorreo.setStyleSheet("""
            QMessageBox {
                background-color: #DD4254;
            }
            QMessageBox QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #43DE64;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 10px;
            }
        """)
        copiaCorreo.setWindowTitle('Copiado al Portapapeles')
        copiaCorreo.setText(f'Correo electrónico copiado al portapapeles: {self.email}')
        
        copiaCorreo.exec_()
        

    def mostrarLinkDonacion(self):
        # Mostrar cuadro de diálogo con link de donacion
        ventanaDonac = QMessageBox(self)
        ventanaDonac.setStyleSheet("""
            QMessageBox {
                background-color: #DD4254;
            }
            QMessageBox QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #43DE64;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 10px;
            }
        """)

        ventanaDonac.setWindowTitle('Apoya nuestro Proyecto: ¡Haz una Donación!')
        ventanaDonac.setText('¡Apoya nuestro proyecto para mantenerlo actualizado y en funcionamiento! Las donaciones nos permiten continuar desarrollando nuevas funcionalidades, mejorar la estabilidad y ofrecerte la mejor experiencia posible. Cada contribución cuenta y nos ayuda a seguir creciendo. Si encuentras útil nuestra aplicación, considera hacer una donación para apoyar nuestro trabajo.')
        ventanaDonac.setInformativeText('¡Gracias por ser parte de nuestro éxito!')
        ventanaDonac.setIcon(QMessageBox.Information)
        ventanaDonac.exec_()
        self.abrirLink()


    def abrirLink(self):
        QDesktopServices.openUrl(QUrl("https://link.mercadopago.com.mx/devmind"))

    def gitPagina(self):
        QDesktopServices.openUrl(QUrl("https://github.com/devhunter253"))

    def tutorial(self):
        QDesktopServices.openUrl(QUrl("https://github.com/devhunter253"))

    def mostrarAgradecimientos(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Agradecimientos")

        # Texto informativo adicional
        msgBox.setInformativeText(
            "Agradecimientos infinitos a los contribuyentes de este proyecto. "
            "En particular, agradecemos a:\n\n"
            "1. Christo Varez: Por su creatividad para el diseño del proyecto.\n\n"
            "Gracias a todos por su compromiso y entusiasmo.\n\n"
            "Proximamente mas personas..."
        )
        
        # Personalizando el color del texto y el botón
        msgBox.setStyleSheet("""
            QMessageBox {
                background-color: #DD4254;
            }
            QMessageBox QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #43DE64;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 10px;
            }
        """)

        msgBox.exec_()






