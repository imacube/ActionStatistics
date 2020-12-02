"""ActionStatistics stores the average time for each of the provided actions."""

class ActionStatistics:
    def __init__(self):
        pass

    def addAction(self, action: str):
        """Add an action's time to the average for that action.

        Parameters
        ----------
        action : str
            A JSON serialized string.
        """
        pass

    def getStats(self):
        """Return the average times for each action.

        Returns
        -------
        str
            JSON serialized string containing a list of the actions and their respective average times.
        """
        pass