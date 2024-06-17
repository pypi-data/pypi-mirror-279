"""Helper codes snippets"""
# -*- coding: utf-8 -*-
# @author Ratnadip Adhikari

# ================================================
# Helper codes snippets -- Leoforce
# ================================================
import sys, os, json
from importlib import reload, import_module
from IPython.core.display import display

# Save 'requirements.txt'
"""
subprocess.run('pipreqs --force .')
display('INFO: Successfully saved requirements file in .\\requirements.txt')
os.system('pipreqs --force . >/dev/null 2>&1')  # save 'requirements.txt' in the script directory
$ `sort-requirements requirements.txt`
https://stackoverflow.com/questions/58737741/how-to-list-all-python-packages-used-by-a-script-in-python3"""

# Load and reseting everything through magic commands
"""
%load <script>.py
%reset -f
%run <script>.py"""

# Install venv in MacOS
"""
$ /opt/homebrew/bin/python3.10 -m venv .venv_ratnadip_p3.10
$ python -m ipykernel install --user --name=.venv_ratnadip_p3.10
$ brew install python-tk"""