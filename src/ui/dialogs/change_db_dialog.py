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
from config import EnvConfig


class ChangeDatabaseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Database")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Database Selection
        db_label = QLabel("Select Database:")
        self.db_combo = QComboBox()

        # OK Button
        self.ok_btn = QPushButton("Change Database")
        self.ok_btn.clicked.connect(self.change_database)

        layout.addWidget(db_label)
        layout.addWidget(self.db_combo)
        layout.addWidget(self.ok_btn)

        # Load databases
        self.load_databases()

    def load_databases(self):
        try:
            client = pymongo.MongoClient(EnvConfig.MONGODB_URI)
            db_list = client.list_database_names()

            self.db_combo.clear()
            self.db_combo.addItems(db_list)

            # Select current database
            if EnvConfig.DB_NAME in db_list:
                self.db_combo.setCurrentText(EnvConfig.DB_NAME)

            client.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load databases: {str(e)}")
            self.reject()

    def change_database(self):
        try:
            new_db = self.db_combo.currentText()

            # Konfirmasi perubahan
            reply = QMessageBox.question(
                self,
                "Confirm Change",
                "Changing database requires application restart.\nProceed with change?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                # Save new database name
                EnvConfig.save_config(EnvConfig.MONGODB_URI, new_db)

                QMessageBox.information(
                    self,
                    "Success",
                    "Database changed successfully.\nApplication will now close.\n\nPlease restart the application.",
                )

                self.parent().close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to change database: {str(e)}")
