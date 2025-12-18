import re
from typing import List, Tuple


class PromptSecurityService:
    """
    Service to protect against prompt injection attacks
    """
    
    def __init__(self):
        # Define patterns that might indicate prompt injection attempts
        self.injection_patterns = [
            # Attempts to instruct the model to ignore previous instructions
            r"(?i)\b(ignore|disregard|forget|override)\b.*\b(instructions|previous|above)\b",
            r"(?i)\b(never|always)\b.*\bsay\b",
            r"(?i)\brepeat\b.*\bexactly\b",
            r"(?i)\b(output|print|return)\b.*\bverbatim\b",
            r"(?i)\b(just)\b.*\b(print|output)\b",
            # Attempts to make the model reveal system prompts
            r"(?i)\b(system|hidden|secret)\b.*\binstructions?\b",
            r"(?i)\b(prompt|input|message)\b.*\bhistory\b",
            # Attempts to escape context
            r"(?i)\b(never|not|no)\b.*\bmention\b",
            r"(?i)\b(above|previous|before)\b.*\bignore\b",
            # Special characters that might be used for injection
            r"(?i)\b(system|user|assistant)\b.*:",
        ]
    
    def check_for_injection(self, user_input: str) -> Tuple[bool, List[str]]:
        """
        Check if the user input contains potential injection patterns
        Returns (is_injected, list_of_detected_patterns)
        """
        detected_patterns = []
        
        for pattern in self.injection_patterns:
            if re.search(pattern, user_input):
                detected_patterns.append(pattern)
        
        return len(detected_patterns) > 0, detected_patterns
    
    def sanitize_query_for_context(self, query: str) -> str:
        """
        Sanitize query to be safely included in LLM context
        """
        # Remove or escape characters that might interfere with the prompt structure
        sanitized = query.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        
        # Ensure the query doesn't contain separator tokens that might be used in the prompt
        sanitized = sanitized.replace('User:', 'user:').replace('Assistant:', 'assistant:').replace('System:', 'system:')
        
        return sanitized
    
    def is_safe_context(self, context: str) -> bool:
        """
        Check if the context (retrieved content) is safe to use
        """
        # For now, just check if it contains obvious signs of being a prompt instruction
        unsafe_patterns = [
            r"(?i)\b(system|assistant)\b.*:",
            r"(?i)^.*\b(user|assistant|system)\b\s*:\s*",
        ]
        
        for pattern in unsafe_patterns:
            if re.search(pattern, context.strip()):
                return False
        
        return True