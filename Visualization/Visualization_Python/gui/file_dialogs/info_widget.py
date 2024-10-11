import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

from utils.constants import CLOSE, SIMULATOR_INSTRUCTIONS, READ
from utils.paths import INFO_WIDGET_CSS
from utils.error_messages import WarningMessages ,ErrorMessages



class InfoDialog(QDialog):
    def __init__(self, parent=None):
        try:
            super().__init__(parent)
            self.setWindowTitle(SIMULATOR_INSTRUCTIONS)  # Set the title of the dialog
            size_x, size_y, width, height = 300, 300, 600, 400
            self.setGeometry(size_x, size_y, width, height)  # Set the initial size and position of the dialog

            # Load the stylesheet from the CSS file
            self.load_stylesheet(INFO_WIDGET_CSS)

            layout = QVBoxLayout()  # Vertical layout for the dialog

            # Instructions text with added margins between lines using HTML
            instructions = """
            <h2 style="color: #2980b9;">Simulator Instructions</h2>
            <p style="color: #2c3e50; font-size: 15px; margin-bottom: 20px;">
            <span style="font-weight: bold;">•</span> To move to the next layer, click on the corresponding element.<br><br>
            <span style="font-weight: bold;">•</span> Right-click on any element to view its logs.<br><br>
            <span style="font-weight: bold;">•</span> Colored elements indicate they contain logs.<br><br>
            <span style="font-weight: bold;">•</span> Use the toolbar to navigate between Host Interface, DIE1, DIE2, and more.<br><br>
            <span style="font-weight: bold;">•</span> Click "Filter" to open the filter menu and refine your view.
            </p>
            """
            self.label = QLabel(instructions)  # Create a label for the instructions
            self.label.setWordWrap(True)  # Allow text to wrap within the label
            self.label.setAlignment(Qt.AlignTop)  # Align text to the top
            self.label.setTextFormat(Qt.RichText)  # Support for HTML formatting

            layout.addWidget(self.label)  # Add the label to the layout

            button_layout = QHBoxLayout()  # Horizontal layout for buttons
            self.close_button = QPushButton(CLOSE)  # Create a close button
            self.close_button.clicked.connect(self.close)  # Connect button click to close the dialog
            button_layout.addStretch(1)  # Add stretchable space before the button
            button_layout.addWidget(self.close_button)  # Add the close button to the layout
            layout.addLayout(button_layout)  # Add button layout to the main layout

            self.setLayout(layout)  # Set the main layout for the dialog

            # Center the dialog on the parent window
            self.setWindowModality(Qt.ApplicationModal)  # Make the dialog modal
            if self.parent():
                self.move(self.parent().x() + (self.parent().width() - self.width()) // 2,
                          self.parent().y() + (self.parent().height() - self.height()) // 2)

        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))

    def load_stylesheet(self, filename):
        """Load a stylesheet from a file and set it to the dialog."""
        try:
            if os.path.exists(filename):
                with open(filename, READ) as file:
                    stylesheet = file.read()
                    self.setStyleSheet(stylesheet)
            else:
                raise FileNotFoundError(f"Stylesheet file not found: {filename}")
        except FileNotFoundError as fnf_error:
            self.show_error_message(WarningMessages.STYLE_SHEET_FILE_NOT_FOUND.value.format(filename=filename))
        except Exception as e:
            self.show_error_message(ErrorMessages.ERROR_OCCURRED.value.format(error=e))


    def show_error_message(self, message):
        """Display an error message to the user in a popup."""
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()
