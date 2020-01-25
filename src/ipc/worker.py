import sys
import shlex
import inspect
from subprocess import Popen, PIPE
from threading import Thread, Event

class Worker:
    def __init__(self, command, callback=None):
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
        self.__cmd = command
        self.__callback = callback
        self.__data = None
        self.__process = None
        self.__running = Event()
        self.run()

    @property
    def running(self):
        return self.__running.is_set() and self.__process and self.__process.returncode is None

    @property
    def data(self):
        return self.__data

    def __read(self):
        while self.running:
            try:
                readout = self.__process.stdout.readline().strip()
                if readout:
                    self.__data = readout.decode()
                    if self.__callback:
                        self.__callback(self.__data)
            except Exception:
                print('Error reading data!')

    def __run(self):
        print('Started worker')
        exit_code = self.__process.wait()
        self.shutdown()
        print('Stopped worker [exit code: {}]'.format(exit_code))

    def run(self):
        if not self.running:
            try:
                self.__process = Popen(self.__cmd, stdin=PIPE, stdout=PIPE)
            except Exception as e:
                print('Error opening "{}": {}'.format(' '.join(self.__cmd), e.strerror))
                return
            self.__running.set()
            Thread(target=self.__run).start()
            Thread(target=self.__read).start()

    def send(self, data):
        if self.running:
            try:
                self.__process.stdin.write((str(data) + '\n').encode())
                self.__process.stdin.flush()
            except (OSError, IOError):
                print('Error sending data!')
        else:
            print('Worker not running!')

    def shutdown(self):
        if self.running:
            self.__process.terminate()
        self.__running.clear()
        self.__process = None
        self.__data = None
