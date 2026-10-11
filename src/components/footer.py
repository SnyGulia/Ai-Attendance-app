import streamlit as st


def footer_home():
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #1e1e5a;
            color: white;
            text-align: center;
            padding: 0.8rem 0;
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            z-index: 999;
        }
        </style>

        <div class="footer">
            Created by Sunny Gulia <span style="color:#ff2d55;">❤️</span>
        </div>
    """, unsafe_allow_html=True)
