# test_imports.py

import sys
import os

print("--- Testing Imports ---")
print(f"Current Working Directory: {os.getcwd()}")

try:
    # We are trying to do the same import that Uvicorn does
    from .main import app
    print("\n✅ SUCCESS: Successfully imported 'app' from 'hackrx_app.main'")
    print("Your project structure and imports are likely correct.")

except ImportError as e:
    print(f"\n❌ FAILED: Could not import from 'hackrx_app'.")
    print(f"Error Message: {e}")

    print("\n--- Python Search Paths (sys.path) ---")
    # Print the list of directories Python is searching for modules
    for path in sys.path:
        print(path)
    print("\nThis list should contain the path to your project folder:")
    print(os.getcwd())

print("\n--- Test Complete ---")