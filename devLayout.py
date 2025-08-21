
from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractItemModel, QVariant, QThread, QObject, pyqtSlot, pyqtSignal, QPersistentModelIndex, QModelIndex
from PyQt6.QtGui import qRgb, QIcon, QPalette, QFont
from PyQt6.QtWidgets import (QTabWidget, QApplication, QLayout, QComboBox, QCheckBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QTableView, QVBoxLayout, QHeaderView, QWidget, QTableWidgetItem, QStyleFactory)
from models import TableModel

class DevStudentLayout:
    def __init__(self):
        self.activeForm()
        self.Form()
        self.settingsTab()


        self.activeFormW = QWidget()
        self.activeFormW.setLayout(self.votingShownLayout)

        self.formW = QGroupBox()
        self.formW.setLayout(self.formOptionsLayout)

        self.settingsTabW = QGroupBox()
        self.settingsTabW.setLayout(self.settingsTabLayout)

        #self.studentsTabW = QGroupBox("Students")
        #self.studentsTabW.setLayout(self.studentTabLayout)
        
        self.tabs = QTabWidget()
        self.tabs.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.tabs.addTab(self.formW, "Poll Options")
        self.tabs.addTab(self.settingsTabW, "Settings")
        #self.tabs.addTab(self.studentsTabW, "Students")

        self.tabs.setDocumentMode(True)
        
        self.fullPage = QWidget()
        self.fullPageLayout = QHBoxLayout()
        self.fullPageLayout.addWidget(self.activeFormW)
        self.fullPageLayout.addWidget(self.tabs)


    def Form(self):
        self.votingBox = QGroupBox("Voting Choices")
        self.votinglayout = QVBoxLayout()
        self.votingBox.setLayout(self.votinglayout)

        self.showVotingBox = QGroupBox()
        self.showVoteOptions = QHBoxLayout()
        self.showVotingBox.setLayout(self.showVoteOptions)

        
        self.removeVoteButton = QPushButton("Remove Vote")
        self.removeVoteButton.setFixedHeight(40)
        self.removeVoteButton.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.votinglayout.addWidget(self.showVotingBox)
        self.votinglayout.addWidget(self.removeVoteButton)

        self.helpBreakBox = QGroupBox("Need Help / Break?")

        self.helpTicketButton = QPushButton("Send Help Ticket")
        self.helpTicketButton.setFixedHeight(40)
        self.helpTicketButton.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.takeBreakButton = QPushButton("Take a Break")
        self.takeBreakButton.setFixedHeight(40)
        self.takeBreakButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self.helpBreakLayout = QVBoxLayout()
        self.helpBreakLayout.addWidget(self.helpTicketButton)
        self.helpBreakLayout.addWidget(self.takeBreakButton)
        self.helpBreakLayout.setSpacing(0)
        self.helpBreakBox.setLayout(self.helpBreakLayout)

        self.formOptionsLayout = QVBoxLayout()
        self.formOptionsLayout.addStretch()
        self.formOptionsLayout.addWidget(self.votingBox)
        self.formOptionsLayout.addWidget(self.helpBreakBox)
        self.formOptionsLayout.addStretch()

    def settingsTab(self):
        self.settingsBox = QGroupBox("Settings")

        self.themeDropdownLabel = QLabel("Theme:")
        self.themeDropdown = QComboBox()
        self.themeDropdown.addItems(["Dark", "Red", "Blue", "Pink"])
        self.themeDropdown.setFixedHeight(40)
        self.themeDropdown.setCursor(Qt.CursorShape.PointingHandCursor)

        self.stayOnTopCheckLabel = QLabel("Keep window on top?")
        self.stayOnTopCheck = QCheckBox()

        self.settingsApiKeyLabel = QLabel("Your API Key:")
        self.settingsApiKey = QLineEdit("")
        self.settingsApiKey.setFixedHeight(40)
        self.settingsApiKey.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.settingsApiLinkLabel = QLabel("API Link (Leave this field blank if you're not a developer):")
        self.settingsApiLink = QLineEdit("")
        self.settingsApiLink.setFixedHeight(40)

        self.settingsConnect = QPushButton("Connect")
        self.settingsConnect.setFixedHeight(40)
        self.settingsConnect.setCursor(Qt.CursorShape.PointingHandCursor)

        self.settingsTabLayout = QVBoxLayout()
        self.settingsTabLayout.addStretch(1)
        self.settingsTabLayout.addWidget(self.stayOnTopCheckLabel)
        self.settingsTabLayout.addWidget(self.stayOnTopCheck)
        self.settingsTabLayout.addWidget(self.themeDropdownLabel)
        self.settingsTabLayout.addWidget(self.themeDropdown)
        self.settingsTabLayout.addWidget(self.settingsApiKeyLabel)
        self.settingsTabLayout.addWidget(self.settingsApiKey)
        self.settingsTabLayout.addWidget(self.settingsApiLinkLabel)
        self.settingsTabLayout.addWidget(self.settingsApiLink)
        self.settingsTabLayout.addWidget(self.settingsConnect)
        self.settingsTabLayout.addStretch(1)
        self.settingsConnect.setDefault(True)
        
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

        #? Main Layout

        self.votingShownLayout = QGridLayout()
        self.votingShownLayout.addWidget(self.promptText, 0, 0, 1, 0)
        self.votingShownLayout.addWidget(self.votesGroup, 1, 0, 2, 0)
        self.votingShownLayout.setRowStretch(1, 1)
        self.votingShownLayout.setRowStretch(2, 1)
        self.votingShownLayout.setColumnStretch(0, 1)
        self.votingShownLayout.setColumnStretch(1, 1)