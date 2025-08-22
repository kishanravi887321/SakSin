"""
Django App Configuration for LangChain Central
Professional configuration for AI service integration
"""

from django.apps import AppConfig


class CentralConfig(AppConfig):
    """Configuration for the Central LangChain app"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.central'
    verbose_name = 'LangChain Central Services'
    
    def ready(self):
        """Initialize the app when Django starts"""
        try:
            # Import signals if any
            # from . import signals
            
            # Initialize LangChain configuration
            self._initialize_langchain()
            
            # Set up logging
            self._setup_logging()
            
            print("✅ LangChain Central app initialized successfully")
            
        except Exception as e:
            print(f"⚠️ Warning: Error initializing LangChain Central app: {e}")
    
    def _initialize_langchain(self):
        """Initialize LangChain configuration on app startup"""
        try:
            from .langchain_setup.config import LangChainConfig
            
            # Validate configuration
            LangChainConfig.validate_config()
            
            print("✅ LangChain configuration validated")
            
        except ImportError:
            print("⚠️ LangChain setup not found - run setup_langchain management command")
        except Exception as e:
            print(f"⚠️ LangChain configuration error: {e}")
    
    def _setup_logging(self):
        """Set up logging for the central app"""
        import logging
        
        # Configure logger for this app
        logger = logging.getLogger('apps.central')
        
        if not logger.handlers:
            # Create console handler
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
