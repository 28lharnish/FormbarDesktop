from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractItemModel, QVariant, QThread, QObject, pyqtSlot, pyqtSignal, QPersistentModelIndex, QModelIndex
from PyQt6.QtGui import qRgb, QIcon, QPalette
from PyQt6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QRadioButton, QTableView, QVBoxLayout, QHeaderView, QWidget, QTableWidgetItem, QStyleFactory)
from functools import partial
import sys, os
import socketio

debug = True
versionNumber = "1.0.2"
try:
    from ctypes import windll  # Only exists on Windows.
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

        #? Prompt

        promptText = QLineEdit("Please input your API Key, then click Connect.")
        promptText.setReadOnly(True)
        promptText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        promptText.setFixedHeight(40)

        #? VoteBox

        votesGroup = QGroupBox("Votes")


        model = TableModel(None, ["Votes", "Responses", "Color"], [])
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

        def changeTheme(theme):
            match theme:
                case 0:
                    QApplication.setPalette(lightpalette)
                case 1:
                    QApplication.setPalette(darkpalette)
                case 2:
                    QApplication.setPalette(redPalette)
                case 3:
                    QApplication.setPalette(bluePalette)



        settingsBox = QGroupBox("Settings")

        themeDropdownLabel = QLabel("Theme:")
        themeDropdown = QComboBox()
        themeDropdown.addItems(["Light", "Dark", "Red", "Blue"])
        themeDropdown.currentIndexChanged.connect(changeTheme)

        settingsApiKeyLabel = QLabel("Your Api Key:")
        settingsApiKey = QLineEdit("")
        settingsApiKey.setEchoMode(QLineEdit.EchoMode.Password)
        settingsApiKey.setFixedHeight(20)
        
        settingsApiLinkLabel = QLabel("API Link (leave blank if not a developer):")
        settingsApiLink = QLineEdit("")
        settingsApiLink.setFixedHeight(20)

        settingsConnect = QPushButton("Connect")
        def submitApi(s):
            apiKey = settingsApiKey.text()
            apiLink = settingsApiLink.text()
            self.startSocketSignal.emit(apiKey, apiLink)

        settingsConnect.clicked.connect(submitApi)

        settingslayout = QVBoxLayout()
        settingslayout.addWidget(themeDropdownLabel)
        settingslayout.addWidget(themeDropdown)
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
        mainLayout.addWidget(settingsBox, 5, 0, 2, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setFixedSize(500, 700)
        self.setLayout(mainLayout)
        self.setWindowTitle("Formbar Desktop v" + versionNumber + " | Made by Landon Harnish")
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icon.ico')))
        QApplication.setPalette(lightpalette)


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
                optionRadio.setStyleSheet("color: " + option["color"])
                optionColorPalette = optionRadio.palette()
                hexToRgb = tuple(int(option["color"].strip("#")[i:i+2], 16) for i in (0, 2, 4))
                optionColorPalette.setColor(optionColorPalette.ColorRole.Accent, qRgb(hexToRgb[0], hexToRgb[1], hexToRgb[2]))
                optionRadio.setPalette(optionColorPalette)

                if option["answer"] == self.lastVote:
                    optionRadio.setChecked(True)

                votinglayout.addWidget(optionRadio)

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
            voteView.setModel(None) 
            model = TableModel(None, ["Votes", "Responses", "Color"], voteRows)
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
                try:
                    if debug: 
                        print('The user is currently in the class with the id ' + newClassId)
                    self.sio.emit('vbUpdate')
                except:
                    print("No class, or couldn't send update.")
                    

            @self.sio.event
            def vbUpdate(data):
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