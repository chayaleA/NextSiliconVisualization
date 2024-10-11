from PyQt5.QtWidgets import QMenu, QLabel, QWidgetAction, QPushButton, QHBoxLayout,QWidget, QMessageBox
from gui.filter_input_dialog_widget import FilterInputDialogWidget

from utils.filter_types import FILTER_TYPES_NAMES, TIMERANGE, TIME
from utils.constants import POINTING_CURSOR ,FILTER


class FilterMenuWidget(QMenu):
    def __init__(self, parent=None):
        super().__init__(f'{FILTER} ▼', parent)
        self.parent = parent
        self.filters_action = []
        self.ThreadId_array = []
        self.initUI()

    def initUI(self) -> None:
        self.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                border: 1px solid #000;
            }
            QMenu::item:selected {
                background-color: #555;
            }
        """)

        self.hovered.connect(lambda: self.parent.setCursor(POINTING_CURSOR))



        self.actions = {}
        for filter_type in FILTER_TYPES_NAMES.values():
            if filter_type not in [FILTER_TYPES_NAMES[TIME],FILTER_TYPES_NAMES[TIMERANGE]]:
                widget = QWidget()
                layout = QHBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)

                label = QLabel(filter_type)
                label.setStyleSheet("padding: 8px 20px; color: white; background-color: #2d2d2d;")
                layout.addWidget(label)

                # Add "X" button
                remove_button = QPushButton("X")
                remove_button.setFixedWidth(30)
                remove_button.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background-color: #ff4d4d;  /* Red background */
                        color: white;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #ff6666;  /* Lighter red */
                        border: 1px solid grey;  /* Grey border on hover */
                    }
                """)
                remove_button.clicked.connect(lambda _, ft=filter_type: self.remove_filter(ft))
                layout.addWidget(remove_button)
                remove_button.hide()  # Hide the "X" button initially

                # Arrow button for additional options or input
                if filter_type == 'ThreadId':
                    arrow_button = QPushButton("➕")
                else:
                    arrow_button = QPushButton("🖋️")
                arrow_button.setFixedWidth(30)
                arrow_button.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background-color: #2d2d2d; 
                        color: white;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #0069d9;  /* Darker blue */
                        border: 1px solid grey;  /* Grey border on hover */
                    }
                """)
                arrow_button.clicked.connect(lambda _, ft=filter_type: self.show_input_dialog(ft))
                layout.addWidget(arrow_button)
                arrow_button.hide()  # Hide the arrow button initially

                widget.setLayout(layout)
                action = QWidgetAction(self)
                action.setDefaultWidget(widget)
                self.addAction(action)

                # Connect action trigger to filter selection
                label.mouseReleaseEvent = lambda event, name=filter_type: self.filter_selected(name)

                # Store actions without the buttons
                self.actions[filter_type] = (label, remove_button, arrow_button)

        self.add_clear_filters_button()
        self.update_filter_Text()

    def add_clear_filters_button(self) -> None:
        """Add a button to clear all filters."""
        clear_button = QPushButton('Clear Filters')
        clear_button.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                color: white;
                background-color: #d9534f; /* Red color for emphasis */
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c9302c; /* Darker red for hover effect */
            }
        """)
        clear_button.clicked.connect(self.clear_all_filters)

        # Create a QWidgetAction for the button
        action = QWidgetAction(self)
        action.setDefaultWidget(clear_button)
        self.addAction(action)

    def filter_selected(self, filter_type: str) -> None:
        """Handle filter selection."""
        if filter_type not in self.filters_action:
            # Add filter and show the input dialog
            self.show_input_dialog(filter_type)

    def update_filter_Text(self) -> None:
        """Update the styles of the menu items based on the selected filters."""
        for filter_type, (label, remove_button, arrow_button) in self.actions.items():
            if filter_type in self.filters_action:
                label.setText(f"{filter_type}  ✓")
                remove_button.show()  # Show the remove button when filter is active
                arrow_button.show()  # Show the arrow button to modify the filter
                label.mouseReleaseEvent = lambda event: None  # Disable clicking on the label
            else:
                label.setText(filter_type)
                remove_button.hide()  # Hide the remove button when filter is not active
                arrow_button.hide()  # Hide the arrow button when filter is not active
                label.mouseReleaseEvent = lambda event, name=filter_type: self.filter_selected(name)  # Enable clicking

    def show_input_dialog(self, filter_type: str) -> None:
        """Show the input dialog for the selected filter."""
        dialog = FilterInputDialogWidget(filter_type, self.ThreadId_array, self)
        dialog.exec_()

    from typing import Literal
    def remove_tid(self, tid):
        print(self.ThreadId_array, tid , "*****")
        if tid in self.ThreadId_array:
            self.ThreadId_array.remove(tid)
        else:
            QMessageBox.warning(self, "Warning", f"TID {tid} not found in the list.")
        if self.ThreadId_array == []:
            self.remove_filter("ThreadId")
        else:
            self.parent.update_filter_in_chain("ThreadId", self.ThreadId_array)
            dialog = FilterInputDialogWidget("ThreadId", self.ThreadId_array, self)
            dialog.exec_()

    def apply_filter(self, filter_type: str, values: list) -> None:
        """Apply the filter with the given name and values."""
        print(f'Filter {filter_type} applied with values: {values}')
        if self.parent is not None or (filter_type == 'ThreadId' and self.ThreadId_array == []):
            if filter_type == 'ThreadId':
                self.ThreadId_array.append(int(values))
                values = self.ThreadId_array
                print(values, "filter menu")
            if filter_type in self.filters_action:
                self.parent.update_filter_in_chain(filter_type,values)
            else:
                self.filters_action.append(filter_type)
                self.update_filter_Text()
                self.parent.change_filter(filter_type, values)

    def clear_all_filters(self) -> None:
        """Clear all selected filters and update the menu."""
        self.ThreadId_array = []
        self.filters_action.clear()
        self.update_filter_Text()
        self.parent.clear_all_filters()

    def remove_filter(self, filter_type: str) -> None:
        """Remove a specific filter and update the menu."""
        self.close()
        if filter_type == 'ThreadId':
            self.ThreadId_array = []
        if filter_type in self.filters_action:
            self.filters_action.remove(filter_type)
            self.update_filter_Text()
            self.parent.filter_removal(filter_type)
