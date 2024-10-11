import os

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QComboBox, QFormLayout, QMessageBox, QWidget, QScrollArea)
from PyQt5.QtCore import Qt

from utils.type_names import AREAS, UNITS, DIE1, DIE2, DIE
from utils.filter_types import FILTER_TYPES_NAMES, CLUSTER, QUAD, THREADID, IO, AREA, UNIT
from utils.constants import WHITE ,X_BUTTON, RED,ROW, COLUMN, READ
from utils.paths import DIALOG_FILTAR_CSS
from utils.error_messages import WarningMessages


class FilterInputDialogWidget(QDialog):

    def __init__(self, filter_type: str, ThreadId_array=None, parent=None) -> None:
        """Initialize the dialog with a filter name."""
        super().__init__(parent)
        self.filter_type = filter_type  # Store the filter name to customize the dialog
        self.parent = parent  # Reference to the parent widget
        self.ThreadId_array = ThreadId_array or []  # Initialize ThreadId_array
        self.initUI()

    def initUI(self) -> None:
        """Initialize the user interface for the dialog."""
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(f'Enter values for {self.filter_type}')
        self.setFixedSize(600, 450)  # Set a fixed size for the dialog

        self.load_stylesheet(DIALOG_FILTAR_CSS)




        self.setLayout(QVBoxLayout())  # Set the main layout of the dialog

        self.form_layout = QFormLayout()  # Initialize the form layout
        self.layout().addLayout(self.form_layout)  # Add form layout to main layout
        self.setup_buttons()
        self.setup_form_fields()  # Set up form fields based on filter_type



    def setup_form_fields(self) -> None:
        """Create and add form fields based on the filter name."""

        try:
            if self.filter_type == FILTER_TYPES_NAMES[CLUSTER]:
                self.chip_input = QComboBox(self)
                self.chip_input.addItems(['0'])  # Currently only 0 available
                self.form_layout.addRow('Chip:', self.chip_input)
                self.die_input = QComboBox(self)
                self.die_input.addItems([DIE1, DIE2])
                self.form_layout.addRow(f'{DIE}:', self.die_input)
                self.quad_input = QComboBox(self)
                self.quad_input.addItems(['NW', 'NE', 'SW', 'SE'])  # Human-readable options
                self.form_layout.addRow(f'{QUAD}:', self.quad_input)
                self.row_input = QComboBox(self)
                self.row_input.addItems([str(row) for row in range(8)])  # 0-7 for row
                self.form_layout.addRow(f'{ROW}:', self.row_input)
                self.column_input = QComboBox(self)
                self.column_input.addItems([str(col) for col in range(8)])  # 0-7 for column
                self.form_layout.addRow(f'{COLUMN}:', self.column_input)
            elif self.filter_type == FILTER_TYPES_NAMES[QUAD]:
                self.chip_input = QComboBox(self)
                self.chip_input.addItems(['0'])  # Currently only 0 available
                self.form_layout.addRow('Chip:', self.chip_input)
                self.die_input = QComboBox(self)
                self.die_input.addItems([DIE1, DIE2])
                self.form_layout.addRow(f'{DIE}:', self.die_input)
                self.quad_input = QComboBox(self)
                self.quad_input.addItems(['HW', 'NE', 'SW', 'SE'])  # Human-readable options for quad
                self.form_layout.addRow(f'{QUAD}:', self.quad_input)
            elif self.filter_type == FILTER_TYPES_NAMES[THREADID]:
                full_width_layout = QVBoxLayout()
                self.tid_input = QLineEdit(self)
                self.tid_input.setPlaceholderText('Enter TID number')
                full_width_layout.addWidget(self.tid_input)
                input_layout = QVBoxLayout()
                self.error_label = QLabel(self)
                self.error_label.setStyleSheet(
                    f"color: {RED}; font-size: 15px; background: transparent; border: none; padding-top: 1px;")
                self.error_label.hide()
                input_layout.addWidget(self.error_label)
                self.apply_button.setEnabled(False)

                # Add the vertical layout to the form layout
                self.form_layout.addRow('TID:', input_layout)

                # Connect to check_input
                self.tid_input.textChanged.connect(self.check_input)

                scroll_area = QScrollArea(self)
                scroll_area.setWidgetResizable(True)

                # Create a QWidget to hold the list of Thread IDs
                thread_id_widget = QWidget()
                thread_id_layout = QVBoxLayout(thread_id_widget)
                print(self.ThreadId_array)
                # Add each Thread ID with a red X button
                for thread_id in self.ThreadId_array:
                    self.tid_layout = QHBoxLayout()  # Horizontal layout for TID and X button

                    # Create the Thread ID label
                    label = QLabel(str(thread_id), self)
                    label.setAlignment(Qt.AlignLeft)
                    label.setStyleSheet("font-size: 18px; padding: 10px;")

                    # Create the red X button
                    remove_button = QPushButton(X_BUTTON, self)
                    remove_button.setStyleSheet("""
                            QPushButton {
                                background-color: red;
                                color: white;
                                border: none;
                                font-size: 16px;
                                width: 30px;
                                height: 30px;
                            }
                            QPushButton:hover {
                                background-color: darkred;
                            }
                        """)
                    remove_button.clicked.connect(lambda _, tid=thread_id: self.remove_tid(tid))

                    # Add the Thread ID label and X button to the horizontal layout
                    self.tid_layout.addWidget(label)
                    self.tid_layout.addWidget(remove_button)
                    self.tid_layout.addStretch()  # Add stretch to push the button to the right

                    # Add the horizontal layout to the main thread ID layout
                    thread_id_layout.addLayout(self.tid_layout)

                # Set the thread ID layout in the widget
                thread_id_widget.setLayout(thread_id_layout)
                scroll_area.setWidget(thread_id_widget)
                # Add the scroll area with full width
                full_width_layout.addWidget(scroll_area)
                # Add the full width layout to the main layout
                self.layout().addLayout(full_width_layout)
            elif self.filter_type == FILTER_TYPES_NAMES[IO]:
                self.inout_input = QComboBox(self)
                self.inout_input.addItems(['in', 'out'])
                self.form_layout.addRow('Select In/Out:', self.inout_input)
            elif self.filter_type == FILTER_TYPES_NAMES[AREA]:
                self.area_input = QComboBox(self)
                self.area_input.addItems(AREAS.keys())
                self.form_layout.addRow('Select Area:', self.area_input)
            elif self.filter_type == FILTER_TYPES_NAMES[UNIT]:
                self.unit_input = QComboBox(self)
                self.unit_input.addItems(UNITS)
                self.form_layout.addRow('Select Unit:', self.unit_input)

        except AttributeError as e:
                QMessageBox.critical(self, "Configuration Error", "Invalid filter type configuration.")
                self.reject()
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {str(e)}")
            print(f"error:{e}")
            self.reject()

    def remove_tid(self, tid):
        self.accept()
        self.parent.remove_tid(tid)
    def update_tid_display(self):
        # Rebuild the TID list
        for thread_id in self.ThreadId_array:
            tid_item = QHBoxLayout()

            label = QLabel(str(thread_id), self)
            label.setAlignment(Qt.AlignLeft)
            label.setStyleSheet("font-size: 18px; padding: 10px;")

            remove_button = QPushButton(X_BUTTON, self)
            remove_button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    color: white;
                    border: none;
                    font-size: 16px;
                    width: 30px;
                    height: 30px;
                }
                QPushButton:hover {
                    background-color: darkred;
                }
            """)
            remove_button.clicked.connect(lambda _, tid=thread_id: self.remove_tid(tid))

            tid_item.addWidget(label)
            tid_item.addWidget(remove_button)
            tid_item.addStretch()


        # Update the main layout if needed
        self.form_layout.addRow(self.tid_layout)
        self.form_layout.addWidget(self.error_label)  # Ensure error label is still shown if necessary

    def check_input(self) -> None:
            text = self.tid_input.text()
            try:
                tid_value = int(text)

                # If conversion succeeds, enable the apply button and hide error label
                self.apply_button.setEnabled(True)
                self.tid_input.setStyleSheet("")
                self.error_label.hide()

            except ValueError:
                # If conversion fails, show the error message
                self.apply_button.setEnabled(False)
                self.tid_input.setStyleSheet(f"border: 1px solid {RED};")
                self.error_label.setText("Please enter a valid number.")
                self.error_label.show()

    def setup_buttons(self) -> None:
        """Create and add buttons to the dialog."""
        button_layout = QVBoxLayout()
        try:

            self.apply_button = QPushButton("apply", self)
            self.apply_button.clicked.connect(self.apply_filter)
            button_layout.addWidget(self.apply_button)

            self.cancel_button = QPushButton("cancel", self)
            self.cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(self.cancel_button)

            self.layout().addLayout(button_layout)  # Add buttons to the main layout

        except Exception as e:
         QMessageBox.critical(self, "Button Setup Error", f"Failed to set up buttons: {str(e)}")

    def apply_filter(self) -> None:

        """Validate and apply the filter based on user input."""

        values = None
        try:
            if self.filter_type == FILTER_TYPES_NAMES[CLUSTER]:
                chip_value = (self.chip_input.currentText())  # Convert chip value to integer
                die_value = (self.die_input.currentIndex())  # Index corresponds to Die 1 => 0, Die 2 => 1
                quad_value = (self.quad_input.currentIndex())  # Index corresponds to HW => 0, NE => 1, SW => 2, SE => 3

                # Reverse the quad value if Die 2 is selected
                if die_value == 1:  # This corresponds to Die 2
                    quad_value = 3 - quad_value  # Reverse: 0 -> 3, 1 -> 2, 2 -> 1, 3 -> 0

                row_value = (self.row_input.currentText())  # Row as integer
                column_value = (self.column_input.currentText())  # Column as integer

                values = [int(chip_value), die_value, quad_value, int(row_value), int(column_value)]

            elif self.filter_type == FILTER_TYPES_NAMES[QUAD]:
                chip_value = int(self.chip_input.currentText())  # Convert chip value to integer
                die_value = int(self.die_input.currentIndex())
                quad_value = int(self.quad_input.currentIndex())

                # Reverse the quad value if Die 2 is selected
                if die_value == 1:  # Die 2 selected
                    quad_value = 3 - quad_value  # Reverse the quad selection

                values = (chip_value, die_value, quad_value)

            elif self.filter_type == FILTER_TYPES_NAMES[THREADID]:
                tid_value = self.tid_input.text().strip()  # Ensure no leading/trailing spaces
                if tid_value:  # Make sure the value is not empty
                    values = int(tid_value)
            elif self.filter_type == FILTER_TYPES_NAMES[IO]:
                values = self.inout_input.currentText()


            elif self.filter_type == FILTER_TYPES_NAMES[AREA]:
                area_value = self.area_input.currentText()
                values = area_value

            elif self.filter_type == FILTER_TYPES_NAMES[UNIT]:
                unit_value = self.unit_input.currentText()
                values = unit_value

            # Apply the filter with the collected values

            if values is not None:
                self.parent.apply_filter(self.filter_type, values)
                self.accept()
            else:
                QMessageBox.warning(self, "Input Error", "No valid values provided.")


        except AttributeError:
            QMessageBox.critical(self, "System Error", "An error occurred. Please try again.")
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {str(e)}")

    def load_stylesheet(self, filename):
        """Load a stylesheet from a file and set it to the dialog."""
        if os.path.exists(filename):
            with open(filename, READ) as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        else:
            print(WarningMessages.STYLE_SHEET_FILE_NOT_FOUND.value.format(filename=filename))
