from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractItemModel, QVariant, QThread, QObject, pyqtSlot, pyqtSignal, QPersistentModelIndex, QModelIndex
from PyQt6.QtGui import qRgb, QIcon, QPalette
from PyQt6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QTableView, QVBoxLayout, QHeaderView, QWidget, QTabWidget, QTableWidgetItem, QStyleFactory)
from functools import partial
import sys, os
import socketio
import json

#? Import external layouts
from models import *
from managerLayout import ManagerLayout

debug = True
versionNumber = "1.0.0b"

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
    allowAllVotingS = pyqtSignal(bool)
    voteSelectedSignal = pyqtSignal(str)
    sendPollSignalTUTD = pyqtSignal()

    def __init__(self, parent=None):
        super(FormbarApp, self).__init__(parent)

        self.allowAllVoting = False

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
        self.allowAllVotingS.connect(self.worker.getVotingStyle)
        self.sendPollSignalTUTD.connect(self.worker.sendTUTD)
        self.thread.start()
        
        def getLayout():
            return ManagerLayout()
        
        managerLayout = getLayout()

        def submitApi(s):
            apiKey = managerLayout.settingsApiKey.text()
            apiLink = managerLayout.settingsApiLink.text()
            self.startSocketSignal.emit(apiKey, apiLink)

        def changeVoting(b):
            self.allowAllVoting = b
            self.allowAllVotingS.emit(b)

        managerLayout.allowAllVotes.clicked.connect(changeVoting)
        managerLayout.settingsConnect.clicked.connect(submitApi)

        formPage = QWidget()
        formPageLayout = QHBoxLayout()
        formPageStudentView = QWidget()
        formPageStudentView.setLayout(managerLayout.votingShownLayout)
        formPageStudentView.setFixedWidth(500)

        formPageManagerView = QWidget()
        formPageManagerView.setLayout(managerLayout.managerFormLayout)
        managerLayout.fastPollTUTD.clicked.connect(self.sendPollSignalTUTD.emit)
        formPageLayout.addWidget(formPageStudentView, 0, Qt.AlignmentFlag.AlignLeft)
        formPageLayout.addWidget(formPageManagerView)
        formPage.setLayout(formPageLayout)

        tabs = QTabWidget()
        tabs.addTab(formPage, "Active Form")

        layout = QHBoxLayout()
        layout.addWidget(tabs)

        self.setLayout(layout)
        self.setFixedSize(1200, 700)
        self.setWindowTitle("Formbar Desktop v" + versionNumber + " | Made by Landon Harnish")
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '/icons/icon.ico')))
        QApplication.setPalette(lightpalette)


        #? Load configs
        
        def setConfig(keys):
            configJSON = open(os.path.join(os.path.dirname(__file__), 'managerconfig.json'), 'r')
            configData = json.load(configJSON)
            configJSON.close()

            for key in keys:
                configData[key[0]] = key[1]

            configJSON = open(os.path.join(os.path.dirname(__file__), 'managerconfig.json'), 'w')
            json.dump(configData, configJSON)
            configJSON.close()

        def setTheme(t):
            setConfig([("fdTheme", t)])
            managerLayout.themeDropdown.setCurrentIndex(t)
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
            configJSON = open(os.path.join(os.path.dirname(__file__), 'managerconfig.json'), 'r')
            configData = json.load(configJSON)

            if "apiKey" in configData:
                managerLayout.settingsApiKey.setText(configData["apiKey"])
            if "apiLink" in configData:
                managerLayout.settingsApiLink.setText(configData["apiLink"])

            if "fdTheme" in configData:
                setTheme(configData["fdTheme"])

            configJSON.close()
        except:
            print("No Config JSON, creating one now.")
            configJSON = open(os.path.join(os.path.dirname(__file__), 'managerconfig.json'), 'w')
            json.dump({"fdTheme": "0"}, configJSON)
            configJSON.close()


        managerLayout.themeDropdown.currentIndexChanged.connect(setTheme)


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
            updateVotes()


        def updatePrompt():
            managerLayout.promptText.setText(self.currentData["prompt"])
            if self.currentData["status"] == False:
                managerLayout.promptText.setText("No current poll.")

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
            managerLayout.voteView.setModel(None) 
            model = TableModel(None, ["Votes", "Responses", "Color"], voteRows)
            managerLayout.voteView.setModel(model)
            
        
        def disableApi():
            setConfig([("apiKey", str(managerLayout.settingsApiKey.text())), ("apiLink", str(managerLayout.settingsApiLink.text()))])
            managerLayout.settingsApiKeyLabel.deleteLater()
            managerLayout.settingsApiKey.deleteLater()
            managerLayout.settingsApiLinkLabel.deleteLater()
            managerLayout.settingsApiLink.deleteLater()
            managerLayout.settingsConnect.deleteLater()

        #? Connect Functions

        self.worker.updateData.connect(updateData)
        self.worker.disableApi.connect(disableApi)


class TableModel(QAbstractTableModel):
    def __init__(self, parent, header, tabledata):
        QAbstractTableModel.__init__(self, parent)
        self.modelTableData = tabledata
        self.header = header

        self.background_colors = dict()

    def rowCount(self, parent=QModelIndex()):
        return len(self.modelTableData)

    def columnCount(self, parent=QModelIndex()):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            return None
        if (
            0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
        ):
            if role == Qt.ItemDataRole.BackgroundRole:
                return qRgb(255, 5, 0)
            elif role == Qt.ItemDataRole.DisplayRole:
                return self.modelTableData[index.row()][index.column()]

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if (
            0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
        ):
            if role == Qt.ItemDataRole.BackgroundRole and index.isValid():
                ix = self.index(index.row(), 0)
                pix = QPersistentModelIndex(ix)
                self.background_colors[pix] = value
                return True
        return False

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.header[col]
        return None


class WorkerObject(QObject):
    updateData = pyqtSignal(dict)
    disableApi = pyqtSignal()
    pyqtSlot()
    def backgroundSocket(self, apikey, apilink):
        self.studentsInClass = []
        self.studentsInClassByName = []
        self.allowAllVotes = False

        try:
            self.sio = socketio.Client()
            self.joined = False

            if debug: 
                print(apikey)
            @self.sio.event
            def connect():
                if debug: 
                    print("connection established")
                self.sio.emit('getOwnedClasses', 'landonh')
                self.sio.emit('getActiveClass')
                self.sio.emit('cpUpdate')

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
                    else:
                        print("No class.")
                except:
                    print("No class, or couldn't send update.")
                
            @self.sio.event
            def getOwnedClasses(classes):
                return
                #print(classes)
                #print('here')

            @self.sio.event
            def cpUpdate(classroom):
                tempStudents = classroom['students']
                tempStudentKeys = list(dict(classroom['students']).keys())
                self.studentsInClass = []
                self.studentsInClassByName = []
                for student in range(0, len(tempStudentKeys)):
                    if tempStudents[tempStudentKeys[student]]['API'] != apikey:
                        self.studentsInClass.append(tempStudents[tempStudentKeys[student]])
                        self.studentsInClassByName.append(tempStudents[tempStudentKeys[student]]["username"])
                        if self.allowAllVotes:
                            self.sio.emit('votingRightChange', (tempStudents[tempStudentKeys[student]]["username"], True, self.studentsInClassByName))

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

    def getVotingStyle(self, boola):
        self.allowAllVotes = boola

    def sendTUTD(self):
        self.sio.emit('startPoll', (3, 0, 'Thumbs?', [{'answer': 'Up', 'weight': '1.0', 'color': '#00FF00'},{'answer': 'Wiggle', 'weight': '1.0', 'color': '#00FFFF'},{'answer': 'Down', 'weight': '1.0', 'color': '#FF0000'}], False, 1, [], [], [], [], False))
        self.sio.emit('cpUpdate')

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