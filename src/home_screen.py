import streamlit as st
from src.components.header import header_home
from ui.base_layout import style_base_home, style_base_layout
from src.components.footer import footer_home


def home_screen():
    header_home()
    style_base_home()
    style_base_layout()
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.header("Teacher Portal")
        st.image("https://cdn-icons-png.flaticon.com/128/5369/5369664.png", width=100)
        if st.button("Teacher Portal", ):
            st.session_state["login_type"] = "teacher"
            st.rerun()
    with col2:
        st.header("Student Portal")
        st.image("https://cdn-icons-png.flaticon.com/128/2995/2995459.png", width=100)
        if st.button("Student Portal"):
            st.session_state["login_type"] = "student"
            st.rerun()

    footer_home()
