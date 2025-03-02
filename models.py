from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QPersistentModelIndex
from PyQt6.QtGui import qRgb

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
