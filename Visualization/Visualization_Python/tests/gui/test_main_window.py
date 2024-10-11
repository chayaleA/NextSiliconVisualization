import unittest
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from utils.data_manager import DataManager

import sys
import os

from utils.paths import CHIP_DATA_JSON

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Visualization_Python')))

class TestMainWindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create an instance of QApplication for PyQt tests
        cls.app = QApplication([])

    def setUp(self):
        # Create an instance of DataManager and MainWindow
        self.data_manager = DataManager(CHIP_DATA_JSON, SL_JSON)
        self.main_window = MainWindow(self.data_manager)

    def test_initialization(self):
        # Check the UI initialization
        self.assertEqual(self.main_window.windowTitle(), 'HW simulator')
        self.assertEqual(self.main_window.geometry().width(), 800)
        self.assertEqual(self.main_window.geometry().height(), 600)

    def test_load_dies(self):
        # Check that the DIE data is loaded correctly
        self.assertIn(0, self.main_window.dies)
        self.assertIn(1, self.main_window.dies)

    def test_create_navbar(self):
        # Check the creation of the navbar and its actions
        menu_bar = self.main_window.menuBar()
        self.assertIsNotNone(menu_bar)
        self.assertTrue(menu_bar.actions())

    def test_clear_content(self):
        # Check that the content is cleared correctly
        self.main_window.show_die1()
        self.main_window.clear_content()
        # Verify the die_widget is removed from the layout
        self.assertEqual(self.main_window.scroll_content_layout.count(), 0)

    @classmethod
    def tearDownClass(cls):
        # Close the QApplication after the tests
        cls.app.quit()

# if __name__ == '__main__':
#     unittest.main()