from PyQt6.QtCore import Qt, QAbstractTableModel, QVariant, QThread, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtGui import qRgb, QIcon
from PyQt6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QRadioButton, QTableView, QVBoxLayout, QHeaderView)
from functools import partial
import sys, os
import socketio

debug = True

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'ljharnish.formbardesktop.1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class FormbarApp(QDialog):
    startSocketSignal = pyqtSignal(str, str)
    helpTicketSignal = pyqtSignal()
    takeBreakSignal = pyqtSignal()
    voteSelectedSignal = pyqtSignal(str)

    def __init__(self, parent=None): 
        voteHeaders = ["Votes", "Responses", "Color"]
        voteRows = []

        super(FormbarApp, self).__init__(parent)


        #lightpalette = QApplication.palette()
        #lightpalette.setColor(lightpalette.ColorRole.Window, qRgb(255, 255, 255))
        #lightpalette.setColor(lightpalette.ColorRole.WindowText, qRgb(0, 0, 0))
        #lightpalette.setColor(lightpalette.ColorRole.Base, qRgb(150, 150, 150))
        #lightpalette.setColor(lightpalette.ColorRole.AlternateBase, qRgb(120, 120, 120))
        #lightpalette.setColor(lightpalette.ColorRole.ToolTipBase, qRgb(0, 0, 0))
        #lightpalette.setColor(lightpalette.ColorRole.ToolTipText, qRgb(0, 0, 0))
        #lightpalette.setColor(lightpalette.ColorRole.Accent, qRgb(255, 0, 0))
        #lightpalette.setColor(lightpalette.ColorRole.Midlight, qRgb(255, 0, 0))
        #lightpalette.setColor(lightpalette.ColorRole.Text, qRgb(255, 255, 255))
        #lightpalette.setColor(lightpalette.ColorRole.Button, qRgb(120, 120, 120))
        #lightpalette.setColor(lightpalette.ColorRole.ButtonText, qRgb(0, 0, 0))
        #lightpalette.setColor(lightpalette.ColorRole.BrightText, qRgb(255, 0, 0))
        #lightpalette.setColor(lightpalette.ColorRole.Highlight, qRgb(100, 100, 225))
        #lightpalette.setColor(lightpalette.ColorRole.HighlightedText, qRgb(0, 0, 0))
        #QApplication.setPalette(lightpalette)

        darkpalette = QApplication.palette()
        darkpalette.setColor(darkpalette.ColorRole.Window, qRgb(34, 34, 34))
        darkpalette.setColor(darkpalette.ColorRole.WindowText, qRgb(255, 255, 255))
        darkpalette.setColor(darkpalette.ColorRole.Base, qRgb(15, 15, 15))
        darkpalette.setColor(darkpalette.ColorRole.AlternateBase, qRgb(41, 44, 51))
        darkpalette.setColor(darkpalette.ColorRole.ToolTipBase, qRgb(255, 255, 255))
        darkpalette.setColor(darkpalette.ColorRole.ToolTipText, qRgb(255, 255, 255))
        darkpalette.setColor(darkpalette.ColorRole.Text, qRgb(255, 255, 255))
        darkpalette.setColor(darkpalette.ColorRole.Accent, qRgb(255, 0, 0))
        darkpalette.setColor(darkpalette.ColorRole.Button, qRgb(41, 44, 51))
        darkpalette.setColor(darkpalette.ColorRole.ButtonText, qRgb(255, 255, 255))
        darkpalette.setColor(darkpalette.ColorRole.BrightText, qRgb(255, 0, 0))
        darkpalette.setColor(darkpalette.ColorRole.Highlight, qRgb(100, 100, 225))
        darkpalette.setColor(darkpalette.ColorRole.HighlightedText, qRgb(0, 0, 0))
        QApplication.setPalette(darkpalette)


        self.worker = WorkerObject()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.startSocketSignal.connect(self.worker.backgroundSocket)
        self.helpTicketSignal.connect(self.worker.helpTicket)
        self.takeBreakSignal.connect(self.worker.takeBreak)
        self.voteSelectedSignal.connect(self.worker.voteSelected)
        self.thread.start()

        #? Prompt

        promptText = QLineEdit("Please input your API Key, then click Connect.")
        promptText.setReadOnly(True)
        promptText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        promptText.setFixedHeight(40)

        #? VoteBox

        class TableModel(QAbstractTableModel):
            def rowCount(self, parent):
                return len(voteRows)
            def columnCount(self, parent):
                return len(voteHeaders)
            def data(self, index, role):
                if role != Qt.ItemDataRole.DisplayRole:
                    return QVariant()
                return voteRows[index.row()][index.column()]
            def headerData(self, section, orientation, role):
                if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
                    return QVariant()
                return voteHeaders[section]

        votesGroup = QGroupBox("Votes")

        model = TableModel()
        voteView = QTableView()
        voteView.setModel(model)
        voteView.setSelectionMode(voteView.SelectionMode.NoSelection)
        voteView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        voteView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        voteView.verticalHeader().hide()

        votesLayout = QGridLayout()
        votesLayout.addWidget(voteView, 1, 0, 1, 2)
        votesLayout.setRowStretch(0, 0)
        votesGroup.setLayout(votesLayout)
        votesGroup.setMinimumHeight(175)



        #? VotingBox

        votingBox = QGroupBox("Voting Choices")
        votinglayout = QVBoxLayout()
        votinglayout.addStretch(1)
        votingBox.setLayout(votinglayout)






        #? Help / Break Box

        helpBreakBox = QGroupBox("Need Help / Break?")

        helpTicketButton = QPushButton("Send Help Ticket")
        helpTicketButton.clicked.connect(self.helpTicketSignal.emit)

        takeBreakButton = QPushButton("Take a Break")
        takeBreakButton.clicked.connect(self.takeBreakSignal.emit)
        
        removeVoteButton = QPushButton("Remove Vote")
        removeVoteButton.clicked.connect(partial(self.voteSelectedSignal.emit, 'remove'))

        helpBreakLayout = QVBoxLayout()
        helpBreakLayout.addWidget(helpTicketButton)
        helpBreakLayout.addWidget(takeBreakButton)
        helpBreakLayout.addWidget(removeVoteButton)
        helpBreakLayout.addStretch(1)
        helpBreakBox.setLayout(helpBreakLayout)








        #? Settings Box

        settingsBox = QGroupBox("Settings")

        #darkModeButton = QCheckBox("Dark Mode (WIP)")
        #darkModeButton.clicked.connect(self.darkModeToggle)

        settingsApiKeyLabel = QLabel("Your Api Key:")
        settingsApiKey = QLineEdit("")
        settingsApiKey.setEchoMode(QLineEdit.EchoMode.Password)
        settingsApiKey.setFixedHeight(20)
        
        settingsApiLinkLabel = QLabel("API Link (leave blank if not a developer)")
        settingsApiLink = QLineEdit("")
        settingsApiLink.setFixedHeight(20)

        settingsConnect = QPushButton("Connect")
        def submitApi(s):
            apiKey = settingsApiKey.text()
            apiLink = settingsApiLink.text()
            self.startSocketSignal.emit(apiKey, apiLink)

        settingsConnect.clicked.connect(submitApi)

        settingslayout = QVBoxLayout()
        #settingslayout.addWidget(darkModeButton)
        settingslayout.addWidget(settingsApiKeyLabel)
        settingslayout.addWidget(settingsApiKey)
        settingslayout.addWidget(settingsApiLinkLabel)
        settingslayout.addWidget(settingsApiLink)
        settingslayout.addWidget(settingsConnect)
        settingsConnect.setDefault(True)
        settingsBox.setLayout(settingslayout)






        #? Main Layout

        mainLayout = QGridLayout()
        mainLayout.addWidget(promptText, 0, 0, 1, 0)
        mainLayout.addWidget(votesGroup, 1, 0, 2, 0)
        mainLayout.addWidget(votingBox, 4, 0)
        mainLayout.addWidget(helpBreakBox, 4, 1)
        mainLayout.addWidget(settingsBox, 5, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setFixedSize(500, 600)
        self.setLayout(mainLayout)
        #print(QStyleFactory.keys())
        self.setWindowTitle("Formbar Desktop v1.0 | Made by Landon Harnish")
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icon.ico')))
        #QApplication.setStyle(QStyleFactory.create("Fusion"))
        #QApplication.setPalette(QApplication.style().standardPalette())


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
            promptText.setText(self.currentData["prompt"])
            if self.currentData["status"] == False:
                promptText.setText("No current poll.")

        def updateVoteOptions():
            while votinglayout.count():
                item = votinglayout.takeAt(0)
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

                if option["answer"] == self.lastVote:
                    optionRadio.setChecked(True)

                votinglayout.addWidget(optionRadio)

        def createRows(data):
            newRows = []

            for option in self.voteOptions:
                newRow = (option["answer"], option["responses"], option["color"])
                newRows.append(newRow)
            

            #noResRow = ("No Response", self.currentData["totalResponders"] - self.currentData["totalResponses"], "None")
            #newRows.append(noResRow)

            return newRows


        def updateVotes():
            voteRows = createRows(self.currentData)

            class TableModel(QAbstractTableModel):
                def rowCount(self, parent):
                    return len(voteRows)
                def columnCount(self, parent):
                    return len(voteHeaders)
                def data(self, index, role):
                    if role != Qt.ItemDataRole.DisplayRole:
                        return QVariant()
                    return voteRows[index.row()][index.column()]
                def headerData(self, section, orientation, role):
                    if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
                        return QVariant()
                    return voteHeaders[section]
                
            voteView.setModel(None) 
            model = TableModel()
            voteView.setModel(model)
            
        
        def disableApi():
            settingsApiKeyLabel.deleteLater()
            settingsApiKey.deleteLater()
            settingsApiLinkLabel.deleteLater()
            settingsApiLink.deleteLater()
            settingsConnect.deleteLater()

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
            if debug: 
                print(apikey)
            @self.sio.event
            def connect():
                if debug: 
                    print("connection established")
                self.sio.emit('getActiveClass')
                self.disableApi.emit()

            @self.sio.event
            def setClass(newClassId):
                if debug: 
                    print('The user is currently in the class with the id ' + newClassId)
                self.sio.emit('vbUpdate')

            @self.sio.event
            def vbUpdate(data):
                self.updateData.emit(data)

            @self.sio.event
            def disconnect():
                if debug:
                    print("disconnected from server")

            if not apilink:
                apilink = 'https://formbeta.yorktechapps.com'
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