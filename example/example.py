# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                           #
#   Setup:                                                                                  #
#   As part of the example a "program.c" file is included which can be compiled             #
#   with "gcc program.c -o program", though a compiled executable for windows and           #
#   linux is included. On linux one extra step is required to execute this example.         #
#   You have to change the permissions of "program" with "chmod +x program".                #
#                                                                                           #
#   Explanation:                                                                            #
#   The included program reads numbers from stdin and sends modified values back via        #
#   stdout. As it only accepts numbers, it will not respond to data that contains letters   #
#   or other symbols. A '\n' (newline) at the end of the data is needed to function         #
#   properly. The numbers are exemplary reduced to a range of 1 to 42 and the program       #
#   will close when the input is 42.                                                        #
#                                                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import time
import ipc

# callback function
def new_data(data):
    # print the data immediately after receiving
    print('Received: {}'.format(data))

def main():
    # name of the included example program
    program = 'program'

    # add file extention on windows
    if os.name == 'nt':
        program += '.exe'

    # get path of the program
    example_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(example_dir, program)

    # create a worker object
    worker = ipc.Worker(path, new_data)

    while True:                                    # repeat forever
        number = 0                                 # here data is a number
        while worker.running:                      # run until the external program terminates
            print('Sending: {}'.format(number))    # print what will be sent
            worker.send(number)                    # send the data to the external program
            time.sleep(0.2)                        # small delay to see what is happening
            print('Data: {}'.format(worker.data))  # sporadic printing of the latest value
            number += 6                            # incrementing the value
        time.sleep(2)                              # delay to see that the program has ended
        worker.run()                               # launch the external program again


from random import randint

if __name__ == '__main__':
    #main()
    worker = ipc.Worker('program.exe', new_data)
    while True:


        while worker.running:
            number = randint(1, 10)
            print(f'Sending: {number}')
            worker.send(number)
            print(f'Data: {worker.data}')
