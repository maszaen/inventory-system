from PySide6.QtCore import Qt, QAbstractTableModel


class ProductTableModel(QAbstractTableModel):
    def __init__(self, products=None, parent=None):
        super().__init__(parent)
        self._products = products or []

    def rowCount(self, parent=None):
        return len(self._products)

    def columnCount(self, parent=None):
        return 4  # ID, Name, Price, Stock

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        product = self._products[row]

        if role == Qt.DisplayRole:
            if col == 0:
                return str(product._id)
            elif col == 1:
                return product.name
            elif col == 2:
                return f"Rp{product.price:,}"
            elif col == 3:
                return str(product.stock)
        return None

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            headers = ["ID", "Name", "Price", "Stock"]
            return headers[section]
        return None
