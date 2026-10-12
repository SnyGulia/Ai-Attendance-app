import streamlit as st


def footer_home():
    st.markdown(
        """
        <style>
        .footer { margin:2rem 0 0; padding:1rem 0; text-align:center;
            color:#718187; font:500 12px 'Outfit',sans-serif; }
        </style>
        <div class="footer">ClassPulse · Classroom attendance, made easier</div>
        """,
        unsafe_allow_html=True,
    )
