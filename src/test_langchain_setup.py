"""
Test script for LangChain Central Services
Run this to verify the setup is working correctly
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_imports():
    """Test if all imports work correctly"""
    print("🔍 Testing imports...")
    
    try:
        from apps.central.models import (
            ConversationSession, ConversationMessage, InterviewSession,
            InterviewQuestion, AnalysisRequest, UserFeedback, SystemMetrics
        )
        print("✅ Models imported successfully")
    except ImportError as e:
        print(f"❌ Model import error: {e}")
        return False
    
    try:
        from apps.central.serializers import (
            ChatMessageSerializer, ChatResponseSerializer,
            InterviewConfigSerializer, AnalysisRequestSerializer
        )
        print("✅ Serializers imported successfully")
    except ImportError as e:
        print(f"❌ Serializer import error: {e}")
        return False
    
    try:
        from apps.central.views import (
            ChatAPIView, InterviewSessionAPIView, AnalysisAPIView
        )
        print("✅ Views imported successfully")
    except ImportError as e:
        print(f"❌ View import error: {e}")
        return False
    
    return True

def test_langchain_setup():
    """Test LangChain setup"""
    print("\n🔍 Testing LangChain setup...")
    
    try:
        from apps.central.langchain_setup.config import LangChainConfig
        print("✅ LangChain config imported successfully")
        
        # Test configuration validation
        try:
            LangChainConfig.validate_config()
            print("✅ LangChain configuration is valid")
        except Exception as e:
            print(f"⚠️  LangChain configuration warning: {e}")
            print("💡 Make sure to set GOOGLE_API_KEY environment variable")
        
    except ImportError as e:
        print(f"❌ LangChain setup import error: {e}")
        return False
    
    try:
        from apps.central.langchain_setup.clients import ClientFactory
        print("✅ LangChain clients imported successfully")
    except ImportError as e:
        print(f"❌ LangChain clients import error: {e}")
        return False
    
    try:
        from apps.central.langchain_setup.services import (
            ChatService, InterviewService, AnalysisService
        )
        print("✅ LangChain services imported successfully")
    except ImportError as e:
        print(f"❌ LangChain services import error: {e}")
        return False
    
    return True

def test_database_models():
    """Test database model creation"""
    print("\n🔍 Testing database models...")
    
    try:
        from apps.accounts.models import User
        print("✅ User model imported successfully")
        
        # Test if we can create model instances (without saving)
        from apps.central.models import ConversationSession
        
        # This won't save to database, just tests model creation
        session = ConversationSession(
            title="Test Conversation"
        )
        print("✅ ConversationSession model can be instantiated")
        
    except Exception as e:
        print(f"❌ Database model error: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 Starting LangChain Central Services Test\n")
    
    tests = [
        ("Imports", test_imports),
        ("LangChain Setup", test_langchain_setup),
        ("Database Models", test_database_models),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! LangChain Central Services is ready to use!")
        print("\n📝 Next steps:")
        print("1. Run migrations: python manage.py makemigrations central")
        print("2. Apply migrations: python manage.py migrate")
        print("3. Set GOOGLE_API_KEY environment variable")
        print("4. Test the API endpoints via /docs/")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
