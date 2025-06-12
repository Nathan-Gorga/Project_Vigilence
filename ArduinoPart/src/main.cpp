#include "includes.h"
#include "sanity_check.h"

#include "pattern.h"

void setup() { 
  Serial.begin(9600); 
  while (!Serial);

  // calibration

  // get pattern
  initPatternDuration();
}

void loop() { 
  sanity_loop_start();



  // is data in the buffer an event? (should be super fast, no more than 1/SFREQ seconds should go in this function)
  
    // no -> return to data line

    // yes -> create thread 1 to fill the buffer while we work on the data 

      // detect event

      // clean event

        //save to external memory

        // return to data line and destroy thread 1

  sanity_loop_end();
}
