import json
import unittest

from entities.die import Die
from entities.quad import Quad

from utils.constants import TOP, DIES
from utils.type_names import DIE

from utils.paths import CHIP_DATA_JSON


class TestDie(unittest.TestCase):

    def setUp(self):
        # Mock data for creating a Die instance
        with open(f"../{CHIP_DATA_JSON}", 'r') as config:
            chip_data = json.load(config)

        die_data = chip_data.get(TOP, {}).get(DIES, [])[0]  # Retrieve the first die data
        self.die = Die(1, die_data)  # Create a Die instance with ID 1 and the retrieved data

    def test_initialization(self):
        # Check that the Die class is initialized correctly
        self.assertEqual(self.die.id, 1)  # Verify ID is set correctly
        self.assertEqual(self.die.type_name, DIE)  # Verify type name is set correctly
        self.assertFalse(self.die.is_enable)  # Verify that the die is not enabled
        self.assertEqual(len(self.die.quads), 2)  # Ensure there are 2 rows in quads

    def test_init_quads(self):
        # Check that the quads are initialized correctly
        quads_matrix = self.die.quads

        # Check that each row contains 2 columns
        self.assertEqual(len(quads_matrix[0]), 2)
        self.assertEqual(len(quads_matrix[1]), 2)

        # Check that Quad objects are created properly
        self.assertIsInstance(quads_matrix[0][0], Quad)
        self.assertIsInstance(quads_matrix[1][1], Quad)

        # Check that the quads match the provided data
        self.assertEqual(quads_matrix[0][0].id, 1)
        self.assertEqual(quads_matrix[1][1].id, 4)

    def test_get_attribute_from_active_logs(self):
        mock_attribute = 'some_attribute'  # Example attribute to test
        attributes = self.die.get_attribute_from_active_logs(mock_attribute)

        self.assertIsInstance(attributes, list)  # Verify that the returned attributes are in a list

# if __name__ == '__main__':
#     unittest.main()
