#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <mqueue.h>
#include <limits.h>
#include <time.h>
#include <errno.h>
#include <assert.h>

#define STDOUT_PREFIX "cont: "
#define STDERR_PREFIX "cont: "

#define SNDR_NONE 0
#define SNDR_VISN 1
#define SNDR_USND 2
#define SNDR_CONT 3
#define SNDR_DRIV 4

#define SNDR_UNKN_STR "unknown"
#define SNDR_VISN_STR "visn"
#define SNDR_USND_STR "usnd"
#define SNDR_CONT_STR "cont"
#define SNDR_DRIV_STR "driv"

#define QUEUE_READ_NAME "/DRC-CONT-DATA"
#define QUEUE_READ_SIZE 64
#define QUEUE_READ_ELMS 10

#define QUEUE_WRITE_NAME "/DRC-DRIV-DATA"
#define QUEUE_WRITE_SIZE 64
#define SIGNITURE SNDR_CONT

#define GET_NTH_INT(buffer, n)      (((int *) buffer)[n])
#define GET_SENDER(message)         GET_NTH_INT(message, 0)
#define GET_LANE_CENT_X(message)    GET_NTH_INT(message, 1)
#define GET_LANE_CENT_Y(message)    GET_NTH_INT(message, 2)
#define GET_DIST_IN_FRONT(message)  GET_NTH_INT(message, 1)

#define NSEC_PER_SEC 1000000000

#define MAX_LANE_CENT_X 639
#define MIN_LANE_CENT_X 0
#define MAY_LANE_CENT_Y 479
#define MIN_LANE_CENT_Y 0

struct State {
    int laneCentX;
    int laneCentY;
    int distInFront;
};


void unlink_read_queue();
void attach_unlink_sig_handler();
mqd_t open_read_queue(char *qName);
mqd_t open_write_queue(char *qName);
void update_sense_data(struct State *state, mqd_t readQueue);
float calc_speed(struct State *state);
float calc_turn_angle(struct State *state);
void write_message(char *message, float speed, float turnAngle);

int main(int argc, char **argv) {
    atexit(unlink_read_queue);
    attach_unlink_sig_handler();

    mqd_t readQueue = open_read_queue(QUEUE_READ_NAME);
    printf(STDOUT_PREFIX "Opened queue \"%s\"\n", QUEUE_READ_NAME);
    fflush(stdout);

    mqd_t writeQueue = open_write_queue(QUEUE_WRITE_NAME);
    printf(STDOUT_PREFIX "Opened queue \"%s\"\n", QUEUE_WRITE_NAME);
    fflush(stdout);

    char message[QUEUE_WRITE_SIZE];
    memset(message, 0, QUEUE_WRITE_SIZE);

    struct State state;
    memset(&state, 0, sizeof(state));
    while (1) {
        update_sense_data(&state, readQueue);

        printf(
            STDOUT_PREFIX
            "Sense data (%i, %i, %i)\n",
            state.laneCentX,
            state.laneCentY,
            state.distInFront);
        fflush(stdout);

        float speed = calc_speed(&state);
        float turnAngle = calc_turn_angle(&state);

        write_message(message, speed, turnAngle);
        mq_send(writeQueue, message, sizeof(message), 0);

        printf(
            STDOUT_PREFIX
            "Sent       (%.2f, %.2f)\n",
            turnAngle,
            speed);
        fflush(stdout);

        struct timespec delay;
        delay.tv_sec = 5;
        delay.tv_nsec = 0;
        nanosleep(&delay, NULL);
    }

}

static void timespec_sum(struct timespec *dest, const struct timespec *toAdd) {
    if (toAdd == NULL || dest == NULL) {
        return;
    }

    dest->tv_sec += toAdd->tv_sec;
    dest->tv_nsec += toAdd->tv_nsec;

    while (dest->tv_nsec >= NSEC_PER_SEC) {
        dest->tv_sec++;
        dest->tv_nsec -= NSEC_PER_SEC;
    }
}

void unlink_read_queue() {
    mq_unlink(QUEUE_READ_NAME);
    printf(STDOUT_PREFIX "Unlinked queue \"%s\"\n", QUEUE_READ_NAME);
    fflush(stdout);
}

void sig_handler_unlink_then_exit(int signum) {
    printf(STDOUT_PREFIX "Received signal %i\n", signum);
    fflush(stdout);
    exit(signum);
}

void attach_unlink_sig_handler() {
    struct sigaction sa;

    sa.sa_handler = sig_handler_unlink_then_exit;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;

    int signals[] = {SIGINT, SIGTERM, SIGABRT, SIGQUIT, SIGHUP, 0};

    for (int *cursor = signals; *cursor != 0; cursor++) {
        int error = sigaction(*cursor, &sa, NULL);
        if (error == -1) {
            perror(STDERR_PREFIX "sigaction failed");
            fflush(stderr);
            exit(EXIT_FAILURE);
        }
    }
}

mqd_t open_read_queue(char *qName) {
    mqd_t queue;

    struct mq_attr attr;
    attr.mq_maxmsg = QUEUE_READ_ELMS;
    attr.mq_msgsize = QUEUE_READ_SIZE;

    queue = mq_open(
        qName,
        O_CREAT | O_RDONLY,
        S_IRWXU,
        &attr);

    if (queue == (mqd_t) -1) {
        perror(STDERR_PREFIX "mq_open failed");
        fflush(stderr);
        exit(EXIT_FAILURE);
    }

    return queue;
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

int extract_data(struct State *state, char *message) {
    int sender = GET_SENDER(message);
    switch(sender) {
        default:
            sender = SNDR_NONE;
            break;
        case SNDR_VISN:
            state->laneCentX = GET_LANE_CENT_X(message);
            state->laneCentY = GET_LANE_CENT_Y(message);
            break;
        case SNDR_USND:
            state->distInFront = GET_DIST_IN_FRONT(message);
            break;
    }
    return sender;
}

int read_message(char *message, mqd_t queue, const struct timespec *timeout) {
    int bytesRead = 0;

    struct timespec absTimeout;
    clock_gettime(CLOCK_REALTIME, &absTimeout);
    timespec_sum(&absTimeout, timeout);

    bytesRead = mq_timedreceive(
        queue,
        message,
        QUEUE_READ_SIZE,
        NULL,
        &absTimeout);

    if (bytesRead == -1) {
        if (errno == ETIMEDOUT) {
            return 0;
        }

        perror(STDERR_PREFIX "mq_receive failed");
        fflush(stderr);
        exit(EXIT_FAILURE);
    }

    return bytesRead;
}

char *get_sender_str(int s) {
    switch(s) {
        default:
            return SNDR_UNKN_STR;
        case SNDR_VISN:
            return SNDR_VISN_STR;
        case SNDR_USND:
            return SNDR_USND_STR;
        case SNDR_CONT:
            return SNDR_CONT_STR;
        case SNDR_DRIV:
            return SNDR_DRIV_STR;
    }
}

void update_sense_data(struct State *state, mqd_t readQueue) {
    int sender;
    int bytesRead = 0;
    char message[QUEUE_READ_SIZE];

    // 100 year timeout
    struct timespec maxTimeout;
    maxTimeout.tv_sec = 100L * 365L * 24L * 60L * 60L;
    maxTimeout.tv_nsec = 999999999L;

    bytesRead = read_message(message, readQueue, &maxTimeout);
    while (bytesRead > 0) {
        sender = extract_data(state, message);
        printf(
            STDOUT_PREFIX
            "Received message from %s\n",
            get_sender_str(sender));
        fflush(stdout);

        bytesRead = read_message(message, readQueue, NULL);
    }
}

float calc_speed(struct State *state) {
    return 100;
}

float calc_turn_angle(struct State *state) {
    float value = (state->laneCentX - MIN_LANE_CENT_X);
    float range = (MAX_LANE_CENT_X - MIN_LANE_CENT_X);
    return 180 * value/range;
}

void write_message(char *buff, float speed, float turnAngle) {
    struct Message {
        int sig;
        float speed;
        float turnAngle;
    };

    assert(sizeof(struct Message) <= QUEUE_WRITE_SIZE);
    
    struct Message m = {SIGNITURE, speed, turnAngle};
    memcpy(buff, &m, sizeof(m));
}
