#include "detection.h"
#include "pattern.h"

bool baselineDetection(void){
    float * curr = ring_buffer + read;//pointer to starting location
    
    const float * stop = ring_buffer + write;//pointer to end location
    
    const float * buffer_limit = ring_buffer + BUFFER_SIZE;//DO NOT GO OVER THIS LIMIT !!! 

    uint8_t pattern_size; //cannot go over 256 so 1 byte is enough

    while(curr != stop){
        curr++; pattern_size++;
        if(curr >= buffer_limit) curr = ring_buffer;
    }

    
    


}