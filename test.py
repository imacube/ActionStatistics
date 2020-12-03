"""Basic tests for this module."""
import threading
import unittest
from json import loads, dumps
from random import randint
from statistics import mean
from time import sleep

from action_statistics.ActionStatistics import ActionStatistics


class TestInit(unittest.TestCase):
    """Test the ActionStatistics.__init__ method."""

    def test_init(self):
        """Test the most basic init of the ActionStatistics class."""
        ActionStatistics()


class TestConcurrent(unittest.TestCase):
    """Test concurrency."""

    @staticmethod
    def sub_process(action_stats: ActionStatistics, add_action: dict, sleep_window=0):
        """Action to be taken by a subprocess.

        Parameter
        ---------
        action_stats : ActionStatistics
            Class to utilize.
        add_action : dict
            Action to add to the shared dict.
        sleep_window : int
            How long to sleep before taking any action. This is a positive integer value.
        """
        if sleep_window > 0:
            sleep(randint(1, sleep_window))

        for action in add_action:
            action_stats.addAction(dumps(action))

    def test_empty(self):
        """Test accessing the shared dictionary."""
        action_stats = ActionStatistics()
        assert action_stats.getStats() == '[]'

    def test_add_action(self):
        """Test the internal _add_action method."""
        action_stats = ActionStatistics()
        action_stats._add_action('''{"action":"jump", "time":100}''')
        action_stats._add_action('''{"action":"jump", "time":200}''')
        assert action_stats._dict == {'jump': [100, 200]}

    def test_get_stats(self):
        """Test the internal _get_stats method."""
        action_stats = ActionStatistics()
        action_stats._dict = {'jump': [100]}
        assert loads(action_stats._get_stats()) == [{"action": "jump", "avg": 100}]

    def test_addAction(self):
        """Test adding an item."""
        action_stats = ActionStatistics()
        action_stats.addAction('''{"action":"jump", "time":100}''')
        sleep(2)
        assert action_stats._dict == {'jump': [100]}

    def test_getStats(self):
        """Test getting an item."""
        action_stats = ActionStatistics()
        action_stats._dict = {'jump': [100]}
        assert loads(action_stats.getStats()) == [{"action": "jump", "avg": 100}]

    def test_addAction_multiple(self):
        """Test that the average is being calculated correctly."""
        action_stats = ActionStatistics()
        action_stats.addAction('''{"action":"jump", "time":100}''')
        action_stats.addAction('''{"action":"jump", "time":200}''')
        sleep(2)
        assert action_stats.getStats() == '''[{"action": "jump", "avg": 150}]'''

    def test_thread(self):
        """Test a thread accessing the shared dict."""
        action_stats = ActionStatistics()
        thread = threading.Thread(target=self.sub_process, args=(
            action_stats,
            [
                {"action": "jump", "time": 100},
                {"action": "run", "time": 75},
                {"action": "jump", "time": 200}
            ],
            3
        ))
        thread.start()
        thread.join()
        sleep(2)
        assert action_stats._dict == {'jump': [100, 200], 'run': [75]}
        assert action_stats.getStats() == dumps([{"action":"jump", "avg":150}, {"action":"run", "avg":75}])

    def test_multiple_threads(self):
        """Test multiple threads accessing the method."""

        def trial_run():
            _action_stats = ActionStatistics()
            threads = list()
            for d in [[{'action': 'jump', 'time': x}] for x in range(100)]:
                t = threading.Thread(target=self.sub_process, args=(_action_stats, d, 5))
                threads.append(t)

            for t in threads:
                t.start()
            for t in threads:
                t.join()

            sleep(10)
            assert mean(_action_stats._dict['jump']) == 49.5
            return _action_stats

        # If the values are not in a random order, re-run the test
        for _ in range(5):
            action_stats = trial_run()
            if action_stats._dict['jump'] != [x for x in
                                              range(100)]:
                break
        assert action_stats._dict['jump'] != [x for x in range(100)]


if __name__ == '__main__':
    unittest.main()
