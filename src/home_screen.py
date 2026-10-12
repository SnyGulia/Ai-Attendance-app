import streamlit as st
from src.components.header import header_home
from ui.base_layout import style_base_home, style_base_layout
from src.components.footer import footer_home


def home_screen():
    style_base_home()
    style_base_layout()
    header_home()

    st.markdown(
        """
        <section class="hero-copy">
            <div class="eyebrow">SMARTER CLASSROOM ROUTINES</div>
            <h1>Attendance that keeps<br><span>class moving.</span></h1>
            <p>Take attendance with AI, review the results, and keep every class record in one place.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    teacher_col, student_col = st.columns(2, gap="large")
    with teacher_col:
        st.markdown(
            '<div class="portal-card"><div class="portal-icon">✦</div>'
            '<div class="portal-kicker">FOR EDUCATORS</div><h2>Teacher portal</h2>'
            '<p>Start a class session, review attendance, and manage your subjects.</p></div>',
            unsafe_allow_html=True,
        )
        if st.button("Continue as teacher", key="teacher_portal", type="primary", width="stretch"):
            st.session_state["login_type"] = "teacher"
            st.rerun()

    with student_col:
        st.markdown(
            '<div class="portal-card"><div class="portal-icon student-icon">◎</div>'
            '<div class="portal-kicker">FOR STUDENTS</div><h2>Student portal</h2>'
            '<p>See your subjects, check attendance, and join a class with a code.</p></div>',
            unsafe_allow_html=True,
        )
        if st.button("Continue as student", key="student_portal", type="primary", width="stretch"):
            st.session_state["login_type"] = "student"
            st.rerun()

    st.markdown(
        '<div class="home-note"><span>AI-assisted attendance</span><span>·</span>'
        '<span>Teacher-reviewed records</span><span>·</span><span>One simple workflow</span></div>',
        unsafe_allow_html=True,
    )
    footer_home()
