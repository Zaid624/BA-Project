"""
Check if the virtual environment is properly configured
"""

import os
import sys

print("=" * 60)
print("Virtual Environment Check")
print("=" * 60)

print(f"\nPython version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(
    f"Virtual environment: {'Yes' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'No'}"
)

print("\n" + "=" * 60)
print("Installed Packages")
print("=" * 60)

try:
    import psycopg2

    print(f"✓ psycopg2: {psycopg2.__version__}")
except ImportError:
    print("✗ psycopg2: NOT INSTALLED")

try:
    import dotenv

    print(f"✓ python-dotenv: installed")
except ImportError:
    print("✗ python-dotenv: NOT INSTALLED")

print("\n" + "=" * 60)
print("Environment Configuration")
print("=" * 60)

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Mask the password for security
    if "@" in DATABASE_URL:
        parts = DATABASE_URL.split("@")
        masked = parts[0].split(":")[0] + ":****@" + parts[1]
        print(f"✓ DATABASE_URL: {masked}")
    else:
        print("✓ DATABASE_URL: Set (unable to parse)")
else:
    print("✗ DATABASE_URL: NOT SET")

print("\n" + "=" * 60)
status = "READY" if DATABASE_URL else "INCOMPLETE - Set DATABASE_URL in .env"
print(f"Status: {status}")
print("=" * 60)
