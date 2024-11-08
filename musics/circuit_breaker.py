from typing import Callable
from enum import Enum
from datetime import timedelta
import time
import logging

logger = logging.getLogger('django')

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

        logger.info(f'{self.main_func.__repr__()} and {self.sub_func.__repr__()}')

    def execute(self, *args, **kwargs):
        logger.info(f'CircuitBreaker status: {self.status}, using api handler:' + 
                        f'{self.sub_func.__repr__() if self.status == CircuitBreakerStatus.OPEN \
                                                    else self.main_func.__repr__()}')  
        if self.status == CircuitBreakerStatus.OPEN:
            if self.last_failure_time and time.time() - self.last_failure_time > self.delay.total_seconds():
                self.status = CircuitBreakerStatus.HALF_OPEN
                self.last_failure_time = time.time()
            else:
                return self.sub_func(*args, **kwargs)
        elif self.status == CircuitBreakerStatus.CLOSED:
            try:
                return self.main_func(*args, **kwargs)
            except Exception:
                self.failure_count += 1
                
                if self.failure_count >= self.max_failures:
                    self.status = CircuitBreakerStatus.OPEN
                self.last_failure_time = time.time()

                return self.sub_func(*args, **kwargs)
        else:#HALF_OPEN
            try:
                result = self.main_func(*args, **kwargs)
                self.failure_count = 0
                self.status = CircuitBreakerStatus.CLOSED
                return result
            except Exception:
                self.status = CircuitBreakerStatus.OPEN
                self.last_failure_time = time.time()
                self.sub_func(*args, **kwargs)
            

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .circuit_breaker import CircuitBreaker

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

from .search_api_handler import SpotifyAPIHandler,ShazamAPIHandler

main_api_handler = SpotifyAPIHandler(sp)
sub_api_handler = ShazamAPIHandler()

circuit_breaker = CircuitBreaker(main_api_handler.search, 
                                 sub_api_handler.search, 
                                 3, 
                                 timedelta(seconds=10))