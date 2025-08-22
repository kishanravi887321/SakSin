"""
Django Management Command for LangChain Setup
Professional command for initializing and managing LangChain integrations
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import sys

from apps.central.langchain_setup.config import LangChainConfig
from apps.central.langchain_setup.clients import ClientFactory
from apps.central.langchain_setup.services import ChatService, InterviewService, AnalysisService


class Command(BaseCommand):
    help = 'Initialize and manage LangChain setup for Sākṣin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['init', 'test', 'validate', 'status'],
            default='init',
            help='Action to perform'
        )
        
        parser.add_argument(
            '--api-key',
            type=str,
            help='Google API Key for Gemini'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        try:
            if action == 'init':
                self.initialize_langchain(options.get('api_key'))
            elif action == 'test':
                self.test_integration()
            elif action == 'validate':
                self.validate_configuration()
            elif action == 'status':
                self.show_status()
                
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')

    def initialize_langchain(self, api_key=None):
        """Initialize LangChain configuration"""
        self.stdout.write(self.style.SUCCESS('🚀 Initializing LangChain Setup for Sākṣin...'))
        
        # Set API key if provided
        if api_key:
            os.environ['GOOGLE_API_KEY'] = api_key
            self.stdout.write(self.style.SUCCESS('✅ Google API Key set'))
        
        # Validate configuration
        try:
            LangChainConfig.validate_config()
            self.stdout.write(self.style.SUCCESS('✅ Configuration validated'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'❌ Configuration error: {e}'))
            return
        
        # Test client initialization
        try:
            client = ClientFactory.get_default_client()
            self.stdout.write(self.style.SUCCESS('✅ Gemini client initialized'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Client initialization failed: {e}'))
            return
        
        # Initialize services
        try:
            chat_service = ChatService()
            interview_service = InterviewService()
            analysis_service = AnalysisService()
            self.stdout.write(self.style.SUCCESS('✅ All services initialized'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Service initialization failed: {e}'))
            return
        
        self.stdout.write(self.style.SUCCESS('🎉 LangChain setup completed successfully!'))

    def test_integration(self):
        """Test LangChain integration"""
        self.stdout.write(self.style.SUCCESS('🧪 Testing LangChain Integration...'))
        
        try:
            # Test client
            client = ClientFactory.get_default_client()
            response = client.generate_response("Hello, this is a test message.")
            self.stdout.write(self.style.SUCCESS('✅ Client test passed'))
            
            # Test chat service
            chat_service = ChatService()
            chat_response = chat_service.send_message("Test message", "test_user")
            if chat_response['status'] == 'success':
                self.stdout.write(self.style.SUCCESS('✅ Chat service test passed'))
            else:
                self.stdout.write(self.style.ERROR('❌ Chat service test failed'))
            
            # Test interview service
            interview_service = InterviewService()
            interview_config = {
                'role': 'Software Engineer',
                'experience': 'Mid-level',
                'industry': 'Technology'
            }
            session_response = interview_service.start_interview_session("test_user", interview_config)
            if session_response['status'] == 'success':
                self.stdout.write(self.style.SUCCESS('✅ Interview service test passed'))
            else:
                self.stdout.write(self.style.ERROR('❌ Interview service test failed'))
            
            self.stdout.write(self.style.SUCCESS('🎉 All tests passed!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Test failed: {str(e)}'))

    def validate_configuration(self):
        """Validate LangChain configuration"""
        self.stdout.write(self.style.SUCCESS('🔍 Validating Configuration...'))
        
        # Check environment variables
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            self.stdout.write(self.style.SUCCESS('✅ GOOGLE_API_KEY is set'))
        else:
            self.stdout.write(self.style.ERROR('❌ GOOGLE_API_KEY is not set'))
        
        # Check Django settings
        debug_mode = getattr(settings, 'DEBUG', False)
        self.stdout.write(f'ℹ️  Debug mode: {debug_mode}')
        
        # Check configuration
        try:
            config = LangChainConfig()
            self.stdout.write(f'ℹ️  Gemini model: {config.GEMINI_MODEL}')
            self.stdout.write(f'ℹ️  Temperature: {config.GEMINI_TEMPERATURE}')
            self.stdout.write(f'ℹ️  Max tokens: {config.GEMINI_MAX_TOKENS}')
            self.stdout.write(f'ℹ️  Cache enabled: {config.CACHE_ENABLED}')
            self.stdout.write(self.style.SUCCESS('✅ Configuration is valid'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Configuration error: {e}'))

    def show_status(self):
        """Show current status of LangChain integration"""
        self.stdout.write(self.style.SUCCESS('📊 LangChain Integration Status'))
        self.stdout.write('=' * 50)
        
        # Configuration status
        try:
            LangChainConfig.validate_config()
            self.stdout.write(self.style.SUCCESS('✅ Configuration: Valid'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Configuration: {e}'))
        
        # Client status
        try:
            client = ClientFactory.get_default_client()
            self.stdout.write(self.style.SUCCESS('✅ Gemini Client: Available'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Gemini Client: {e}'))
        
        # Services status
        try:
            ChatService()
            self.stdout.write(self.style.SUCCESS('✅ Chat Service: Ready'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Chat Service: {e}'))
        
        try:
            InterviewService()
            self.stdout.write(self.style.SUCCESS('✅ Interview Service: Ready'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Interview Service: {e}'))
        
        try:
            AnalysisService()
            self.stdout.write(self.style.SUCCESS('✅ Analysis Service: Ready'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Analysis Service: {e}'))
        
        self.stdout.write('=' * 50)
