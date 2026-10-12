import streamlit as st


def render_footer():
    st.markdown(
        """
        <style>
        .footer { margin:2rem 0 0; padding:1rem 0; text-align:center;
            border-top:1px solid #e1eae6; color:#718187; font:500 12px 'Outfit',sans-serif; }
        </style>
        <div class="footer">✨ Created by Sunny Gulia</div>
        """,
        unsafe_allow_html=True,
    )
