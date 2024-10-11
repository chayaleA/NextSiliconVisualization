from typing import Optional

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QLabel, QWidget, QGridLayout, QMenu, QAction, QMessageBox)

from entities.component import Component
from entities.g2h import G2h

from utils.error_messages import ErrorMessages
from utils.constants import OBJECT_COLORS, TID, PACKET, UNKNOWN, CLOSE, BLACK, WHITE, VIEW_LOGS, COMPONENT_LOGS, POINTING_CURSOR
from utils.type_names import G2H

from gui.component_widget import ComponentWidget
from gui.log_colors_dialog import LogColorDialog
from gui.packets_colors import get_colors_by_tids



class G2hWidget(QWidget):
    def __init__(self, g2h: G2h, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.g2h = g2h
        try:
            self.g2h_tids = self.g2h.get_attribute_from_active_logs(TID)
            self.colors = get_colors_by_tids(self.g2h_tids)  # Fetch colors
            self.packet_messages = self.g2h.get_attribute_from_active_logs(PACKET)  # Fetch packet messages
        except Exception as e:
            self.show_error_dialog(
                ErrorMessages.ERROR.value + ErrorMessages.FAILED_TO_RETIEVE_ATTRIBUTE.value.format(attribute="G2H attributes", error=str(e))
            )
        self.initUI()

    def initUI(self) -> None:
        self.layout = QVBoxLayout()

        self.title_label = QLabel(G2H)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            f'border-bottom: 2px solid {BLACK}; padding-bottom: 5px; margin-bottom: 10px; font-weight: bold;')
        self.layout.addWidget(self.title_label)

        # Layout for G2H components (grid layout)
        self.components_layout = QGridLayout()
        self.components_layout.setSpacing(10)
        self.components_layout.setContentsMargins(10, 10, 10, 10)

        # Add g2h_irqa first
        if self.g2h.g2h_irqa:
            component_widget = ComponentWidget(self.g2h.g2h_irqa, self.g2h.g2h_irqa.type_name)
            row, column = 0, 0
            self.components_layout.addWidget(component_widget, row, column)

        # Add EQS components
        row = 1
        col = 0
        for eq in self.g2h.eqs:
            component_widget = ComponentWidget(eq, eq.type_name)
            self.components_layout.addWidget(component_widget, row, col)
            col += 1
            limit_col = 7
            if col >= limit_col:
                col = 0  # Reset column
                row += 1  # Move to the next row

        self.layout.addLayout(self.components_layout)

        # Close button
        self.close_button = QPushButton(CLOSE, self)
        self.close_button.clicked.connect(self.hide_components)
        self.close_button.setStyleSheet(
            f'background-color: #d9534f; color: {WHITE}; border-radius: 5px; padding: 10px;')
        self.close_button.setCursor(POINTING_CURSOR)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)
        self.setVisible(False)

    def create_component_button(self, component: Component, row: Optional[int] = None,
                                col: Optional[int] = None) -> None:
        if component is None:
            return

        color = OBJECT_COLORS.get(component.type_name, WHITE)
        first_color = self.colors[0] if self.colors else WHITE

        button = QPushButton(component.type_name or UNKNOWN, self)
        button.setFixedSize(150, 50)
        button.setStyleSheet(
            f'background-color: {first_color}; border: 2px solid {color}; border-radius: 5px; padding: 10px; color: {BLACK};'
        )
        button.setContextMenuPolicy(Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(
            lambda pos, comp=component: self.show_context_menu(button.mapToGlobal(pos), comp))

        if row is not None and col is not None:
            self.components_layout.addWidget(button, row, col)
        else:
            self.components_layout.addWidget(button)

    def show_context_menu(self, global_pos: QPoint, component: Component) -> None:
        context_menu = QMenu(self)
        view_logs_action = QAction(VIEW_LOGS, self)
        view_logs_action.triggered.connect(lambda: self.show_logs(component))
        context_menu.exec_(global_pos)

    def show_logs(self, component: Component) -> None:
        dialog = LogColorDialog(self.g2h, COMPONENT_LOGS.format(component=component.type_name), self)
        dialog.exec_()

    def show_error_dialog(self, title: str, message: str) -> None:
        """Show an error dialog with the specified title and message."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def show_components(self) -> None:
        self.setVisible(True)

    def hide_components(self) -> None:
        self.setVisible(False)
