from PyQt6.QtCharts import QPieSeries, QBarSeries, QBarSet, QChart, QChartView
from PyQt6.QtCore import QSize, Qt, QAbstractTableModel, QAbstractItemModel, QVariant, QThread, QObject, pyqtSlot, pyqtSignal, QPersistentModelIndex, QModelIndex
from PyQt6.QtGui import qRgb, QIcon, QPalette, QFont, QPainter, QPen, QColor
from PyQt6.QtWidgets import (QTabWidget, QApplication, QLayout, QComboBox, QCheckBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QTableView, QVBoxLayout, QHeaderView, QWidget, QTableWidgetItem, QStyleFactory, QStyle)
from models import TableModel

class StudentLayout:
    def __init__(self):
        self.activeForm()

        self.FormOptions()
        self.debugTestingTab()
        self.profileTab()
        self.settingsTab()

        self.activeFormW = QWidget()
        self.activeFormW.setLayout(self.votingShownLayout)
        self.activeFormW.setMinimumWidth(600)

        self.formW = QGroupBox()
        self.formW.setLayout(self.formOptionsLayout)

        self.profileTabW = QGroupBox()
        self.profileTabW.setLayout(self.profileTabLayout)

        self.settingsTabW = QGroupBox()
        self.settingsTabW.setLayout(self.settingsTabLayout)

        self.debugTabW = QGroupBox()
        self.debugTabW.setLayout(self.debugLayout)
        
        self.tabs = QTabWidget()
        self.tabs.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.tabs.addTab(self.formW, "Poll Options")
        self.tabs.addTab(self.profileTabW, "Profile")
        self.tabs.addTab(self.settingsTabW, "Settings")
        self.tabs.addTab(self.debugTabW, "Debug")
        #self.tabs.addTab(self.studentsTabW, "Students")

        self.tabs.setDocumentMode(True)
        
        self.fullPage = QWidget()
        self.fullPageLayout = QHBoxLayout()
        self.fullPageLayout.addWidget(self.activeFormW)
        self.fullPageLayout.addWidget(self.tabs)
        

    def FormOptions(self):
        self.votingBox = QGroupBox()
        self.votingBox.setObjectName('votingBox')
        self.votinglayout = QVBoxLayout()
        self.votingBox.setLayout(self.votinglayout)

        self.currentVoteLabel = QLabel()
        self.currentVoteLabel.setText("Your current vote is:")
        self.currentVoteLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.currentVoteLabel.setObjectName("currentVoteLabel")

        self.currentVoteShow = QPushButton("None")
        self.currentVoteShow.setObjectName("currentVoteButton")
        self.currentVoteShow.setFixedWidth(240)
        self.currentVoteShow.setEnabled(False)

        self.showVotingBox = QGroupBox()
        self.showVoteOptions = QHBoxLayout()
        self.showVotingBox.setLayout(self.showVoteOptions)

        
        self.removeVoteButton = QPushButton("Remove Vote")
        self.removeVoteButton.setFixedHeight(40)
        self.removeVoteButton.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.votinglayout.addWidget(self.showVotingBox)
        self.votinglayout.addWidget(self.removeVoteButton)

        self.helpBreakBox = QGroupBox()

        self.helpTicketButton = QPushButton("Send Help Ticket")
        self.helpTicketButton.setFixedHeight(60)
        self.helpTicketButton.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.takeBreakButton = QPushButton("Take a Break")
        self.takeBreakButton.setFixedHeight(60)
        self.takeBreakButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self.helpBreakLayout = QHBoxLayout()
        self.helpBreakLayout.addWidget(self.helpTicketButton)
        self.helpBreakLayout.addWidget(self.takeBreakButton)
        self.helpBreakLayout.setSpacing(0)
        self.helpBreakBox.setLayout(self.helpBreakLayout)

        self.formOptionsLayout = QVBoxLayout()
        self.formOptionsLayout.addStretch()
        self.formOptionsLayout.addWidget(self.currentVoteLabel)
        self.formOptionsLayout.addWidget(self.currentVoteShow, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.formOptionsLayout.addWidget(self.votingBox)
        self.formOptionsLayout.addWidget(self.helpBreakBox)
        self.formOptionsLayout.addStretch()



    def profileTab(self):
        self.profileTabLayout = QVBoxLayout()
        
        self.profileTabLayoutText = QLabel()
        self.profileTabLayoutText.setText("The profile page is currently\nunavailable.")
        self.profileTabLayoutText.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.profileTabLayoutText.setObjectName("currentVoteLabel")
        self.profileTabLayout.addWidget(self.profileTabLayoutText)

    def debugTestingTab(self):
        self.debugLayout = QVBoxLayout()

    def settingsTab(self):
        self.settingsBox = QWidget()

        stayOnTopBox = QWidget()
        stayOnTopBoxLayout = QHBoxLayout()
        stayOnTopBox.setLayout(stayOnTopBoxLayout)
        self.stayOnTopCheckLabel = QLabel("Keep window on top?")
        self.stayOnTopCheck = QCheckBox()
        stayOnTopBoxLayout.addWidget(self.stayOnTopCheckLabel)
        stayOnTopBoxLayout.addWidget(self.stayOnTopCheck)
        stayOnTopBoxLayout.addStretch(1)

        self.themeDropdownLabel = QLabel("Theme:")
        self.themeDropdown = QComboBox()
        self.themeDropdown.addItems(["Light (ew)", "Dark", "Red", "Blue", "Pink"])
        self.themeDropdown.setFixedHeight(40)
        self.themeDropdown.setCursor(Qt.CursorShape.PointingHandCursor)

        self.graphViewLabel = QLabel("Graph View:")
        self.graphViewDropdown = QComboBox()
        self.graphViewDropdown.addItems(["Bar", "Donut", "Table", "Pie"])
        self.graphViewDropdown.setFixedHeight(40)
        self.graphViewDropdown.setCursor(Qt.CursorShape.PointingHandCursor)
       
        graphLegendCheckbox = QWidget()
        graphLegendCheckLayout = QHBoxLayout()
        graphLegendCheckbox.setLayout(graphLegendCheckLayout)
        self.graphLegendCheckboxLabel = QLabel("Show Graph Legend?")
        self.graphLegendCheckboxCB = QCheckBox()
        graphLegendCheckLayout.addWidget(self.graphLegendCheckboxLabel)
        graphLegendCheckLayout.addWidget(self.graphLegendCheckboxCB)
        graphLegendCheckLayout.addStretch(1)
       
        graphAnimationCheckbox = QWidget()
        graphAnimationCheckLayout = QHBoxLayout()
        graphAnimationCheckbox.setLayout(graphAnimationCheckLayout)
        self.graphAnimationCheckboxLabel = QLabel("Enable Graph Animations?")
        self.graphAnimationCheckboxCB = QCheckBox()
        graphAnimationCheckLayout.addWidget(self.graphAnimationCheckboxLabel)
        graphAnimationCheckLayout.addWidget(self.graphAnimationCheckboxCB)
        graphAnimationCheckLayout.addStretch(1)
        graphAnimationCheckbox.hide()

        self.settingsApiKeyLabel = QLabel("Your API Key:")
        self.settingsApiKey = QLineEdit("")
        self.settingsApiKey.setObjectName("textInputs")
        self.settingsApiKey.setFixedHeight(40)
        self.settingsApiKey.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.settingsApiLinkLabel = QLabel("API Link (Developer Only):")
        self.settingsApiLink = QLineEdit("")
        self.settingsApiLink.setObjectName("textInputs")
        self.settingsApiLink.setFixedHeight(40)

        self.settingsConnect = QPushButton("Connect")
        self.settingsConnect.setFixedHeight(40)
        self.settingsConnect.setCursor(Qt.CursorShape.PointingHandCursor)

        self.settingsRemoveAll = QPushButton("Clear Settings")
        self.settingsRemoveAll.setFixedHeight(40)
        self.settingsRemoveAll.setCursor(Qt.CursorShape.PointingHandCursor)

        self.settingsTabLayout = QVBoxLayout()
        self.settingsTabLayout.addStretch(1)
        self.settingsTabLayout.addWidget(stayOnTopBox)
        self.settingsTabLayout.addWidget(self.themeDropdownLabel)
        self.settingsTabLayout.addWidget(self.themeDropdown)
        self.settingsTabLayout.addWidget(self.graphViewLabel)
        self.settingsTabLayout.addWidget(self.graphViewDropdown)
        self.settingsTabLayout.addWidget(graphLegendCheckbox)
        self.settingsTabLayout.addWidget(graphAnimationCheckbox)
        self.settingsTabLayout.addWidget(self.settingsApiKeyLabel)
        self.settingsTabLayout.addWidget(self.settingsApiKey)
        self.settingsTabLayout.addWidget(self.settingsApiLinkLabel)
        self.settingsTabLayout.addWidget(self.settingsApiLink)
        self.settingsTabLayout.addWidget(self.settingsConnect)
        self.settingsTabLayout.addWidget(self.settingsRemoveAll)
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

        
        

        self.votesGroup = QGroupBox()

        model = TableModel(None, ["Votes", "Responses", "Color"], [])
        self.voteViewTable = QTableView()
        self.voteViewTable.setModel(model)
        self.voteViewTable.setSelectionMode(self.voteViewTable.SelectionMode.NoSelection)
        self.voteViewTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.voteViewTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.voteViewTable.verticalHeader().hide()
        votesFont = QFont()
        votesFont.setBold(True)
        votesFont.setPointSize(16)
        headFont = QFont()
        headFont.setBold(False)
        headFont.setPointSize(10)
        self.voteViewTable.setFont(votesFont)
        self.voteViewTable.horizontalHeader().setFont(headFont)

        self.graphViewBarChartSeries = QBarSeries()
        self.graphViewBarChartSet = QBarSet("name")
        self.graphViewBarChartSet2 = QBarSet("name")
        self.graphViewBarChartSet.append(2)
        self.graphViewBarChartSet2.append(5)
        self.graphViewBarChartSeries.append(self.graphViewBarChartSet)
        self.graphViewBarChartSeries.append(self.graphViewBarChartSet2)
        self.graphViewBarChart = QChart()
        self.graphViewBarChart.setBackgroundPen(QColor("transparent"))
        self.graphViewBarChart.setBackgroundBrush(QColor("transparent"))
        self.graphViewBarChart.addSeries(self.graphViewBarChartSeries)
        #self.graphViewBarChart.legend().hide()
        self.graphViewBarChart.legend().setLabelColor(QColor("black"))
        self.graphViewBarChart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.graphViewBarChartView = QChartView(self.graphViewBarChart)
        self.graphViewBarChartView.setBackgroundBrush(QColor(255, 255, 255, 0))
        self.graphViewBarChartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.graphViewDonutChartSeries = QPieSeries()
        self.graphViewDonutChartSeries.setHoleSize(0.35)
        self.graphViewDonutChartSeries.append('', 1)
        self.graphViewDonutChartSeries.append('', 2)
        self.graphViewDonutChartSeries.append('', 3)
        self.graphViewDonutChartSeries.append('', 4)
        self.graphViewDonutChartSeries.append('', 5)
        self.graphViewDonutChart = QChart()
        self.graphViewDonutChart.setBackgroundPen(QColor("transparent"))
        self.graphViewDonutChart.setBackgroundBrush(QColor("transparent"))
        self.graphViewDonutChart.addSeries(self.graphViewDonutChartSeries)
        #self.graphViewDonutChart.legend().hide()
        self.graphViewDonutChart.legend().setLabelColor(QColor("black"))
        self.graphViewDonutChart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.graphViewDonutChartView = QChartView(self.graphViewDonutChart)
        self.graphViewDonutChartView.setBackgroundBrush(QColor(255, 255, 255, 0))
        self.graphViewDonutChartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.graphViewPieChartSeries = QPieSeries()
        self.graphViewPieChartSeries.setHoleSize(0)
        self.graphViewPieChartSeries.append('', 1)
        self.graphViewPieChartSeries.append('', 2)
        self.graphViewPieChartSeries.append('', 3)
        self.graphViewPieChartSeries.append('', 4)
        self.graphViewPieChartSeries.append('', 5)
        self.graphViewPieChart = QChart()
        self.graphViewPieChart.setBackgroundPen(QColor("transparent"))
        self.graphViewPieChart.setBackgroundBrush(QColor("transparent"))
        self.graphViewPieChart.addSeries(self.graphViewPieChartSeries)
        #self.graphViewPieChart.legend().hide()
        self.graphViewPieChart.legend().setLabelColor(QColor("black"))
        self.graphViewPieChart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.graphViewPieChartView = QChartView(self.graphViewPieChart)
        self.graphViewPieChartView.setBackgroundBrush(QColor(255, 255, 255, 0))
        self.graphViewPieChartView.setRenderHint(QPainter.RenderHint.Antialiasing)


        self.votesLayout = QVBoxLayout()
        self.votesLayout.addWidget(self.graphViewBarChartView)
        self.votesLayout.addWidget(self.graphViewDonutChartView)
        self.votesLayout.addWidget(self.voteViewTable)
        self.votesLayout.addWidget(self.graphViewPieChartView)
        self.votesGroup.setLayout(self.votesLayout)

        #? Main Layout

        self.votingShownLayout = QGridLayout()
        self.votingShownLayout.addWidget(self.promptText, 0, 0, 1, 0)
        self.votingShownLayout.addWidget(self.votesGroup, 1, 0, 2, 0)
        self.votingShownLayout.setRowStretch(1, 1)
        self.votingShownLayout.setRowStretch(2, 1)
        self.votingShownLayout.setColumnStretch(0, 1)
        self.votingShownLayout.setColumnStretch(1, 1)