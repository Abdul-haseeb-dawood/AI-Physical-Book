import logging
from datetime import datetime
import json
from typing import Dict, Any


class Logger:
    """
    Utility class for logging with security monitoring
    """
    def __init__(self, name: str = "rag_chatbot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create console handler if not already exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_security_event(self, event_type: str, details: Dict[str, Any], ip_address: str = None):
        """
        Log security-related events
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details,
            "ip_address": ip_address
        }
        
        self.logger.info(f"SECURITY_EVENT: {json.dumps(log_data)}")

    def log_query(self, query: str, response: str, user_id: str = None, ip_address: str = None):
        """
        Log user queries for monitoring
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query[:100] + "..." if len(query) > 100 else query,  # Truncate long queries
            "response_length": len(response),
            "user_id": user_id,
            "ip_address": ip_address
        }
        
        self.logger.info(f"QUERY_LOG: {json.dumps(log_data)}")

    def log_error(self, error: str, context: Dict[str, Any] = None):
        """
        Log errors with context
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "error": error,
            "context": context
        }
        
        self.logger.error(f"ERROR_LOG: {json.dumps(log_data)}")

    def log_info(self, message: str):
        """
        Log general information
        """
        self.logger.info(message)


# Global logger instance
logger = Logger()