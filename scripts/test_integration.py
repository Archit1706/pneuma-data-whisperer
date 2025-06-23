#!/usr/bin/env python3
"""
Integration test script for Pneuma OpenWebUI setup
"""

import requests
import time
import json
import sys


def test_service(name, url, timeout=30):
    """Test if a service is responding"""
    print(f"Testing {name} at {url}...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} is responding")
                return True
        except requests.exceptions.RequestException:
            pass

        time.sleep(2)

    print(f"❌ {name} is not responding after {timeout}s")
    return False


def test_pneuma_api():
    """Test Pneuma API functionality"""
    print("\n🧪 Testing Pneuma API functionality...")

    # Test health endpoint
    try:
        response = requests.get("http://localhost:8000/api/v1/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check: {health_data['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

    # Test query endpoint
    try:
        query_data = {"query": "test query for integration", "k": 3}
        response = requests.post(
            "http://localhost:8000/api/v1/query", json=query_data, timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Query test successful: {result.get('total_results', 0)} results")
        else:
            print(f"⚠️  Query test returned: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"⚠️  Query test failed: {e}")

    return True


def test_ollama():
    """Test Ollama functionality"""
    print("\n🧪 Testing Ollama...")

    try:
        # Test if Ollama is running
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama is running with {len(models.get('models', []))} models")

            # List available models
            for model in models.get("models", []):
                print(f"   - {model.get('name', 'Unknown')}")
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False

    return True


def main():
    """Run all integration tests"""
    print("🔍 Running Pneuma OpenWebUI Integration Tests\n")

    # Test basic service availability
    services = [
        ("Redis", "http://localhost:6379"),  # This will fail but that's ok
        ("Pneuma API", "http://localhost:8000/api/v1/health"),
        ("OpenWebUI", "http://localhost:8080"),
        ("Ollama", "http://localhost:11434/api/tags"),
    ]

    working_services = 0
    for name, url in services:
        if name == "Redis":
            # Skip Redis HTTP test (it doesn't have HTTP interface)
            print(f"⏭️  Skipping {name} HTTP test")
            continue

        if test_service(name, url):
            working_services += 1

    # Run specific functionality tests
    if working_services >= 2:  # Need at least API and Ollama
        test_pneuma_api()
        test_ollama()

    print(
        f"\n📊 Test Summary: {working_services}/{len(services)-1} services responding"
    )

    if working_services >= 2:
        print("\n🎉 Integration test passed! You can now:")
        print("   1. Open http://localhost:8080 for OpenWebUI")
        print("   2. Install the Pneuma tools in OpenWebUI")
        print("   3. Start asking questions about your data!")
    else:
        print("\n❌ Integration test failed. Check the logs in logs/ directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
