import streamlit as st
from src.database.db import create_subject


# Opens as a popup window on top of the page
@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of new subject")

    # Input boxes for the subject details
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input(
        "Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")

    if st.button("Create Subject Now", type="primary", width="stretch"):
        # Make sure all fields are filled
        if sub_id and sub_name and sub_section:
            try:
                # Save the subject in the database
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast("Subject Created Successfully!")
                st.rerun()  # close the popup and refresh the page
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all the fields")
