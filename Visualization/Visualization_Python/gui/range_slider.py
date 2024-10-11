from PyQt5.QtCore import Qt, QTime, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QToolTip
from PyQt5.QtGui import QMouseEvent, QPainter, QColor, QPen
import datetime

class RangeSlider(QSlider):
    range_changed = pyqtSignal(int, int)

    def __init__(self, orientation: Qt.Orientation, main_window: QWidget = None) -> None:
        super().__init__(orientation, main_window)
        self.start_handle_pos = 0
        self.end_handle_pos = self.maximum()
        self.temp_start_pos = self.start_handle_pos
        self.temp_end_pos = self.end_handle_pos
        self.dragging_handle = None
        self.setMouseTracking(True)
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 4px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: transparent;
                width: 0px;
                height: 0px;
            }
        """)
        self.start_time = datetime.datetime.now()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)

        handle_radius = 7

        # Draw start handle
        painter.setPen(QPen(QColor(0, 0, 255), 2))
        painter.setBrush(QColor(0, 0, 255))
        start_pos = max(handle_radius, min(self.width() - handle_radius, self.positionFromValue(self.start_handle_pos)))
        painter.drawEllipse(start_pos - handle_radius, self.height() // 2 - handle_radius, handle_radius * 2, handle_radius * 2)

        # Draw end handle
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.setBrush(QColor(255, 0, 0))
        end_pos = max(handle_radius, min(self.width() - handle_radius, self.positionFromValue(self.end_handle_pos)))
        painter.drawEllipse(end_pos - handle_radius, self.height() // 2 - handle_radius, handle_radius * 2, handle_radius * 2)

        # Draw temporary handles during drag
        if self.dragging_handle == 'start':
            painter.setPen(QPen(QColor(0, 0, 255, 128), 2))
            painter.setBrush(QColor(0, 0, 255, 128))
            temp_start_pos = max(handle_radius, min(self.width() - handle_radius, self.positionFromValue(self.temp_start_pos)))
            painter.drawEllipse(temp_start_pos - handle_radius, self.height() // 2 - handle_radius, handle_radius * 2, handle_radius * 2)
        elif self.dragging_handle == 'end':
            painter.setPen(QPen(QColor(255, 0, 0, 128), 2))
            painter.setBrush(QColor(255, 0, 0, 128))
            temp_end_pos = max(handle_radius, min(self.width() - handle_radius, self.positionFromValue(self.temp_end_pos)))
            painter.drawEllipse(temp_end_pos - handle_radius, self.height() // 2 - handle_radius, handle_radius * 2, handle_radius * 2)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = max(0, min(self.maximum(), self.valueFromPosition(event.pos())))
        if abs(pos - self.start_handle_pos) <= 5:
            self.dragging_handle = 'start'
            self.temp_start_pos = self.start_handle_pos
        elif abs(pos - self.end_handle_pos) <= 5:
            self.dragging_handle = 'end'
            self.temp_end_pos = self.end_handle_pos
        else:
            if pos < self.start_handle_pos:
                self.dragging_handle = 'start'
                self.temp_start_pos = pos
            elif pos > self.end_handle_pos:
                self.dragging_handle = 'end'
                self.temp_end_pos = pos
            else:
                if abs(pos - self.start_handle_pos) < abs(pos - self.end_handle_pos):
                    self.dragging_handle = 'start'
                    self.temp_start_pos = pos
                else:
                    self.dragging_handle = 'end'
                    self.temp_end_pos = pos
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.LeftButton:
            pos = max(0, min(self.maximum(), self.valueFromPosition(event.pos())))
            if self.dragging_handle == 'start':
                # Ensure that the start handle never passes the end handle
                self.temp_start_pos = min(pos, self.end_handle_pos - 1)
            elif self.dragging_handle == 'end':
                # Ensure that the end handle never passes the start handle
                self.temp_end_pos = max(pos, self.start_handle_pos + 1)
            self.update()
        self.updateToolTip(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.dragging_handle == 'start':
            self.start_handle_pos = self.temp_start_pos
        elif self.dragging_handle == 'end':
            self.end_handle_pos = self.temp_end_pos

        # Ensure start and end positions are always valid
        if self.start_handle_pos >= self.end_handle_pos:
            self.start_handle_pos = max(0, self.end_handle_pos - 1)
        if self.end_handle_pos <= self.start_handle_pos:
            self.end_handle_pos = min(self.maximum(), self.start_handle_pos + 1)

        self.dragging_handle = None
        self.range_changed.emit(self.start_handle_pos, self.end_handle_pos)
        self.update()

    def updateToolTip(self, event: QMouseEvent) -> None:
        pos = self.valueFromPosition(event.pos())
        time = self.start_time + datetime.timedelta(seconds=pos)
        formatted_time = time.strftime("%H:%M:%S")
        QToolTip.showText(event.globalPos(), formatted_time)

    def valueFromPosition(self, pos: QMouseEvent) -> int:
        return round(self.minimum() + (self.maximum() - self.minimum()) * pos.x() / self.width())

    def positionFromValue(self, value: int) -> int:
        return round(self.width() * (value - self.minimum()) / (self.maximum() - self.minimum()))

