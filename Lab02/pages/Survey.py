# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

if "session_started" not in st.session_state:
    outfile = open("data.csv", "w")
    outfile.write("Day,Minutes\n")
    outfile.close()
    st.session_state.session_started = True


# PAGE TITLE AND USER DIRECTIONS
st.title("Physical Activty Tracker 📝")
st.write("Log your physical activity by entering the day and minutes of your last time you exercised during the week!")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    category_input = st.selectbox("What day did you exercise?", days)
    
    value_input = st.slider("How Many minutes did you exercise?", 0, 120)

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
     # --- YOUR LOGIC GOES HERE ---
    if submitted:
        if category_input and value_input:
            outfile = open("data.csv","a")
            outfile.write(f'{category_input},{value_input}\n')
            outfile.close()
        
        elif value_input == 0:
            st.warning("You logged 0 minutes today — everyone deserves a rest day!")
            outfile = open("data.csv","a")
            outfile.write(f'{category_input},{value_input}\n')
            outfile.close()

        else:
            st.warning("Please enter both entries!")
        
        st.success("Your data has been submitted!")
        st.write(f"You entered: **Day:** {category_input}, **Minutes:** {value_input}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
