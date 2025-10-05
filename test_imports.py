#!/usr/bin/env python3
"""
Test Django imports after fixing missing files
"""

import os
import sys
import django
from django.conf import settings

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_django_setup():
    """Test if Django can start without errors"""
    try:
        # Configure Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        
        # Add some dummy environment variables
        os.environ['SECRET_KEY'] = 'test-secret-key-for-import-test'
        os.environ['DEBUG'] = 'True'
        os.environ['GOOGLE_API_KEY_1'] = 'dummy-key-for-test'
        
        # Setup Django
        django.setup()
        print("✅ Django setup successful")
        
        # Test LangChain imports
        from apps.central.langchain_setup.config import LangChainConfig
        print("✅ LangChainConfig imported successfully")
        
        from apps.central.langchain_setup.clients import GeminiClient, ClientFactory
        print("✅ Clients imported successfully")
        
        from apps.central.langchain_setup.services import ChatService, InterviewService, AnalysisService
        print("✅ Services imported successfully")
        
        # Test configuration
        config = LangChainConfig.get_gemini_config()
        print(f"✅ Configuration loaded - Model: {config['model']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 Testing Django Import Fix")
    print("=" * 35)
    
    if test_django_setup():
        print("\n🎉 SUCCESS!")
        print("✅ All imports working correctly")
        print("✅ Django can start without module errors")
        print("🚀 Your server should now start properly")
    else:
        print("\n❌ Still having issues")
        print("Check the error messages above")

if __name__ == "__main__":
    main()