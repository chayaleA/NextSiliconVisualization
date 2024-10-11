from PyQt5.QtGui import QCloseEvent, QContextMenuEvent, QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
                             QGridLayout, QScrollArea, QLayout, QMessageBox)
from PyQt5.QtCore import Qt

from typing import Optional

from entities.cluster import Cluster
from entities.component import Component
from entities.mcu import Mcu

from gui.component_widget import ComponentWidget
from gui.log_colors_dialog import LogColorDialog
from gui.mcu_widget import McuInfoWidget
from gui.packets_colors import get_colors_by_tids


from utils.constants import TID, OBJECT_COLORS, LIGHTGRAY, WHITE, X_BUTTON, COMPONENT_LOGS, FORBIDDEN_CURSOR, POINTING_CURSOR, RED
from utils.type_names import MCU, LNB
from utils.error_messages import ErrorMessages, WarningMessages


class ClusterInfoWidget(QWidget):
    CLOSE_BUTTON_NAME = "close_button"
    SCROLL_AREA_NAME = "scroll_area"
    CLUSTER_TITLE = "Cluster ID: {cluster_id}"

    def __init__(self, cluster: Cluster, parent: Optional[QWidget] = None) -> None:
        try:
            super().__init__(parent)
            self.cluster = cluster
            self.initUI()
        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))

    def initUI(self) -> None:
        try:
            self.setStyleSheet(
                f'background-color: #f0f0f0; border: 1px solid {self.cluster.color}; padding: 0px; border-radius: 10px;')
            layout = QVBoxLayout()

            # Header Layout
            header_layout = QHBoxLayout()
            close_button = QPushButton(X_BUTTON)
            close_button.clicked.connect(self.close)
            close_button.setObjectName(self.CLOSE_BUTTON_NAME)
            close_button.setStyleSheet(
                f"background-color: {RED}; color: {WHITE}; font-weight: bold; border: none; padding: 10px;")
            close_button.setCursor(POINTING_CURSOR)
            header_layout.addWidget(close_button, alignment=Qt.AlignRight)
            layout.addLayout(header_layout)

            # Scroll Area for Grid Layout
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("border: none;")

            scroll_area_widget = QWidget()
            scroll_area_layout = QVBoxLayout(scroll_area_widget)

            # First row layout for MCU and LNB
            first_row_layout = QHBoxLayout()

            # Grid layout for the remaining components
            grid_layout = QGridLayout()
            grid_layout.setSpacing(5)

            components = self.cluster.get_details()
            for index_component, component in enumerate(components):
                component_widget = ComponentWidget(component, component.type_name)
                component_tids = component.get_attribute_from_active_logs(TID)
                colors = list(get_colors_by_tids(component_tids))
                back_color = colors[0] if colors else LIGHTGRAY
                color = OBJECT_COLORS.get(component_widget.type_name, WHITE)
                component_widget.setStyleSheet(
                    f'background-color: {back_color}; border: 1px solid {color}; padding: 0px; border-radius: 5px;')

                # Adjust sizes based on component type
                if component.type_name in [MCU, LNB]:
                    width, hight = 160, 115
                    component_widget.setMinimumSize(width, hight)  # Larger size for MCU and LNB
                    first_row_layout.addWidget(component_widget)  # Add to first row layout
                else:
                    width, hight = 80, 80
                    component_widget.setMinimumSize(width, hight)  # Smaller size for other components
                    num_components_to_skip = 2  # skip MCU and LNB
                    num_components_in_row = 4
                    row = (index_component - num_components_to_skip) // num_components_in_row
                    col = (index_component - num_components_to_skip) % num_components_in_row
                    grid_layout.addWidget(component_widget, row, col)

                # Decrease font size for all component widgets
                font = QFont()
                font.setPointSize(4)
                component_widget.setFont(font)

                # Set cursor based on component type
                if component.type_name == MCU:
                    component_widget.setCursor(POINTING_CURSOR)
                    component_widget.mousePressEvent = lambda event, comp=component: self.handle_mouse_event(event, comp)
                else:
                    component_widget.setCursor(FORBIDDEN_CURSOR)

                # Context menu for logs
                component_widget.contextMenuEvent = lambda event, comp=component: self.show_logs(comp)

            # Add both layouts (first row and grid) to the scroll area layout
            scroll_area_layout.addLayout(first_row_layout)
            scroll_area_layout.addLayout(grid_layout)

            scroll_area.setWidget(scroll_area_widget)
            scroll_area.setObjectName(self.SCROLL_AREA_NAME)
            layout.addWidget(scroll_area)

            self.setLayout(layout)
            self.setWindowTitle(self.CLUSTER_TITLE.format(cluster_id=str(self.cluster.id)))

        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))

    def handle_mouse_event(self, event: QContextMenuEvent, component: Component) -> None:
        try:
            if event.button() == Qt.LeftButton and component.type_name == MCU:
                # Check if the component has logs
                if not component.get_attribute_from_active_logs(TID):
                    return  # Do nothing if there are no logs

                self.show_mcu_info(component)
        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))

    def show_mcu_info(self, mcu: Mcu) -> None:
        try:
            self.previous_layout = self.layout()
            self.mcu_info_widget = McuInfoWidget(mcu, self)
            self.build_mcu(mcu)
        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))

    def build_mcu(self, mcu: Mcu) -> None:
        try:
            self.mcu_info_widget = McuInfoWidget(mcu, self)
            self.mcu_info_widget.setObjectName(MCU)
            self.layout().addWidget(self.mcu_info_widget)

            self.widget_to_remove = self.findChild(QWidget, name=self.SCROLL_AREA_NAME)
            self.widget_to_remove2 = self.findChild(QWidget, name=self.CLOSE_BUTTON_NAME)
            self.widget_to_remove.hide()
            self.widget_to_remove2.hide()
        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))

    def show_logs(self, component) -> None:
        try:
            if component:
                dialog = LogColorDialog(component, COMPONENT_LOGS.format(component=component.type_name), self)
                dialog.exec_()
        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))

    def show_error_message(self, message: str) -> None:
        """Display an error message to the user in a popup."""
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()

    def closeEvent(self, event: QCloseEvent) -> None:
        try:
            from gui.quad_widget import QuadWidget  # Import to avoid circular dependency
            if isinstance(self.parent(), QuadWidget):
                self.parent().show_quad(1)
            else:
                super().closeEvent(event)
        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))

    def clear_layout(self, layout: Optional[QLayout] = None) -> None:
        if layout is None:
            layout = self.layout()

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                pass
            elif item.layout():
                self.clear_layout(item.layout())

    def show_again(self) -> None:

        try:
            self.layout().addWidget(self.widget_to_remove2, alignment=Qt.AlignRight)
            self.layout().addWidget(self.widget_to_remove)
            self.widget_to_remove2.show()
            self.widget_to_remove.show()
        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))
