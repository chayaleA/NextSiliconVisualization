import os
import shutil
from pathlib import Path

from PyQt5.QtCore import Qt, QThreadPool, QTimer
from PyQt5.QtGui import QFont, QIcon,QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QFileDialog

from utils.data_manager import DataManager
from utils.paths import APP_ICON_IMAGE, LOADING_DATA_IMAGE,CHIP_DATA_JSON

from gui.main_window import MainWindow
from gui.worker_thread import WorkerThread


class FileSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.sl_file = None
        self.csv_file = None
        self.threadpool = QThreadPool()
        self.setWindowTitle("Select Required Files")
        icon_path = os.path.join(os.getcwd(), APP_ICON_IMAGE)
        self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(400, 200, 600, 300)
        self.setStyleSheet(self.get_stylesheet())

        self.init_ui()

    def init_ui(self):
        """Initialize the UI with labels, buttons, and layout."""
        layout = QVBoxLayout()

        title_label = QLabel("Please select the required files to continue:")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Row for SL JSON file
        sl_layout = QHBoxLayout()
        sl_label = QLabel("SL File:  ")
        self.sl_file_input = QLineEdit()
        self.sl_file_input.setReadOnly(True)
        sl_button = QPushButton("Browse")
        sl_button.clicked.connect(self.select_sl_file)
        sl_layout.addWidget(sl_label)
        sl_layout.addWidget(self.sl_file_input)
        sl_layout.addWidget(sl_button)

        # Row for CSV file
        csv_layout = QHBoxLayout()
        csv_label = QLabel("CSV File:")
        self.csv_file_input = QLineEdit()
        self.csv_file_input.setReadOnly(True)
        csv_button = QPushButton("Browse")
        csv_button.clicked.connect(self.select_csv_file)
        csv_layout.addWidget(csv_label)
        csv_layout.addWidget(self.csv_file_input)
        csv_layout.addWidget(csv_button)

        # Proceed button
        self.proceed_button = QPushButton("Proceed")
        self.proceed_button.setEnabled(False)
        self.proceed_button.clicked.connect(self.proceed)

        layout.addLayout(sl_layout)
        layout.addLayout(csv_layout)
        layout.addWidget(self.proceed_button, alignment=Qt.AlignCenter)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.setLayout(layout)

    def show_error(self, message):
        """Show an error message box."""
        error_msg = QMessageBox(self)
        error_msg.setWindowTitle("Error")
        error_msg.setText(message)
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setStyleSheet(self.get_stylesheet())
        error_msg.exec_()

    def show_success(self, message):
        """Show a success message box."""
        success_msg = QLabel(message, self)
        success_msg.setAlignment(Qt.AlignCenter)
        success_msg.setStyleSheet("color: green; font-size: 12pt; font-weight: bold; padding: 10px;")
        self.layout().addWidget(success_msg)

        # Set a timer to remove the success message after 3 seconds
        QTimer.singleShot(1000, lambda: self.layout().removeWidget(success_msg))

    def select_sl_file(self):
        """Open file dialog to select SL JSON file and validate."""
        try:
            file, _ = QFileDialog.getOpenFileName(self, "Select SL JSON File", "", "JSON Files (*.json);;All Files (*)")
            if file:
                if not file.endswith('.json'):
                    self.show_error("The selected SL file is not a valid JSON file.")
                    return

                self.sl_file = Path(file)
                self.sl_file_input.setText(self.sl_file.name)
                self.check_files_selected()
                self.show_success("SL file selected successfully.")

        except Exception as e:
            self.show_error(f"An error occurred while selecting the SL file: {e}")

    def select_csv_file(self):
        """Open file dialog to select CSV file and validate."""
        try:
            file, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)")
            if file:
                if not file.endswith('.csv'):
                    self.show_error("The selected file is not a valid CSV file.")
                    return

                destination_dir = Path(os.getcwd()) / 'data'
                destination_dir.mkdir(exist_ok=True)

                base_name = 'logs.csv'
                destination_file = destination_dir / base_name
                temp_file = destination_dir / 'temp_logs.csv'

                try:
                    shutil.copy(file, temp_file)
                    if destination_file.exists():
                        destination_file.unlink()

                    temp_file.rename(destination_file)
                    self.csv_file = destination_file
                    self.csv_file_input.setText(self.csv_file.name)
                    self.check_files_selected()
                    self.show_success("CSV file selected and saved successfully.")

                except OSError as e:
                    self.show_error(f"An error occurred while handling the CSV file: {e}")
                    if temp_file.exists():
                        temp_file.unlink()

        except Exception as e:
            self.show_error(f"An unexpected error occurred: {e}")

    def check_files_selected(self):
        """Enable the proceed button if both files are selected."""
        if self.sl_file and self.csv_file:
            self.proceed_button.setEnabled(True)

    def proceed(self):
        """Proceed with the selected files and initialize data manager."""
        if not self.sl_file or not self.csv_file:
            self.show_error("Both files are required!")
            return

        self.show_loading_overlay()
        self.perform_action_with_wait(self.create_data_manager,CHIP_DATA_JSON, self.sl_file, self.csv_file)

    def perform_action_with_wait(self, action, *args):
        self.show_loading_overlay()
        self.worker_thread = WorkerThread(action, args)
        self.worker_thread.finished.connect(self.on_data_manager_created)
        self.worker_thread.start()

    def create_data_manager(self, *args):
        """Create the data manager instance."""
        self.data_menager= DataManager(*args)

    def on_data_manager_created(self):
        """Handle success and open the main window."""
        # self.hide_loading_overlay()
        main_window = MainWindow(self.data_menager)
        main_window.showMaximized()
        self.close()

    def on_error(self, error_message):
        """Handle errors that occur during processing."""
        self.hide_loading_overlay()
        self.show_error(f"An error occurred during processing: {error_message}")

    def show_loading_overlay(self):
        """Show a loading overlay with an image while processing."""
        self.overlay = QWidget(self)
        self.overlay.setGeometry(self.rect())

        self.overlay.setAttribute(Qt.WA_TranslucentBackground, True)

        layout = QVBoxLayout(self.overlay)

        loading_image = QLabel(self.overlay)
        image_path = os.path.join(os.getcwd(), LOADING_DATA_IMAGE)

        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"Failed to load image from {image_path}.")
            return  # Stop here if the image fails to load

        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        loading_image.setPixmap(pixmap)

        loading_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(loading_image)

        self.overlay.show()
        self.setEnabled(False)  # Disable interaction during loading

    def hide_loading_overlay(self):
        """Hide the loading overlay after processing."""
        if hasattr(self, 'overlay'):
            self.overlay.hide()
            self.overlay.deleteLater()

    def get_stylesheet(self):
        """Return the QSS stylesheet for widget styling."""
        return """
            QWidget {
                background-color: #f0f4f7;
                font-family: Arial;
            }
            QLabel {
                color: #333;
                font-size: 12pt;
            }
            QLineEdit {
                background-color: #fff;
                border: 2px solid #b0c4de;
                padding: 4px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #87ceeb;
                color: #fff;
                border: none;
                padding: 8px 16px;
                font-size: 12pt;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #00bfff;
            }
            QPushButton:pressed {
                background-color: #1e90ff;
            }
        """
