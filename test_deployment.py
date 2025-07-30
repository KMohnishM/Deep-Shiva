#!/usr/bin/env python3
"""
Test script to verify deployment setup
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        from langchain_openai import AzureChatOpenAI
        print("✅ langchain-openai imported successfully")
    except ImportError as e:
        print(f"❌ langchain-openai import failed: {e}")
        return False
    
    try:
        from langchain.prompts import ChatPromptTemplate
        print("✅ langchain prompts imported successfully")
    except ImportError as e:
        print(f"❌ langchain prompts import failed: {e}")
        return False
    
    return True

def test_environment_variables():
    """Test if environment variables are set"""
    print("\nTesting environment variables...")
    
    required_vars = [
        'OPENAI_API_VERSION',
        'AZURE_GPT_DEPLOYMENT',
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_API_KEY',
        'FLASK_SECRET_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def test_chatbot_initialization():
    """Test if chatbot can be initialized"""
    print("\nTesting chatbot initialization...")
    
    try:
        from chatbot import TourismChatbot
        chatbot = TourismChatbot()
        print("✅ Chatbot initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Chatbot initialization failed: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    print("\nTesting Flask app...")
    
    try:
        from app import app
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Deep Shiva Deployment Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_environment_variables,
        test_chatbot_initialization,
        test_flask_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your deployment should work.")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 