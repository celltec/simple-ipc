# simple-ipc

#### Inter-process communication based on stdio

[![Python Version](https://badgen.net/badge/python/2.7%20%7C%203/)](https://www.python.org/downloads)
[![PyPI Version](https://badgen.net/pypi/v/simple-ipc/)](https://pypi.org/project/simple-ipc)
[![License](https://badgen.net/badge/license/MIT/)](https://opensource.org/licenses/mit-license.php)

A simple python interface for inter-process communication, a way to asynchronously 
exchange data with external programs at runtime. The internal mechanism functions 
by writing data to *stdout* and reading from *stdin* using multi threading. 

## Installation
`pip install simple-ipc`

## Usage
Import the module first:
- `import ipc`
- `from ipc import Worker`

### Parameters
```
Worker(command, callback=None, start=True, verbose=False)
```

- `command` a path to an executable along with optional arguments  
  - **list:** may include spaces 
  - **str:** no support for spaces

- `callback` *(optional)* a function that is called after new data has been received  
  - must take exactly one argument

- `start` *(optional)* start the worker automatically when created

- `verbose` *(optional)* print status messages

#### Examples
```python
worker = Worker(['with space.exe', 'spaced arg'], start=False)
```

```python
with Worker('program.exe', verbose=True) as worker:
    ...
```

```python
Worker('path/to/program.exe arg', lambda data: print(data))
```

### A worker object

All data will be converted to type `str` internally.

#### Methods
- `start()` starts the worker
- `send(data)` sends the data to the external process
- `stop()` initiates the termination of all threads and clears all data

#### Properties
- `running` indicates the status of the worker *(read-only)*
- `data` contains the most recent value *(read-only)*

## Example program
```python
from random import randint
from ipc import Worker

def process(data):
    if int(data) == 5:
        print('Process data...')

worker = Worker('program.exe', process)

while worker.running:
    number = randint(1, 10)
    worker.send(number)
    print(f'Data: {worker.data}')
```

More example code can be found [here](https://github.com/celltec/simple-ipc/tree/master/example/example.py).
