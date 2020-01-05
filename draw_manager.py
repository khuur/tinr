from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import sys
import time

class DrawManager:
    def __init__(self, narray):
        self.app = QApplication([])
        self.widget = QDialog()
        self.widget.setWindowTitle("Labirint")
        self.widget.setLayout(QVBoxLayout())
        self.widget.resize(1000, 1000)
        self.widget.layout().setContentsMargins(2, 2, 2, 2)
        self.widget.scene = QGraphicsScene(self.widget)
        self.widget.scene.setBackgroundBrush(Qt.white)
        self.widget.view = QGraphicsView(self.widget.scene, self.widget)
        self.widget.view.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.widget.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.widget.view.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.widget.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.widget.layout().addWidget(self.widget.view)
        self.widget.scene.setSceneRect(0, 0, self.widget.view.width(), self.widget.view.height())
        self.widget.view.setSceneRect(0, 0, self.widget.view.width(), self.widget.view.height())
        self.widget.show()
        self.widget.raise_()
        self.widget.scene.update()
        self.narray = narray
    def draw_lab(self):

        maxVal = np.max(self.narray)
        self.widget.scene.clear()
        for y in range(np.size(self.narray, 0)):
            for x in range(np.size(self.narray, 1)):
                if (self.narray[(y, x)] == -1):
                    color = QBrush(QColor(0, 0, 0))
                elif (self.narray[(y, x)] == -2):
                    color = QBrush(QColor(0, 0, 255))
                elif (self.narray[(y, x)] == -3):
                    color = QBrush(QColor(0, 255, 0))
                else:
                    weight = 1 - self.narray[(y, x)] / maxVal
                    color = QBrush(QColor(255, 255 * weight, 255 * weight))

                self.widget.scene.addRect(x * 10, y * 10, 10, 10, QPen(color, 1), color)
                self.widget.scene.update()
        qApp.processEvents()

    def draw_end_path(self, path):
        color = QBrush(QColor(255, 255, 0))
        for step in path:
            if (self.narray[tuple(step)] >= 0):
                self.widget.scene.addRect(step[1] * 10, step[0] * 10, 10, 10, QPen(color, 1), color)
                self.widget.scene.update()
                qApp.processEvents()

    def call_sys_exit(self):
        sys.exit(self.app.exec_())
