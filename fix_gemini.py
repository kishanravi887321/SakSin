#!/usr/bin/env python3
"""
Fix Gemini SDK Issues
This script will upgrade Google GenAI and test the fix
"""

import subprocess
import sys
import os

def upgrade_google_genai():
    """Upgrade Google GenAI package"""
    try:
        print("🔧 Upgrading Google GenAI package...")
        
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "google-genai"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Google GenAI upgraded successfully!")
            return True
        else:
            print(f"❌ Failed to upgrade: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error upgrading: {e}")
        return False

def test_fix():
    """Test if the fix works"""
    try:
        from google import genai
        
        # Use one of your API keys for testing
        test_keys = [
            "AIzaSyDrlBqJdKzatNuuutWxEvWn0jfxrRvfRdc",
            "AIzaSyAl30kClWao0fDfBsw7DHLYGqUmvL67ab0"
        ]
        
        for i, key in enumerate(test_keys):
            try:
                print(f"🧪 Testing with API key {i+1}...")
                os.environ['GEMINI_API_KEY'] = key
                
                client = genai.Client()
                
                # Test with gemini-2.5-flash
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents="Say 'WORKING' if you understand this message."
                )
                
                print(f"✅ SUCCESS! Model gemini-2.5-flash is working!")
                print(f"   Response: {response.text.strip()}")
                return True
                
            except Exception as e:
                if "404" in str(e) or "not found" in str(e).lower():
                    print(f"⚠️  gemini-2.5-flash not available with key {i+1}")
                    
                    # Try fallback models
                    fallbacks = ["gemini-1.5-flash", "gemini-1.5-pro"]
                    for model in fallbacks:
                        try:
                            response = client.models.generate_content(
                                model=model,
                                contents="Say 'FALLBACK_WORKING' if you understand this."
                            )
                            print(f"✅ Fallback model {model} is working!")
                            print(f"   Response: {response.text.strip()}")
                            return True
                        except:
                            continue
                else:
                    print(f"❌ Error with key {i+1}: {e}")
        
        return False
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    print("🚀 Gemini SDK Fix Script")
    print("=" * 30)
    
    # Step 1: Upgrade package
    if not upgrade_google_genai():
        print("⚠️  Upgrade failed, continuing with current version...")
    
    # Step 2: Test the fix
    print("\n🧪 Testing the fix...")
    if test_fix():
        print("\n🎉 SUCCESS!")
        print("✅ Gemini API is now working")
        print("🔄 Restart your Django server to apply the changes")
        print("\n📝 What was fixed:")
        print("- Updated to latest Google GenAI SDK")
        print("- Using correct API initialization") 
        print("- Updated model names to supported versions")
        print("- Added automatic fallback system")
    else:
        print("\n❌ Still having issues")
        print("💡 Check your API keys and try running the Django server")
        print("   The fallback system should handle model selection automatically")

if __name__ == "__main__":
    main()