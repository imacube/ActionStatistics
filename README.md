# Action Statistics

This library provides methods for storing actions and their respective times. It can then return the average time for
all the stored actions. The methods permit concurrent access.

## Requirements

This library was written with Python 3.7.5.

This library uses `threading.Thread` to manage all access to the internal data store, thereby allowing for concurrent
operations. While it is possible to directly access the internal data storage object, this is strongly discouraged.
Depending on which python implementation is used, it cannot be assumed that the Global Interpreter Lock (GIL) will
safeguard access to the storage object. However, as this is python threading performance will be limited by the GIL.

## Future Considerations

There is no input error checking for input values or exception handling, this is left to the user at this time.

An initial attempt was made to use a `multiprocessing.Manager` proxy object which would bypass the Python's Global 
Interpreter Lock (GIL), but preliminary sanity checks revealed a number of entries not getting stored. To see this 
early stage code please see git commit `61b44847`.

# Build

# Test

Run the `test.py` script.

```shell
python3 test.py
```

The test execution time will vary some due to random sleep intervals introduced to test for concurrency issues.