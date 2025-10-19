#!/usr/bin/env python3
"""
Test script for the Stage 0 Profile API
Run this after starting your server to verify all endpoints work correctly
"""

import requests
import json
from datetime import datetime
import sys

# Configuration
BASE_URL = "http://localhost:8000"  # Change to your deployed URL for production testing

def test_endpoint(name, url, expected_status=200):
    """Test a single endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        
        if response.status_code == expected_status:
            print("✅ Status code matches expected")
        else:
            print(f"❌ Expected {expected_status}, got {response.status_code}")
            return False
        
        # Pretty print JSON response
        try:
            data = response.json()
            print(f"\nResponse Body:")
            print(json.dumps(data, indent=2))
            return data
        except json.JSONDecodeError:
            print(f"❌ Response is not valid JSON")
            print(f"Raw response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def validate_me_endpoint(data):
    """Validate the /me endpoint response structure"""
    print(f"\n{'='*60}")
    print("Validating /me endpoint response...")
    print(f"{'='*60}")
    
    checks = []
    
    # Check status field
    if data.get("status") == "success":
        print("✅ status field is 'success'")
        checks.append(True)
    else:
        print(f"❌ status field is '{data.get('status')}', expected 'success'")
        checks.append(False)
    
    # Check user object
    user = data.get("user", {})
    if isinstance(user, dict):
        print("✅ user field is an object")
        checks.append(True)
        
        # Check user.email
        if user.get("email") and isinstance(user.get("email"), str):
            print(f"✅ user.email exists: {user.get('email')}")
            checks.append(True)
        else:
            print("❌ user.email is missing or not a string")
            checks.append(False)
        
        # Check user.name
        if user.get("name") and isinstance(user.get("name"), str):
            print(f"✅ user.name exists: {user.get('name')}")
            checks.append(True)
        else:
            print("❌ user.name is missing or not a string")
            checks.append(False)
        
        # Check user.stack
        if user.get("stack") and isinstance(user.get("stack"), str):
            print(f"✅ user.stack exists: {user.get('stack')}")
            checks.append(True)
        else:
            print("❌ user.stack is missing or not a string")
            checks.append(False)
    else:
        print("❌ user field is not an object")
        checks.append(False)
    
    # Check timestamp
    timestamp = data.get("timestamp")
    if timestamp:
        print(f"✅ timestamp field exists: {timestamp}")
        try:
            # Validate ISO 8601 format
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            print("✅ timestamp is in valid ISO 8601 format")
            checks.append(True)
        except ValueError:
            print("❌ timestamp is not in valid ISO 8601 format")
            checks.append(False)
    else:
        print("❌ timestamp field is missing")
        checks.append(False)
    
    # Check fact
    fact = data.get("fact")
    if fact and isinstance(fact, str):
        print(f"✅ fact field exists: {fact[:50]}...")
        checks.append(True)
    else:
        print("❌ fact field is missing or not a string")
        checks.append(False)
    
    return all(checks)

def test_dynamic_updates():
    """Test that timestamp and fact update on each request"""
    print(f"\n{'='*60}")
    print("Testing dynamic updates (timestamp and fact)...")
    print(f"{'='*60}")
    
    url = f"{BASE_URL}/me"
    
    # First request
    response1 = requests.get(url)
    data1 = response1.json()
    timestamp1 = data1.get("timestamp")
    fact1 = data1.get("fact")
    
    print(f"Request 1 - Timestamp: {timestamp1}")
    print(f"Request 1 - Fact: {fact1[:50]}...")
    
    # Wait a moment
    import time
    time.sleep(2)
    
    # Second request
    response2 = requests.get(url)
    data2 = response2.json()
    timestamp2 = data2.get("timestamp")
    fact2 = data2.get("fact")
    
    print(f"\nRequest 2 - Timestamp: {timestamp2}")
    print(f"Request 2 - Fact: {fact2[:50]}...")
    
    # Validate timestamps are different
    if timestamp1 != timestamp2:
        print("\n✅ Timestamps are updating dynamically")
    else:
        print("\n❌ Timestamps are not updating (they should be different)")
    
    # Note: Facts might occasionally be the same by chance
    if fact1 != fact2:
        print("✅ Cat facts are updating dynamically")
    else:
        print("⚠️  Cat facts are the same (might be coincidence)")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("STAGE 0 API TEST SUITE")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Note: Make sure your server is running before running this script!")
    print("="*60)
    
    # Test root endpoint
    test_endpoint("Root Endpoint", f"{BASE_URL}/")
    
    # Test health endpoint
    test_endpoint("Health Check", f"{BASE_URL}/health")
    
    # Test /me endpoint
    me_data = test_endpoint("Profile Endpoint (/me)", f"{BASE_URL}/me")
    
    if me_data:
        # Validate /me response structure
        validation_passed = validate_me_endpoint(me_data)
        
        if validation_passed:
            print(f"\n{'='*60}")
            print("✅ ALL VALIDATION CHECKS PASSED!")
            print(f"{'='*60}")
            
            # Test dynamic updates
            test_dynamic_updates()
        else:
            print(f"\n{'='*60}")
            print("❌ SOME VALIDATION CHECKS FAILED")
            print(f"{'='*60}")
            sys.exit(1)
    else:
        print(f"\n{'='*60}")
        print("❌ FAILED TO GET RESPONSE FROM /me ENDPOINT")
        print(f"{'='*60}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("TEST SUITE COMPLETED SUCCESSFULLY!")
    print(f"{'='*60}")
    print("\nYour API is ready for submission!")
    print("Remember to:")
    print("1. Deploy to Railway (or your chosen platform)")
    print("2. Test from multiple networks")
    print("3. Update your .env with correct information")
    print("4. Create your LinkedIn/Dev.to post")
    print("5. Submit using /stage-zero-backend in Slack")

if __name__ == "__main__":
    # Allow custom URL via command line
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1].rstrip('/')
    
    main()
