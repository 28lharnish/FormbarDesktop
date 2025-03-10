from PyQt6.QtCore import Qt, QThread, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtGui import qRgb, QIcon
from PyQt6.QtWidgets import QApplication, QDialog, QRadioButton
from functools import partial
import sys, os
import socketio
import datetime as DT
import json
from custLogging import custLogging

#? Import external layouts
from models import *
from studentLayout import StudentLayout
from themes import Themes

debug = True
versionNumber = "1.0.4"

try:
    from ctypes import windll
    myappid = 'ljharnish.formbardesktop.' + versionNumber
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

Logger = custLogging().log

class FormbarApp(QDialog):
    startSocketSignal = pyqtSignal(str, str)
    helpTicketSignal = pyqtSignal()
    takeBreakSignal = pyqtSignal()
    voteSelectedSignal = pyqtSignal(str)

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
        self.thread.start()

        def getLayout():
            return StudentLayout()
        
        studentLayout = getLayout()

        def submitApi(s):
            apiKey = studentLayout.settingsApiKey.text()
            apiLink = studentLayout.settingsApiLink.text()
            self.startSocketSignal.emit(apiKey, apiLink)

        #def stayOnTop(checked):
        #    print(checked)
        #    if checked == True:
        #        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        #    else:
        #        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)


        studentLayout.settingsConnect.clicked.connect(submitApi)
        studentLayout.helpTicketButton.clicked.connect(self.helpTicketSignal.emit)
        studentLayout.takeBreakButton.clicked.connect(self.takeBreakSignal.emit)
        studentLayout.removeVoteButton.clicked.connect(partial(self.voteSelectedSignal.emit, 'remove'))
        #studentLayout.stayOnTopCheck.clicked.connect(stayOnTop)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setLayout(studentLayout.mainLayout)
        self.setFixedSize(500, 700)
        self.setWindowTitle("Formbar Desktop v" + versionNumber + " | Made by Landon Harnish")
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icon.ico')))
        QApplication.setPalette(themes.lightpalette)


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
                    QApplication.setPalette(themes.lightpalette)
                case 1:
                    QApplication.setPalette(themes.darkpalette)
                case 2:
                    QApplication.setPalette(themes.redPalette)
                case 3:
                    QApplication.setPalette(themes.bluePalette)

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
            Logger('ConfigJSON', "No Config JSON, creating one now.")
            configJSON = open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w')
            json.dump({"fdTheme": "0"}, configJSON)
            configJSON.close()


        studentLayout.themeDropdown.currentIndexChanged.connect(setTheme)


        self.currentData = {}
        self.lastVote = ''
        self.voteOptions = []
        
        def updateData(data):
            self.voteOptions = []
            self.currentData = data
            for option in data["polls"]:
                self.voteOptions.append(data["polls"][option])
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
                optionColorPalette.setColor(optionColorPalette.ColorRole.WindowText, qRgb(hexToRgb[0], hexToRgb[1], hexToRgb[2]))
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
                Logger('APIKey', apikey)
            @self.sio.event
            def connect():
                if debug:
                    Logger("SocketConnect", "Connected.")
                self.sio.emit('getActiveClass')

            @self.sio.event
            def setClass(newClassId):
                try:
                    if newClassId != None:
                        Logger("SetClass", 'User in class: ' + str(newClassId))
                        if not self.joined:
                            self.sio.emit('joinClass', newClassId)
                            self.disableApi.emit()
                            self.joined = True
                        self.sio.emit('vbUpdate')
                    else:
                        print("No class.")
                except:
                    Logger("SetClass", "ERR: No Class / Update Failed to Send")
                

            @self.sio.event
            def vbUpdate(data):
                Logger("VirtualBarUpdate", data)
                self.updateData.emit(data)

            @self.sio.event
            def disconnect():
                if debug:
                    Logger("SocketConnect", "Disconnected")

            if not apilink:
                apilink = 'https://formbeta.yorktechapps.com/'
            self.sio.connect(apilink, { "api": apikey })
        except:
            Logger("SocketConnect", "Couldn't connect.")
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