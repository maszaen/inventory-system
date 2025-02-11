from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
)
import pymongo
from config import Config
from src.style_config import Theme


class ChangeDatabaseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Database")
        self.setModal(True)
        self.setFixedSize(400, 120)
        self.setup_ui()

    def setup_ui(self):
        cbox = Theme.cbox()
        btn = Theme.btn()
        layout = QVBoxLayout(self)

        # Database Selection
        db_label = QLabel("Select Database:")
        self.db_combo = QComboBox()
        self.db_combo.setStyleSheet(cbox)

        # OK Button
        self.ok_btn = QPushButton("Change Database")
        self.ok_btn.setStyleSheet(btn)
        self.ok_btn.clicked.connect(self.change_database)

        layout.addWidget(db_label)
        layout.addWidget(self.db_combo)
        layout.addWidget(self.ok_btn)

        # Load databases
        self.load_databases()

    def load_databases(self):
        try:
            client = pymongo.MongoClient(Config.MONGODB_URI)
            db_list = client.list_database_names()

            self.db_combo.clear()
            self.db_combo.addItems(db_list)

            # Select current database
            if Config.DB_NAME in db_list:
                self.db_combo.setCurrentText(Config.DB_NAME)

            client.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load databases: {str(e)}")
            self.reject()

    def change_database(self):
        try:
            new_db = self.db_combo.currentText()

            reply = QMessageBox.question(
                self,
                "Confirm Change",
                "Changing database requires application restart.\nProceed with change?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                Config.save_config(Config.MONGODB_URI, new_db)

                QMessageBox.information(
                    self,
                    "Success",
                    "Database changed successfully.\nApplication will now close.\n\nPlease restart the application.",
                )

                self.parent().close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to change database: {str(e)}")
