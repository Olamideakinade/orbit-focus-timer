"""
Orbit Focus Timer - Entry Point
"""
import sys
import os

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ui import OrbitApp

def main():
    app = OrbitApp()
    app.run()

if __name__ == "__main":
    main()
