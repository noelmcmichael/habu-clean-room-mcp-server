"""
Comprehensive error handling and resilience utilities
"""
import logging
import traceback
import asyncio
from typing import Optional, Callable, Any, Dict
from functools import wraps
import json

logger = logging.getLogger(__name__)

class HabuError(Exception):
    """Base exception for Habu-related errors"""
    def __init__(self, message: str, error_code: str = "HABU_ERROR", details: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class APIError(HabuError):
    """API-related errors"""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict] = None):
        self.status_code = status_code
        super().__init__(message, "API_ERROR", details)

class AuthenticationError(HabuError):
    """Authentication-related errors"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "AUTH_ERROR", details)

class ConfigurationError(HabuError):
    """Configuration-related errors"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "CONFIG_ERROR", details)

class NetworkError(HabuError):
    """Network-related errors"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "NETWORK_ERROR", details)

def retry_async(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Retry decorator for async functions with exponential backoff
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = delay * (backoff ** attempt)
                        logger.warning(f"{func.__name__} attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"{func.__name__} failed after {max_retries} attempts")
            
            raise last_exception
        return wrapper
    return decorator

def handle_exceptions(default_return: Any = None, log_error: bool = True):
    """
    Exception handler decorator that returns a default value on error
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.error(f"Error in {func.__name__}: {e}")
                    logger.debug(traceback.format_exc())
                return default_return
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.error(f"Error in {func.__name__}: {e}")
                    logger.debug(traceback.format_exc())
                return default_return
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

def format_error_response(error: Exception, include_details: bool = False) -> str:
    """
    Format error as JSON response for MCP tools
    """
    error_response = {
        "status": "error",
        "error_type": type(error).__name__,
        "message": str(error)
    }
    
    if isinstance(error, HabuError):
        error_response["error_code"] = error.error_code
        if include_details and error.details:
            error_response["details"] = error.details
    
    if isinstance(error, APIError):
        error_response["status_code"] = error.status_code
    
    # Add summary for LLM consumption
    error_response["summary"] = f"An error occurred: {str(error)}"
    
    return json.dumps(error_response, indent=2)

class CircuitBreaker:
    """
    Circuit breaker pattern implementation for API resilience
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def is_open(self) -> bool:
        """Check if circuit breaker is open"""
        if self.state == "OPEN":
            if self.last_failure_time and \
               (asyncio.get_event_loop().time() - self.last_failure_time) > self.recovery_timeout:
                self.state = "HALF_OPEN"
                return False
            return True
        return False
    
    def record_success(self):
        """Record successful operation"""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def record_failure(self):
        """Record failed operation"""
        self.failure_count += 1
        self.last_failure_time = asyncio.get_event_loop().time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit breaker opened after {self.failure_count} failures")

def with_circuit_breaker(circuit_breaker: CircuitBreaker):
    """
    Decorator to add circuit breaker protection to functions
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if circuit_breaker.is_open():
                raise NetworkError("Service temporarily unavailable (circuit breaker open)")
            
            try:
                result = await func(*args, **kwargs)
                circuit_breaker.record_success()
                return result
            except Exception as e:
                circuit_breaker.record_failure()
                raise
        
        return wrapper
    return decorator

# Global circuit breaker instances
habu_api_circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)
openai_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)