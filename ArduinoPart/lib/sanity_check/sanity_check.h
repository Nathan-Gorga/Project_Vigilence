// ==================== SANITY CHECK LIBRARY ====================
// Comprehensive diagnostic library for Arduino development
// ===============================================================

#include "includes.h"



#ifndef SANITY_CHECK_H
#define SANITY_CHECK_H

// Configuration - Enable/disable features to save memory

// #define SANITY_ENABLE_MEMORY_TRACKING 
// #define SANITY_ENABLE_PERFORMANCE_TIMING
#define SANITY_ENABLE_LOOP_MONITORING
// #define SANITY_ENABLE_WATCHDOG
// #define SANITY_ENABLE_SYSTEM_HEALTH
#define SANITY_MAX_TIMERS 10

// Memory thresholds (bytes)
#define SANITY_MEMORY_WARNING_THRESHOLD  200
#define SANITY_MEMORY_CRITICAL_THRESHOLD 100

// Performance timing structure
typedef struct {
    const char* name;
    unsigned long start_time;
    unsigned long total_time;
    unsigned long call_count;
    unsigned long min_time;
    unsigned long max_time;
    bool active;
} performance_timer_t;

// System health status
typedef struct {
    unsigned long uptime_ms;
    int free_ram;
    int min_free_ram;
    unsigned long heap_usage;
    unsigned long stack_usage_estimate;
    unsigned long loop_count;
    unsigned long max_loop_time;
    unsigned long avg_loop_time;
    bool memory_warning;
    bool memory_critical;
} system_health_t;

// Global variables
static performance_timer_t timers[SANITY_MAX_TIMERS];
static system_health_t health_status;
static unsigned long last_loop_time = 0;
static unsigned long loop_time_accumulator = 0;
static int timer_count = 0;
static unsigned long watchdog_last_feed = 0;



#ifdef SANITY_ENABLE_MEMORY_TRACKING
// ==================== MEMORY FUNCTIONS ====================

// Get current free RAM
int sanity_get_free_ram() {
    extern int __heap_start, *__brkval;
    int v;
    return (int)&v - (__brkval == 0 ? (int)&__heap_start : (int)__brkval);
}

// Get stack usage estimate (not 100% accurate but useful)
int sanity_get_stack_usage() {
    extern int __heap_start;
    int stack_var;
    return (int)&__heap_start - (int)&stack_var;
}

// Initialize memory monitoring
void sanity_memory_init() {
    health_status.free_ram = sanity_get_free_ram();
    health_status.min_free_ram = health_status.free_ram;
    health_status.heap_usage = 0;
    health_status.memory_warning = false;
    health_status.memory_critical = false;
}

// Update memory statistics
void sanity_memory_update() {
    health_status.free_ram = sanity_get_free_ram();
    health_status.stack_usage_estimate = sanity_get_stack_usage();
    
    // Track minimum free RAM
    if (health_status.free_ram < health_status.min_free_ram) {
        health_status.min_free_ram = health_status.free_ram;
    }
    
    // Set warning flags
    health_status.memory_warning = (health_status.free_ram < SANITY_MEMORY_WARNING_THRESHOLD);
    health_status.memory_critical = (health_status.free_ram < SANITY_MEMORY_CRITICAL_THRESHOLD);
    
    // Emergency action if critical
    if (health_status.memory_critical) {
        Serial.println("CRITICAL: Memory critically low!");
        sanity_print_memory_status();
    }
}

// Print detailed memory status
void sanity_print_memory_status() {
    Serial.println("=== MEMORY STATUS ===");
    Serial.print("Free RAM: ");
    Serial.print(health_status.free_ram);
    Serial.println(" bytes");
    Serial.print("Minimum Free RAM: ");
    Serial.print(health_status.min_free_ram);
    Serial.println(" bytes");
    Serial.print("Stack Usage (est): ");
    Serial.print(health_status.stack_usage_estimate);
    Serial.println(" bytes");
    Serial.print("Status: ");
    if (health_status.memory_critical) {
        Serial.println("CRITICAL");
    } else if (health_status.memory_warning) {
        Serial.println("WARNING");
    } else {
        Serial.println("OK");
    }
    Serial.println("====================");
}

#endif // SANITY_ENABLE_MEMORY_TRACKING


#ifdef SANITY_ENABLE_PERFORMANCE_TIMING
// ==================== PERFORMANCE TIMING ====================

// Start timing a function
int sanity_timer_start(const char* name) {
    // Find existing timer or create new one
    int timer_id = -1;
    
    // Look for existing timer
    for (int i = 0; i < timer_count; i++) {
        if (strcmp(timers[i].name, name) == 0) {
            timer_id = i;
            break;
        }
    }
    
    // Create new timer if not found
    if (timer_id == -1 && timer_count < SANITY_MAX_TIMERS) {
        timer_id = timer_count++;
        timers[timer_id].name = name;
        timers[timer_id].total_time = 0;
        timers[timer_id].call_count = 0;
        timers[timer_id].min_time = ULONG_MAX;
        timers[timer_id].max_time = 0;
    }
    
    if (timer_id >= 0) {
        timers[timer_id].start_time = micros();
        timers[timer_id].active = true;
    }
    
    return timer_id;
}

// Stop timing and record results
void sanity_timer_stop(int timer_id) {
    if (timer_id < 0 || timer_id >= timer_count || !timers[timer_id].active) {
        return;
    }
    
    unsigned long elapsed = micros() - timers[timer_id].start_time;
    
    timers[timer_id].total_time += elapsed;
    timers[timer_id].call_count++;
    
    if (elapsed < timers[timer_id].min_time) {
        timers[timer_id].min_time = elapsed;
    }
    if (elapsed > timers[timer_id].max_time) {
        timers[timer_id].max_time = elapsed;
    }
    
    timers[timer_id].active = false;
}

// Convenience macro for timing a block of code
#define SANITY_TIME_BLOCK(name, code) \
    do { \
        int timer_id = sanity_timer_start(name); \
        code; \
        sanity_timer_stop(timer_id); \
    } while(0)

// Print performance statistics
void sanity_print_performance() {
    Serial.println("=== PERFORMANCE STATS ===");
    for (int i = 0; i < timer_count; i++) {
        Serial.print(timers[i].name);
        Serial.print(": ");
        Serial.print(timers[i].call_count);
        Serial.print(" calls, Avg: ");
        if (timers[i].call_count > 0) {
            Serial.print(timers[i].total_time / timers[i].call_count);
        } else {
            Serial.print("0");
        }
        Serial.print("μs, Min: ");
        Serial.print(timers[i].min_time == ULONG_MAX ? 0 : timers[i].min_time);
        Serial.print("μs, Max: ");
        Serial.print(timers[i].max_time);
        Serial.println("μs");
    }
    Serial.println("========================");
}

#endif // SANITY_ENABLE_PERFORMANCE_TIMING


#ifdef SANITY_ENABLE_LOOP_MONITORING
// ==================== LOOP MONITORING ====================

// Call this at the start of each loop()
void sanity_loop_start() {
    last_loop_time = micros();
}

// Call this at the end of each loop()
void sanity_loop_end() {
    unsigned long loop_time = micros() - last_loop_time;
    
    health_status.loop_count++;
    loop_time_accumulator += loop_time;
    
    if (loop_time > health_status.max_loop_time) {
        health_status.max_loop_time = loop_time;
    }
    
    health_status.avg_loop_time = loop_time_accumulator / health_status.loop_count;
    
    // Warn about slow loops (>50ms)
    if (loop_time > 50000) {
        Serial.print("WARNING: Slow loop detected: ");
        Serial.print(loop_time);
        Serial.println("μs");
    }
}

#endif // SANITY_ENABLE_LOOP_MONITORING

#ifdef SANITY_ENABLE_WATCHDOG

// ==================== WATCHDOG FUNCTIONS ====================

// Software watchdog - call periodically to prevent lockup detection
void sanity_watchdog_feed() {
    watchdog_last_feed = millis();
}

// Check if watchdog has been fed recently (call from main loop)
void sanity_watchdog_check(unsigned long timeout_ms) {
    if (millis() - watchdog_last_feed > timeout_ms) {
        Serial.println("WATCHDOG: Potential system lockup detected!");
        Serial.print("Last feed: ");
        Serial.print(millis() - watchdog_last_feed);
        Serial.println("ms ago");
        
        // Could trigger a reset here if needed
        // wdt_reset(); // If using hardware watchdog
    }
}

#endif // SANITY_ENABLE_WATCHDOG

#ifdef SANITY_ENABLE_SYSTEM_HEALTH
// ==================== SYSTEM HEALTH ====================

// Initialize the sanity check system
void sanity_init() {
    Serial.println("=== SANITY CHECK SYSTEM INITIALIZED ===");
    
    // Initialize all subsystems
    sanity_memory_init();
    
    // Reset health status
    health_status.uptime_ms = 0;
    health_status.loop_count = 0;
    health_status.max_loop_time = 0;
    health_status.avg_loop_time = 0;
    
    // Initialize timers
    timer_count = 0;
    for (int i = 0; i < SANITY_MAX_TIMERS; i++) {
        timers[i].active = false;
    }
    
    // Feed watchdog
    sanity_watchdog_feed();
    
    Serial.print("Initial Free RAM: ");
    Serial.print(health_status.free_ram);
    Serial.println(" bytes");
}

// Update all health monitoring (call regularly)
void sanity_update() {
    health_status.uptime_ms = millis();
    sanity_memory_update();
    sanity_watchdog_check(5000); // 5 second watchdog timeout
}

// Print comprehensive system health report
void sanity_print_health_report() {
    Serial.println("=============== SYSTEM HEALTH REPORT ===============");
    
    // Uptime
    Serial.print("Uptime: ");
    Serial.print(health_status.uptime_ms / 1000);
    Serial.println(" seconds");
    
    // Memory status
    sanity_print_memory_status();
    
    // Loop performance
    Serial.println("=== LOOP PERFORMANCE ===");
    Serial.print("Total loops: ");
    Serial.println(health_status.loop_count);
    Serial.print("Average loop time: ");
    Serial.print(health_status.avg_loop_time);
    Serial.println("μs");
    Serial.print("Maximum loop time: ");
    Serial.print(health_status.max_loop_time);
    Serial.println("μs");
    
    // Performance timers
    sanity_print_performance();
    
    Serial.println("==================================================");
}

// Quick status check - returns true if system is healthy
bool sanity_is_healthy() {
    return !health_status.memory_critical && 
           health_status.max_loop_time < 100000 && // Less than 100ms loops
           (millis() - watchdog_last_feed) < 10000; // Watchdog fed within 10s
}

#endif // SANITY_ENABLE_SYSTEM_HEALTH

#endif // SANITY_CHECK_H

// ==================== DEMO CODE ====================
/*
// Example function to test timing
void slow_function() {
    delay(10);  // Simulate slow operation
    for (int i = 0; i < 1000; i++) {
        float dummy = sqrt(i) * 3.14159;
        (void)dummy; // Prevent optimization
    }
}

void fast_function() {
    int sum = 0;
    for (int i = 0; i < 100; i++) {
        sum += i;
    }
}

void setup() {
    Serial.begin(9600);
    delay(2000);
    
    // Initialize sanity check system
    sanity_init();
    
    Serial.println("Running sanity check demos...");
    
    // Demo 1: Time some functions
    Serial.println("\n--- Timing Functions ---");
    for (int i = 0; i < 5; i++) {
        // Time the slow function
        int timer1 = sanity_timer_start("slow_function");
        slow_function();
        sanity_timer_stop(timer1);
        
        // Time the fast function
        int timer2 = sanity_timer_start("fast_function");
        fast_function();
        sanity_timer_stop(timer2);
        
        // You can also use the macro
        SANITY_TIME_BLOCK("macro_test", {
            delayMicroseconds(500);
            digitalRead(2);
        });
    }
    
    // Demo 2: Memory stress test
    Serial.println("\n--- Memory Stress Test ---");
    for (int i = 0; i < 10; i++) {
        void* ptr = malloc(100);
        if (ptr) {
            memset(ptr, i, 100);
            Serial.print("Allocated 100 bytes, iteration ");
            Serial.println(i);
            sanity_update(); // Update health status
        } else {
            Serial.println("Malloc failed!");
            break;
        }
        delay(200);
    }
    
    sanity_print_health_report();
}

void loop() {
    sanity_loop_start();
    
    // Simulate normal work
    static unsigned long lastReport = 0;
    static int workCounter = 0;
    
    // Do some work
    SANITY_TIME_BLOCK("main_work", {
        // Simulate sensor reading
        int sensor = analogRead(A0);
        
        // Simulate processing
        float processed = sensor * 0.1 + sin(workCounter * 0.1);
        (void)processed; // Prevent optimization
        
        workCounter++;
    });
    
    // Update sanity checks
    sanity_update();
    
    // Feed the watchdog
    sanity_watchdog_feed();
    
    // Print health report every 10 seconds
    if (millis() - lastReport > 10000) {
        sanity_print_health_report();
        lastReport = millis();
        
        // Check overall health
        if (sanity_is_healthy()) {
            Serial.println("✓ System is healthy");
        } else {
            Serial.println("⚠ System health issues detected!");
        }
    }
    
    sanity_loop_end();
    delay(100); // Simulate loop timing
}*/