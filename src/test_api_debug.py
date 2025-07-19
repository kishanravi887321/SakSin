"""
Debug script to test the interview API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(url, method="GET", data=None, token=None):
    """Test an endpoint with optional authentication"""
    headers = {"Content-Type": "application/json"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        
        print(f"\n🔍 Testing {method} {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
            
        return response
        
    except Exception as e:
        print(f"❌ Error testing {url}: {e}")
        return None

def main():
    """Test various endpoints to debug the 401 error"""
    
    print("🚀 Starting API Endpoint Tests\n")
    
    # Test 1: Health check (should work without auth)
    print("="*50)
    print("TEST 1: Health Check")
    test_endpoint(f"{BASE_URL}/api/central/api/v1/health/")
    
    # Test 2: Test endpoint (should work without auth)
    print("\n" + "="*50)
    print("TEST 2: Test Endpoint")
    test_endpoint(f"{BASE_URL}/api/central/api/v1/health/test/")
    
    # Test 3: Test POST to test endpoint
    print("\n" + "="*50)
    print("TEST 3: Test POST Endpoint")
    test_data = {"test": "data"}
    test_endpoint(f"{BASE_URL}/api/central/api/v1/health/test/", "POST", test_data)
    
    # Test 4: Interview start without auth (should work now)
    print("\n" + "="*50)
    print("TEST 4: Interview Start (No Auth)")
    interview_data = {
        "role": "Software Engineer",
        "interview_type": "technical",
        "difficulty": "intermediate",
        "duration_minutes": 45,
        "experience": "3 years",
        "industry": "Technology",
        "position": "Backend Developer",
        "skills": ["Python", "Django", "REST APIs"]
    }
    test_endpoint(f"{BASE_URL}/api/central/api/v1/interview/start/", "POST", interview_data)
    
    # Test 5: Interview start with fake token
    print("\n" + "="*50)
    print("TEST 5: Interview Start (Fake Token)")
    fake_token = "fake_token_123"
    test_endpoint(f"{BASE_URL}/api/central/api/v1/interview/start/", "POST", interview_data, fake_token)
    
    print("\n" + "="*50)
    print("📊 Test Summary:")
    print("1. If Test 1-3 work: Basic routing is OK")
    print("2. If Test 4 works: Authentication is the issue")
    print("3. If Test 5 fails: Authentication middleware is working")
    print("4. Check Django logs for detailed error information")

if __name__ == "__main__":
    main()
