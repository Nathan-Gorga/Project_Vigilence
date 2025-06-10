#include "includes.h"
#include "sanity_check.h"

#define BUFFER_SIZE 16

float ring_buffer[BUFFER_SIZE];
uint16_t head = 0;
uint16_t tail = 0;

static struct pt_sem full, empty;

static struct pt pt_producer, pt_consumer;

static
PT_THREAD(producer(struct pt * pt)){
  static uint16_t i = 0;
  PT_BEGIN(pt);
  
  while (1) {
    PT_SEM_WAIT(pt, &empty);
    ring_buffer[head] = i;
    head = (head + 1) % BUFFER_SIZE;
    i++; // next value
    PT_SEM_SIGNAL(pt, &full);
  }

  PT_END(pt);
}

static
PT_THREAD(consumer(struct pt *pt)){
  PT_BEGIN(pt);

  while (1) {
    PT_SEM_WAIT(pt, &full);
    Serial.println(ring_buffer[tail]);
    tail = (tail + 1) % BUFFER_SIZE;
    PT_SEM_SIGNAL(pt, &empty);
  }

  PT_END(pt);
}

void setup() { 
  Serial.begin(9600); 
  while (!Serial);

  PT_SEM_INIT(&empty, BUFFER_SIZE);
  PT_SEM_INIT(&full, 0);

  PT_INIT(&pt_producer);
  PT_INIT(&pt_consumer);
}

void loop() { 
  sanity_loop_start();

  PT_SCHEDULE(producer(&pt_producer));
  PT_SCHEDULE(consumer(&pt_consumer));

  sanity_loop_end();
}
