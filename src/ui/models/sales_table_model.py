from PySide6.QtCore import Qt, QAbstractTableModel


class SalesTableModel(QAbstractTableModel):
    def __init__(self, transactions=None, parent=None):
        super().__init__(parent)
        self._transactions = transactions or []

    def rowCount(self, parent=None):
        return len(self._transactions)

    def columnCount(self, parent=None):
        return 5  # ID, Date, Product, Quantity, Total

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        transaction = self._transactions[row]

        if role == Qt.DisplayRole:
            if col == 0:
                return str(transaction._id)
            elif col == 1:
                return transaction.date.strftime("%Y-%m-%d")
            elif col == 2:
                return transaction.product_name
            elif col == 3:
                return str(transaction.quantity)
            elif col == 4:
                return f"Rp{transaction.total:,}"
        return None

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            headers = ["ID", "Date", "Product", "Quantity", "Total"]
            return headers[section]
        return None
