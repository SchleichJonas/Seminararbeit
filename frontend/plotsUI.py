import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os
from shared.db import executeCustomQueryDF
from frontend.selector import selectFolder, selectboxWrapper
import datetime
import plotly.express as px
from shared.defines import IMPORTANTDATES
import pandas as pd


def eventSelector():
    with st.expander("Select release dates to be included in the plot", expanded=False):
        selected_map = {}
        for entry in IMPORTANTDATES.keys():
            selected_map[entry] = st.checkbox(f"{entry} - {IMPORTANTDATES.get(entry)}", value=False)
        return selected_map


def plotQuestionsAnswers():
    if "path" not in st.session_state:
        st.session_state.path = ""
    if "col" not in st.session_state:
        st.session_state.col = ""
    if "query" not in st.session_state:
        st.session_state.query = ""
    if "file" not in st.session_state:
        st.session_state.file = "Posts.parquet"
    if "dates" not in st.session_state:
        st.session_state.dates = True
    if "rolling" not in st.session_state:
        st.session_state.rolling = 30

    st.session_state.rolling = st.number_input("Rolling average range", min_value=1, max_value=1000, value=30, step=1)
    selected_map = eventSelector()
    
    if(st.session_state.path != ""):       
        if(st.session_state.file != ""):
            try:
                start_date, end_date = st.session_state.dates
                if(st.session_state.query != ""):
                    df = executeCustomQueryDF(st.session_state.query)
                    if df.empty:
                        st.warning("Query is empty")
                    else:
                        df["PostDate"] = pd.to_datetime(df["PostDate"])
                        df[f"{st.session_state.rolling} day trend"] = df["PostCount"].rolling(window=st.session_state.rolling, min_periods=1).mean()
                        fig = px.line(df, x="PostDate", y=["PostCount", f"{st.session_state.rolling} day trend"])
                        fig.data[1].line.color = 'red'
                        fig.data[1].line.width = 3
                        fig.update_xaxes(range=[pd.to_datetime(start_date), pd.to_datetime(end_date)])
                        fig.update_layout(uirevision=str(st.session_state.dates))
                        st.session_state.last_dates = st.session_state.dates
                        for event_name, event_date in IMPORTANTDATES.items():
                            if(selected_map[event_name]):
                                date_ms = pd.Timestamp(event_date).timestamp() * 1000
                                fig.add_vline(
                                    x=date_ms, 
                                    line_width=2, 
                                    line_dash="dash", 
                                    line_color="red",
                                    annotation_text=event_name, 
                                    annotation_position="top right")
                        st.plotly_chart(fig, width='stretch')
                        
                        with st.expander("Show raw data table"):
                            st.dataframe(df)

            except Exception as e:
                st.error(f"Something went wrong: {e}")


def plotTags():
    if "path" not in st.session_state:
        st.session_state.path = ""
    if "col" not in st.session_state:
        st.session_state.col = ""
    if "query" not in st.session_state:
        st.session_state.query = ""
    if "file" not in st.session_state:
        st.session_state.file = "Posts.parquet"
    if "rolling" not in st.session_state:
        st.session_state.rolling = 30
       
    selected_map = eventSelector()
    
    if(st.session_state.path != ""):
        if(st.session_state.file != ""):
            try:
                start_date, end_date = st.session_state.dates
                if(st.session_state.query != ""):
                    df = executeCustomQueryDF(st.session_state.query)
                    if df.empty:
                        st.warning("Query is empty")
                    else:
                        fig = px.line(df, x="PostDate", y="TagCount", color="TagName")
                        fig.update_traces(line_width=2)
                        fig.update_xaxes(range=[pd.to_datetime(start_date), pd.to_datetime(end_date)])
                        fig.update_layout(uirevision=str(st.session_state.dates))
                        st.session_state.last_dates = st.session_state.dates
                        for event_name, event_date in IMPORTANTDATES.items():
                            if(selected_map[event_name]):
                                date_ms = pd.Timestamp(event_date).timestamp() * 1000
                                fig.add_vline(
                                    x=date_ms, 
                                    line_width=2, 
                                    line_dash="dash", 
                                    line_color="red",
                                    annotation_text=event_name, 
                                    annotation_position="top right")
                        st.plotly_chart(fig, width='stretch')
                        
                        with st.expander("Show raw data table"):
                            st.dataframe(df)

            except Exception as e:
                st.error(f"Something went wrong: {e}")


def plotsSite():
    if "path" not in st.session_state:
        st.session_state.path = ""
    if "col" not in st.session_state:
        st.session_state.col = ""
    if "query" not in st.session_state:
        st.session_state.query = ""
    if "file" not in st.session_state:
        st.session_state.file = "Posts.parquet"
    if "dates" not in st.session_state:
        st.session_state.dates = ""
    if "rolling" not in st.session_state:
        st.session_state.rolling = 30
    if "plot" not in st.session_state:
        st.session_state.plot_index = 0
    if "tag_count" not in st.session_state:
        st.session_state.tag_count = 10
        
        
    if st.button("Select folder"):
        st.session_state.path = selectFolder()
        
    try:
        files = [f for f in os.listdir(st.session_state.path) if f.lower().endswith('.parquet')]
    except Exception as e:
        st.write(f"Something went wrong: {e}")
        
    st.session_state.dates = st.date_input("Select Timespan:",value=[datetime.date(2022, 1, 1), datetime.date(2023, 1, 1)], min_value=datetime.date(2009, 1, 1), max_value=datetime.date(2026, 1, 1))
        
    if(len(files) > 0):
        st.session_state.file = selectboxWrapper("Select the table you want to plot something of:", files, st.session_state.file)
        
    
    filepath = os.path.join(st.session_state.path, st.session_state.file)
    queries = [f"SELECT CAST(CreationDate AS DATE) AS PostDate, COUNT(*) AS PostCount FROM '{filepath}' WHERE PostTypeId = 1 GROUP BY PostDate ORDER BY PostDate",
               f"SELECT CAST(CreationDate AS DATE) AS PostDate, COUNT(*) AS PostCount FROM '{filepath}' WHERE PostTypeId = 2 GROUP BY PostDate ORDER BY PostDate",
               f"WITH TopTags AS (SELECT tag FROM (SELECT unnest(string_split(trim(Tags, '<>'), '><')) AS tag FROM '{filepath}' WHERE PostTypeId = 1 AND Tags IS NOT NULL) GROUP BY tag ORDER BY COUNT(*) DESC LIMIT 10),MonthlyTags AS (SELECT date_trunc('month', CreationDate) AS PostMonth,unnest(string_split(trim(Tags, '<>'), '><')) AS tag FROM '{filepath}'WHERE PostTypeId = 1 AND Tags IS NOT NULL)SELECT CAST(PostMonth AS DATE) AS PostDate, tag AS TagName,COUNT(*) AS TagCount FROM MonthlyTags WHERE tag IN (SELECT tag FROM TopTags) GROUP BY PostDate, TagName ORDER BY PostDate"
               ]
    plots = [f"Question count over time",
             f"Answer count over time",
             f"Top {st.session_state.tag_count} tags usage over time"
                ]
    selected_plot = selectboxWrapper("Select a predefined plot:", plots, "")
    st.session_state.plot_index = plots.index(selected_plot)
    
    st.session_state.query = queries[st.session_state.plot_index]

    if(st.session_state.plot_index == 0 or st.session_state.plot_index == 1):
        plotQuestionsAnswers()
    elif(st.session_state.plot_index == 2):
        plotTags()
        