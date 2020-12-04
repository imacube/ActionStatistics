# Action Statistics

This library provides methods for storing actions with their respective times and returning the average time for each
action. The methods permit concurrent access.

## Usage

Sample usage of this library:

```python
from action_statistics import ActionStatistics

action_stats = ActionStatistics()
action_stats.addAction('''{"action":"jump", "time":100}''')  # Adds an action with time
action_stats.getStats()  # Get actions and their mean time
```

## Requirements

This library was written with Python 3.7.5.

This library uses `threading.Thread` to manage all access to the internal data store, thereby allowing for concurrent
operations. While it is possible to directly access the internal data storage object, this is strongly discouraged.
Depending on which python implementation is used, it cannot be assumed that the Global Interpreter Lock (GIL) will
safeguard access to the storage object. However, as this is python threading performance will be limited by the GIL.

## Future Considerations

There is no input error checking for input values or exception handling, this is left to the user at this time.

An initial attempt was made to use a `multiprocessing.Manager` proxy object which would bypass the Python's Global
Interpreter Lock (GIL), but preliminary sanity checks revealed a number of entries not getting stored. To see this early
stage code please see git commit `61b44847`.

# Install

This assumes you have Python 3.7.5 and `pip` installed.

```shell
pip install <path or URL of this repo>
```

# Test

Run the `test.py` script.

```shell
python3 test.py
```

The test execution time will vary some due to random sleep intervals introduced to test for concurrency issues.