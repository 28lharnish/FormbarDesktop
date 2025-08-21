from PyQt6.QtCore import Qt, QThread, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtGui import qRgb, QIcon
from PyQt6.QtWidgets import QApplication, QDialog, QRadioButton, QPushButton
from functools import partial
import sys, os
import socketio
import datetime as DT
import json
from custLogging import custLogging

#? Import external layouts
from models import *
from devLayout import DevStudentLayout
from themes import Themes

debug = True
versionNumber = "1.0.5-dev"

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
            return DevStudentLayout()
        
        studentLayout = getLayout()

        def submitApi(s):
            apiKey = studentLayout.settingsApiKey.text()
            apiLink = studentLayout.settingsApiLink.text()
            self.startSocketSignal.emit(apiKey, apiLink)

        def stayOnTop(checked):
            setConfig([("fdStayOnTop", checked)])
            if checked == True:
                self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
                self.show()
                self.activateWindow()
                print("Stay on top.")
                return
            else:
                self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
                self.show()
                self.activateWindow()
                print("Stay off top.")
                return


        studentLayout.settingsConnect.clicked.connect(submitApi)
        studentLayout.helpTicketButton.clicked.connect(self.helpTicketSignal.emit)
        studentLayout.takeBreakButton.clicked.connect(self.takeBreakSignal.emit)
        studentLayout.removeVoteButton.clicked.connect(partial(self.voteSelectedSignal.emit, 'remove'))
        #studentLayout.stayOnTopCheck.clicked.connect(stayOnTop)

        self.setWindowFlags(Qt.WindowType.Window)
        self.setLayout(studentLayout.fullPageLayout)
        self.setMinimumSize(1200, 700)
        self.setWindowTitle("Formbar Desktop v" + versionNumber + " | Made by Landon Harnish")
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icon.ico')))
        QApplication.setPalette(themes.darkpalette)


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
                    QApplication.setPalette(themes.darkpalette)
                case 1:
                    QApplication.setPalette(themes.redPalette)
                case 2:
                    QApplication.setPalette(themes.bluePalette)
                case 3:
                    QApplication.setPalette(themes.pinkGradient)

        try:
            configJSON = open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r')
            configData = json.load(configJSON)

            if "apiKey" in configData:
                studentLayout.settingsApiKey.setText(configData["apiKey"])
            if "apiLink" in configData:
                studentLayout.settingsApiLink.setText(configData["apiLink"])

            if "fdTheme" in configData:
                setTheme(configData["fdTheme"])

            if "fdStayOnTop" in configData:
                stayOnTop(configData["fdStayOnTop"])
                studentLayout.stayOnTopCheck.setChecked(configData["fdStayOnTop"])

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
            while studentLayout.showVoteOptions.count():
                item = studentLayout.showVoteOptions.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    item.layout().deleteLater()

            for option in self.voteOptions:
                def saveVote(name):
                    self.lastVote = name

                optionRadio = QPushButton(option["answer"])
                optionRadio.clicked.connect(partial(self.voteSelectedSignal.emit, option["answer"]))
                optionRadio.clicked.connect(partial(saveVote, option["answer"]))
                optionColorPalette = optionRadio.palette()
                optionRadio.setFixedHeight(40)
                hexToRgb = tuple(int(option["color"].strip("#")[i:i+2], 16) for i in (0, 2, 4))
                darken = 100
                red = hexToRgb[0] - darken
                if(red < 0): red = 0
                grn = hexToRgb[1] - darken
                if(grn < 0): grn = 0
                blu = hexToRgb[2] - darken
                if(blu < 0): blu = 0


                lighten = 30
                lred = hexToRgb[0] - lighten
                if(lred < 0): lred = 0
                lgrn = hexToRgb[1] - lighten
                if(lgrn < 0): lgrn = 0
                lblu = hexToRgb[2] - lighten
                if(lblu < 0): lblu = 0

                optionRadio.setCursor(Qt.CursorShape.PointingHandCursor)
                optionColorPalette.setColor(optionColorPalette.ColorRole.Button, qRgb(red, grn, blu))
                optionColorPalette.setColor(optionColorPalette.ColorRole.ButtonText, qRgb(255, 255, 255))
                optionRadio.setStyleSheet(
                    "QPushButton::hover {" + f"background: rgb({lred}, {lgrn}, {lblu});" + "transform: scale(2);" +"}"
                )
                optionRadio.setPalette(optionColorPalette)

                #if option["answer"] == self.lastVote:
                    #optionRadio.setChecked(True)

                studentLayout.showVoteOptions.addWidget(optionRadio)


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