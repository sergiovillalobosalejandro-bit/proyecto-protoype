"""
Centralized logging configuration for the Clinical Intervention Tracking System
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

class ClinicalLogger:
    """Custom logger for clinical operations"""
    
    def __init__(self, name: str = "clinical_system"):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with custom formatting"""
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Set log level
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler for all logs
        file_handler = logging.FileHandler(
            logs_dir / f"clinical_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Error file handler
        error_handler = logging.FileHandler(
            logs_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
    
    def log_user_action(self, user_id: int, action: str, details: Optional[str] = None):
        """Log user actions for audit trail"""
        message = f"User {user_id} performed: {action}"
        if details:
            message += f" - {details}"
        self.logger.info(f"[USER_ACTION] {message}")
    
    def log_api_request(self, endpoint: str, method: str, user_id: Optional[int] = None, 
                       status_code: int = 200, duration_ms: Optional[float] = None):
        """Log API requests for monitoring"""
        message = f"{method} {endpoint} - {status_code}"
        if user_id:
            message += f" - User: {user_id}"
        if duration_ms:
            message += f" - Duration: {duration_ms:.2f}ms"
        self.logger.info(f"[API_REQUEST] {message}")
    
    def log_database_operation(self, operation: str, table: str, record_id: Optional[int] = None):
        """Log database operations"""
        message = f"{operation} on {table}"
        if record_id:
            message += f" - ID: {record_id}"
        self.logger.info(f"[DB_OPERATION] {message}")
    
    def log_ai_operation(self, operation: str, couder_id: int, success: bool = True, 
                        error: Optional[str] = None):
        """Log AI operations"""
        status = "SUCCESS" if success else "FAILED"
        message = f"{operation} for Couder {couder_id} - {status}"
        if error:
            message += f" - Error: {error}"
        self.logger.info(f"[AI_OPERATION] {message}")
    
    def log_security_event(self, event: str, user_id: Optional[int] = None, 
                          ip_address: Optional[str] = None, details: Optional[str] = None):
        """Log security-related events"""
        message = f"SECURITY: {event}"
        if user_id:
            message += f" - User: {user_id}"
        if ip_address:
            message += f" - IP: {ip_address}"
        if details:
            message += f" - {details}"
        self.logger.warning(f"[SECURITY] {message}")
    
    def log_error(self, error: Exception, context: Optional[str] = None, 
                 user_id: Optional[int] = None):
        """Log errors with context"""
        message = f"Error: {str(error)}"
        if context:
            message += f" - Context: {context}"
        if user_id:
            message += f" - User: {user_id}"
        self.logger.error(f"[ERROR] {message}", exc_info=True)

# Global logger instance
logger = ClinicalLogger()
