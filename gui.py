import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os
from parser import startParsing


def main():
    st.set_page_config(page_title="Stack exchange analyzer", layout="wide")

    st.sidebar.title("Actions")
    action = st.sidebar.radio(
        "Please select what you would like to do:",
        [
            "Parse XML to Parquet", 
            "Describe Tables", 
            "Cast Tables to Types", 
            "Calculate Complexity"
        ]
    )

    st.title(action)

    if action == "Parse XML to Parquet":
        if "path" not in st.session_state:
            st.session_state.path = ""
        if st.button("Select folder"):
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            st.session_state.path = filedialog.askdirectory(master=root)
            root.destroy()
                
                
        
        st.write(f"Folder to parse:{st.session_state.path}")
        if(st.session_state.path != ""):
            try:
                files = [f for f in os.listdir(st.session_state.path) if f.lower().endswith('.xml')]
                if(len(files) == 0):
                    st.error("No XML files found in this path!")
                else:
                    st.write(f"Found {len(files)} XML files.")
            except:
                st.error(f"Path not found in {st.session_state.path}!")
            
        if st.button("Start Parsing"):
            if(st.session_state.path != "" and len(files) > 0):
                with st.spinner("Parsing..."):
                    startParsing(st.session_state.path)
                    st.success("Parsing complete!")

    elif action == "Describe Tables":
        st.info("Table details")

    elif action == "Cast Tables to Types":
        st.warning("This will create new '_typed.parquet' files.")
        if st.button("Run Type Casting"):
            st.success("Casting complete.")

    elif action == "Calculate Complexity":
        st.write("Calculating complexity metrics...")
        # test()


if __name__ == "__main__":
    main()