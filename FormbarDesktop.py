from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractItemModel, QVariant, QThread, QObject, pyqtSlot, pyqtSignal, QPersistentModelIndex, QModelIndex
from PyQt6.QtGui import qRgb, QIcon, QPalette, QFont
from PyQt6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QRadioButton, QTableView, QVBoxLayout, QHeaderView, QWidget, QTableWidgetItem, QStyleFactory)
from functools import partial
import sys, os
import socketio
import json

#? Import external layouts
from models import *
from studentLayout import StudentLayout

debug = True
versionNumber = "1.0.4b"

try:
    from ctypes import windll
    myappid = 'ljharnish.formbardesktop.' + versionNumber
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class FormbarApp(QDialog):
    startSocketSignal = pyqtSignal(str, str)
    helpTicketSignal = pyqtSignal()
    takeBreakSignal = pyqtSignal()
    voteSelectedSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(FormbarApp, self).__init__(parent)

        #? Themes
        lightpalette = QApplication.palette()
        lightpalette.setColor(lightpalette.ColorRole.Window, qRgb(110, 110, 110))
        lightpalette.setColor(lightpalette.ColorRole.WindowText, qRgb(255, 255, 255))
        lightpalette.setColor(lightpalette.ColorRole.Base, qRgb(150, 150, 150))
        lightpalette.setColor(lightpalette.ColorRole.AlternateBase, qRgb(120, 120, 120))
        lightpalette.setColor(lightpalette.ColorRole.Accent, qRgb(255, 0, 0))
        lightpalette.setColor(lightpalette.ColorRole.Text, qRgb(255, 255, 255))
        lightpalette.setColor(lightpalette.ColorRole.Button, qRgb(120, 120, 120))
        lightpalette.setColor(lightpalette.ColorRole.ButtonText, qRgb(255, 255, 255))

        darkpalette = QApplication.palette()
        darkpalette.setColor(darkpalette.ColorRole.Window, qRgb(34, 34, 34))
        darkpalette.setColor(darkpalette.ColorRole.WindowText, qRgb(255, 255, 255))
        darkpalette.setColor(darkpalette.ColorRole.Base, qRgb(15, 15, 15))
        darkpalette.setColor(darkpalette.ColorRole.AlternateBase, qRgb(41, 44, 51))
        darkpalette.setColor(darkpalette.ColorRole.Accent, qRgb(255, 0, 0))
        darkpalette.setColor(darkpalette.ColorRole.Text, qRgb(255, 255, 255))
        darkpalette.setColor(darkpalette.ColorRole.Button, qRgb(41, 44, 51))
        darkpalette.setColor(darkpalette.ColorRole.ButtonText, qRgb(255, 255, 255))
        
        redPalette = QApplication.palette()
        redPalette.setColor(redPalette.ColorRole.Window, qRgb(133, 0, 7))
        redPalette.setColor(redPalette.ColorRole.WindowText, qRgb(255, 173, 178))
        redPalette.setColor(redPalette.ColorRole.Base, qRgb(56, 0, 3))
        redPalette.setColor(redPalette.ColorRole.AlternateBase, qRgb(36, 0, 2))
        redPalette.setColor(redPalette.ColorRole.Accent, qRgb(255, 0, 0))
        redPalette.setColor(redPalette.ColorRole.Text, qRgb(255, 173, 178))
        redPalette.setColor(redPalette.ColorRole.Button, qRgb(56, 0, 3))
        redPalette.setColor(redPalette.ColorRole.ButtonText, qRgb(255, 173, 178))

        bluePalette = QApplication.palette()
        bluePalette.setColor(bluePalette.ColorRole.Window, qRgb(0, 70, 140))
        bluePalette.setColor(bluePalette.ColorRole.WindowText, qRgb(171, 213, 255))
        bluePalette.setColor(bluePalette.ColorRole.Base, qRgb(0, 27, 54))
        bluePalette.setColor(bluePalette.ColorRole.AlternateBase, qRgb(0, 18, 36))
        bluePalette.setColor(bluePalette.ColorRole.Accent, qRgb(0, 0, 255))
        bluePalette.setColor(bluePalette.ColorRole.Text, qRgb(171, 213, 255))
        bluePalette.setColor(bluePalette.ColorRole.Button, qRgb(0, 27, 54))
        bluePalette.setColor(bluePalette.ColorRole.ButtonText, qRgb(171, 213, 255))

        self.worker = WorkerObject()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.startSocketSignal.connect(self.worker.backgroundSocket)
        self.helpTicketSignal.connect(self.worker.helpTicket)
        self.takeBreakSignal.connect(self.worker.takeBreak)
        self.voteSelectedSignal.connect(self.worker.voteSelected)
        self.thread.start()

        def getLayout():
            return StudentLayout()
        
        studentLayout = getLayout()

        def submitApi(s):
            apiKey = studentLayout.settingsApiKey.text()
            apiLink = studentLayout.settingsApiLink.text()
            self.startSocketSignal.emit(apiKey, apiLink)

        studentLayout.settingsConnect.clicked.connect(submitApi)
        studentLayout.helpTicketButton.clicked.connect(self.helpTicketSignal.emit)
        studentLayout.takeBreakButton.clicked.connect(self.takeBreakSignal.emit)
        studentLayout.removeVoteButton.clicked.connect(partial(self.voteSelectedSignal.emit, 'remove'))

        self.setLayout(studentLayout.mainLayout)
        self.setFixedSize(500, 700)
        self.setWindowTitle("Formbar Desktop v" + versionNumber + " | Made by Landon Harnish")
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icon.ico')))
        QApplication.setPalette(lightpalette)


        #? Load configs
        
        def setConfig(keys):
            configJSON = open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r')
            configData = json.load(configJSON)
            configJSON.close()

            for key in keys:
                configData[key[0]] = key[1]

            configJSON = open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w')
            json.dump(configData, configJSON)
            configJSON.close()

        def setTheme(t):
            setConfig([("fdTheme", t)])
            studentLayout.themeDropdown.setCurrentIndex(t)
            match t:
                case 0:
                    QApplication.setPalette(lightpalette)
                case 1:
                    QApplication.setPalette(darkpalette)
                case 2:
                    QApplication.setPalette(redPalette)
                case 3:
                    QApplication.setPalette(bluePalette)

        try:
            configJSON = open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r')
            configData = json.load(configJSON)

            if "apiKey" in configData:
                studentLayout.settingsApiKey.setText(configData["apiKey"])
            if "apiLink" in configData:
                studentLayout.settingsApiLink.setText(configData["apiLink"])

            if "fdTheme" in configData:
                setTheme(configData["fdTheme"])

            configJSON.close()
        except:
            print("No Config JSON, creating one now.")
            configJSON = open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w')
            json.dump({"fdTheme": "0"}, configJSON)
            configJSON.close()


        studentLayout.themeDropdown.currentIndexChanged.connect(setTheme)


        self.currentData = {}
        self.lastVote = ''
        self.voteOptions = []
        
        def updateData(data):
            if debug: 
                print(data)
            self.voteOptions = []
            self.currentData = data
            for option in data["polls"]:
                self.voteOptions.append(data["polls"][option])
                if debug: 
                    print(self.voteOptions)

            updatePrompt()
            updateVoteOptions()
            updateVotes()


        def updatePrompt():
            studentLayout.promptText.setText(self.currentData["prompt"])
            if self.currentData["status"] == False:
                studentLayout.promptText.setText("No current poll.")

        def updateVoteOptions():
            while studentLayout.votinglayout.count():
                item = studentLayout.votinglayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    item.layout().deleteLater()

            for option in self.voteOptions:
                def saveVote(name):
                    self.lastVote = name

                optionRadio = QRadioButton(option["answer"])
                optionRadio.clicked.connect(partial(self.voteSelectedSignal.emit, option["answer"]))
                optionRadio.clicked.connect(partial(saveVote, option["answer"]))
                optionColorPalette = optionRadio.palette()
                hexToRgb = tuple(int(option["color"].strip("#")[i:i+2], 16) for i in (0, 2, 4))
                optionColorPalette.setColor(optionColorPalette.ColorRole.Accent, qRgb(hexToRgb[0], hexToRgb[1], hexToRgb[2]))
                optionRadio.setPalette(optionColorPalette)

                if option["answer"] == self.lastVote:
                    optionRadio.setChecked(True)

                studentLayout.votinglayout.addWidget(optionRadio)

        def createRows(data):
            newRows = []

            allResponses = 0

            for option in self.voteOptions:
                allResponses += option["responses"]
                newRow = (option["answer"], option["responses"], option["color"])
                newRows.append(newRow)
            

            noResRow = ("No Response", self.currentData["totalResponders"] - allResponses, "None")
            newRows.append(noResRow)

            return newRows


        def updateVotes():
            voteRows = createRows(self.currentData)
            studentLayout.voteView.setModel(None) 
            model = TableModel(None, ["Votes", "Responses", "Color"], voteRows)
            studentLayout.voteView.setModel(model)
            
        
        def disableApi():
            setConfig([("apiKey", str(studentLayout.settingsApiKey.text())), ("apiLink", str(studentLayout.settingsApiLink.text()))])
            studentLayout.settingsApiKeyLabel.deleteLater()
            studentLayout.settingsApiKey.deleteLater()
            studentLayout.settingsApiLinkLabel.deleteLater()
            studentLayout.settingsApiLink.deleteLater()
            studentLayout.settingsConnect.deleteLater()

        #? Connect Functions

        self.worker.updateData.connect(updateData)
        self.worker.disableApi.connect(disableApi)

class WorkerObject(QObject):
    updateData = pyqtSignal(dict)
    disableApi = pyqtSignal()
    pyqtSlot()
    def backgroundSocket(self, apikey, apilink):
        try:
            self.sio = socketio.Client()
            self.joined = False

            if debug: 
                print(apikey)
            @self.sio.event
            def connect():
                if debug: 
                    print("connection established")
                self.sio.emit('getActiveClass')

            @self.sio.event
            def setClass(newClassId):
                print(newClassId)
                try:
                    if newClassId != None:
                        if debug: 
                            print('The user is currently in the class with the id ' + str(newClassId))
                        if not self.joined:
                            self.sio.emit('joinClass', newClassId)
                            self.disableApi.emit()
                            self.joined = True
                        self.sio.emit('vbUpdate')
                except:
                    print("No class, or couldn't send update.")
                

            @self.sio.event
            def vbUpdate(data):
                print('data')
                self.updateData.emit(data)

            @self.sio.event
            def disconnect():
                if debug:
                    print("disconnected from server")

            if not apilink:
                apilink = 'https://formbeta.yorktechapps.com/'
            print(apilink)
            self.sio.connect(apilink, { "api": apikey })
        except:
            print("Couldn't connect.")
        pass


    def voteSelected(self, voteName):
        try:
            self.sio.emit('pollResp', voteName)
        except:
            return

    def helpTicket(self):
        try:
            self.sio.emit('help', '')
        except:
            return

    def takeBreak(self):
        try:
            self.sio.emit('requestBreak', ' ')
        except:
            return


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    formapp = FormbarApp()
    formapp.show()
    sys.exit(app.exec())