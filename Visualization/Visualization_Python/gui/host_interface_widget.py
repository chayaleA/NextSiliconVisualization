from typing import Dict, Optional

from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QFrame, QMenu, QAction, QMessageBox)
from PyQt5.QtCore import Qt, QPoint

from entities.component import Component
from entities.host_interface import HostInterface

from gui.g2h_widget import G2hWidget
from gui.h2g_widget import H2gWidget
from gui.log_colors_dialog import LogColorDialog
from gui.packets_colors import get_colors_by_tids

from utils.constants import OBJECT_COLORS, TID, PACKET, LIGHTGRAY, WHITE, BLACK, COMPONENT_LOGS, VIEW_LOGS, FORBIDDEN_CURSOR, POINTING_CURSOR
from utils.type_names import HOST_INTERFACE, H2G, G2H, BMT, PCIE
from utils.error_messages import ErrorMessages


class HostInterfaceWidget(QWidget):
    def __init__(self, host_interface: HostInterface, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.host_interface = host_interface
        self.host_interface_tids = self.host_interface.get_attribute_from_active_logs(TID)
        self.colors = list(get_colors_by_tids(self.host_interface_tids))
        self.colors_bmt = list(self.get_colors(self.host_interface.bmt))
        self.colors_H2G = list(self.get_colors(self.host_interface.h2g))
        self.colors_G2H = list(self.get_colors(self.host_interface.g2h))
        self.colors_pcie = list(self.get_colors(self.host_interface.pcie))
        self.packet_messages = self.host_interface.get_attribute_from_active_logs(PACKET)

        self.color_map = self.create_color_map()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_host_interface_logs)
        self.initUI()

    def initUI(self) -> None:
        self.main_layout = QVBoxLayout()

        self.outer_frame = QFrame()
        self.outer_frame.setFrameShape(QFrame.StyledPanel)
        self.outer_frame.setFrameShadow(QFrame.Raised)

        # Ensure color lists are not empty before accessing their elements
        self.title_color = self.colors[0] if self.colors else WHITE
        self.title_color_bmt = self.colors_bmt[0] if self.colors_bmt else WHITE
        self.title_color_H2G = self.colors_H2G[0] if self.colors_H2G else WHITE
        self.title_color_G2H = self.colors_G2H[0] if self.colors_G2H else WHITE
        self.title_color_pcie = self.colors_pcie[0] if self.colors_pcie else WHITE

        self.title_label = QLabel(HOST_INTERFACE)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            f'border-bottom: 2px solid {BLACK}; padding-bottom: 5px; margin-bottom: 10px; background-color: {self.title_color}; font-weight: bold;'
        )

        self.title_label.setCursor(POINTING_CURSOR)

        self.frame_layout = QVBoxLayout()
        self.frame_layout.addWidget(self.title_label)

        self.component_buttons_layout = QWidget()
        self.component_buttons_layout.setLayout(QHBoxLayout())
        self.create_component_button(self.host_interface.bmt)
        self.create_component_button(self.host_interface.h2g, clickable=True)
        self.create_component_button(self.host_interface.g2h, clickable=True)
        self.create_component_button(self.host_interface.pcie)
        self.component_buttons_layout.setVisible(True)
        self.frame_layout.addWidget(self.component_buttons_layout)

        self.outer_frame.setLayout(self.frame_layout)
        self.main_layout.addWidget(self.outer_frame)
        self.setLayout(self.main_layout)

        self.h2g_widget = H2gWidget(self.host_interface.h2g) if self.host_interface.h2g else None
        self.g2h_widget = G2hWidget(self.host_interface.g2h) if self.host_interface.g2h else None

        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout()
        self.details_widget.setLayout(self.details_layout)
        self.details_widget.setVisible(False)
        self.main_layout.addWidget(self.details_widget)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def toggle_content(self, event) -> None:
        is_visible = self.component_buttons_layout.isVisible()
        self.component_buttons_layout.setVisible(not is_visible)
        self.details_widget.setVisible(False)

    def create_color_map(self) -> Dict[str, str]:
        """
        Create a mapping of TID to colors.
        """
        color_map = {}
        for idx, tid in enumerate(self.host_interface_tids):
            if idx < len(self.colors):
                color_map[tid] = self.colors[idx]
            else:
                color_map[tid] = WHITE
        return color_map

    def show_context_menu_for_component(self, point: QPoint, component: Component) -> None:
        """Show a context menu for the given component."""
        context_menu = QMenu(self)
        log_action = QAction(VIEW_LOGS, self)
        log_action.triggered.connect(
            lambda: self.show_colors_and_logs(component, COMPONENT_LOGS.format(component=component.type_name)))
        context_menu.addAction(log_action)
        context_menu.exec_(self.mapToGlobal(point))

    def show_context_menu(self, point: QPoint) -> None:
        """Show a general context menu."""
        context_menu = QMenu(self)
        context_menu.exec_(self.mapToGlobal(point))

    def get_colors(self, data) -> list:
        data_tids = data.get_attribute_from_active_logs(TID)
        return list(get_colors_by_tids(data_tids))

    def show_error_dialog(self, title: str, message: str) -> None:
        """Show an error dialog with the specified title and message."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def create_component_button(self, component: Component, clickable: Optional[bool] = False) -> None:
        if component is None:
            return

        button = QPushButton(component.type_name, self)
        button.setFixedSize(200, 70)

        # Set the background color based on the component type
        if component.type_name == BMT:
            background_color = self.title_color_bmt
        elif component.type_name == H2G:
            background_color = self.title_color_H2G
        elif component.type_name == G2H:
            background_color = self.title_color_G2H
        elif component.type_name == PCIE:
            background_color = self.title_color_pcie
        else:
            background_color = LIGHTGRAY  # Default color if type_name is unrecognized

        if not component.get_attribute_from_active_logs(TID):
            background_color = LIGHTGRAY
            clickable = False

        button.setStyleSheet(
            f'background-color: {background_color}; border: 2.5px solid  {LIGHTGRAY}; border-radius: 7px; padding: 10px; margin: 10px;')

        if clickable:
            button.setCursor(POINTING_CURSOR)
            button.clicked.connect(lambda: self.show_details(component.type_name))
        else:
            button.setCursor(FORBIDDEN_CURSOR)
            button.setStyleSheet(button.styleSheet() + f'color: {WHITE};')

        button.setContextMenuPolicy(Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(
            lambda point: self.show_colors_and_logs(component, COMPONENT_LOGS.format(component=component.type_name)))

        self.component_buttons_layout.layout().addWidget(button)

    def show_details(self, section_name: str) -> None:
        """Show details for the selected section (H2G or G2H)."""
        try:
            self.details_widget.setVisible(True)
            if section_name == H2G and self.h2g_widget:
                self.g2h_widget.hide_components()
                self.details_layout.addWidget(self.h2g_widget)
                self.h2g_widget.show_components()
                self.h2g_widget.setCursor(POINTING_CURSOR)

            elif section_name == G2H and self.g2h_widget:
                self.h2g_widget.hide_components()
                self.details_layout.addWidget(self.g2h_widget)
                self.g2h_widget.show_components()
                self.g2h_widget.setCursor(POINTING_CURSOR)

            else:
                raise ValueError(ErrorMessages.ERROR.value,
                                 ErrorMessages.SHOWING_WIDGET.value.format(widget=section_name))
        except ValueError as e:
            self.show_error_dialog(ErrorMessages.ERROR.value, str(e))
        except Exception as e:
            self.show_error_dialog(ErrorMessages.ERROR.value,ErrorMessages.ERROR_OCCURRED.value.format(error=str(e)))

    def show_colors_and_logs(self, component: Component, title: str) -> None:
        """Show a dialog with colors and logs for the given component."""
        try:
            if component is None:
                raise ValueError(ErrorMessages.COMPONENT_NOT_FOUND.value.format(component=title))

            dialog = LogColorDialog(component, title, self)
            dialog.exec_()
        except Exception as e:
            self.show_error_dialog(ErrorMessages.ERROR_OCCURRED.value.format(error=str(e)))

    def show_host_interface_logs(self, point: QPoint) -> None:
        try:
            dialog = LogColorDialog(self.host_interface, COMPONENT_LOGS.format(component=HOST_INTERFACE), self)
            dialog.exec_()
        except Exception as e:
            self.show_error_dialog(ErrorMessages.ERROR_OCCURRED.value.format(error=str(e)))

