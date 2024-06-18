
import sys
import subprocess
import argparse

from pyDendron import pyDendron_panel

try:
    parser = argparse.ArgumentParser(description="pydenron: A dendrochronology tool for tree-ring data analysis.")
    parser.add_argument('--www', action='store_true', help='A flag to enable www mode')

    args = parser.parse_args()
    if args.www:
        subprocess.run([
            sys.executable, "-m", "panel", "serve", "--show", "--autoreload", pyDendron_panel.__file__, "--args", "--www"])
    else:
        subprocess.run([
            sys.executable, "-m", "panel", "serve", "--show", "--autoreload", pyDendron_panel.__file__])
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

