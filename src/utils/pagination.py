from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
)
from PySide6.QtCore import Signal


class PaginationWidget(QWidget):
    # Signal untuk memberitahu parent widget ketika halaman berubah
    pageChanged = Signal(int, int)  # current_page, items_per_page

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 1
        self.total_items = 0
        self.items_per_page = 10
        self._setting_total = False
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        # Items per page selector
        self.page_size_label = QLabel("Items per page:", self)
        self.page_size_label.setStyleSheet("color: #888888; font-size: 13px;")

        self.page_size_combo = QComboBox(self)
        self.page_size_combo.addItems(["10", "25", "50", "100"])
        self.page_size_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
                color: white;
                min-width: 70px;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #3c3c3c;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
        """
        )
        self.page_size_combo.currentTextChanged.connect(self.on_page_size_changed)

        # Navigation buttons style
        button_style = """
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px 10px;
                color: white;
                min-width: 30px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
            QPushButton:disabled {
                background-color: #1e1e1e;
                color: #666666;
            }
        """

        # Navigation buttons
        self.first_button = QPushButton("«", self)
        self.prev_button = QPushButton("‹", self)
        self.next_button = QPushButton("›", self)
        self.last_button = QPushButton("»", self)

        for button in [
            self.first_button,
            self.prev_button,
            self.next_button,
            self.last_button,
        ]:
            button.setStyleSheet(button_style)

        self.first_button.clicked.connect(lambda: self.set_page(1))
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.last_button.clicked.connect(lambda: self.set_page(self.total_pages))

        # Page info label
        self.page_info = QLabel(self)
        self.page_info.setStyleSheet("color: white; margin: 0 10px;")

        # Add widgets to layout
        layout.addWidget(self.page_size_label)
        layout.addWidget(self.page_size_combo)
        layout.addStretch()
        layout.addWidget(self.first_button)
        layout.addWidget(self.prev_button)
        layout.addWidget(self.page_info)
        layout.addWidget(self.next_button)
        layout.addWidget(self.last_button)

        self.update_ui()

    def set_total_items(self, total):
        """Set total number of items and update UI"""
        if self._setting_total or total == self.total_items:
            return

        self._setting_total = True
        self.total_items = total
        self.current_page = 1
        self.update_ui()
        self.pageChanged.emit(self.current_page, self.items_per_page)
        self._setting_total = False

    def update_ui(self):
        """Update UI state based on current page and total items"""
        self.total_pages = max(
            1, (self.total_items + self.items_per_page - 1) // self.items_per_page
        )

        # Update page info
        start_item = (self.current_page - 1) * self.items_per_page + 1
        end_item = min(self.current_page * self.items_per_page, self.total_items)
        self.page_info.setText(
            f"Page {self.current_page} of {self.total_pages} ({start_item}-{end_item} of {self.total_items})"
        )

        # Update button states
        self.first_button.setEnabled(self.current_page > 1)
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < self.total_pages)
        self.last_button.setEnabled(self.current_page < self.total_pages)

    def set_page(self, page):
        """Set current page and emit signal"""
        if 1 <= page <= self.total_pages and page != self.current_page:
            self.current_page = page
            self.update_ui()
            self.pageChanged.emit(self.current_page, self.items_per_page)

    def prev_page(self):
        """Go to previous page"""
        self.set_page(self.current_page - 1)

    def next_page(self):
        """Go to next page"""
        self.set_page(self.current_page + 1)

    def on_page_size_changed(self, size):
        """Handle page size change"""
        self.items_per_page = int(size)
        self.current_page = 1
        self.update_ui()
        self.pageChanged.emit(self.current_page, self.items_per_page)
