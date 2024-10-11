from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox


from typing import Dict, Optional

from entities.die import Die

from gui.quad_widget import QuadWidget

from utils.data_manager import DataManager
from utils.constants import BLACK, NUM_QUADS_PER_SIDE, EMPTY, QUADS, FORBIDDEN_CURSOR, POINTING_CURSOR
from utils.error_messages import ErrorMessages
from utils.type_names import DIE

class DieWidget(QWidget):
    def __init__(self, data_manager: DataManager, dies: Dict[str, Die], main_window: QMainWindow) -> None:
        super().__init__()
        self.data_manager = data_manager
        self.main_window = main_window
        self.dies = dies
        self.initUI()

    def initUI(self) -> None:
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Container for Quad Matrix
        self.quad_container = QWidget()
        self.quad_layout = QGridLayout(self.quad_container)
        self.quad_layout.setSpacing(0)  # Reduced spacing
        self.quad_layout.setContentsMargins(140, 0, 140, 0)  # Add small margins
        self.layout.addWidget(self.quad_container)

        self.quad_container.setVisible(False)

    def show_quads(self, die_index: int) -> None:
        try:
            die = self.dies.get(die_index)
            if die is None:
                raise ValueError(ErrorMessages.ERROR.value, ErrorMessages.OBJECT_IS_NONE.value.format(object=DIE))

            # Clear previous widgets from the quad layout
            self.clear_layout(self.quad_layout)

            # Display new matrix of the quads
            for row in range(NUM_QUADS_PER_SIDE):
                for column in range(NUM_QUADS_PER_SIDE):
                    quad = die.quads[row][column]
                    if quad:
                        quad_widget = QuadWidget(quad, column == 1, self)  # Pass position (row, column)
                        if quad.is_enable:
                            quad_widget.setCursor(POINTING_CURSOR)
                        else:
                            quad_widget.setCursor(FORBIDDEN_CURSOR)
                    else:
                        quad_widget = QLabel(EMPTY, self)
                        quad_widget.setAlignment(Qt.AlignCenter)
                        quad_widget.setStyleSheet(
                            f'border: 1px dashed {BLACK}; min-width: 150px; min-height: 150px; background-color: red;')
                    self.quad_layout.addWidget(quad_widget, row, column, alignment=Qt.AlignCenter)

            self.adjust_quad_sizes()
            self.quad_container.setVisible(True)
        except Exception as e:
            self.show_error_dialog(ErrorMessages.ERROR.value, str(e))

    def clear_layout(self, layout: Optional[QGridLayout] = None) -> None:
        if layout is None:
            layout = self.quad_layout

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
        layout.update()

    def adjust_quad_sizes(self) -> None:
        try:
            div_size, add_px_size = 3, 150
            size = self.size().width() // div_size + add_px_size
            for row in range(NUM_QUADS_PER_SIDE):
                for column in range(NUM_QUADS_PER_SIDE):
                    item = self.quad_layout.itemAtPosition(row, column)
                    if item:
                        widget = item.widget()
                        if widget:
                            widget.setFixedSize(size, size)
        except Exception as e:
            self.show_error_dialog(ErrorMessages.ERROR.value, str(e))

    def show_error_dialog(self, title: str, message: str) -> None:
        """Show an error dialog with the specified title and message."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.adjust_quad_sizes()
        super().resizeEvent(event)
