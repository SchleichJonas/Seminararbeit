import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os
from parser import startParsing
from main import executeCustomQueryDF, get_connection
from castingTables import CastToCorrectTypes


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
        if "path" not in st.session_state:
            st.session_state.path = ""
        if "file" not in st.session_state:
            st.session_state.file = ""
            
        if st.button("Select folder"):
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            st.session_state.path = filedialog.askdirectory(master=root)
            root.destroy()
            
            
        if(st.session_state.path != ""):
            try:
                files = [f for f in os.listdir(st.session_state.path) if f.lower().endswith('.parquet')]
                if(len(files) == 0):
                    st.error("Found no parquet files in this directory")
            except:
                st.write("Path error")
                
            if(len(files) > 0):
                try:
                    st.session_state.file = st.selectbox("Select a table to describe:", files, index=files.index(st.session_state.file))
                except:
                    st.session_state.file = st.selectbox("Select a table to describe:", files)

                if st.session_state.file:
                    file_path = os.path.join(st.session_state.path, st.session_state.file)
                    
                    st.subheader(f"Description for `{st.session_state.file}`")
                    
                    try:
                        description = executeCustomQueryDF(f"DESCRIBE SELECT * FROM '{file_path}'")
                        st.dataframe(description, use_container_width=True)

                        st.subheader(f"First 5 rows of `{st.session_state.file}`")
                        preview_df = executeCustomQueryDF(f"SELECT * FROM '{file_path}' LIMIT 5")
                        st.dataframe(preview_df) 

                    except Exception as e:
                        st.error(f"Failed to describe table!")

    elif action == "Cast Tables to Types":
        st.warning("This will create new '_typed.parquet' files.")
        if "path" not in st.session_state:
            st.session_state.path = ""
        if st.button("Select folder"):
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            st.session_state.path = filedialog.askdirectory(master=root)
            root.destroy()
                

        st.write(f"Folder to convert:{st.session_state.path}")
        
        
        if(st.session_state.path != ""):
            try:
                files = [f for f in os.listdir(st.session_state.path) if f.lower().endswith('.parquet') and not "_typed" in f]
                if(len(files) == 0):
                    st.error("Found no parquet files in this directory")
            except:
                st.write("Path error")
                
        con = get_connection()
        
        if(st.session_state.path != "" and len(files) > 0):                
                with st.expander("Select files to cast", expanded=True):
                    selected_map = {}
                    for f in files:
                        selected_map[f] = st.checkbox(f"Cast {f}", value=True)

                files_to_cast = [f for f, checked in selected_map.items() if checked]
        
        if st.button("Run Type Casting"):
            if(st.session_state.path != "" and len(files) > 0):
                CastToCorrectTypes(con, st.session_state.path, files_to_cast)
            st.success("Casting complete.")
            
        

    elif action == "Calculate Complexity":
        st.write("Calculating complexity metrics...")
        # test()


if __name__ == "__main__":
    main()