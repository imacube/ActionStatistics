"""Basic tests for this module."""
import unittest

from action_statistics.ActionStatistics import ActionStatistics


class TestInit(unittest.TestCase):
    def test_init(self):
        """Test the most basic init of the ActionStatistics class."""
        ActionStatistics()


if __name__ == '__main__':
    unittest.main()
