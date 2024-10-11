import os
import sys
import ctypes
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from utils.paths import APP_ICON_IMAGE
from gui.file_dialogs.file_selection_widget import FileSelectionWidget

if __name__ == '__main__':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(' ')
    app = QApplication(sys.argv)
    icon_path = os.path.join(os.getcwd(),APP_ICON_IMAGE)
    app.setWindowIcon(QIcon(icon_path))
    # Open the file selection window
    file_selection_widget = FileSelectionWidget()
    file_selection_widget.show()

    sys.exit(app.exec_())