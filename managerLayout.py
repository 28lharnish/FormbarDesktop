
from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractItemModel, QVariant, QThread, QObject, pyqtSlot, pyqtSignal, QPersistentModelIndex, QModelIndex
from PyQt6.QtGui import qRgb, QIcon, QPalette, QFont
from PyQt6.QtWidgets import (QTabWidget, QApplication, QLayout, QComboBox, QCheckBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QTableView, QVBoxLayout, QHeaderView, QWidget, QTableWidgetItem, QStyleFactory)
from models import TableModel

class ManagerLayout:
    def __init__(self):
        self.activeForm()
        self.fastPoll()


        self.activeFormW = QWidget()
        self.activeFormW.setLayout(self.votingShownLayout)



        self.fastPollW = QWidget()
        self.fastPollW.setLayout(self.fastPollLayout)

        self.customPollW = QWidget()
        self.customPollW.setLayout(QVBoxLayout())
        
        self.tabs = QTabWidget()
        self.tabs.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.tabs.addTab(self.fastPollW, "Fast Poll")
        #self.tabs.addTab(self.customPollW, "Custom Form")
        self.tabs.setDocumentMode(True)
        
        self.fullPage = QWidget()
        self.fullPageLayout = QHBoxLayout()
        self.fullPageLayout.addWidget(self.activeFormW)
        self.fullPageLayout.addWidget(self.tabs)


    def fastPoll(self):
        self.fastPollBox = QGroupBox("Fast Poll")
        self.fastPollBox.setMinimumHeight(60)
        self.fastPollTUTD = QPushButton("TUTD")
        self.fastPollTrueFalse = QPushButton("True / False")
        self.fastPollDoneReady = QPushButton("Done / Ready")
        self.fastPollMultiChoi = QPushButton("Multiple Choice")
        
        self.fastPollTUTD.setFixedHeight(40)
        self.fastPollTrueFalse.setFixedHeight(40)
        self.fastPollDoneReady.setFixedHeight(40)
        self.fastPollMultiChoi.setFixedHeight(40)
        
        self.fastPollTUTD.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fastPollTrueFalse.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fastPollDoneReady.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fastPollMultiChoi.setCursor(Qt.CursorShape.PointingHandCursor)

        self.fastPollBoxLayout = QHBoxLayout()
        self.fastPollBoxLayout.addWidget(self.fastPollTUTD)
        self.fastPollBoxLayout.addWidget(self.fastPollTrueFalse)
        self.fastPollBoxLayout.addWidget(self.fastPollDoneReady)
        self.fastPollBoxLayout.addWidget(self.fastPollMultiChoi)
        self.fastPollBox.setLayout(self.fastPollBoxLayout)


        self.allowAllVotes = QPushButton("Allow All Votes")
        self.allowAllVotes.setFixedHeight(40)
        self.allowAllVotes.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.fastPollLayout = QVBoxLayout()
        self.fastPollLayout.addStretch()
        self.fastPollLayout.addWidget(self.fastPollBox)
        self.fastPollLayout.addWidget(self.allowAllVotes)
        self.fastPollLayout.addStretch()

        
    def activeForm(self):
        self.promptText = QLineEdit("Please input your API Key, then click Connect.")
        self.promptText.setReadOnly(True)
        self.promptText.setDisabled(True)
        self.promptText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.promptText.setFixedHeight(40)
        promptFont = QFont()
        promptFont.setBold(True)
        promptFont.setPointSize(16)
        self.promptText.setFont(promptFont)

        #? VoteBox

        self.votesGroup = QGroupBox("Votes")

        model = TableModel(None, ["Votes", "Responses", "Color"], [])
        self.voteView = QTableView()
        self.voteView.setModel(model)
        self.voteView.setSelectionMode(self.voteView.SelectionMode.NoSelection)
        self.voteView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.voteView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.voteView.verticalHeader().hide()
        votesFont = QFont()
        votesFont.setBold(True)
        votesFont.setPointSize(16)
        headFont = QFont()
        headFont.setBold(False)
        headFont.setPointSize(10)
        self.voteView.setFont(votesFont)
        self.voteView.horizontalHeader().setFont(headFont)

        self.votesLayout = QGridLayout()
        self.votesLayout.addWidget(self.voteView, 1, 0, 1, 2)
        self.votesLayout.setRowStretch(0, 0)
        self.votesGroup.setLayout(self.votesLayout)
        self.votesGroup.setMinimumHeight(175)

        #? Settings Box
        
        self.settingsBox = QGroupBox("Settings")

        self.themeDropdownLabel = QLabel("Theme:")
        self.themeDropdown = QComboBox()
        self.themeDropdown.addItems(["Light", "Dark", "Red", "Blue"])
        self.themeDropdown.setFixedHeight(40)
        self.themeDropdown.setCursor(Qt.CursorShape.PointingHandCursor)

        self.settingsApiKeyLabel = QLabel("Your Api Key:")
        self.settingsApiKey = QLineEdit("")
        self.settingsApiKey.setEchoMode(QLineEdit.EchoMode.Password)
        self.settingsApiKey.setFixedHeight(40)
        
        self.settingsApiLinkLabel = QLabel("API Link (Leave this field blank if you're not a developer):")
        self.settingsApiLink = QLineEdit("")
        self.settingsApiLink.setFixedHeight(40)

        self.settingsConnect = QPushButton("Connect")
        self.settingsConnect.setFixedHeight(40)
        self.settingsConnect.setCursor(Qt.CursorShape.PointingHandCursor)

        self.settingslayout = QVBoxLayout()
        self.settingslayout.addWidget(self.themeDropdownLabel)
        self.settingslayout.addWidget(self.themeDropdown)
        self.settingslayout.addWidget(self.settingsApiKeyLabel)
        self.settingslayout.addWidget(self.settingsApiKey)
        self.settingslayout.addWidget(self.settingsApiLinkLabel)
        self.settingslayout.addWidget(self.settingsApiLink)
        self.settingslayout.addWidget(self.settingsConnect)
        self.settingsConnect.setDefault(True)
        self.settingsBox.setLayout(self.settingslayout)

        #? Main Layout

        self.votingShownLayout = QGridLayout()
        self.votingShownLayout.addWidget(self.promptText, 0, 0, 1, 0)
        self.votingShownLayout.addWidget(self.votesGroup, 1, 0, 2, 0)
        self.votingShownLayout.addWidget(self.settingsBox, 5, 0, 2, 2)
        self.votingShownLayout.setRowStretch(1, 1)
        self.votingShownLayout.setRowStretch(2, 1)
        self.votingShownLayout.setColumnStretch(0, 1)
        self.votingShownLayout.setColumnStretch(1, 1)