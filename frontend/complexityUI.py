import streamlit as st
import os
from backend.complexity import calculateComplexity
from shared.db import executeCustomQueryDF
from frontend.selector import selectFolder, selectboxWrapper

def complexitySite():
    """
    Provides the webpage to compute complexity of a table
    """  
    if "path" not in st.session_state:
        st.session_state.path = ""
    if "col" not in st.session_state:
        st.session_state.col = ""
        
    st.session_state.file = ""
        
    if st.button("Select folder"):
        st.session_state.path = st.session_state.path = selectFolder()
        
    st.write(f"Folder to parse:{st.session_state.path}")
        
    if(st.session_state.path != ""):
        try:
            files = [f for f in os.listdir(st.session_state.path) if f.lower().endswith('.parquet') and "_typed" in f and not "_complexity" in f]
        except Exception as e:
            st.write("Path error")
            
        if(len(files) > 0):
            st.session_state.file = selectboxWrapper("Select the table you want to compute the complexity of:", files, st.session_state.file)
        else:
            st.error("Found no parquet files in this directory")
        
        if(st.session_state.file != ""):
            try:
                file_path = os.path.join(st.session_state.path, st.session_state.file)
                cols = executeCustomQueryDF(f"DESCRIBE SELECT * FROM '{file_path}'")['column_name']
                st.session_state.col = selectboxWrapper("Select the column for complexity compution", cols, "Body")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                
    if st.button("Compute complexity"):
        if(st.session_state.path != "" and len(files) > 0 and st.session_state.file != ""):
            with st.spinner("Computing complexity..."):
                calculateComplexity(True, st.session_state.path, st.session_state.file, st.session_state.col)
                st.success("Casting complete.")
                st.subheader(f"First 10 rows of `{file_path[:-8]}_complexity.parquet`")
                preview_df = executeCustomQueryDF(f"SELECT * FROM '{file_path[:-8]}_complexity.parquet' LIMIT 10")
                st.dataframe(preview_df) 
        else:
            st.info("Please first select a directory with parquet files.")