from typing import Optional
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QMouseEvent

from utils.constants import TID, PACKET, LIGHTGRAY, POINTING_CURSOR, COMPONENT_LOGS
from entities.cluster import Cluster
from gui.log_colors_dialog import LogColorDialog
from gui.packets_colors import get_colors_by_tids
from utils.error_messages import ErrorMessages

class ClusterWidget(QWidget):
    def __init__(self, cluster: Cluster, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.cluster = cluster
        self.cluster_tids = self.cluster.get_attribute_from_active_logs(TID)
        self.colors = list(get_colors_by_tids(self.cluster_tids))  # Convert set to list
        self.packet_messages = self.cluster.get_attribute_from_active_logs(PACKET)  # Fetch packet messages
        self.is_enable = False
        if self.cluster.is_enable and self.colors:
            self.is_enable = True
        self.initUI()

    def initUI(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(0)  # Reduce spacing between widgets
        layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.setLayout(layout)

        color = QColor(self.cluster.color)
        text_color = color.name()
        self.label = QLabel(f'{self.cluster.type_name}\nCluster {self.cluster.id}', self)
        self.label.setAlignment(Qt.AlignCenter)
        text_color = text_color if self.is_enable else LIGHTGRAY
        self.label.setStyleSheet(f'color: {text_color}; font-size: 12px;')

        layout.addWidget(self.label)

        back_color = LIGHTGRAY
        if self.colors:
            back_color = self.colors[0]

        self.setStyleSheet(f'background-color: {back_color}; border: 2px dashed {text_color};')

        self.setCursor(POINTING_CURSOR)

        self.setEnabled(self.is_enable)
        self.mousePressEvent = self.show_log_messages

    def show_log_messages(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            try:
                dialog = LogColorDialog(self.cluster, COMPONENT_LOGS.format(component=self.cluster.type_name), self)
                dialog.exec_()
            except Exception as e:
                self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))
        else:
            self.show_cluster_info(event)

    def show_cluster_info(self, event: QMouseEvent) -> None:
        from gui.quad_widget import QuadWidget  # Import to avoid circular dependency
        try:
            parent_widget = self.parent()
            while parent_widget and not isinstance(parent_widget, QuadWidget):
                parent_widget = parent_widget.parent()
            if parent_widget:
                parent_widget.show_cluster_info(self.cluster)
        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))

    def update_display(self) -> None:
        # Update display with new colors and packet messages
        try:
            self.colors = list(get_colors_by_tids(self.cluster.get_attribute_from_active_logs(TID)))
            self.packet_messages = self.get_messages_by_packet()
            back_color = self.colors[0] if self.colors else LIGHTGRAY
            self.setStyleSheet(f'background-color: {back_color}; border: 2px dashed {self.cluster.color};')
            self.label.setText(f'{self.cluster.type_name}\nCluster {self.cluster.id}')
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
