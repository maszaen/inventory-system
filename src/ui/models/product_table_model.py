from PySide6.QtCore import Qt, QAbstractTableModel


from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class ProductTableModel(QAbstractTableModel):
    def __init__(self, products=None, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._products = products or []
        self._headers = [
            "ID",
            "Name",
            "Price",
            "Capital",
            "Stock",
        ]

    def rowCount(self, parent=None):
        return len(self._products)

    def columnCount(self, parent=None):
        return len(self._headers)

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
                return f"Rp{product.capital:,}"
            elif col == 4:
                if product.stock < 3:
                    return f"{product.stock} (Need Restock)"
                else:
                    return str(product.stock)

        elif role == Qt.ForegroundRole:
            if col == 4:
                if product.stock < 3:
                    return QColor("red")

        return None

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._headers[section] if section < len(self._headers) else None
        return None
