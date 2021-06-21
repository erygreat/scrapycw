import os
import sys
import platform

pytest_plugins = "pytester"
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if platform.system() == "Windows":
    current_dir = current_dir.replace("\\", "\\\\")
sys.path.insert(0, current_dir)
