#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include <fcntl.h>
#include <sys/stat.h>
#include <mqueue.h>
#include <time.h>
#include <errno.h>
#include <assert.h>

#define STDOUT_PREFIX "usnd: "
#define STDERR_PREFIX "usnd: "

#define QUEUE_WRITE_NAME "/DRC-CONT-DATA"
#define QUEUE_WRITE_SIZE 64
#define SIGNITURE 2

mqd_t open_write_queue(char *qName);
int get_distance();
void write_message(char *buff, int distance);

int main(int argc, char **argv) {
    mqd_t writeQueue = open_write_queue(QUEUE_WRITE_NAME);
    printf(STDOUT_PREFIX "Opened queue \"%s\"\n", QUEUE_WRITE_NAME);
    fflush(stdout);

    char message[QUEUE_WRITE_SIZE];
    while(1) {
        int distance = get_distance();

        write_message(message, distance);
        
        mq_send(writeQueue, message, QUEUE_WRITE_SIZE, 0);

        printf(STDOUT_PREFIX "Sent %i\n", distance);
        fflush(stdout);

        struct timespec delay = {1, 0}; // 1 second
        nanosleep(&delay, NULL);
    }
}

mqd_t open_write_queue(char *qName) {
    mqd_t queue = mq_open(qName, O_WRONLY);
    while (queue == -1) {
        if (queue == (mqd_t) -1 && errno != ENOENT) {
            perror(STDERR_PREFIX "mq_open failed");
            fflush(stderr);
            exit(EXIT_FAILURE);
        }

        printf(STDOUT_PREFIX "Failed to open queue \"%s\"\n", qName);
        printf(STDOUT_PREFIX "Retrying\n");
        fflush(stdout);

        struct timespec delay = {0, 200000000}; // 200 ms
        nanosleep(&delay, NULL);

        queue = mq_open(qName, O_WRONLY);
    }

    return queue;
}

int get_distance() {
    static bool randInitialised = false;
    if (!randInitialised) {
        srand(time(NULL));
        randInitialised = true;
    }
        
    return random() % 1000;
}

void write_message(char *buff, int distance) {
    struct Message {
        int sig;
        int distance;
    };

    assert(sizeof(struct Message) <= QUEUE_WRITE_SIZE);

    struct Message m = {SIGNITURE, distance};
    memcpy(buff, &m, sizeof(m));
}
