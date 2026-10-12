import streamlit as st
from ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipelines import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome {student_data['name']}""")

        if st.button("Logout", type="secondary", key="loginbackbtn", shortcut="ctrl+h"):
            st.session_state["is_logged_in"] = False
            del st.session_state.student_data
            st.rerun()
    st.space()
    c1, c2 = st.columns(2)
    with c1:
        st.header("Your Enrolled Subjects")
    with c2:
        if st.button("Enroll in subjects", type="primary", width="stretch"):
            enroll_dialog()

    st.divider()

    with st.spinner("Loading Your Subjets...."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def unenroll_button():
            if st.button("Unenroll From this course", type="tertiary", width="stretch", key=f"unenroll {sid}"):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f"unenroll from {sub['name']} successfully")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )


def student_screen():
    style_background_dashboard()
    style_base_layout()
    if "student_data" in st.session_state:
        student_dashboard()
        return
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("GO To Home", type="secondary", key="loginbackbtn", shortcut="ctrl+h"):
            st.session_state["login_type"] = None
            st.rerun()
    st.header("Login using Faceid", text_alignment="center")
    st.space()
    st.space()
    show_registration = False
    photo_source = st.camera_input("Keep your face in Center")
    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner("Ai is Scanning...."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face Not Found!")
            elif num_faces > 1:
                st.warning("Multiple Faces Found")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if s["student_id"] == student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        import time
                        time.sleep(1)
                        st.rerun()

                else:
                    st.info("Face Not Recognised! You must be a new student")
                    show_registration = True
    if show_registration:
        with st.container(border=True):
            st.header("Register New Profile")
            new_name = st.text_input(
                "Enter Your Name", placeholder="e.g. Kabir")
            new_email = st.text_input(
                "Email", placeholder="e.g. kabir@gmail.com")
            new_phone = st.text_input(
                "Parent Phone", placeholder="e.g +91 1234567890")

            st.subheader("Optional  Voice Enrollment")
            st.info("Enroll for voice only attendance")

            audio_data = None

            try:
                audio_data = st.audio_input(
                    "Record a short sentence ! Like I am Present My name is Simran.")
            except Exception:
                st.error("Audio Failed")

            if st.button("Create Account ", type="primary"):
                if new_name and new_email:
                    with st.spinner("Creating new profile..."):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                    if encodings:
                        face_emb = encodings[0].tolist()
                        voice_emb = None
                        if audio_data:
                            voice_emb = get_voice_embedding(audio_data.read())
                        response_data = create_student(
                            new_name, face_embedding=face_emb, voice_embedding=voice_emb, email=new_email, parent_phone=new_phone)

                        if response_data:
                            train_classifier()
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = response_data[0]
                            st.toast(f"Profile Created! {new_name}!")
                            import time
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.warning(
                            "couldnt Capture Your Facial Feature for registration")

                else:
                    st.warning("Please Enter Your Name and Email")
