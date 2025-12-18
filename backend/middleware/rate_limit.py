import time
from typing import Dict
from fastapi import Request, HTTPException
from config.settings import settings


class RateLimiter:
    """
    Simple in-memory rate limiter
    """
    def __init__(self):
        self.requests: Dict[str, list] = {}  # IP -> list of request timestamps
        self.limit = settings.RATE_LIMIT_REQUESTS
        self.window = settings.RATE_LIMIT_WINDOW

    def is_allowed(self, ip: str) -> bool:
        """
        Check if a request from the given IP is allowed
        """
        current_time = time.time()
        
        # Clean old requests outside the window
        if ip in self.requests:
            self.requests[ip] = [
                req_time for req_time in self.requests[ip]
                if current_time - req_time < self.window
            ]
        else:
            self.requests[ip] = []
        
        # Check if limit exceeded
        if len(self.requests[ip]) >= self.limit:
            return False
        
        # Add current request
        self.requests[ip].append(current_time)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit_middleware(request: Request) -> bool:
    """
    Rate limiting middleware function
    """
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return True