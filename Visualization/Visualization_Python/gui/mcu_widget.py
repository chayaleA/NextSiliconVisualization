from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QGridLayout, QMessageBox
from typing import Optional

from entities.mcu import Mcu

from utils.constants import POINTING_CURSOR, X_BUTTON, WHITE, RED
from utils.type_names import MCU
from utils.error_messages import ErrorMessages  # Import ErrorMessages

MAX_COLS = 4

class McuInfoWidget(QWidget):
    mcu_closed = pyqtSignal()  # Signal to indicate that MCU is closed

    def __init__(self, mcu: Mcu, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.mcu = mcu
        self.initUI()

    def initUI(self) -> None:
        layout = QVBoxLayout()
        header_layout = QHBoxLayout()

        close_button = QPushButton(X_BUTTON)
        close_button.clicked.connect(self.back)
        close_button.setCursor(POINTING_CURSOR)
        close_button.setStyleSheet(
            f"background-color: {RED}; color: {WHITE}; font-weight: bold; "
            "border: solid; border-radius: 6px; padding: 10px;"
        )
        header_layout.addWidget(close_button, alignment=Qt.AlignRight)

        layout.addLayout(header_layout)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)

        try:
            mcu_components = self.mcu.get_details()  # Attempt to get MCU details
            for index_component, component in enumerate(mcu_components):
                from gui.cluster_info_widget import ComponentWidget

                # Create and add component widgets to the grid
                component_widget = ComponentWidget(component, component.type_name)
                row = index_component // MAX_COLS
                col = index_component % MAX_COLS
                grid_layout.addWidget(component_widget, row, col)

        except Exception as e:
            self.show_error_dialog(ErrorMessages.FAILED_TO_RETIEVE_ATTRIBUTE.value.format(attribute="MCU details", error=str(e)))

        # Add grid layout to main layout
        layout.addLayout(grid_layout)

        # Set the main layout and window title
        self.setLayout(layout)
        self.setWindowTitle(f"{MCU} Details: {self.mcu.id}")

    def show_error_dialog(self, message: str) -> None:
        """Show an error dialog with the specified message."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def back(self):
        self.close()
        self.mcu_closed.emit()  # Emit signal to notify that MCU is closed
        self.parent().show_again()  # Call parent's method to show the previous widget again
