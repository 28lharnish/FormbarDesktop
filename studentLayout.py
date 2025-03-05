
from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractItemModel, QVariant, QThread, QObject, pyqtSlot, pyqtSignal, QPersistentModelIndex, QModelIndex
from PyQt6.QtGui import qRgb, QIcon, QPalette, QFont
from PyQt6.QtWidgets import (QApplication, QAbstractItemView, QCheckBox, QComboBox, QDialog, QStyle, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QRadioButton, QTableView, QVBoxLayout, QHeaderView, QWidget, QTableWidgetItem, QStyleFactory)
from models import TableModel

class StudentLayout:
    def __init__(self):
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
        self.voteView.setDisabled(True)
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



        #? VotingBox

        self.votingBox = QGroupBox("Voting Choices")
        self.votinglayout = QVBoxLayout()
        self.votinglayout.addStretch(1)
        self.votingBox.setLayout(self.votinglayout)






        #? Help / Break Box

        self.helpBreakBox = QGroupBox("Need Help / Break?")

        self.helpTicketButton = QPushButton("Send Help Ticket")
        self.helpTicketButton.setFixedHeight(40)
        self.helpTicketButton.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.takeBreakButton = QPushButton("Take a Break")
        self.takeBreakButton.setFixedHeight(40)
        self.takeBreakButton.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.removeVoteButton = QPushButton("Remove Vote")
        self.removeVoteButton.setFixedHeight(40)
        self.removeVoteButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self.helpBreakLayout = QVBoxLayout()
        self.helpBreakLayout.addWidget(self.helpTicketButton)
        self.helpBreakLayout.addWidget(self.takeBreakButton)
        self.helpBreakLayout.addWidget(self.removeVoteButton)
        self.helpBreakLayout.addStretch(1)
        self.helpBreakBox.setLayout(self.helpBreakLayout)








        #? Settings Box
        
        self.settingsBox = QGroupBox("Settings")

        self.themeDropdownLabel = QLabel("Theme:")
        self.themeDropdown = QComboBox()
        self.themeDropdown.addItems(["Light", "Dark", "Red", "Blue"])
        self.themeDropdown.setFixedHeight(40)
        self.themeDropdown.setCursor(Qt.CursorShape.PointingHandCursor)

        #self.stayOnTopCheckLabel = QLabel("Keep window on top?")
        #self.stayOnTopCheck = QCheckBox()

        self.settingsApiKeyLabel = QLabel("Your Api Key:")
        self.settingsApiKey = QLineEdit("")
        self.settingsApiKey.setFixedHeight(40)
        self.settingsApiKey.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.settingsApiLinkLabel = QLabel("API Link (Leave this field blank if you're not a developer):")
        self.settingsApiLink = QLineEdit("")
        self.settingsApiLink.setFixedHeight(40)

        self.settingsConnect = QPushButton("Connect")
        self.settingsConnect.setFixedHeight(40)
        self.settingsConnect.setCursor(Qt.CursorShape.PointingHandCursor)

        self.settingslayout = QVBoxLayout()
        #self.settingslayout.addWidget(self.stayOnTopCheckLabel)
        #self.settingslayout.addWidget(self.stayOnTopCheck)
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

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.promptText, 0, 0, 1, 0)
        self.mainLayout.addWidget(self.votesGroup, 1, 0, 2, 0)
        self.mainLayout.addWidget(self.votingBox, 4, 0)
        self.mainLayout.addWidget(self.helpBreakBox, 4, 1)
        self.mainLayout.addWidget(self.settingsBox, 5, 0, 2, 2)
        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setRowStretch(2, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 1)