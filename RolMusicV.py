import sys
from PyQt5.QtWidgets import QApplication
from gui import MiVentana
from interfazReproductor import interfazReproductor
from interfazBuscador import interfazBuscador

def main():
    app = QApplication(sys.argv)
    ventana = MiVentana()
    reproductor = interfazReproductor(ventana)
    buscador = interfazBuscador(ventana)
    ventana.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()