"""
Middleware for logging and security monitoring
"""

import time
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable
import logging
from ..core.logging import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all HTTP requests"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Get user info if available
        user_id = None
        try:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                # Note: In a real implementation, you'd decode the JWT here
                # For now, we'll just log the request
                pass
        except:
            pass
        
        # Log request
        logger.log_api_request(
            endpoint=str(request.url.path),
            method=request.method,
            user_id=user_id
        )
        
        # Process request
        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000
            
            # Log successful response
            logger.log_api_request(
                endpoint=str(request.url.path),
                method=request.method,
                user_id=user_id,
                status_code=response.status_code,
                duration_ms=duration_ms
            )
            
            return response
            
        except HTTPException as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log HTTP exception
            logger.log_api_request(
                endpoint=str(request.url.path),
                method=request.method,
                user_id=user_id,
                status_code=e.status_code,
                duration_ms=duration_ms
            )
            
            # Log security events for 401/403
            if e.status_code in [401, 403]:
                logger.log_security_event(
                    event=f"HTTP_{e.status_code}",
                    user_id=user_id,
                    ip_address=client_ip,
                    details=str(e.detail)
                )
            
            raise
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log unexpected error
            logger.log_error(
                error=e,
                context=f"Request: {request.method} {request.url.path}",
                user_id=user_id
            )
            
            logger.log_api_request(
                endpoint=str(request.url.path),
                method=request.method,
                user_id=user_id,
                status_code=500,
                duration_ms=duration_ms
            )
            
            raise

class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware for security headers and rate limiting"""
    
    def __init__(self, app, calls_per_minute: int = 60):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute
        self.request_counts = {}  # In production, use Redis
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Simple rate limiting (per IP)
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
        
        # Clean old requests (older than 1 minute)
        self.request_counts[client_ip] = [
            req_time for req_time in self.request_counts[client_ip]
            if current_time - req_time < 60
        ]
        
        # Check rate limit
        if len(self.request_counts[client_ip]) >= self.calls_per_minute:
            logger.log_security_event(
                event="RATE_LIMIT_EXCEEDED",
                ip_address=client_ip,
                details=f"More than {self.calls_per_minute} requests per minute"
            )
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        
        # Add current request
        self.request_counts[client_ip].append(current_time)
        
        # Process request
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Remove server headers
        if "Server" in response.headers:
            del response.headers["Server"]
        
        return response
