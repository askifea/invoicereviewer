import streamlit as st
import os
import io
import zipfile
from pathlib import Path

# Set page configuration
st.set_page_config(page_title="File Review and Assignment", layout="wide")

# Initialize session state to store uploaded files and assignments
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}
if "file_assignments" not in st.session_state:
    st.session_state.file_assignments = {}  # Structure: {"filename": "List A"}

# Define the available lists
available_lists = ["List A", "List B", "List C"]

# Title
st.title("File Review and Assignment App")
st.markdown("### Upload files, assign them to lists, and download grouped files.")

# File Upload Section
st.markdown("### Upload Files")
uploaded_files = st.file_uploader(
    "Drag and drop your files here, or click to upload",
    type=None,
    accept_multiple_files=True,
)

if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.uploaded_files:
            # Save file in session state
            st.session_state.uploaded_files[file.name] = file
            st.session_state.file_assignments[file.name] = None  # Initially unassigned

# File Review and Assignment Section
st.markdown("### Review and Assign Files")
if st.session_state.uploaded_files:
    for filename, file in st.session_state.uploaded_files.items():
        col1, col2 = st.columns([3, 1])

        # Display file details
        with col1:
            st.markdown(f"**File:** {filename}")
            if st.session_state.file_assignments[filename]:
                st.success(f"Assigned to: {st.session_state.file_assignments[filename]}")
            else:
                st.warning("Not yet assigned.")

        # Assignment dropdown
        with col2:
            selected_list = st.selectbox(
                "Assign to list",
                options=["Unassigned"] + available_lists,
                index=available_lists.index(st.session_state.file_assignments[filename])
                + 1 if st.session_state.file_assignments[filename] else 0,
                key=f"assign_{filename}",
            )
            if selected_list != "Unassigned":
                st.session_state.file_assignments[filename] = selected_list

# Download Section
st.markdown("### Download Files by List")
for list_name in available_lists:
    files_in_list = [
        (name, file)
        for name, file in st.session_state.uploaded_files.items()
        if st.session_state.file_assignments[name] == list_name
    ]

    if files_in_list:
        st.markdown(f"**{list_name}:** {len(files_in_list)} file(s) assigned.")
        # Create a ZIP file for download
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for filename, file in files_in_list:
                zip_file.writestr(filename, file.read())
        zip_buffer.seek(0)

        st.download_button(
            label=f"Download {list_name} ZIP",
            data=zip_buffer,
            file_name=f"{list_name}.zip",
            mime="application/zip",
        )
    else:
        st.markdown(f"**{list_name}:** No files assigned.")

# Clear All Button
if st.button("Clear All"):
    st.session_state.uploaded_files = {}
    st.session_state.file_assignments = {}
    st.experimental_rerun()
