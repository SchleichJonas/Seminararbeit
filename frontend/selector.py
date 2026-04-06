import sys
import subprocess
import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os


def selectFolder():
    tkinter_script = """
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
root.wm_attributes('-topmost', 1)
path = filedialog.askdirectory(master=root)
print(path)
"""
    
    result = subprocess.run(
                [sys.executable, "-c", tkinter_script], 
                capture_output=True, 
                text=True
            )
    path = result.stdout.strip()
    return path