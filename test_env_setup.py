#!/usr/bin/env python3
"""
Test script to verify .env setup is working correctly.
"""

import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    
    # Look for .env file in project root
    project_root = Path(__file__).parent
    env_file = project_root / ".env"
    
    print("🔍 Checking .env setup...")
    print(f"   Looking for .env file at: {env_file}")
    
    if env_file.exists():
        load_dotenv(env_file)
        print("✅ .env file found and loaded")
    else:
        print("❌ .env file not found")
        print("   Create one by copying .env.example")
        
except ImportError:
    print("❌ python-dotenv not installed")
    print("   Install with: pip install python-dotenv")

# Check environment variables
print("\n🔐 Checking API keys...")

anthropic_key = os.getenv('ANTHROPIC_API_KEY')
openai_key = os.getenv('OPENAI_API_KEY')

if anthropic_key:
    print(f"✅ ANTHROPIC_API_KEY: {anthropic_key[:10]}...{anthropic_key[-4:] if len(anthropic_key) > 14 else 'too short'}")
else:
    print("❌ ANTHROPIC_API_KEY: Not set")

if openai_key:
    print(f"✅ OPENAI_API_KEY: {openai_key[:10]}...{openai_key[-4:] if len(openai_key) > 14 else 'too short'}")
else:
    print("❌ OPENAI_API_KEY: Not set")

# Check other optional variables
debug_mode = os.getenv('LANGTOOLS_DEBUG', 'true').lower() == 'true'
default_model = os.getenv('LANGTOOLS_DEFAULT_MODEL', 'claude-3-5-sonnet-20241022')

print(f"\n⚙️  Configuration:")
print(f"   Debug mode: {debug_mode}")
print(f"   Default model: {default_model}")

# Summary
if anthropic_key or openai_key:
    print("\n🎉 Environment setup looks good!")
    print("   Ready to run integration tests")
else:
    print("\n⚠️  No API keys configured")
    print("   Edit .env file to add your API keys")
    print("   At least one of ANTHROPIC_API_KEY or OPENAI_API_KEY is required")