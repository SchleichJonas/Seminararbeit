import sys
import subprocess
import streamlit as st


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


def selectboxWrapper(text, items, default):
    try:
        result = st.selectbox(f"{text}:", items, index=items.index(default))
    except Exception as e:
        result = st.selectbox(f"{text}:", items)
    return result