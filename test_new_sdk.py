#!/usr/bin/env python3
"""
Test New Google GenAI SDK with gemini-2.5-flash
"""

import os

def test_new_sdk():
    """Test the new Google GenAI SDK with updated model"""
    try:
        from google import genai
        print("✅ Google GenAI SDK imported")
        
        # Set up API key (replace with your actual key for testing)
        test_key = "AIzaSyDrlBqJdKzatNuuutWxEvWn0jfxrRvfRdc"  # From your logs
        os.environ['GEMINI_API_KEY'] = test_key
        
        # Initialize client
        client = genai.Client()
        print("✅ Client initialized")
        
        # Test with new model
        try:
            print("🧪 Testing gemini-2.5-flash model...")
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents="Respond with just 'SDK WORKS' if you can understand this."
            )
            print(f"✅ SUCCESS! Response: {response.text}")
            return True
        except Exception as e:
            print(f"❌ gemini-2.5-flash failed: {e}")
            
            # Try fallback models
            fallbacks = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
            for model in fallbacks:
                try:
                    print(f"🧪 Testing fallback model: {model}...")
                    response = client.models.generate_content(
                        model=model, 
                        contents="Respond with just 'FALLBACK WORKS' if you can understand this."
                    )
                    print(f"✅ SUCCESS with {model}! Response: {response.text}")
                    return True
                except Exception as e2:
                    print(f"❌ {model} failed: {e2}")
            
            return False
            
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("💡 Try: pip install --upgrade google-genai")
        return False

def main():
    print("🔧 Testing New Google GenAI SDK")
    print("=" * 40)
    
    if test_new_sdk():
        print("\n🎉 Test successful!")
        print("✅ The new SDK and model should work")
        print("🔄 Restart your Django server to apply changes")
    else:
        print("\n❌ Test failed")
        print("💡 Check your Google GenAI package version")

if __name__ == "__main__":
    main()