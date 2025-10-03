#!/usr/bin/env python3
"""
Install Google GenAI Package
This will install the new google-genai package for the updated integration
"""

import subprocess
import sys
import os

def install_package():
    """Install google-genai package"""
    try:
        print("🔧 Installing google-genai package...")
        
        # Try to install the package
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "google-genai==0.5.2"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Successfully installed google-genai!")
            print(result.stdout)
            return True
        else:
            print(f"❌ Failed to install google-genai:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing package: {e}")
        return False

def verify_installation():
    """Verify the installation works"""
    try:
        from google import genai
        print("✅ Google GenAI package verified!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def main():
    print("🚀 Google GenAI Installation Script")
    print("=" * 40)
    
    # First check if already installed
    try:
        from google import genai
        print("✅ google-genai is already installed!")
        return True
    except ImportError:
        print("📦 google-genai not found, installing...")
    
    # Install the package
    if install_package():
        # Verify it works
        if verify_installation():
            print("\n🎉 Installation complete!")
            print("\n🔧 Next steps:")
            print("1. Restart your Django server")
            print("2. Test your API endpoints")
            print("3. You should now see improved performance with the new SDK!")
            return True
        else:
            print("\n❌ Installation completed but verification failed")
            print("💡 Try restarting your Python environment")
            return False
    else:
        print("\n❌ Installation failed")
        print("💡 Try running manually: pip install google-genai")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n🔄 Fallback: The code will use LangChain integration if google-genai is not available")
    sys.exit(0 if success else 1)