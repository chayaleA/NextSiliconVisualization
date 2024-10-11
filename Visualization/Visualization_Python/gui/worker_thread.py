from PyQt5.QtCore import Qt, QThread, pyqtSignal

class WorkerThread(QThread):
    finished = pyqtSignal()  # Signal emitted when the worker thread finishes.

    def __init__(self, action, args):
        """Initialize the WorkerThread with an action and its arguments."""
        super().__init__()
        self.action = action  # The action to be executed in the thread.
        self.args = args  # Arguments to pass to the action.

    def run(self):
        """Run the action in the worker thread."""
        self.action(*self.args)  # Execute the action with the provided arguments.
        self.finished.emit()  # Emit the 'finished' signal once the action is complete.
