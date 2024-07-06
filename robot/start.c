#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv) {
    pid_t pid = -1;

    pid = fork();
    if (pid == 0) {
        execl(
            "/usr/bin/chrt",
            "chrt",
            "--fifo",
            "85",
            "./control",
            (char*) NULL);
        perror("control execl failed");
        exit(EXIT_FAILURE);
    }

    pid = fork();
    if (pid == 0) {
        execl(
            "/usr/bin/chrt",
            "chrt",
            "--fifo",
            "80",
            ".venv/DRC/bin/python",
            "driver.py",
            (char*) NULL);
        perror("vision execl failed");
        exit(EXIT_FAILURE);
    }

    pid = fork();
    if (pid == 0) {
        execl(
            "/usr/bin/chrt",
            "chrt",
            "--fifo",
            "80",
            ".venv/DRC/bin/python",
            "vision.py",
            (char*) NULL);
        perror("vision execl failed");
        exit(EXIT_FAILURE);
    }

    pid = fork();
    if (pid == 0) {
        execl(
            "/usr/bin/chrt",
            "chrt",
            "--fifo",
            "80",
            "./ultra_sonic",
            (char*) NULL);
        perror("ultra sonic execl failed");
        exit(EXIT_FAILURE);
    }

    // wait for all child processes to terminate
    while (wait(NULL) > -1);

    return 0;
}

