#ifndef PATTERN_H
#define PATTERN_H

#include "includes.h"

#define BLINK_PATTERN_LENGTH BLINK_DURATION

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

void initPatternDuration(void);


#endif