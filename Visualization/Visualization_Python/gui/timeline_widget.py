
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

import datetime


from gui.range_slider import RangeSlider


class TimelineWidget(QWidget):
    """
    A QWidget for displaying and controlling a timeline with start and end times.
    """
    def __init__(self, data_manager, start_time=None, end_time=None, main_window=None) -> None:
        super().__init__(main_window)
        """
        Initializes the TimelineWidget with given start and end times.
        """
        self.data_manager = data_manager
        self.start_time = start_time
        self.end_time = end_time
        self.main_window = main_window
        self.previous_start_pos = 0
        self.previous_end_pos = None  # Initialize to None for comparison
        self.initUI()
        self.setupTimes()

        # Connect the range_changed signal to update_labels
        self.timeline_slider.range_changed.connect(self.update_labels)

    def initUI(self) -> None:
        """
        Sets up the user interface with labels and a slider for timeline control.
        """
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        self.start_label = QLabel(self)
        self.layout.addWidget(self.start_label)

        self.timeline_slider = RangeSlider(Qt.Horizontal, self)
        self.layout.addWidget(self.timeline_slider)

        self.end_label = QLabel(self)
        self.layout.addWidget(self.end_label)

    def setupTimes(self) -> None:
        """
        Sets the start and end times for the timeline, either from the input or current time.
        """
        if self.start_time is None or self.end_time is None:
            now = datetime.datetime.now()
            self.start_time = now
            self.end_time = now + datetime.timedelta(minutes=30)

        self.timeline_slider.start_time = self.start_time

        start_time_q = QTime(self.start_time.hour, self.start_time.minute, self.start_time.second)
        end_time_q = QTime(self.end_time.hour, self.end_time.minute, self.end_time.second)

        self.set_start_time(start_time_q.toString("HH:mm:ss"))
        self.set_end_time(end_time_q.toString("HH:mm:ss"))

        seconds_range = int((self.end_time - self.start_time).total_seconds())
        self.timeline_slider.setRange(0, seconds_range)
        self.timeline_slider.start_handle_pos = 0
        self.timeline_slider.end_handle_pos = seconds_range

    def update_labels(self, start_pos: int, end_pos: int) -> None:
        """
        Updates the displayed start and end times based on the slider positions.
        """
        start_time = self.start_time + datetime.timedelta(seconds=start_pos)
        end_time = self.start_time + datetime.timedelta(seconds=end_pos)

        self.set_start_time(start_time.strftime("%H:%M:%S"))
        self.set_end_time(end_time.strftime("%H:%M:%S"))
        self.previous_start_pos = start_pos
        self.main_window.perform_action_with_wait(self.data_manager.change_time, int(start_time.timestamp()), int(end_time.timestamp()))

        self.timeline_slider.end_handle_pos = end_pos  # Update the previous end position
        print("start", int(start_time.timestamp()))
        print("end", int(end_time.timestamp()))

    def set_start_time(self, start_time: str) -> None:
        """
        Sets the text for the start time label.
        """
        self.start_label.setText(f"Start Time: {start_time}")

    def set_end_time(self, end_time: str) -> None:
        """
        Sets the text for the end time label.
        """
        self.end_label.setText(f"End Time: {end_time}")

    def update_times(self, start_time: datetime.datetime, end_time: datetime.datetime) -> None:
        """
        Updates the start and end times and refreshes the timeline.
        """
        self.start_time = start_time
        self.end_time = end_time
        self.setupTimes()
