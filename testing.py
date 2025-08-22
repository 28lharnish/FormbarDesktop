import sys

from PyQt6.QtCharts import QPieSeries, QChart, QChartView
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton



# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.series = QPieSeries()

        self.series.append('Jane', 1)
        self.series.append('Joe', 2)
        self.series.append('Andy', 3)
        self.series.append('Barbara', 4)
        self.series.append('Axel', 5)

        self.slice = self.series.slices()[1]
        self.slice.setExploded()
        self.slice.setLabelVisible()
        self.pen = QPen(QColor(255, 0, 0), 3)
        self.slice.setPen(self.pen)
        self.slice.setBrush(QColor(255, 0, 0))

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle('Simple piechart example')
        self.chart.legend().hide()

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        self.setCentralWidget(self._chart_view)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()