"""ActionStatistics stores the average time for each of the provided actions."""
import threading
from json import loads, dumps  # minor performance improvement not calling a . sub-method
from queue import SimpleQueue
from statistics import mean
from time import sleep


class ActionStatistics:
    def __init__(self):
        self.queue_add_action = SimpleQueue()
        self.queue_get_stats = SimpleQueue()
        self.queue_get_stats_response = SimpleQueue()
        self._dict = dict()
        threading.Thread(target=self.worker, daemon=True).start()

    def worker(self):
        """Manages queue needs."""
        while True:
            if self.queue_add_action.empty() and self.queue_get_stats.empty():
                sleep(0.5)
                continue
            if not self.queue_add_action.empty():
                item = self.queue_add_action.get_nowait()
                if item:
                    self._add_action(item)
            if not self.queue_get_stats.empty() and self.queue_get_stats.get_nowait():
                self.queue_get_stats_response.put(self._get_stats())

    def addAction(self, action: str):
        """Add an action's time to the average for that action.

        Parameters
        ----------
        action : str
            A JSON serialized string.
        """
        self.queue_add_action.put(action)

    def getStats(self):
        """Return the average times for each action.

        Returns
        -------
        str
            JSON serialized string containing a list of the actions and their respective average times.
        """
        self.queue_get_stats.put(True)
        return self.queue_get_stats_response.get(block=True, timeout=5)

    def _add_action(self, action: str):
        """Add an action to the internal storage object.

        Parameter
        ---------
        action : str
            JSON serialized action to add.
        """
        action = loads(action)
        action_time = action['time']
        action = action['action']
        internal_action = self._dict.get(action, list())
        internal_action.append(int(action_time))
        self._dict[action] = internal_action

    def _get_stats(self):
        """Return the stats."""
        return dumps(
            [
                {'action': k, 'avg': mean(v)} for k, v in
                self._dict.items()
            ]
        )
