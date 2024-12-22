import streamlit as st
import pandas as pd
import tempfile
from functools import reduce


st.title("CSV Merger Application")

# Step 1: Upload multiple CSV files
st.header("Step 1: Upload CSV Files")
uploaded_files = st.file_uploader("Upload one or more CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("Uploaded Files Preview")
    dataframes = []
    columns = []
    
    # Display previews and allow column selection for each file
    for i, uploaded_file in enumerate(uploaded_files):
        df = pd.read_csv(uploaded_file)
        st.write(f"Preview of **{uploaded_file.name}**:")
        st.dataframe(df.head())
        
        key_column = st.selectbox(
            f"Select key",
            df.columns.tolist()
        )
        select_columns = st.multiselect(
            f"Select columns",
            df.columns.tolist()
        )
        df['key'] = df[key_column]
        select_columns.append('key')
        df = df[select_columns]
        dataframes.append(df)

# Step 2: Merge Selected Data
if uploaded_files:
    st.header("Step 2: Merge Data")
    merge_button = st.button("Merge Selected Data")
    merged_data = None

    if merge_button:
        merged_data = pd.DataFrame()
        merged_data = reduce(lambda left, right: pd.merge(left, right, on='key'), dataframes) 
        merged_data = merged_data.drop('key', axis=1)
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
