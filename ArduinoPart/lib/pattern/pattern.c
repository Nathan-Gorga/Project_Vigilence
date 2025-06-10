#include "pattern.h"

#define MAXIMUM_PATTERN_DURATION 256

float patterns[NUM_EVENTS][MAXIMUM_PATTERN_DURATION];
uint16_t pattern_durations[NUM_EVENTS];


void initPatternDuration(void){
    for(int i = 0; i < NUM_EVENTS; ++i){
        pattern_durations[i] = 0;
    }
}

void createPattern(enum EVENT_TYPE type){
    //extract pattern from file

    //add pattern to specified event location

    //change pattern duration

}