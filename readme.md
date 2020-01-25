# simple-ipc

A simple python interface for inter-process communication, a way to asynchronously exchange data with external programs at runtime. The internal mechanism functions by writing data to *stdout* and reading from *stdin* using multi threading. 

## Installation
- `pip install simple-ipc`

In the python code:
- `import ipc` or
- `from ipc import Worker`

## Usage

### The constructor
```
Worker(command, callback=None)
```
- ```command``` a path to an executable [arguments]  
May be a **list** of seperate arguments that *can include spaces*  
or of type **str** that is split internally with *no support for spaces*.

- ```callback``` [optional] a function that is called after new data has been received  
The data will be passed to the callback function, so it must have exactly one argument.

#### Example
```python
def new_data(data):
    print(data)

worker1 = Worker("/path/to/program.exe arg1 arg2", new_data)
worker2 = Worker(["with space.exe", "arg1", "spaced arg2"])
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



## Example program

As part of the example a "program.c" file is included which can be compiled with ```gcc program.c -o program```, though a compiled executable for windows and linux are also included. It is a program that reads numbers from *stdin* and sends modified values back via *stdout*. As it only accepts numbers, it will not respond to data that contains letters or other symbols. A ```'\n'``` (newline) at the end of the data is needed to function properly. The numbers are exemplary reduced to a range of 1 to 42 and the program will close when the input is 42.

**Example code:**
```python
import ipc

def new_data(data):
    print('Received: {}'.format(data))

cmd = 'program.exe'
worker = ipc.Worker(cmd, new_data)
while True:
    number = 0
    while worker.running:
        print('Sending: {}'.format(number))
        worker.send(number)
        print('Data in main: {}'.format(worker.data))
        number += 21
    worker.run()
```

**Output:**
```
Started worker
Sending: 0
Received: 1
Data in main: 1
Sending: 21
Received: 22
Data in main: 22
Sending: 42
Stopped worker [exit code: 0]
Data in main: None
```