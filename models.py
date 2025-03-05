from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QPersistentModelIndex
from PyQt6.QtGui import qRgb, QBrush, QFont

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
            if role == Qt.ItemDataRole.BackgroundRole: # Set Background

                if index.column() == 2:
                    def getColor():
                        if "#" in self.modelTableData[index.row()][index.column()]:
                            rgbColor = tuple(int(str(self.modelTableData[index.row()][index.column()]).split('#')[1][i:i+2], 16) for i in (0, 2, 4))
                            color = QBrush(qRgb(rgbColor[0],rgbColor[1], rgbColor[2]), Qt.BrushStyle.SolidPattern)
                            return color
                        elif "None" in self.modelTableData[index.row()][index.column()]:
                            color = QBrush(qRgb(222, 222, 222), Qt.BrushStyle.SolidPattern)
                            return color
                    return getColor()
                
            elif role == Qt.ItemDataRole.DisplayRole: # Set Text (hides color text)
                if index.column() == 2:
                    return ''
                return self.modelTableData[index.row()][index.column()]

            elif role == Qt.ItemDataRole.TextAlignmentRole: # Set Text Alignment
                return Qt.AlignmentFlag.AlignCenter
            
            elif role == Qt.ItemDataRole.ForegroundRole:
                def getColor():
                    if "#" in self.modelTableData[index.row()][2]:
                        rgbColor = tuple(int(str(self.modelTableData[index.row()][2]).split('#')[1][i:i+2], 16) for i in (0, 2, 4))
                        color = QBrush(qRgb(rgbColor[0],rgbColor[1], rgbColor[2]), Qt.BrushStyle.SolidPattern)
                        return color
                    elif "None" in self.modelTableData[index.row()][2]:
                        color = QBrush(qRgb(222, 222, 222), Qt.BrushStyle.SolidPattern)
                        return color
                return getColor()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.header[col]
        return None
