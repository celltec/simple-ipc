# simple-ipc

#### Inter-process communication based on stdio

![Python Version](https://img.shields.io/pypi/pyversions/simple-ipc)
![PyPI Version](https://img.shields.io/pypi/v/simple-ipc)
![License](https://img.shields.io/github/license/celltec/simple-ipc)

A simple python interface for inter-process communication, a way to asynchronously 
exchange data with external programs at runtime. The internal mechanism functions 
by writing data to *stdout* and reading from *stdin* using multi threading. 

## Installation
`pip install simple-ipc`

## Usage

### Importing
- `import ipc`  
or
- `from ipc import Worker`


### The worker constructor
```
Worker(command, callback=None)
```
- ```command``` a path to an executable [arguments]  
May be a **list** of seperate arguments that *can include spaces*  
or of type **str** that is split internally with *no support for spaces*.

- ```callback``` (optional) a function that is called after new data has been received  
The data will be passed to the callback function, so it must have exactly one argument.

#### Example
```python
def new_data(data):
    print(data)

worker1 = Worker('program.exe arg1 arg2', new_data)
worker2 = Worker(['with space.exe', 'spaced arg'])
```

### A worker object

The worker starts automatically when created.

#### Methods
- `run()` starts the worker
- `send(data)` sends the data to the external process
- `shutdown()` initiates the termination of all threads and clears all data

#### Properties
- `running` indicates the status of the worker *(read-only)*
- `data` holds the data from the external program *(read-only)*  
Note that any data will be converted to type `str` internally.

#### Example
```python
while worker.running:
    worker.send(123)
    print(worker.data)
```

### Example program
```python
from random import randint
from ipc import Worker

def new_data(data):
    print(f'Received: {data}')

worker = Worker('program.exe', new_data)

while worker.running:
    number = randint(1, 10)
    print(f'Sending: {number}')
    worker.send(number)
    print(f'Data: {worker.data}')
```
