#include "includes.h"

void setup() {
  Serial.begin(9600);

  const enum EVENT_TYPE test = NUM_EVENTS;
  Serial.print(test);
}

void loop() {
 
}

