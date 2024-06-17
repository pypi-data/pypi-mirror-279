#!/usr/bin/env python
#encoding: utf-8

import subprocess
import sys
import os
#from importlib.resources import as_file, files, path

from pyDendron import pyDendron_panel

def main():
    try:
            subprocess.run([
                sys.executable, "-m", "panel", "serve", pyDendron_panel.__file__, "--show", "--admin", "--autoreload"])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
