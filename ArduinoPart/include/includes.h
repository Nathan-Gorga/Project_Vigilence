#ifndef INCLUDES_H
#define INCLUDES_H

#include <Arduino.h>
#include <pt.h>
#include <limits.h>

#define BLINK_DURATION 160

#define S_FREQ 200

//let's try 1 second for now
#define BUFFER_SIZE S_FREQ * 1//seconds

////FOR NOW , WE WILL USE 1 CHANNEL TO RECORD DATA (THEREFOR JUST 1 FLOAT) TO MAKE SURE SRAM CAN HANDLE IT, WILL SEE ABOUT SCALING IT LATER
// typedef struct data_point{
//     float y_channel1;
//     float y_channel2;
// }data_point;

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