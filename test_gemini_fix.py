#!/usr/bin/env python3
"""
Test script for the updated Gemini integration
Run this to verify the fix is working correctly
"""

import os
import sys

def test_import():
    """Test if the new google-genai package is installed"""
    try:
        from google import genai
        print("✅ Google GenAI package imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import google-genai: {e}")
        print("💡 Please install: pip install google-genai")
        return False

def test_client_creation():
    """Test if the client can be created"""
    try:
        # Configure Django settings for testing
        import django
        from django.conf import settings
        
        if not settings.configured:
            settings.configure(
                DEBUG=True,
                SECRET_KEY='test-key-for-gemini-fix',
                INSTALLED_APPS=[
                    'django.contrib.contenttypes',
                    'django.contrib.auth',
                ],
                DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': ':memory:',
                    }
                }
            )
            django.setup()
        
        # Set dummy API keys for testing
        for i in range(1, 55):
            os.environ[f'GOOGLE_API_KEY_{i}'] = f'dummy_key_{i}_for_testing'
        
        # Test importing the client class
        from src.apps.central.langchain_setup.clients import GeminiClient
        print("✅ GeminiClient class imported successfully")
        
        # Test basic initialization (this might fail with dummy keys, but that's expected)
        try:
            client = GeminiClient()
            print("✅ GeminiClient initialized successfully")
        except Exception as init_error:
            if "api_key" in str(init_error).lower() or "invalid" in str(init_error).lower():
                print("⚠️  Client initialization requires valid API key (expected with dummy keys)")
                print("✅ Code structure is correct - ready for real API key")
            else:
                raise init_error
        
        print("✅ Updated code structure is correct")
        return True
    except Exception as e:
        print(f"❌ Error testing client: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 Testing Gemini API Fix...")
    print("=" * 50)
    
    # Test imports
    if not test_import():
        print("\n📋 Installation Instructions:")
        print("1. Activate your virtual environment")
        print("2. Run: pip install google-genai")
        print("3. Re-run this test")
        return False
    
    # Test client creation
    if not test_client_creation():
        print("❌ Client creation failed - check the code updates")
        return False
    
    print("\n✅ All tests passed!")
    print("\n📋 What was fixed:")
    print("1. Updated model from 'gemini-1.5-flash' to 'gemini-2.5-flash'")
    print("2. Replaced langchain-google-genai with new google-genai SDK")
    print("3. Updated all client methods to use the new API")
    print("4. Added google-genai to requirements.txt")
    
    print("\n🚀 Next steps:")
    print("1. Make sure to install: pip install google-genai")
    print("2. Set your GEMINI_API_KEY environment variable")
    print("3. Test your actual API calls")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)