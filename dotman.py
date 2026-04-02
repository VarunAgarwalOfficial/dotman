#!/usr/bin/env python3
"""Entry point for Dotman - imports from src and runs main."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from main import main

if __name__ == '__main__':
    main()
