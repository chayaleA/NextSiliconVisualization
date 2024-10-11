import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QApplication, QMainWindow, QAction, QLabel, QDialog, QTextEdit, QMenu,
    QPushButton, QToolBar, QComboBox, QFrame, QProgressDialog, QStyle, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie


from gui.die_widget import DieWidget
from gui.host_interface_widget import HostInterfaceWidget
from gui.log_colors_dialog import LogColorDialog
from gui.timeline_widget import TimelineWidget
from gui.filter_menu_widget import FilterMenuWidget
from gui.packets_colors import get_colors_by_tids
from gui.file_dialogs.info_widget import InfoDialog
from gui.worker_thread import WorkerThread

from utils.data_manager import DataManager
from utils.paths import APP_ICON_IMAGE, INSTRUCTIONS_ICON_IMAGE ,LOADING_ICON_IMAGE
from utils.type_names import HOST_INTERFACE, DIE1, DIE2, DIE2DIE
from utils.constants import TID, PACKET, LIGHTGRAY, WHITE, BLACK, FORBIDDEN_CURSOR, SIMULATOR, MAIN_TOOLBAR, DIE2DIE_LOGS, \
    HOST_INTERFACE_Logs, FILTER, GRAY ,READ





class MainWindow(QMainWindow):
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.die_widget = None
        self.data_manager = data_manager
        self.is_closing = False
        self.host_interface_widget = None
        self.dies = {}
        self.load_dies()
        self.initUI()
        self.fade_in()

    def initUI(self) -> None:
        self.setWindowTitle(SIMULATOR)
        icon_path = os.path.join(os.getcwd(), APP_ICON_IMAGE)
        self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, 800, 600)
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.filter_menu = FilterMenuWidget(self)
        self.create_top_layout()
        self.create_scroll_area()
        self.create_timeline_widget()
        self.create_navbar()

        self.host_interface_widget = HostInterfaceWidget(self.data_manager.host_interface)
        self.die_widget = DieWidget(self.data_manager, self.dies, self)
        self.die_widget.setVisible(False)
        self.apply_stylesheet()

    def fade_in(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def create_top_layout(self) -> None:
        self.top_layout = QVBoxLayout()
        self.main_layout.addLayout(self.top_layout)

    def create_scroll_area(self) -> None:
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content_widget = QWidget()
        self.scroll_content_layout = QVBoxLayout(self.scroll_content_widget)
        self.scroll_content_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.scroll_content_widget)
        self.main_layout.addWidget(self.scroll_area)

    def create_timeline_widget(self) -> None:
        """ Create the timeline widget for event tracking"""
        self.timeline_widget = TimelineWidget(
            self.data_manager, self.data_manager.get_start_time(), self.data_manager.get_end_time(), main_window=self
        )
        self.top_layout.addWidget(self.timeline_widget)

    def create_navbar(self) -> None:
        # Create the navigation bar for the main window
        if hasattr(self, 'toolBar') and self.toolBar:
            self.removeToolBar(self.toolBar)
            self.toolBar = None

        self.toolBar = QToolBar(MAIN_TOOLBAR)
        self.toolBar.setStyleSheet(f"background-color: {LIGHTGRAY}; width: 220px; height: 60px;")
        self.addToolBar(self.toolBar)


        # Host Interface Button
        host_interface_colors = self.get_data_colors(self.data_manager.host_interface)
        self.host_interface_button = QPushButton(f'{HOST_INTERFACE} 🖥')
        if host_interface_colors and self.has_active_logs(self.data_manager.host_interface):
            self.host_interface_button.setStyleSheet(
                f"background-color: {host_interface_colors[0]}; color: {BLACK}; padding: 10px;"
            )
        else:
            self.host_interface_button.setEnabled(False)  # Disable the button if there are no active logs
        self.host_interface_button.clicked.connect(self.show_host_interface)
        self.host_interface_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.host_interface_button.customContextMenuRequested.connect(self.show_host_interface_logs_and_colors)
        self.toolBar.addWidget(self.host_interface_button)

        # DIE1 Button
        die1_colors = self.get_data_colors(
            self.dies.get(0))  # Ensure this method exists and returns a color or a list of colors
        self.die1_button = self.create_toolbar_button(f'{DIE1} 🔲', self.show_die1, index=0)
        if not self.is_die1_enable():
            self.die1_button.setEnabled(False)
        self.toolBar.addWidget(self.die1_button)

        # DIE2 Button
        self.die2_button = self.create_toolbar_button(f'{DIE2} 🔲', self.show_die2, index=1)
        if not self.is_die2_enable():
            self.die2_button.setEnabled(False)
            self.die2_button.setStyleSheet(f"background-color: {LIGHTGRAY}; color: {GRAY}; padding: 10px;")
        self.toolBar.addWidget(self.die2_button)

        die2die_colors = self.get_data_colors(self.data_manager.die2die)
        self.die2die_button = QPushButton(f'{DIE2DIE} 🔲 ↔️ 🔲')
        if die2die_colors:
            self.die2die_button.setStyleSheet(
                f"padding: 10px; background-color: {die2die_colors[0]}; color: {BLACK};"
            )
        else:
            self.die2die_button.setStyleSheet(f"padding: 10px; background-color: #6e6e6e; color: {WHITE};")
        self.die2die_button.clicked.connect(self.clear_content)
        self.die2die_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.die2die_button.customContextMenuRequested.connect(self.show_die2die_logs)
        self.toolBar.addWidget(self.die2die_button)
        # Filter Button
        self.filter_button = QPushButton(f'{FILTER} ▼')
        self.filter_button.setStyleSheet(f"background-color: #6e6e6e; color: {WHITE}; padding: 10px;")
        self.filter_button.clicked.connect(self.show_filter_menu)
        self.toolBar.addWidget(self.filter_button)

        # Filter Menu
        self.filter_menu.setVisible(False)
        self.filter_menu.setStyleSheet("background-color: lightblue;")
        self.filter_menu.raise_()
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(spacer)
        # Info Button
        self.info_button = QPushButton()
        self.info_button.setToolTip("Click for instructions")
        self.info_button.setIcon(QIcon(INSTRUCTIONS_ICON_IMAGE))
        self.info_button.setIconSize(QSize(34, 34))
        self.info_button.setStyleSheet("padding: 6px; border: none; background: transparent;")
        self.info_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.info_button.clicked.connect(self.show_info_dialog)
        self.toolBar.addWidget(self.info_button)
        with open("gui/styles.css", READ, encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def show_info_dialog(self) -> None:
        info_dialog = InfoDialog(self)
        info_dialog.exec_()

    def is_die1_enable(self) -> bool:
        # Check if DIE1 is enabled
        return self.data_manager.die_objects[0].is_enable and self.get_colors_for_index(0)

    def is_die2_enable(self) -> bool:
        # Check if DIE2 is enabled
        return self.data_manager.die_objects[1].is_enable and self.get_colors_for_index(1)

    def has_active_logs(self, data) -> bool:
        # Check if there are active logs in the given data
        return bool(data.get_attribute_from_active_logs(TID))  # Adjust the method as necessary

    def create_toolbar_button(self, text: str, click_action, index: int = None) -> QPushButton:
        # Create a toolbar button with optional colors and actions
        button = QPushButton(text)
        colors = self.get_colors_for_index(index)
        if colors:
            button.setStyleSheet(f"background-color: {colors[0]}; color: {BLACK}; padding: 10px;")
        button.clicked.connect(click_action)
        button.setContextMenuPolicy(Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(
            lambda: self.show_die_colors_and_logs(index) if index is not None else None
        )
        return button

    def get_colors_for_index(self, index: int) -> list:
        # Get colors for the given die index
        if index is None:
            return []
        die_data = self.dies.get(index)
        if die_data:
            tids = die_data.get_attribute_from_active_logs(TID)
            return list(get_colors_by_tids(tids))
        return []

    def get_data_colors(self, data) -> list:
        # Get colors for the host interface
        tids = data.get_attribute_from_active_logs(TID)
        return list(get_colors_by_tids(tids))

    def load_dies(self) -> None:
        # Load DIE1 and DIE2 from the data manager
        self.dies[0] = self.data_manager.load_die(0)
        self.dies[1] = self.data_manager.load_die(1)

    def apply_stylesheet(self) -> str:
        # Apply stylesheet from external CSS file
        with open("gui/styles.css", 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def clear_content(self) -> None:
        # Clear the content in the scroll area
        for i in reversed(range(self.scroll_content_layout.count())):
            widget = self.scroll_content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def show_die1(self) -> None:
        # Show content for DIE1
        self.show_die(0)

    def show_die2(self) -> None:
        # Show content for DIE2
        self.show_die(1)

    def show_die(self, die_index: int) -> None:
        # Display DIE based on the provided index
        self.clear_content()
        self.die_widget.setVisible(True)
        self.die_widget.setCursor(FORBIDDEN_CURSOR)
        self.scroll_content_layout.addWidget(self.die_widget)
        self.die_widget.show_quads(die_index)


    def show_host_interface(self) -> None:
        self.clear_content()
        self.host_interface_widget = HostInterfaceWidget(self.data_manager.host_interface)
        self.scroll_content_layout.addWidget(self.host_interface_widget)

    def show_host_interface_logs_and_colors(self, pos) -> None:
        dialog = LogColorDialog(self.data_manager.host_interface, HOST_INTERFACE_Logs, self)
        dialog.exec_()

    def show_die_colors_and_logs(self, index) -> None:
        die_data = self.dies.get(index)
        if die_data:
            dialog = LogColorDialog(die_data, f"DIE{index + 1} Logs and Colors", self)
            dialog.exec_()

    def show_die2die_logs(self, pos):

        dialog = LogColorDialog(self.data_manager.die2die, DIE2DIE_LOGS, self)
        dialog.exec_()

    def show_filter_menu(self) -> None:
        if not self.filter_menu.isVisible():
            button_rect = self.filter_button.rect()
            global_pos = self.filter_button.mapToGlobal(button_rect.bottomLeft())
            menu_width = self.filter_menu.sizeHint().width()
            menu_height = self.filter_menu.sizeHint().height()
            self.filter_menu.setGeometry(global_pos.x(), global_pos.y(), menu_width, menu_height)
            self.filter_menu.show()
        else:
            self.filter_menu.hide()


    def show_wait_message(self, message):
        self.setWindowOpacity(0.95)

        self.overlay = QWidget(self)
        self.overlay.setGeometry(self.rect())
        self.overlay.setStyleSheet("background-color: transparent;")
        self.overlay.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.gif_label = QLabel(self.overlay)
        self.gif_label.setAlignment(Qt.AlignCenter)
        gif_path = os.path.join(os.getcwd(), LOADING_ICON_IMAGE)
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(QSize(200, 200))
        self.gif_label.setMovie(self.movie)

        self.gif_label.setGeometry(self.overlay.rect())

        self.overlay.show()
        self.movie.start()
        self.overlay.raise_()
        self.gif_label.raise_()
        QApplication.processEvents()

    def hide_wait_message(self):
        if hasattr(self, 'overlay'):
            self.movie.stop()
            self.overlay.hide()
            self.overlay.deleteLater()
            del self.overlay
            self.setWindowOpacity(1.0)

    def perform_action_with_wait(self, action, *args):
        self.show_wait_message("Please wait, processing...")

        self.worker_thread = WorkerThread(action, args)
        self.worker_thread.finished.connect(self.on_action_finished)
        self.worker_thread.start()

    def on_action_finished(self):
        self.hide_wait_message()
        self.clear_content()
        self.create_navbar()

    def change_filter(self, filter_type: str, values: list) -> None:
        self.perform_action_with_wait(self.data_manager.change_filter, filter_type, values)

    def update_filter_in_chain(self, filter_type: str, values: list) -> None:
        self.perform_action_with_wait(self.data_manager.update_filter_in_chain, filter_type, values)

    def clear_all_filters(self) -> None:
        self.perform_action_with_wait(self.data_manager.clear_all_filters)

    def filter_removal(self, filter_type) -> None:
        self.perform_action_with_wait(self.data_manager.filter_removal, filter_type)

    def fade_out_and_close(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(self.close)
        self.animation.start()

    def closeEvent(self, event):

        if not self.is_closing:
            event.ignore()
            self.is_closing = True
            self.fade_out_and_close()
        else:
            event.accept()
