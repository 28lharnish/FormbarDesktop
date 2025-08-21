from PyQt6.QtGui import qRgb, QBrush, QLinearGradient, QColor
from PyQt6.QtWidgets import QApplication

class Themes:
    def __init__(self):
        super(Themes, self).__init__()

        self.darkpalette = QApplication.palette()
        self.darkpalette.setColor(self.darkpalette.ColorRole.Window, qRgb(34, 34, 34))
        self.darkpalette.setColor(self.darkpalette.ColorRole.WindowText, qRgb(255, 255, 255))
        self.darkpalette.setColor(self.darkpalette.ColorRole.Base, qRgb(15, 15, 15))
        self.darkpalette.setColor(self.darkpalette.ColorRole.AlternateBase, qRgb(41, 44, 51))
        self.darkpalette.setColor(self.darkpalette.ColorRole.Accent, qRgb(255, 0, 0))
        self.darkpalette.setColor(self.darkpalette.ColorRole.Text, qRgb(255, 255, 255))
        self.darkpalette.setColor(self.darkpalette.ColorRole.Button, qRgb(41, 44, 51))
        self.darkpalette.setColor(self.darkpalette.ColorRole.ButtonText, qRgb(255, 255, 255))

        self.redPalette = QApplication.palette()
        self.redPalette.setColor(self.redPalette.ColorRole.Window, qRgb(133, 0, 7))
        self.redPalette.setColor(self.redPalette.ColorRole.WindowText, qRgb(255, 173, 178))
        self.redPalette.setColor(self.redPalette.ColorRole.Base, qRgb(56, 0, 3))
        self.redPalette.setColor(self.redPalette.ColorRole.AlternateBase, qRgb(36, 0, 2))
        self.redPalette.setColor(self.redPalette.ColorRole.Accent, qRgb(255, 0, 0))
        self.redPalette.setColor(self.redPalette.ColorRole.Text, qRgb(255, 173, 178))
        self.redPalette.setColor(self.redPalette.ColorRole.Button, qRgb(56, 0, 3))
        self.redPalette.setColor(self.redPalette.ColorRole.ButtonText, qRgb(255, 173, 178))

        self.bluePalette = QApplication.palette()
        self.bluePalette.setColor(self.bluePalette.ColorRole.Window, qRgb(0, 70, 140))
        self.bluePalette.setColor(self.bluePalette.ColorRole.WindowText, qRgb(171, 213, 255))
        self.bluePalette.setColor(self.bluePalette.ColorRole.Base, qRgb(0, 27, 54))
        self.bluePalette.setColor(self.bluePalette.ColorRole.AlternateBase, qRgb(0, 18, 36))
        self.bluePalette.setColor(self.bluePalette.ColorRole.Accent, qRgb(0, 0, 255))
        self.bluePalette.setColor(self.bluePalette.ColorRole.Text, qRgb(171, 213, 255))
        self.bluePalette.setColor(self.bluePalette.ColorRole.Button, qRgb(0, 27, 54))
        self.bluePalette.setColor(self.bluePalette.ColorRole.ButtonText, qRgb(171, 213, 255))

        self.pinkGradient = QApplication.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor('#ffd6fb'))
        gradient.setColorAt(1.0, QColor('#ffaff8'))
        self.pinkGradient.setBrush(self.pinkGradient.ColorRole.Window, QBrush(gradient))
        self.pinkGradient.setBrush(self.redPalette.ColorRole.Base, QBrush(gradient))
        self.pinkGradient.setBrush(self.redPalette.ColorRole.AlternateBase, QBrush(gradient))