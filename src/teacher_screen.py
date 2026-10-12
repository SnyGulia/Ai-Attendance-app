import streamlit as st
import numpy as np
from ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher, get_students_by_ids
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipelines import predict_attendance
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.notifications import notify_absentees


def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return
    if "teacher_login_type" not in st.session_state:
        st.session_state.teacher_login_type = "login"
    if st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    teacher_id = teacher_data['teacher_id']
    subjects = get_teacher_subjects(teacher_id)
    records = get_attendance_for_teacher(teacher_id)
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome {teacher_data['name']}""")

        if st.button("Logout", type="tertiary", icon=":material/logout:", key="loginbackbtn", shortcut="ctrl+h"):
            st.session_state["is_logged_in"] = False
            del st.session_state.teacher_data
            st.rerun()

    present_count = sum(bool(record.get('is_present')) for record in records)
    attendance_rate = round(present_count / len(records) * 100) if records else 0
    session_keys = {
        (record.get('subject_id'), (record.get('timestamp') or '').split('.')[0])
        for record in records if record.get('timestamp')
    }
    metrics = st.columns(4)
    metrics[0].metric("Subjects", len(subjects), help="Subjects you manage")
    metrics[1].metric("Student enrollments", sum(s.get('total_students', 0) for s in subjects), help="Enrollment count across your subjects")
    metrics[2].metric("Class sessions", len(session_keys), help="Sessions with attendance records")
    metrics[3].metric("Attendance rate", f"{attendance_rate}%", help="Present records divided by all attendance records")

    st.subheader(":material/history: Recent class sessions")
    if records:
        sessions = {}
        for record in records:
            timestamp = record.get('timestamp')
            if not timestamp:
                continue
            subject = record.get('subjects') or {}
            key = (record.get('subject_id'), timestamp.split('.')[0])
            session = sessions.setdefault(key, {
                "Time": timestamp,
                "Subject": subject.get('name', 'Unknown subject'),
                "Present": 0,
                "Students": 0,
            })
            session["Present"] += int(bool(record.get('is_present')))
            session["Students"] += 1
        recent_sessions = sorted(sessions.values(), key=lambda item: item['Time'], reverse=True)[:4]
        for session in recent_sessions:
            try:
                session['Time'] = datetime.fromisoformat(session['Time']).strftime("%b %d, %I:%M %p")
            except ValueError:
                pass
        st.dataframe(pd.DataFrame(recent_sessions), width="stretch", hide_index=True)
    else:
        st.info("No sessions yet. Start by taking attendance for one of your subjects.")

    st.space()
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button("Take Attendance", type=type1, icon=":material/how_to_reg:", width="stretch"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
        if st.button("Manage Subjects", type=type2, icon=":material/menu_book:", width="stretch"):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"
        if st.button("Attendance Records", type=type3, icon=":material/analytics:", width="stretch"):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()
    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance(subjects)
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects(subjects)
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records(records)


def teacher_tab_take_attendance(subjects=None):
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header(':material/face: Take AI Attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    if subjects is None:
        subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning(
            'You havent created any subjects yet! Please create one to begin!')
        return

    subject_options = {
        f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}
    col1, col2 = st.columns([3, 1])

    with col1:
        selected_subject_label = st.selectbox(
            'Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

    for idx, img in enumerate(st.session_state.attendance_images):
        with gallery_cols[idx % 4]:
            st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:

        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(
                                student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select(
                    "*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:

                    results, attendance_to_log = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(
                            int(student['student_id']), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    # Remember who was absent so the "Notify absentees" button can use it
                    st.session_state.absent_ids = [
                        l['student_id'] for l in attendance_to_log if not l['is_present']]
                    st.session_state.absent_subject_name = selected_subject_label

                    attendance_result_dialog(
                        pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button("Voice Attendance", type="primary", icon=":material/graphic_eq:", width="stretch"):
            voice_attendance_dialog(selected_subject_id)

    # Notify absentees (email / SMS)
    if st.session_state.get("absent_ids"):
        st.divider()
        st.write(
            f"{len(st.session_state.absent_ids)} student(s) marked absent")
        if st.button("Notify absentees", type="primary", icon=":material/notifications_active:"):
            absent_students = get_students_by_ids(
                st.session_state.absent_ids)
            sent, failed, errors = notify_absentees(
                absent_students, st.session_state.absent_subject_name)
            st.success(f"Sent: {sent}, Failed: {failed}")
            for err in errors:
                st.error(err)
            st.session_state.absent_ids = []


def teacher_tab_manage_subjects(subjects=None):
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header(":material/menu_book: Manage Subjects", width="stretch")
    with col2:
        if st.button("New Subject", width="stretch", type="primary", icon=":material/add:"):
            create_subject_dialog(teacher_id)

   # List All Subjects
   # LIST all SUBJECTS
    if subjects is None:
        subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("🕒", "Classes", sub['total_classes']),
            ]

            def share_btn():
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])
                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records(records=None):
    st.header(":material/analytics: Attendance Records")

    teacher_id = st.session_state.teacher_data["teacher_id"]
    if records is None:
        records = get_attendance_for_teacher(teacher_id)
    if not records:
        st.info("No attendance records yet.")
        return

    data = []
    for r in records:
        ts = r.get("timestamp")
        student = r.get("students") or {}
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "Student": student.get("name", "Unknown"),
            "is_present": bool(r.get('is_present', False)),
        })

    df = pd.DataFrame(data)

    subject_list = ["All"] + sorted(df["Subject"].unique().tolist())
    chosen = st.selectbox("Filter by subject", subject_list)
    if chosen != "All":
        df = df[df["Subject"] == chosen]

    rows = []
    for (ts_group, time, subject, code), g in df.groupby(
            ['ts_group', 'Time', 'Subject', 'Subject Code']):
        absent = g.loc[~g["is_present"], "Student"].tolist()
        present = g.loc[g["is_present"], "Student"].tolist()
        rows.append({
            "ts_group": ts_group,
            "Time": time,
            "Subject": subject,
            "Code": code,
            "Attendance": f"✅ {len(present)}/{len(g)}",
            "Absent Students": ", ".join(absent) if absent else "None",
            "Present Students": ", ".join(present) if present else "None",
        })

    summary = pd.DataFrame(rows).sort_values("ts_group", ascending=False)
    display_df = summary.drop(columns=["ts_group"])

    st.dataframe(display_df, width="stretch", hide_index=True)
    st.download_button("Download CSV", display_df.to_csv(index=False),
                       "attendance_records.csv", "text/csv", icon=":material/download:")

    st.subheader(":material/groups: Student-wise attendance")
    stu = df.groupby("Student")["is_present"].agg(
        Present="sum", Total="count").reset_index()
    stu["Percentage"] = (stu["Present"] / stu["Total"] * 100).round(1)
    stu["Status"] = stu["Percentage"].apply(
        lambda p: "⚠️ Low" if p < 75 else "✅ Good")
    st.dataframe(stu.sort_values("Percentage"),
                 width="stretch", hide_index=True)


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go to home", type="tertiary", icon=":material/home:", key="loginbackbtn", shortcut="ctrl+h"):
            st.session_state["login_type"] = None
            st.rerun()
    st.header(":material/lock: Login Using Password", text_alignment="center")
    st.space()
    teacher_username = st.text_input("Enter Username", placeholder="Manoj")
    teacher_pass = st.text_input(
        "Enter Password", type="password", key="login_password")
    st.divider()
    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Login", icon=":material/login:",
                     shortcut="Enter", width="stretch"):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome Back")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Info Entered")
    with btnc2:
        if st.button("Register", type="secondary", icon=":material/person_add:", width="stretch", key="go_to_password"):
            st.session_state.teacher_login_type = "register"
            st.rerun()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required "
    if check_teacher_exists(teacher_username):
        return False, "User name taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Pass dont match"
    try:
        create_teacher(teacher_username,  teacher_pass, teacher_name)
        return True, "Sucessfully Created, Login Now"
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, f"Unexpected Error:{e}"


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go to home", type="tertiary", icon=":material/home:", key="registerbackbtn", shortcut="ctrl+h"):
            st.session_state["login_type"] = None
            st.rerun()
    st.header(":material/person_add: Register Your Teacher Account")
    st.space()
    st.space()
    teacher_username = st.text_input(
        "Enter Username", placeholder="Manojku12", key="reg_username")
    teacher_name = st.text_input(
        "Enter Name", placeholder="Manoj Kumar", key="reg_name")
    teacher_pass = st.text_input(
        "Enter Password", type="password", key="reg_pass")
    teacher_pass_confirm = st.text_input(
        "Confirm Password", type="password", key="reg_confirm_pass")
    st.divider()
    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Register", icon=":material/person_add:",
                     shortcut="Enter", width="stretch", key="register_submit"):
            success, message = register_teacher(
                teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
    with btnc2:
        if st.button("Login", type="secondary", icon=":material/login:", width="stretch", key="goto_login"):
            st.session_state.teacher_login_type = "login"
            st.rerun()
