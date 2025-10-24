#!/usr/bin/env python3
"""
Generative Art Studio - Entry Point

A Python application for creating computer-generated art through
various algorithmic methods.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import main

if __name__ == '__main__':
    main()
