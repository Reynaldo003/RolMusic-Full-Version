from PyQt5.QtWidgets import QListWidget
import json


class interfazCompartida:
    def __init__(self, ventana):
        self.listaURL = []
        self.listaNombreVideo = []

        self.playlist = QListWidget(ventana)
        self.playlist.setGeometry(100, 60, 285, 320)
        # Cargar el color de fondo desde el archivo JSON
        with open('config.json', 'r') as f:
            self.config = json.load(f)
            colorLista = self.config.get('C. Lista', '#2B3444')
            colorObjLista = self.config.get('C. Objeto Lista', '#06090B')
            colorHover = self.config.get('C. Sombreado', '#70122A')

        self.playlist.setStyleSheet(f"""
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