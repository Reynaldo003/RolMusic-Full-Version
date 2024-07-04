import sys
from PyQt5.QtWidgets import QApplication, QDialog, QRadioButton, QButtonGroup, QVBoxLayout, QComboBox, QLabel, QPushButton, QColorDialog, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QColor, QIcon
import json
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, Qt
import os

class cambiarColor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)            
        # Cargar el color de fondo desde el archivo JSON
        with open('config.json', 'r') as f:
            self.config = json.load(f)
            colorBuscar = self.config.get('C. Btn. Buscar', '#4CAF50')
            colorDescargar = self.config.get('C. Btn. Descargar', '#2196F3')
            colorLista = self.config.get('C. Lista', '#2B3444')

        self.setWindowTitle("Personalizar Colores")
        self.setFixedSize(320, 200)

        self.componente = QLabel("Componente:", self)
        self.componente.setGeometry(30, 110, 110, 20)
        self.componente.setStyleSheet(f"""
            QLabel {{
                border: None;
                border-radius: 5px; 
                padding-left: 10px;
                color: white;
                background-color: {colorLista};
                border: 1px solid #000000;
            }} """)
        
        self.btnReiniciar = QPushButton("Reiniciar Ahora", self)
        self.btnReiniciar.setGeometry(30, 150, 110, 20)
        self.btnReiniciar.setStyleSheet(f"""QPushButton{{
            background-color: {colorDescargar}; 
            color: black; 
            border: none;
            border-radius: 5px; 
            font-size: 11px;
            font-weight: bold;}}""")
        self.btnReiniciar.clicked.connect(self.reiniciar)

        self.menuDesplegable = QComboBox(self)
        self.menuDesplegable.setGeometry(180, 110, 110, 20)
        self.menuDesplegable.addItems(["C. Fondo", "C. Lista", "C. Objeto Lista", "C. Sombreado",
                                        "C. Btn. Buscar", "C. Btn. Descargar", "C. Barra Busqueda", "C. Barra Menu"])  

        self.btnColor = QPushButton("Seleccionar Color", self)
        self.btnColor.setGeometry(180, 150, 110, 20)
        self.btnColor.setStyleSheet(f"""QPushButton{{
            background-color: {colorBuscar}; 
            color: black; 
            border: none;
            border-radius: 5px; 
            font-size: 11px;
            font-weight: bold;}}""")
        self.btnColor.clicked.connect(self.elegirColor)

        self.grupoRadio = QButtonGroup(self)

        # Crear los radio buttons
        self.temaClaro = QRadioButton("Claro", self)
        self.temaClaro.setGeometry(20,20,60,20)
        self.temaClaro.setStyleSheet(f"""QRadioButton{{
            color: white; 
            font-size: 11px;}}""")
        self.temaOscuro = QRadioButton("Oscuro", self)
        self.temaOscuro.setGeometry(80,20,60,20)
        self.temaOscuro.setStyleSheet(f"""QRadioButton{{
            color: white; 
            font-size: 11px;}}""")
        self.temaSofis = QRadioButton("Sofisticado", self)
        self.temaSofis.setGeometry(150,20,70,20)
        self.temaSofis.setStyleSheet(f"""QRadioButton{{
            color: white; 
            font-size: 11px;}}""")
        self.temaVibr = QRadioButton("Vibrante", self)
        self.temaVibr.setGeometry(230,20,70,20)
        self.temaVibr.setStyleSheet(f"""QRadioButton{{
            color: white; 
            font-size: 11px;}}""")

        # Añadir los radio buttons al grupo para que sean mutuamente excluyentes
        self.grupoRadio.addButton(self.temaClaro)
        self.grupoRadio.addButton(self.temaOscuro)
        self.grupoRadio.addButton(self.temaSofis)
        self.grupoRadio.addButton(self.temaVibr)

        opc1 = QPixmap("_internal/play0.svg").scaled(35, 35, Qt.KeepAspectRatio)
        self.etqOpc1 = QLabel(self)
        self.etqOpc1.setGeometry(30, 50, 35, 35)
        self.etqOpc1.setPixmap(opc1)

        opc2 = QPixmap("_internal/play1.svg").scaled(35, 35, Qt.KeepAspectRatio)
        self.etqOpc2 = QLabel(self)
        self.etqOpc2.setGeometry(95, 50, 35, 35)
        self.etqOpc2.setPixmap(opc2)

        opc3 = QPixmap("_internal/play2.svg").scaled(35, 35, Qt.KeepAspectRatio)
        self.etqOpc3 = QLabel(self)
        self.etqOpc3.setGeometry(170, 50, 35, 35)
        self.etqOpc3.setPixmap(opc3)

        opc4 = QPixmap("_internal/play3.svg").scaled(40, 40, Qt.KeepAspectRatio)
        self.etqOpc4 = QLabel(self)
        self.etqOpc4.setGeometry(245, 50, 40, 40)
        self.etqOpc4.setPixmap(opc4)

        # Conectar las señales para detectar cambios
        self.temaClaro.toggled.connect(self.on_radio_toggled)
        self.temaOscuro.toggled.connect(self.on_radio_toggled)
        self.temaSofis.toggled.connect(self.on_radio_toggled)
        self.temaVibr.toggled.connect(self.on_radio_toggled)

    def elegirColor(self):
        color = QColorDialog.getColor()
        componente = self.menuDesplegable.currentText()
        print(componente)
        if color.isValid():
            # Guardar el color seleccionado en el archivo JSON
            self.config[componente] = color.name()
            with open('config.json', 'w') as f:
                json.dump(self.config, f)

    def on_radio_toggled(self):
        # Obtener el radio button seleccionado
        if self.sender().isChecked() and self.sender().text() == "Claro":
            self.rutas(0)
        elif self.sender().isChecked() and self.sender().text() == "Oscuro":
            self.rutas(1)
        elif self.sender().isChecked() and self.sender().text() == "Sofisticado":
            self.rutas(2)
        elif self.sender().isChecked() and self.sender().text() == "Vibrante":
            self.rutas(3)

    def reiniciar(self):
        QApplication.quit()

        script = "RolMusicV.py"
        os.execl(sys.executable, sys.executable, script)

    def rutas(self, num):
        self.config["anterior"] = f"_internal/anterior{num}.svg"
        self.config["carpeta"] = f"_internal/carpeta{num}.svg"
        self.config["mutear"] = f"_internal/mute{num}.svg"
        self.config["pausa"] = f"_internal/pausa{num}.svg"
        self.config["play"] =  f"_internal/play{num}.svg"
        self.config["ruido"] =  f"_internal/ruido{num}.svg" 
        self.config["siguiente"] = f"_internal/siguiente{num}.svg"
        self.config["aleatorio"] = f"_internal/aleatorio{num}.svg"
        with open('config.json', 'w') as f:
            json.dump(self.config, f)


