#!/usr/bin/env python3
import time
import ipc

def new_data(data):
    print('Received: {}'.format(data))

def main():
    cmd = 'program.exe arg1 arg2 arg3'
    worker = ipc.Worker(cmd, new_data)
    while True:
        number = 0
        while worker.running:
            print('Sending: {}'.format(number))
            worker.send(number)
            time.sleep(0.5)
            print('Data: {}'.format(worker.data))
            number += 6
        worker.run()

if __name__ == '__main__':
    main()
