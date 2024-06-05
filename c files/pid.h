#ifndef PID_H
#define PID_H


typedef struct PID{
    int derivative;
    double proportional;
    int integral;
} PID_t;

#endif


