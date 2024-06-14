#!/usr/bin/env python
#encoding: utf-8

import subprocess
import sys
import os
#from importlib.resources import as_file, files, path

from pyDendron import pyDendron_panel

def main():
    try:
        # if os.path.isdir(os.path.join(os.path.dirname(__file__), 'pyDendron')):
        #     # Si pyDendron n'est pas trouvé, ajoute le répertoire source au PYTHONPATH
        #     current_dir = os.path.dirname(os.path.abspath(__file__))
        #     parent_dir = os.path.dirname(current_dir)
        #     os.environ['PYTHONPATH'] = parent_dir + os.pathsep + os.environ.get('PYTHONPATH', '')
        #     print(f"PYTHONPATH: {os.environ['PYTHONPATH']}")
                
        #from pyDendron import pyDendron_panel
        
        #with as_file(files('pyDendron').joinpath('pyDendronPanel.py')) as panel_script:
        #    print("file:", str(panel_script))
        #    subprocess.run([
        #        sys.executable, "-m", "panel", "serve", pyDendron_panel.__file__, "--show", "--admin", "--autoreload"
        #    ], env=os.environ)
            subprocess.run([
                sys.executable, "-m", "panel", "serve", pyDendron_panel.__file__, "--show", "--admin", "--autoreload"])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
