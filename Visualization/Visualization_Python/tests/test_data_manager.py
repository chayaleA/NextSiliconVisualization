import unittest
from data_manager import DataManager

from utils.paths import CHIP_DATA_JSON, SL_JSON


class TestDataManager(unittest.TestCase):

    def setUp(self):
        # Initialize the DataManager with the specified JSON files
        self.data_manager = DataManager(CHIP_DATA_JSON, SL_JSON)

    def test_load_json(self):
        # Test loading JSON data from chip_data and sl files
        chip_data = self.data_manager.load_json(CHIP_DATA_JSON)
        sl_data = self.data_manager.load_json(SL_JSON)
        self.assertIsInstance(chip_data, dict)  # Verify that chip_data is a dictionary
        self.assertIsInstance(sl_data, dict)     # Verify that sl_data is a dictionary

    def test_get_start_time(self):
        # Test that the start time can be retrieved
        start_time = self.data_manager.get_start_time()
        self.assertIsNotNone(start_time)  # Ensure start time is not None

    def test_get_end_time(self):
        # Test that the end time can be retrieved
        end_time = self.data_manager.get_end_time()
        self.assertIsNotNone(end_time)  # Ensure end time is not None

    def test_enable_die(self):
        # Test enabling dies and check if at least one die is enabled
        self.data_manager.load_die(0)
        self.data_manager.load_die(1)
        self.data_manager.enable_die()
        self.assertTrue(any(die.is_enable for die in self.data_manager.die_objects.values()))  # Check if any die is enabled

# if __name__ == '__main__':
#     unittest.main()