import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QRadioButton, QButtonGroup, QVBoxLayout, QComboBox, QLabel, QPushButton, QColorDialog, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QColor, QIcon
import json
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, Qt
import os

class agradec(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent) 