#!/usr/bin/env python3
"""
Hourly heat decay updater
Run via cron: 0 * * * * /path/to/update_heat_decay.py
"""

import sys
import os

# Add skill scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from content_heat_manager import HeatManager
from datetime import datetime

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Updating heat decay...")
    
    # Initialize with default cache
    manager = HeatManager()
    
    # Update all cached entries
    updated = manager.update_time_decay()
    
    print(f"✅ Updated {updated} cached articles")
    
    # Show distribution
    stats = manager.get_heat_distribution()
    print(f"📊 Current distribution: {stats}")

if __name__ == "__main__":
    main()
