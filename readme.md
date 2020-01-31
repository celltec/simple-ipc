# simple-ipc

#### Inter-process communication based on stdio

[![Python Version](https://img.shields.io/pypi/pyversions/simple-ipc)](https://www.python.org/downloads)
[![Downloads](https://pepy.tech/badge/simple-ipc)](https://pypistats.org/packages/simple-ipc)
[![PyPI Version](https://img.shields.io/pypi/v/simple-ipc)](https://pypi.org/project/simple-ipc)
[![License](https://img.shields.io/github/license/celltec/simple-ipc)](https://en.wikipedia.org/wiki/MIT_License)

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
Worker(command, callback=None, start=True)
```

- `command` a path to an executable along with optional arguments  
  - **list:** may include spaces 
  - **str:** no support for spaces

- `callback` *(optional)* a function that is called after new data has been received  
  - must take exactly one argument

- `start` *(optional)* determines if the worker should start when the object is created

#### Examples
```python
worker = Worker(['with space.exe', 'spaced arg'], start=False)
```

```python
with Worker('program.exe') as worker:
    ...
```

```python
Worker('path/to/program.exe arg', lambda data: print(data))
```

### A worker object
By default the worker starts automatically when created.

#### Methods
- `start()` starts the worker
- `send(data)` sends the data to the external process
- `stop()` initiates the termination of all threads and clears all data

#### Properties
- `running` indicates the status of the worker *(read-only)*
- `data` contains the most recent value *(read-only)*

All data will be converted to type `str` internally.

## Example program
```python
from random import randint
from ipc import Worker

def update(data):
    print(f'Received: {data}')

worker = Worker('program.exe', update)

while worker.running:
    number = randint(1, 10)
    print(f'Sending: {number}')
    worker.send(number)
    print(f'Data: {worker.data}')
```
