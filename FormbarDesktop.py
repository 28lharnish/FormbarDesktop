from PyQt6.QtCore import Qt, QThread, QObject, pyqtSlot, pyqtSignal, QFile, QCoreApplication, QProcess
from PyQt6.QtGui import qRgb, QIcon, QDesktopServices, QPen, QColor
from PyQt6.QtWidgets import QStyleFactory, QApplication, QStyle, QDialog, QRadioButton, QPushButton, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from functools import partial
import sys, os
import socketio
import subprocess
import datetime as DT
import json
import requests
from custLogging import custLogging

#? Import external layouts
from models import *
from Layouts.studentLayout import StudentLayout

debug = True
versionNumber = "1.0.6-dev"

try:
    from ctypes import windll
    myappid = 'ljharnish.formbardesktop.' + versionNumber
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

Logger = custLogging().log

class FormbarApp(QMainWindow):
    startSocketSignal = pyqtSignal(str, str)
    helpTicketSignal = pyqtSignal()
    takeBreakSignal = pyqtSignal()
    voteSelectedSignal = pyqtSignal(str)

    updateAvailVersion = ""
    
    checkNewVersion = requests.get('https://api.github.com/repos/28lharnish/FormbarDesktop/releases/latest')
    updateAvailVersion = checkNewVersion.json()["tag_name"]

    def restart(self):
        QCoreApplication.quit()
        subprocess.call([sys.executable, sys.argv[0]])

    def ReloadStyles(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), "./style.qss"), "r") as f:
                _style = f.read()
            self.setStyleSheet(_style)
        except FileNotFoundError:
            print("Error: style.qss not found. Please ensure the file exists in the same directory.")

    def deleteConfig(self):
        configJSON = open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w')
        json.dump({}, configJSON)
        configJSON.close()
        self.restart()

    def __init__(self, parent=None):
        super(FormbarApp, self).__init__(parent)

        #themes = Themes()
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

        def stayOnTop(checked):
            setConfig([("fdStayOnTop", checked)])
            if checked == True:
                self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
                self.show()
                self.activateWindow()
                return
            else:
                self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
                self.show()
                self.activateWindow()
                return

        def setCurrentVoteNone():
            studentLayout.currentVoteShow.setStyleSheet("")
            studentLayout.currentVoteShow.setText("None")

        studentLayout.settingsConnect.clicked.connect(submitApi)
        studentLayout.helpTicketButton.clicked.connect(self.helpTicketSignal.emit)
        studentLayout.takeBreakButton.clicked.connect(self.takeBreakSignal.emit)
        studentLayout.removeVoteButton.clicked.connect(partial(self.voteSelectedSignal.emit, 'remove'))
        studentLayout.removeVoteButton.clicked.connect(setCurrentVoteNone)
        studentLayout.stayOnTopCheck.clicked.connect(stayOnTop)
        studentLayout.settingsRemoveAll.clicked.connect(self.deleteConfig)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(studentLayout.fullPageLayout)

        self.setMinimumSize(1200, 700)
        self.setWindowFlags(Qt.WindowType.Window)
        self.setWindowTitle("Formbar Desktop | v" + versionNumber + " | Made by Landon Harnish")
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), './Images/icon.ico')))
        self.ReloadStyles()
        self.setObjectName("lightTheme")
        

        self.UpdateAvailable = QDialog(self)
        self.UpdateAvailable.setParent(self)
        # self.UpdateAvailable.setStyleSheet("""
        #                                     QDialog { 
        #                                         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
        #                                     }
                                           
        #                                     QLabel {
        #                                         color: #09172e
        #                                    }

        #                                    QPushButton {
        #                                         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #577fbf, stop: 1 #365c99);
        #                                         border: 2px solid #55000000;
        #                                         margin: 10px;
        #                                         border-radius: 10px;
        #                                         color: #dddddd;
        #                                    }
        #                                    """)
        self.UpdateAvailable.setFixedSize(600, 400)
        self.UpdateAvailable.setWindowTitle("Update Available")

        updateAvailLayout = QVBoxLayout()
        updateAvailTitle = QLabel()
        updateAvailTitle.setText("There is an update available!")
        updateAvailTitle.setFont(QFont("Arial", 24, 900, True))

        updateAvailDesc = QLabel()
        updateAvailDesc.setText(f"You can now update from v{versionNumber} to {self.updateAvailVersion}!")
        updateAvailDesc.setFont(QFont("Arial", 16, 700, True))

        
        helpBreakBox = QWidget()

        helpTicketButton = QPushButton("Ignore")
        helpTicketButton.setFixedHeight(70)
        helpTicketButton.clicked.connect(self.UpdateAvailable.close);
        helpTicketButton.setFont(QFont("Arial", 18, QFont.Weight.DemiBold, False))
        helpTicketButton.setCursor(Qt.CursorShape.PointingHandCursor)
        
        takeBreakButton = QPushButton("Open GitHub")
        takeBreakButton.setFixedHeight(70)
        import webbrowser
        takeBreakButton.clicked.connect(partial(webbrowser.open, 'https://github.com/28lharnish/FormbarDesktop/releases/latest'));
        takeBreakButton.setFont(QFont("Arial", 18, QFont.Weight.DemiBold, False))
        takeBreakButton.setCursor(Qt.CursorShape.PointingHandCursor)

        helpBreakLayout = QHBoxLayout()
        helpBreakLayout.addWidget(helpTicketButton)
        helpBreakLayout.addWidget(takeBreakButton)
        helpBreakLayout.setSpacing(0)
        helpBreakBox.setLayout(helpBreakLayout)

        updateAvailLayout.addWidget(updateAvailTitle)
        updateAvailLayout.addWidget(updateAvailDesc)
        updateAvailLayout.addStretch(1)
        updateAvailLayout.addWidget(helpBreakBox)
        updateAvailLayout.addStretch(1)
        self.UpdateAvailable.setLayout(updateAvailLayout)

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
                    QMainWindow.setObjectName(self, "lightTheme")
                case 1:
                    QMainWindow.setObjectName(self, "darkTheme")
                case 2:
                    QMainWindow.setObjectName(self, "redTheme")
                case 3:
                    QMainWindow.setObjectName(self, "blueTheme")
                case 4:
                    QMainWindow.setObjectName(self, "pinkTheme")
            self.ReloadStyles()

        try:
            configJSON = open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r')
            configData = json.load(configJSON)

            if "apiKey" in configData:
                studentLayout.settingsApiKey.setText(configData["apiKey"])
            if "apiLink" in configData:
                studentLayout.settingsApiLink.setText(configData["apiLink"])

            if "apiKey" in configData and "apiLink" in configData:
                submitApi(self)

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
        self.lastVoteColor = (0, 0, 0)
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
                def showVote(name, color):
                    studentLayout.currentVoteShow.setStyleSheet("QPushButton {" + f"background: rgb({color[0]}, {color[1]}, {color[2]});" +"color:white;}")
                    studentLayout.currentVoteShow.setText(name)


                optionRadio = QPushButton(option["answer"])
                optionRadio.clicked.connect(partial(self.voteSelectedSignal.emit, option["answer"]))
                optionRadio.clicked.connect(partial(showVote, option["answer"], tuple(int(option["color"].strip("#")[i:i+2], 16) for i in (0, 2, 4))))
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
                optionColorPalette.setColor(optionColorPalette.ColorRole.ButtonText, qRgb(255, 255, 255))
                optionRadio.setStyleSheet(
                    "QPushButton::hover {" + f"background: rgb({lred}, {lgrn}, {lblu});" +"}" + "QPushButton {" + f"background: rgb({red}, {grn}, {blu});" +"}"
                )
                optionRadio.setPalette(optionColorPalette)


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
            studentLayout.series.clear()
            print(voteRows)
            for row in voteRows:
                slice = studentLayout.series.append('Jane', row[1])
                if row[2] == "None":  
                    slice.setBrush(QColor("#e1e1e1"))
                    slice.setBorderWidth(0)
                    slice.setBorderColor(QColor("transparent"))
                else:
                    slice.setBrush(QColor(row[2]))
                    slice.setBorderWidth(0)
                    slice.setBorderColor(QColor("transparent"))
            
        
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
            def customPollUpdate(data):
                Logger("customPollUpdate")
                #self.updateData.emit(data)

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

    print(versionNumber)
    print(formapp.updateAvailVersion)

    if f"v{versionNumber}" != formapp.updateAvailVersion:
        if versionNumber.__contains__("-dev") == False:
            formapp.UpdateAvailable.exec()

    sys.exit(app.exec())