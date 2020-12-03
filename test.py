"""Basic tests for this module."""
import unittest
from multiprocessing import Process
from random import randint
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
    def sub_process(action_stats, add_action: dict, sleep_window=0):
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

        for key, value in add_action.items():
            action_stats._dict[key] = value
            history = action_stats._dict.get(f'history_{key}', list())
            history.append(value)
            action_stats._dict[f'history_{key}'] = history

    def test_access_dict(self):
        """Test accessing the shared dictionary."""
        action_stats = ActionStatistics()
        action_stats._dict['a'] = 1

        assert action_stats._dict['a'] == 1

    def test_sub_process(self):
        """Test a subprocess accessing the shared dict."""

        action_stats = ActionStatistics()
        p = Process(target=self.sub_process, args=(action_stats, {'abc': 123}, 3))
        p.start()
        p.join()

        assert action_stats._dict['abc'] == 123

    def test_multiple_sub_processes(self):
        """Test multiple subprocesses accessing the shared dict."""

        action_stats = ActionStatistics()
        processes = list()
        for d in [{'abc': x} for x in range(100)]:
            p = Process(target=self.sub_process, args=(action_stats, d, 0))
            processes.append(p)

        for p in processes:
            p.start()
        for p in processes:
            p.join()

        history = action_stats._dict['history_abc']
        assert history != [x for x in range(100)]
        for x in range(100):
            if x not in history:
                print(f'\nMissing value: {x}')
        assert set(history) == {x for x in range(100)}


if __name__ == '__main__':
    unittest.main()
