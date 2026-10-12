import streamlit as st
from src.database.db import create_attendance


def show_attendance_result(df, logs, subject_name):
    st.write('Please review attendance before confirming.')
    edited_df = st.data_editor(
        df,
        hide_index=True,
        width='stretch',
        disabled=['Name', 'ID', 'Source'],
        column_config={
            'Status': st.column_config.SelectboxColumn(
                'Status',
                options=['✅ Present', '❌ Absent'],
                required=True,
            )
        },
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard', width='stretch'):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button('Confirm & Save', width='stretch', type='primary'):
            try:
                status_by_id = {
                    str(row['ID']): row['Status'] == '✅ Present'
                    for _, row in edited_df.iterrows()
                }
                updated_logs = [
                    {
                        **log,
                        'is_present': status_by_id[str(log['student_id'])],
                    }
                    for log in logs
                ]

                create_attendance(updated_logs)
                st.session_state.absent_ids = [
                    log['student_id']
                    for log in updated_logs
                    if not log['is_present']
                ]
                st.session_state.absent_subject_name = subject_name
                st.toast("Attendance taken")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error('Sync failed!')


@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs, subject_name):
    show_attendance_result(df, logs, subject_name)
