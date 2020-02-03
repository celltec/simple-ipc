import sys
import shlex
import inspect
from subprocess import Popen, PIPE
from threading import Thread, Event


class Worker:
    __id = 0

    def __init__(self, command, callback=None, start=True, verbose=False):
        if isinstance(command, str):
            command = shlex.split(command, posix=False)
        elif not isinstance(command, list):
            raise TypeError('"command" must be of type list or str!')
        if not command:
            raise ValueError('"command" must not be empty!')
        if callback is not None:
            if not callable(callback):
                raise TypeError('Invalid callback format!')
            if sys.version_info[0] == 3:
                arg_amount = len(inspect.getfullargspec(callback).args)
            else:
                arg_amount = len(inspect.getargspec(callback).args)
            if arg_amount != 1:
                raise TypeError('Callback must take exactly one argument!')
        Worker.__id += 1
        self.__id = Worker.__id
        self.__cmd = command
        self.__callback = callback
        self.__verbose = verbose
        self.__data = None
        self.__process = None
        self.__process_thread = None
        self.__read_thread = None
        self.__running = Event()
        if start:
            self.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __del__(self):
        self.stop()

    @property
    def running(self):
        return self.__running.is_set() and self.__process and self.__process.returncode is None

    @property
    def data(self):
        return self.__data

    def __print(self, text):
        print('[IPC Worker {}] {}'.format(self.__id, text))

    def __log(self, text):
        if self.__verbose:
            self.__print(text)

    def __read(self):
        while self.running:
            try:
                readout = self.__process.stdout.readline().strip()
                if readout:
                    self.__data = readout.decode()
                    self.__log('Received: {}'.format(self.__data))
                    if self.__callback:
                        self.__callback(self.__data)
            except Exception:
                self.__print('Error reading data!')

    def __start(self):
        exit_code = self.__process.wait()
        self.__log('Program ended with exit code: {}'.format(exit_code))
        self.stop()

    def start(self):
        self.__log('Started worker')
        if not self.running:
            try:
                self.__process = Popen(self.__cmd, stdin=PIPE, stdout=PIPE)
            except Exception as e:
                self.__print('Error opening "{}": {}'.format(' '.join(self.__cmd), e.strerror))
                return
            self.__running.set()
            self.__process_thread = Thread(target=self.__start).start()
            self.__read_thread = Thread(target=self.__read).start()

    def send(self, data):
        if self.running:
            self.__log('Sending: {}'.format(data))
            try:
                self.__process.stdin.write((str(data) + '\n').encode())
                self.__process.stdin.flush()
            except (OSError, IOError):
                self.__print('Error sending data!')
        else:
            self.__log('Worker not running!')

    def stop(self):
        if self.running:
            self.__process.terminate()
        self.__running.clear()
        if self.__process_thread:
            self.__process_thread.join()
        if self.__read_thread:
            self.__read_thread.join()
        self.__data = None
        self.__process = None
        self.__process_thread = None
        self.__read_thread = None
        self.__log('Stopped worker')
