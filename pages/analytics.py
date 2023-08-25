import streamlit as st

import pandas as pd

# Sidebar
st.sidebar.title("Select Data Type")
data_type = st.sidebar.radio("Choose Data Type", ("Symptom", "Activity", "Medication"))

# Display selected data
st.title(f"{data_type} Data")

if data_type == "Symptom":
    data = st.session_state.Symptom
elif data_type == "Activity":
    data = st.session_state.Activity
else:
    data = st.session_state.Medication

# Display the data in a table
df = pd.DataFrame(data)
st.dataframe(df)

# Filter data by date
# st.sidebar.title("Filter by Date")
# start_date = st.sidebar.date_input("Start Date")
# end_date = st.sidebar.date_input("End Date")
#
# if start_date and end_date:
#     filtered_data = [entry for entry in data if start_date <= entry["date"].date() <= end_date]
#     if filtered_data:
#         st.title(f"Filtered {data_type} Data")
#         filtered_df = pd.DataFrame(filtered_data)
#         st.dataframe(filtered_df)
#     else:
#         st.warning("No data found for the selected date range.")
