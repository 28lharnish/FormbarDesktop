from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractItemModel, QVariant, QThread, QObject, pyqtSlot, pyqtSignal, QPersistentModelIndex, QModelIndex
from PyQt6.QtGui import qRgb, qRgba, QIcon, QPalette
from PyQt6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QTableView, QVBoxLayout, QHeaderView, QWidget, QTabWidget, QTableWidgetItem, QStyleFactory)
from functools import partial
from themes import Themes
import sys, os
import socketio
import json

#? Import external layouts
from models import *
from managerLayout import ManagerLayout

debug = True
versionNumber = "1.0.0"

try:
    from ctypes import windll
    myappid = 'ljharnish.formbardesktopmanager.' + versionNumber
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class FormbarApp(QDialog):
    startSocketSignal = pyqtSignal(str, str)
    helpTicketSignal = pyqtSignal()
    takeBreakSignal = pyqtSignal()
    allowAllVotingS = pyqtSignal()
    voteSelectedSignal = pyqtSignal(str)
    sendPollSignal = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(FormbarApp, self).__init__(parent)

        themes = Themes()
        self.worker = WorkerObject()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.startSocketSignal.connect(self.worker.backgroundSocket)
        self.helpTicketSignal.connect(self.worker.helpTicket)
        self.takeBreakSignal.connect(self.worker.takeBreak)
        self.voteSelectedSignal.connect(self.worker.voteSelected)
        self.allowAllVotingS.connect(self.worker.allowAllVote)
        self.sendPollSignal.connect(self.worker.sendPoll)
        self.thread.start()
        
        def getLayout():
            return ManagerLayout()
        
        managerLayout = getLayout()

        def submitApi(s):
            apiKey = managerLayout.settingsApiKey.text()
            apiLink = managerLayout.settingsApiLink.text()
            self.startSocketSignal.emit(apiKey, apiLink)

        def changeVoting():
            self.allowAllVotingS.emit()

        managerLayout.allowAllVotes.clicked.connect(changeVoting)
        managerLayout.settingsConnect.clicked.connect(submitApi)

        managerLayout.fastPollTUTD.clicked.connect(partial(self.sendPollSignal.emit, (3, 0, 'Thumbs?', [{'answer': 'Up', 'weight': '1.0', 'color': '#00FF00'},{'answer': 'Wiggle', 'weight': '1.0', 'color': '#00FFFF'},{'answer': 'Down', 'weight': '1.0', 'color': '#FF0000'}], False, 1, [], [], [], [], False)))
        managerLayout.fastPollTrueFalse.clicked.connect(partial(self.sendPollSignal.emit, (2, 0, 'True or False', [{'answer': 'True', 'weight': '1.0', 'color': '#00FF00'},{'answer': 'False', 'weight': '1.0', 'color': '#FF0000'}], False, 1, [], [], [], [], False)))
        managerLayout.fastPollDoneReady.clicked.connect(partial(self.sendPollSignal.emit, (1, 0, 'Thumbs?', [{'answer': 'Yes', 'weight': '1.0', 'color': '#00FF00'}], False, 1, [], [], [], [], False)))
        managerLayout.fastPollMultiChoi.clicked.connect(partial(self.sendPollSignal.emit, (4, 0, 'Multiple Choice', [{'answer': 'A', 'weight': '1.0', 'color': '#FF0000'},{'answer': 'B', 'weight': '1.0', 'color': '#0000FF'},{'answer': 'C', 'weight': '1.0', 'color': '#FFFF00'},{'answer': 'D', 'weight': '1.0', 'color': '#00FF00'},], False, 1, [], [], [], [], False)))

        layout = QHBoxLayout()
        layout.addWidget(managerLayout.fullPage)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setLayout(managerLayout.fullPageLayout)
        self.setFixedSize(1200, 700)
        self.setWindowTitle("Formbar Desktop v" + versionNumber + " | Made by Landon Harnish")
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icon.ico')))
        QApplication.setPalette(themes.lightpalette)


        #? Load configsP
        
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
                    QApplication.setPalette(themes.lightpalette)
                case 1:
                    QApplication.setPalette(themes.darkpalette)
                case 2:
                    QApplication.setPalette(themes.redPalette)
                case 3:
                    QApplication.setPalette(themes.bluePalette)

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

class WorkerObject(QObject):
    updateData = pyqtSignal(dict)
    disableApi = pyqtSignal()
    pyqtSlot()
    def backgroundSocket(self, apikey, apilink):
        self.tempStudents = {}
        self.tempStudentKeys = []
        self.studentsInClass = []
        self.studentsInClassByName = []
        self.lastPoll = {}
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
                print(classroom)
                self.tempStudents = classroom['students']
                self.tempStudentKeys = list(dict(classroom['students']).keys())
                self.studentsInClass = []
                self.studentsInClassByName = []
                for student in range(0, len(self.tempStudentKeys)):
                    if self.tempStudents[self.tempStudentKeys[student]]['API'] != apikey:
                        self.studentsInClass.append(self.tempStudents[self.tempStudentKeys[student]])
                        self.studentsInClassByName.append(self.tempStudents[self.tempStudentKeys[student]]["username"])

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

    def allowAllVote(self):
        for student in range(0, len(self.tempStudentKeys)):             
            self.sio.emit('votingRightChange', (self.tempStudents[self.tempStudentKeys[student]]["username"], True, self.studentsInClassByName))

    def sendPoll(self, customPoll):
        try:
            self.sio.emit('startPoll', customPoll)
            self.sio.emit('cpUpdate')
        except:
            print("No socket yet.")

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