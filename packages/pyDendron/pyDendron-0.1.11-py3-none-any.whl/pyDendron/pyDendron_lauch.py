#!/usr/bin/env python
#encoding: utf-8

import subprocess
import sys

from pyDendron import pyDendron_panel

def lauch():
    try:
            subprocess.run([
                sys.executable, "-m", "panel", "serve", pyDendron_panel.__file__, "--show", "--autoreload"])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

