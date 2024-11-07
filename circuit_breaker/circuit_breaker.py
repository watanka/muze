from typing import Callable
from enum import Enum
from datetime import timedelta
import time

class CircuitBreakerStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, main_func: Callable, sub_func: Callable, max_failures: int, delay: timedelta):
        self.max_failures = max_failures
        self.delay = delay
        self.failure_count = 0
        self.last_failure_time = None
        self.status = CircuitBreakerStatus.CLOSED
        self.main_func = main_func
        self.sub_func = sub_func


    def execute(self, exception: Exception):
        if self.status == CircuitBreakerStatus.OPEN:
            if self.last_failure_time and time.time() - self.last_failure_time > self.delay.total_seconds():
                self.status = CircuitBreakerStatus.HALF_OPEN
                self.last_failure_time = time.time()
            else:
                return self.sub_func()
        elif self.status == CircuitBreakerStatus.CLOSED:
            try:
                return self.main_func()
            except exception:
                self.failure_count += 1
                
                if self.failure_count >= self.max_failures:
                    self.status = CircuitBreakerStatus.OPEN
                self.last_failure_time = time.time()
        else:#HALF_OPEN
            try:
                result = self.main_func()
                self.failure_count = 0
                self.status = CircuitBreakerStatus.CLOSED
                return result
            except:
                self.status = CircuitBreakerStatus.OPEN
                self.last_failure_time = time.time()
            
