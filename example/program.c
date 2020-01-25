#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#ifdef __unix__
#include <unistd.h>
#define STDIN STDIN_FILENO
#else
#define STDIN 0
#endif

#define INT_MAX_LEN 10

int  receive(int *);
void send(int);
int  process(int);

int main(int argc, char* argv[])
{
    int i, output, input, dataChanged;

    if (argc > 1)
    {
        for (i = 1; i < argc; i++)
        {
            printf("[%d] %s\n", i, argv[i]);
            fflush(stdout);
        }
    }

    while (1)
    {
        dataChanged = receive(&input);

        if (dataChanged == 1)
        {
            if (input == 42)
            {
                break;
            }

            output = process(input);
            send(output);
        }
    }

    return EXIT_SUCCESS;
}

int receive(int *data)
{
    int i, nBytes;
    char buffer[INT_MAX_LEN + 1];
    memset(buffer, 0x0, INT_MAX_LEN + 1);

    nBytes = read(STDIN, buffer, INT_MAX_LEN);

    if (nBytes > 1)
    {
        for (i = 0; i < nBytes; i++)
        {
            if (buffer[i] == '\n')
            {
                buffer[i] = '\0';
            }
            else if (!isdigit(buffer[i]))
            {
                return -1;
            }
        }

        *data = atoi(buffer);
        return 1;
    }

    return 0;
}

void send(int data)
{
    printf("%d\n", data);
    fflush(stdout);
}

int process(int data)
{
    return (data % 42) + 1;
}
