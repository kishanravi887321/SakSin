"""
Test script specifically for debugging the interview service list index error
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

def test_interview_service_flow():
    """Test the complete interview service flow to identify index errors"""
    print("🔍 Testing Interview Service Flow...")
    
    try:
        from apps.central.langchain_setup.services import InterviewService
        
        service = InterviewService()
        print("✅ Interview service initialized")
        
        # Test starting a session
        test_config = {
            "role": "Software Engineer",
            "experience": "Mid-level",
            "industry": "Technology"
        }
        
        print("📝 Starting interview session...")
        session_result = service.start_interview_session("test_user_123", test_config)
        
        if session_result["status"] != "success":
            print(f"❌ Failed to start session: {session_result}")
            return False
        
        session_id = session_result["session_id"]
        print(f"✅ Session started: {session_id}")
        
        # Check session status
        print("📊 Checking session status...")
        status_result = service.get_session_status(session_id)
        print(f"📊 Session status: {status_result}")
        
        # Test submitting an answer
        print("💬 Submitting test answer...")
        test_answer = "I have 3 years of experience in Python development, working with Django and Flask frameworks."
        
        answer_result = service.submit_answer(session_id, test_answer)
        
        if answer_result["status"] == "error":
            print(f"❌ Error submitting answer: {answer_result}")
            return False
        
        print(f"✅ Answer submitted successfully: {answer_result['status']}")
        
        # Check session status again
        print("📊 Checking session status after answer...")
        status_result_after = service.get_session_status(session_id)
        print(f"📊 Session status after: {status_result_after}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """Test edge cases that might cause index errors"""
    print("\n🔍 Testing Edge Cases...")
    
    try:
        from apps.central.langchain_setup.services import InterviewService
        from django.core.cache import cache
        
        service = InterviewService()
        
        # Test 1: Submit answer to non-existent session
        print("🧪 Test 1: Non-existent session")
        result = service.submit_answer("fake_session_id", "test answer")
        expected_error = result["status"] == "error"
        print(f"{'✅' if expected_error else '❌'} Non-existent session handled: {result['message']}")
        
        # Test 2: Create session with corrupted data
        print("🧪 Test 2: Corrupted session data")
        corrupted_session_id = "corrupted_session_123"
        corrupted_data = {
            "session_id": corrupted_session_id,
            "user_id": "test_user",
            "config": {"role": "Test", "experience": "Test", "industry": "Test"},
            "questions": [],  # Empty questions list
            "responses": [],
            "current_question_index": 5,  # Index higher than questions available
            "status": "active"
        }
        
        cache.set(f"interview_session:{corrupted_session_id}", corrupted_data, 3600)
        
        # Try to submit answer to corrupted session
        result = service.submit_answer(corrupted_session_id, "test answer")
        print(f"📊 Corrupted session result: {result}")
        
        # Test session validation/repair
        status_result = service.get_session_status(corrupted_session_id)
        print(f"📊 Session repair result: {status_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Starting Interview Service Debug Tests\n")
    
    tests = [
        ("Normal Flow", test_interview_service_flow),
        ("Edge Cases", test_edge_cases),
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
        print("\n🎉 All tests passed! The list index error should be fixed!")
    else:
        print("\n⚠️  Some tests failed. The issue may still exist.")
    
    return passed == total

if __name__ == "__main__":
    main()
