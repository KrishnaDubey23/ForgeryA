#!/usr/bin/env python3
"""
Startup check script to verify all dependencies and configurations are correct.
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def check_environment():
    """Check if all environment variables are set"""
    print("=" * 60)
    print("CHECKING ENVIRONMENT CONFIGURATION")
    print("=" * 60)
    
    required_env_vars = [
        "CONVEX_URL",
        "SECRET_KEY",
        "ALGORITHM",
    ]
    
    missing = []
    for var in required_env_vars:
        val = os.getenv(var)
        if val:
            print(f"✓ {var}: {val[:50]}..." if len(val) > 50 else f"✓ {var}: {val}")
        else:
            print(f"✗ {var}: NOT SET")
            missing.append(var)
    
    return len(missing) == 0

def check_imports():
    """Check if all required packages can be imported"""
    print("\n" + "=" * 60)
    print("CHECKING PYTHON IMPORTS")
    print("=" * 60)
    
    packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "passlib",
        "jwt",
        "httpx",
        "dotenv",
        "pillow",
        "cv2",
        "numpy",
        "torch",
    ]
    
    missing = []
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"✓ {pkg}")
        except ImportError as e:
            print(f"✗ {pkg}: {e}")
            missing.append(pkg)
    
    return len(missing) == 0

def check_convex():
    """Check if Convex client can be initialized"""
    print("\n" + "=" * 60)
    print("CHECKING CONVEX CONNECTION")
    print("=" * 60)
    
    try:
        from convex_client import ConvexClient
        client = ConvexClient()
        print(f"✓ Convex client initialized")
        print(f"  Deployment URL: {client.deployment_url}")
        return True
    except Exception as e:
        print(f"✗ Convex client error: {e}")
        return False

def check_routers():
    """Check if all routers can be imported"""
    print("\n" + "=" * 60)
    print("CHECKING ROUTERS")
    print("=" * 60)
    
    try:
        from routers import auth
        print(f"✓ auth router")
        from routers import uploads
        print(f"✓ uploads router")
        from routers import predictions
        print(f"✓ predictions router")
        from routers import admin
        print(f"✓ admin router")
        return True
    except Exception as e:
        print(f"✗ Router import error: {e}")
        return False

def main():
    print("\n")
    print("█" * 60)
    print("█  AADHAAR FORGERY DETECTION - STARTUP CHECK")
    print("█" * 60)
    print()
    
    checks = [
        ("Environment", check_environment),
        ("Imports", check_imports),
        ("Routers", check_routers),
        ("Convex", check_convex),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n✗ {name} check failed with exception: {e}")
            results[name] = False
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All checks passed! Backend should be ready to start.")
        print("\nRun: python main.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
