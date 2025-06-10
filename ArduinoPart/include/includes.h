#ifndef INCLUDES_H
#define INCLUDES_H

#include <Arduino.h>
#include <pt.h>


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




#endif
