import sys
import os
import pandas as pd

# Add current directory to path
sys.path.append(os.getcwd())

from app import analyze_bias

class MockFile:
    def __init__(self, path):
        self.path = path
        self.file = open(path, 'rb')
    def seek(self, pos):
        self.file.seek(pos)
    def read(self, *args):
        return self.file.read(*args)
    def __getattr__(self, name):
        return getattr(self.file, name)

try:
    # Test with data.csv
    print("Testing with data.csv...")
    result = analyze_bias(MockFile('data.csv'))
    print("Result:", result)
    
    # Test with clean.csv
    print("\nTesting with clean.csv...")
    result_clean = analyze_bias(MockFile('clean.csv'))
    print("Result:", result_clean)
    
    if "error" in result:
        print("❌ Failed: Error in result")
    else:
        print("✅ Success: No errors found")
except Exception as e:
    print(f"❌ Failed with exception: {e}")
