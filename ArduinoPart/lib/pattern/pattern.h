#ifndef PATTERN_H
#define PATTERN_H

#include "includes.h"

#define BLINK_PATTERN_LENGTH BLINK_DURATION
#define MAXIMUM_PATTERN_DURATION 256

enum EVENT_TYPE{
    NORMAL_BLINK,
    FAST_BLINK,
    SLOW_BLINK,
    SACCADE_LEFT,
    SACCADE_RIGHT,
    SACCADE_DOWN,
    SACCADE_UP,
    NUM_EVENTS,
    NOT_EVENT
};

float patterns[NUM_EVENTS][MAXIMUM_PATTERN_DURATION];
uint16_t pattern_durations[NUM_EVENTS];

void initPatternDuration(void);


#endif