# LangChain Integration Package
__version__ = "1.0.0"
__author__ = "Sākṣin Development Team"

from .config import LangChainConfig
from .clients import GeminiClient
# from .clients import OllamaClient
from .services import ChatService, AnalysisService, InterviewService
from .utils import ResponseFormatter, ErrorHandler

__all__ = [
    'LangChainConfig',
    'GeminiClient', 
    # 'OllamaClient',
    'ChatService',
    'AnalysisService',
    'InterviewService',
    'ResponseFormatter',
    'ErrorHandler'
]
