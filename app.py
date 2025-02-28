# For any help we can follow streamlit documentation
# https://docs.streamlit.io/

# To run the app, open terminal and run the following command
# streamlit run app.py

#imports
import streamlit as st
import pandas as pd
import os
# Convert Files into Binary and keep them safe temporarily in memory
from io import BytesIO

# Set up our Streamlit app
st.set_page_config(page_title="📊Data Sweeper", layout='wide')
st.title("📊Data Sweeper")
st.write("Transform Your Files Between CSV and Excel Formats with built-in Data Cleaning and Visualization!")

# Upload File
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file, engine="openpyxl")  # Fix: Ensure proper reading of Excel files
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display Info About the File
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Show 5 rows of our data frame
        st.write("Preview of the Data Frame:")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed Successfully!")

            with col2:
                if st.button(f"Fill Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled Successfully!")

        # Choose Specific Columns to Keep or Convert
        st.subheader("Select Columns to Keep or Convert")
        columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create Some Visualizations
        st.subheader("📊 Data Visualizations")
        if st.checkbox(f"Show Visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[::2])

        # Convert File: CSV to Excel OR Excel to CSV
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):  
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False, encoding="utf-8-sig")  # Fix: Encoding added for Excel compatibility
                file_name = file.name.replace(file_ext, '.csv')
                mime_type = 'text/csv'
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")  # Fix: Ensure Excel format is properly written
                file_name = file.name.replace(file_ext, '.xlsx')
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

            buffer.seek(0)  # Fix: Ensure buffer is reset before downloading

            # Download Button
            st.download_button(label=f"⬇ Download {file.name} as {conversion_type}",
                               data=buffer, file_name=file_name, mime=mime_type)

st.success("🎉 All Files Processed Successfully!")
