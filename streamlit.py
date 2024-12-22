import streamlit as st
import pandas as pd
import tempfile
import os

st.title("CSV Merger Application")

# Step 1: Upload multiple CSV files
st.header("Step 1: Upload CSV Files")
uploaded_files = st.file_uploader("Upload one or more CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("Uploaded Files Preview")
    dataframes = {}
    selected_columns = {}
    
    # Display previews and allow column selection for each file
    for i, uploaded_file in enumerate(uploaded_files):
        df = pd.read_csv(uploaded_file)
        st.write(f"Preview of **{uploaded_file.name}**:")
        st.dataframe(df.head())
        
        # Allow column selection for this file
        columns = df.columns.tolist()
        selected_columns[uploaded_file.name] = st.multiselect(
            f"Select columns to include from **{uploaded_file.name}**",
            columns,
            key=f"columns_{i}"
        )
        dataframes[uploaded_file.name] = df
# Step 2: Merge Selected Data
if uploaded_files:
    st.header("Step 2: Merge Data")
    merge_button = st.button("Merge Selected Data")
    merged_data = None

    if merge_button:
        merged_data = pd.DataFrame()
        for file_name, df in dataframes.items():
            selected_cols = selected_columns[file_name]
            if selected_cols:
                print(merged_data)
                # Add selected columns to the merged dataframe
                if merged_data.empty:
                    merged_data = df[selected_cols]
                else:
                    merged_data = pd.concat([merged_data, df[selected_cols]], axis=1)
        
        st.write("Merged Data Preview:")
        st.dataframe(merged_data)

# Step 3: Save Merged Data
if 'merged_data' in locals() and merged_data is not None:
    st.header("Step 3: Save Merged Data")
    if st.button("Save Merged Data to Temporary CSV"):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            merged_data.to_csv(tmp_file.name, index=False)
            tmp_file_path = tmp_file.name
        
        st.success(f"Merged data saved to temporary file: {tmp_file_path}")
        st.write(f"Temporary file path: `{tmp_file_path}`")
