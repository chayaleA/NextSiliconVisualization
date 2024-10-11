from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QWidget, QTextEdit, QScrollArea, QGridLayout, QPushButton, QLineEdit, QLabel
)
from typing import List

from gui.packets_colors import get_colors_by_tids

from utils.constants import TID, PACKET, BLACK, WHITE, LIGHTGRAY,POINTING_CURSOR
from utils.paths import SEARCH_ICON_IMAGE


class LogColorDialog(QDialog):
    def __init__(self, data, title: str, parent=None) -> None:
        super().__init__(parent)
        self.data = data
        self.title = title
        self.is_dark_mode = False
        self.current_animation = None
        self.all_packets = []
        self.all_colors = []
        self.displayed_packets = []
        self.displayed_colors = []
        self.current_index = 0
        self.batch_size = 20
        self.initUI()

    def initUI(self) -> None:
        try:
            self.tids = self.data.get_attribute_from_active_logs(TID)
            self.all_packets = self.data.get_attribute_from_active_logs(PACKET)
            self.all_colors = list(get_colors_by_tids(self.tids))
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            color_tid_map = {color: set() for color in self.all_colors}
            for tid, color in zip(self.tids, self.all_colors):
                color_tid_map[color].add(tid)

            self.setWindowTitle(self.title)
            dialog_layout = QVBoxLayout(self)

            # Search bar setup
            self.search_bar = QLineEdit()
            self.search_bar.setPlaceholderText("Search logs...")
            self.search_bar.setFixedWidth(750)
            self.search_bar.setFixedHeight(60)
            self.search_bar.setObjectName("search_bar")
            self.search_bar.setStyleSheet(f"""
                QLineEdit {{
                    padding-left: 60px;
                    background-image: url({SEARCH_ICON_IMAGE});
                    background-repeat: no-repeat;
                    padding: 10px 70px 10px 70px;
                    border-radius: 20px;
                    border: 2px solid {BLACK};
                    background-color: {WHITE};
                    font-size: 16px;
                    color: {BLACK};
                }}
                QLineEdit::placeholder {{
                    color: gray;
                }}
                QLineEdit:focus {{
                    border: 2px solid deepskyblue;
                }}
            """)
            self.search_bar.textChanged.connect(self.filter_logs)
            dialog_layout.addWidget(self.search_bar)

            # Header for TID buttons
            self.header_widget = QWidget()
            header_layout = QGridLayout(self.header_widget)
            row, col = 0, 0
            max_columns = 4

            for color, tids in color_tid_map.items():
                tids_text = str(tids)
                color_button = QPushButton(f" Thread Id: {tids_text} ")
                color_button.setToolTip(f"Filter logs for TIDs: {tids_text}")
                color_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: {BLACK};
                        padding: 10px 10px;
                        margin: 15px;
                        border-radius: 10px;
                        font-size: 14px;
                        border: none;
                    }}
                    QPushButton:hover {{
                        background-color: gray;
                        color: {BLACK};
                    }}
                """)
                color_button.clicked.connect(lambda _, tids=self.tids: self.handle_tid_selection(tids))
                color_button.setCursor(POINTING_CURSOR)
                header_layout.addWidget(color_button, row, col)
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1

            self.header_widget.setStyleSheet(f"background-color: {WHITE}; padding: 10px; border: none;")
            header_scroll_area = QScrollArea()
            header_scroll_area.setWidgetResizable(True)
            header_scroll_area.setWidget(self.header_widget)
            header_scroll_area.setFixedHeight(150)
            header_scroll_area.setStyleSheet("background-color: transparent; border: none;")
            header_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            dialog_layout.addWidget(header_scroll_area)

            # Content area for logs
            self.content_widget = QWidget()
            self.content_layout = QVBoxLayout(self.content_widget)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(self.content_widget)
            scroll_area.setFixedHeight(350)
            scroll_area.setStyleSheet("background-color: transparent; border: none;")
            dialog_layout.addWidget(scroll_area)

            # Show All Logs button
            self.show_all_button = QPushButton("Show All Logs")
            self.show_all_button.setCursor(POINTING_CURSOR)
            self.show_all_button.clicked.connect(self.show_all_logs)
            self.show_all_button.setStyleSheet(f"""
                QPushButton {{
                    color: {BLACK};
                    font-size: 15px;
                    border-radius: 5px;
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: {LIGHTGRAY};
                }}
            """)
            self.show_all_button.setMinimumSize(180, 50)
            dialog_layout.addWidget(self.show_all_button, alignment=Qt.AlignCenter)

            # Dark mode toggle button
            self.toggle_dark_mode_button = QPushButton("Switch to Dark Mode")
            self.toggle_dark_mode_button.setCursor(POINTING_CURSOR)
            self.toggle_dark_mode_button.clicked.connect(self.toggle_dark_and_light_mode)
            dialog_layout.addWidget(self.toggle_dark_mode_button)

            self.setFixedWidth(800)
            self.setLayout(dialog_layout)
            self.setStyleSheet(f"background-color: {WHITE}; color: {BLACK};")

            # Initialize with all logs
            self.update_content(self.all_packets, self.all_colors)

        except Exception as e:
            print(f"Error initializing UI: {e}")

    def handle_tid_selection(self, tids: set) -> None:
        if self.current_animation:
            self.current_animation.stop()

        filtered_packets = [pkt for idx, pkt in enumerate(self.all_packets) if self.tids[idx] in tids]
        filtered_colors = [color for idx, color in enumerate(self.all_colors) if self.tids[idx] in tids]

        self.update_content(filtered_packets, filtered_colors)

    def show_all_logs(self) -> None:
        self.update_content(self.all_packets, self.all_colors)

    def update_content(self, packets: List[str], colors: List[str]) -> None:
        try:
            self.clear_content()
            self.displayed_packets = packets
            self.displayed_colors = colors
            self.current_index = 0

            # Check if there are no logs available
            if not packets:
                no_logs_message = QLabel("No logs available")
                no_logs_message.setAlignment(Qt.AlignCenter)  # Center the text
                no_logs_message.setStyleSheet("""
                    font-size: 24px;  /* Larger font size */
                    font-weight: bold;  /* Bold text */
                    color: red;  /* Change the text color if needed */
                """)
                self.content_layout.addWidget(no_logs_message)
                return  # Exit the method since there are no logs to display

            self.load_next_batch()

            # Start a timer to load more logs
            self.current_animation = QTimer()
            self.current_animation.timeout.connect(self.load_next_batch)
            self.current_animation.start(100)  # Load a new batch every 100ms
        except Exception as e:
            print(f"Error updating content: {e}")
    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_next_batch(self):
        end_index = min(self.current_index + self.batch_size, len(self.displayed_packets))
        for i in range(self.current_index, end_index):
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setFixedHeight(100)
            text_edit.setStyleSheet(f"background-color: {self.displayed_colors[i]}; border: none; color: {BLACK};")
            text_edit.setPlainText(self.displayed_packets[i])
            self.content_layout.addWidget(text_edit)

        self.current_index = end_index
        if self.current_index >= len(self.displayed_packets):
            self.current_animation.stop()

    def filter_logs(self, text: str) -> None:
        filtered_packets = [pkt for pkt in self.all_packets if text.lower() in pkt.lower()]
        filtered_colors = [self.all_colors[i] for i, pkt in enumerate(self.all_packets) if text.lower() in pkt.lower()]
        self.update_content(filtered_packets, filtered_colors)

    def toggle_dark_and_light_mode(self) -> None:
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.setStyleSheet(f"background-color: {BLACK}; color: {WHITE};")
            self.header_widget.setStyleSheet(f"background-color: {BLACK};")
            self.toggle_dark_mode_button.setText("Switch to Light Mode")
            self.toggle_dark_mode_button.setStyleSheet(f"color: {WHITE};")
            self.show_all_button.setStyleSheet(f"""
                QPushButton {{
                    color: {WHITE};
                    font-size: 15px;
                    border-radius: 5px;
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: {LIGHTGRAY};
                }}
            """)
        else:
            self.setStyleSheet(f"background-color: {WHITE}; color: {BLACK};")
            self.header_widget.setStyleSheet(f"background-color: {WHITE};")
            self.toggle_dark_mode_button.setText("Switch to Dark Mode")
            self.toggle_dark_mode_button.setStyleSheet(f"color: {BLACK};")
            self.show_all_button.setStyleSheet(f"""
                QPushButton {{
                    color: {BLACK};
                    font-size: 15px;
                    border-radius: 5px;
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: {LIGHTGRAY};
                }}
            """)