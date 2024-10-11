from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox

from typing import Optional

from entities.component import Component

from utils.error_messages import ErrorMessages
from utils.constants import OBJECT_COLORS, TID, BLACK, WHITE, LIGHTGRAY, COMPONENT_LOGS, FORBIDDEN_CURSOR, ARROW_CURSOR

from gui.log_colors_dialog import LogColorDialog
from gui.packets_colors import get_colors_by_tids



class ComponentWidget(QWidget):
    def __init__(self, component: Component, type_name: str,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.type_name = type_name

        try:
            self.component = component
            self.comp_tids = self.component.get_attribute_from_active_logs(TID)
            self.colors = get_colors_by_tids(self.comp_tids)  # Fetch colors based on TIDs
        except Exception as e:
            self.show_error_dialog(ErrorMessages.ERROR.value,
                                   ErrorMessages.ERROR_OCCURRED.format(error=str(e)))
            return

        self.initUI()

    def initUI(self) -> None:
        if not self.comp_tids:
            background_color = LIGHTGRAY
            text_color = WHITE
            self.setCursor(ARROW_CURSOR)  # Normal cursor, indicating no interaction
        else:
            # If logs are present, set the normal colors and cursor
            background_color = WHITE
            text_color = BLACK
            if self.colors:
                background_color = self.colors[0]

            self.setCursor(FORBIDDEN_CURSOR)  # Cursor indicating restricted interaction

        self.setStyleSheet(
            f'background-color: {background_color}; border: 1px solid {WHITE}; '
            f'padding: 0px; border-radius: 5px;'
        )

        layout = QVBoxLayout()
        label = QLabel(self.type_name)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f'color: {text_color};')
        layout.addWidget(label)
        self.setLayout(layout)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.comp_tids and event.button() == Qt.RightButton:
            self.show_logs()

    def show_logs(self) -> None:
        try:
            dialog = LogColorDialog(self.component, COMPONENT_LOGS.format(component=self.component.type_name), self)
            dialog.exec_()
        except Exception as e:
            self.show_error_dialog(ErrorMessages.ERROR.value,
                                   ErrorMessages.ERROR_OCCURRED.format(error=str(e)))

    def show_error_dialog(self, title: str, message: str) -> None:
        """Show an error dialog with the specified title and message."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
