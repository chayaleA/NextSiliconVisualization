from typing import Optional
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QAction, QMenu, QDialog,
                             QScrollArea, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, QSize, QPoint

from entities.component import Component
from entities.h2g import H2g

from utils.constants import OBJECT_COLORS, TID, PACKET, CLOSE, BLACK, WHITE, VIEW_LOGS,POINTING_CURSOR,COMPONENT_LOGS
from utils.type_names import H2G
from utils.error_messages import ErrorMessages

from gui.packets_colors import get_colors_by_tids
from gui.component_widget import ComponentWidget
from gui.log_colors_dialog import LogColorDialog

class H2gWidget(QWidget):

    def __init__(self, h2g: H2g, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.h2g = h2g
        self.h2g_tids = self.h2g.get_attribute_from_active_logs(TID)  # Fetch TID attributes from logs
        self.colors = get_colors_by_tids(self.h2g_tids)  # Fetch colors for TIDs
        self.packet_messages = self.h2g.get_attribute_from_active_logs(PACKET)  # Fetch packet messages
        self.initUI()

    def initUI(self) -> None:
        self.layout = QVBoxLayout()

        self.title_label = QLabel(H2G)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            f'border-bottom: 2px solid {BLACK}; padding-bottom: 5px; margin-bottom: 10px; font-weight: bold;')
        self.layout.addWidget(self.title_label)

        # Layout for H2G components (horizontally)
        self.components_layout = QHBoxLayout()
        self.components_layout.setSpacing(10)
        self.components_layout.setContentsMargins(5, 5, 5, 5)

        # Create ComponentWidget instances for each H2G component
        try:
            self.add_component_widget(self.h2g.cbus_inj)
            self.add_component_widget(self.h2g.cbus_clt)
            self.add_component_widget(self.h2g.nfi_inj)
            self.add_component_widget(self.h2g.nfi_clt)
            self.add_component_widget(self.h2g.h2g_irqa)
        except Exception as e:
            self.show_error_dialog(
                ErrorMessages.ERROR.value + ErrorMessages.FAILED_TO_RETIEVE_ATTRIBUTE.value.format(attribute="components", error=str(e))
            )

        self.layout.addLayout(self.components_layout)

        # Context menu for the entire H2G widget
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Enable custom context menu
        self.customContextMenuRequested.connect(self.show_context_menu_area)

        # Close button
        self.close_button = QPushButton(CLOSE, self)
        self.close_button.clicked.connect(self.hide_components)
        self.close_button.setCursor(POINTING_CURSOR)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def add_component_widget(self, component: Component) -> None:
        if component:
            component_widget = ComponentWidget(component, component.type_name)
            self.components_layout.addWidget(component_widget)

    def show_context_menu_area(self, global_pos: QPoint) -> None:
        """ Show a context menu when right-clicked. """
        context_menu = QMenu(self)
        view_logs_action = QAction(VIEW_LOGS, self)
        view_logs_action.triggered.connect(lambda: self.show_logs())  # Show logs for the entire area
        context_menu.exec_(global_pos)

    def show_logs(self) -> None:
        dialog = LogColorDialog(self.h2g, COMPONENT_LOGS.format(component=self.h2g.type_name), self)
        dialog.exec_()

    def show_components(self) -> None:
        """ Show the H2G widget components. """
        self.setVisible(True)

    def hide_components(self) -> None:
        """ Hide the H2G widget components. """
        self.setVisible(False)
