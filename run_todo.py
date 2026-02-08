#!/usr/bin/env python3
"""
Temporary script to run the todo application
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Change to the project directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    import todo_app
    todo_app.main()
except Exception as e:
    print(f"Error running todo app: {e}")
    import traceback
    traceback.print_exc()