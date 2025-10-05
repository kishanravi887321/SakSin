#!/usr/bin/env python3
"""
Test Configuration Loading
Quick test to verify the config loads without dataclass errors
"""

import os
import sys

def test_config_loading():
    """Test if the configuration loads properly"""
    try:
        # Set up Django environment
        sys.path.insert(0, 'src')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        
        import django
        from django.conf import settings
        
        if not settings.configured:
            django.setup()
        
        # Test importing the config
        from apps.central.langchain_setup.config import LangChainConfig
        print("✅ LangChainConfig imported successfully")
        
        # Test accessing the configuration
        model = LangChainConfig.GEMINI_MODEL
        fallbacks = LangChainConfig.GEMINI_FALLBACK_MODELS
        
        print(f"✅ Primary model: {model}")
        print(f"✅ Fallback models: {fallbacks}")
        
        # Test configuration methods
        gemini_config = LangChainConfig.get_gemini_config()
        print(f"✅ Gemini config loaded: {gemini_config['model']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def main():
    print("🔧 Testing Configuration Loading")
    print("=" * 35)
    
    if test_config_loading():
        print("\n🎉 SUCCESS!")
        print("✅ Configuration loads properly")
        print("✅ No more dataclass errors")
        print("🚀 Django server should start normally now")
    else:
        print("\n❌ Configuration test failed")
        print("💡 Check the error details above")

if __name__ == "__main__":
    main()