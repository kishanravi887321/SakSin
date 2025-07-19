"""
LangChain Configuration for Sākṣin
Centralized configuration management for all LangChain integrations
"""

import os
from typing import Dict, Any, Optional
from django.conf import settings
from dataclasses import dataclass


@dataclass
class LangChainConfig:
    """Configuration class for LangChain integrations"""
    
    # Google Gemini Configuration
    GOOGLE_API_KEY: str = os.getenv('GOOGLE_API_KEY', '')
    print(GOOGLE_API_KEY,"this is the key   ")
    GEMINI_MODEL: str = "gemini-1.5-flash"
    # GEMINI_MODEL: str = "llama3"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 4096
    GEMINI_TOP_P: float = 0.9
    GEMINI_TOP_K: int = 40
    
    # General LangChain Settings
    VERBOSE: bool = getattr(settings, 'DEBUG', False)
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 60
    MAX_REQUESTS_PER_HOUR: int = 1000
    
    # Timeout Settings
    REQUEST_TIMEOUT: int = 30  # seconds
    
    # Interview Specific Settings
    INTERVIEW_SESSION_TIMEOUT: int = 3600  # 1 hour
    MAX_INTERVIEW_QUESTIONS: int = 20
    
    # Analysis Settings
    ANALYSIS_BATCH_SIZE: int = 10
    ENABLE_SENTIMENT_ANALYSIS: bool = True
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configurations are present"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        return True
    
    @classmethod
    def get_gemini_config(cls) -> Dict[str, Any]:
        """Get Gemini-specific configuration"""
        return {
            'model': cls.GEMINI_MODEL,
            'temperature': cls.GEMINI_TEMPERATURE,
            'max_tokens': cls.GEMINI_MAX_TOKENS,
            'top_p': cls.GEMINI_TOP_P,
            'top_k': cls.GEMINI_TOP_K,
            'api_key': cls.GOOGLE_API_KEY
        }
    
    @classmethod
    def get_chat_config(cls) -> Dict[str, Any]:
        """Get chat-specific configuration"""
        return {
            'verbose': cls.VERBOSE,
            'temperature': cls.GEMINI_TEMPERATURE,
            'max_tokens': cls.GEMINI_MAX_TOKENS,
            'timeout': cls.REQUEST_TIMEOUT
        }


# Environment validation
try:
    LangChainConfig.validate_config()
except ValueError as e:
    print(f"⚠️  Configuration Warning: {e}")
    print("💡 Please set the GOOGLE_API_KEY environment variable")
