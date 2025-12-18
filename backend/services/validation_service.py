import re
from typing import Optional


class ValidationService:
    """
    Service to handle input validation and sanitization
    """
    
    @staticmethod
    def validate_query(query: str) -> bool:
        """
        Validate query string
        """
        if not query or not query.strip():
            return False
        
        # Check length
        if len(query) > 2000:
            return False
            
        # Check for potentially malicious patterns
        if ValidationService._contains_malicious_content(query):
            return False
            
        return True
    
    @staticmethod
    def validate_selected_text(selected_text: str) -> bool:
        """
        Validate selected text
        """
        if not selected_text or not selected_text.strip():
            return False
            
        # Check length
        if len(selected_text) > 2000:
            return False
            
        # Check for potentially malicious patterns
        if ValidationService._contains_malicious_content(selected_text):
            return False
            
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Sanitize input text by removing potentially harmful content
        """
        # Remove potential script tags
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove potential javascript: urls
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        
        # Remove potential data: urls
        sanitized = re.sub(r'data:', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    @staticmethod
    def _contains_malicious_content(text: str) -> bool:
        """
        Check if text contains potentially malicious content
        """
        # Check for common malicious patterns
        malicious_patterns = [
            r'<script',
            r'javascript:',
            r'vbscript:',
            r'on\w+\s*=',
            r'<iframe',
            r'<object',
            r'<embed',
            r'<form',
        ]
        
        text_lower = text.lower()
        for pattern in malicious_patterns:
            if re.search(pattern, text_lower):
                return True
                
        return False