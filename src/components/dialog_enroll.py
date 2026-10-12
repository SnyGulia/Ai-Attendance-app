import streamlit as st
# DB helper that adds the student to a subject
from src.database.db import enroll_student_to_subject
from src.database.config import supabase  # Supabase client

import time


@st.dialog("Enroll in Subject")  # opens this function as a popup dialog
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary', icon=':material/library_add:', width='stretch'):
        # Make sure the student typed something
        if join_code:
            # Look up the subject by its code
            res = (
                supabase.table('subjects')
                .select('subject_id, name, subject_code')
                .eq('subject_code', join_code)
                .execute()
            )

            # A matching subject was found
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']

                # Check if the student is already enrolled in this subject
                check = (
                    supabase.table('subject_students')
                    .select('*')
                    .eq('subject_id', subject['subject_id'])
                    .eq('student_id', student_id)
                    .execute()
                )

                if check.data:
                    st.warning('You are already enrolled in this program')
                else:
                    # Add the student to the subject
                    enroll_student_to_subject(
                        student_id, subject['subject_id'])
                    st.success('Successfully enrolled!')
                    time.sleep(1)  # let the success message show briefly
                    st.rerun()  # refresh the page to show the new subject
            else:
                st.error('Subject code not found')
        else:
            st.warning('Please enter a subject code')
