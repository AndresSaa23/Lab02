# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Training Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

try:
    infile = open("Lab02/data.json")
    json_data = json.load(infile)
    infile.close()
    st.success("JSON data loaded successfully!")
except FileNotFoundError:
    st.warning("data.json not found?!")
    json_data = {}
except:
    st.error("Error Reading the data")
    json_data = {}


try:
    df = pd.read_csv("data.csv")
    st.success("Training data loaded successfully!")
    st.write(df)
except FileNotFoundError:
    st.warning("data.csv not found?!")
    df = pd.DataFrame()
except:
    st.error("Error Reading the data")
    df = pd.DataFrame()



# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: DYNAMIC GRAPH With CSV
st.subheader("Minutes Exercised per Day") # CHANGE THIS TO THE TITLE OF YOUR GRAPH

if not df.empty:
    min_minutes = st.slider("Minimum Minutes exercised",0,120,0)#NEW

    days = st.multiselect( #NEW
        "Select days to include",
        options = df["Day"].unique(),
        default = df["Day"].unique())

    
    if "filtered_df" not in st.session_state:
        st.session_state.filtered_df = df  


    filtered = df[
        (df["Minutes"] >= min_minutes) &
        (df["Day"].isin(days))
    ]

    
    st.session_state.filtered_df = filtered  


    grouped = filtered.groupby("Day")["Minutes"].sum().reset_index()

    if not grouped.empty:
        grouped = filtered.groupby("Day")["Minutes"].sum()

        order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        grouped = grouped.reindex(order).dropna()

        st.scatter_chart(grouped)#NEW
        st.write("This graph shows a dot plot and you can filter by days and also by minutes")
    else:
        st.warning("The data doesn't match the filters")

# GRAPH 2: DYNAMIC PIE GRAPH With CSV 
st.subheader("Daily Exercise Chart") # CHANGE THIS TO THE TITLE OF YOUR GRAPH

if not df.empty:

    chart_type = st.radio("Select chart type", ["Bar", "Line"])#NEW 

    selected_day = st.selectbox("Highlight a specific day", ["All"] + list(df["Day"].unique())) #NEW

    if "chart_type_g2" not in st.session_state:  
        st.session_state.chart_type_g2 = chart_type  

    if "selected_day" not in st.session_state:  
        st.session_state.selected_day = selected_day  

    st.session_state.chart_type_g2 = chart_type  
    st.session_state.selected_day = selected_day  

    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if selected_day == "All":
        graph_df = df.groupby("Day")["Minutes"].sum()
        graph_df = graph_df.reindex(order).dropna()
    else:
        graph_df = df[df["Day"] == selected_day].set_index("Day")["Minutes"]

    if chart_type == "Bar":
        st.bar_chart(graph_df)
    else:
        st.line_chart(graph_df)

    st.write("This graph allows you to switch between type of graph and also to select which day to focus on")


# GRAPH 3: Static GRAPH With JSON
st.subheader("Weekly Exercise Vs Heart Disease Risk Reduction (%)")

if json_data:
    json_df = pd.DataFrame(json_data["data_points"])
    json_df["Minutes"] = json_df["Minutes"].astype(int) 
    json_df = json_df.sort_values("Minutes")
    
    st.line_chart(
        json_df.set_index("Minutes")["Percentage"],
        x_label = "Minutes Exerciced",
        y_label = "Heart Disease Reduction (%)",
    )
    
    st.caption(f"Source: {json_data['source']}")
    st.write("This graph shows how working out more minutes per week allows for reduced Heart Disease")
