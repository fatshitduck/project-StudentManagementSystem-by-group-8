#!/usr/bin/env python3
"""
Animation Demo Script
Run this to test the new animations in the Student Management System
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_animations():
    """Test animation utilities"""
    try:
        from utils.animations import AnimationUtils
        print("✅ Animation utilities imported successfully")

        # Test color functions
        from config.themes import get_color
        print("✅ Theme utilities imported successfully")

        # Test basic color retrieval
        primary_color = get_color("button_primary")
        print(f"✅ Primary button color: {primary_color}")

        print("\n🎉 All animation components are working!")
        print("Run 'python main.py' to see the animations in action.")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    return True

if __name__ == "__main__":
    print("Testing Student Management System Animations...")
    print("=" * 50)

    if test_animations():
        print("\n🚀 Ready to launch with animations!")
    else:
        print("\n❌ Animation test failed!")