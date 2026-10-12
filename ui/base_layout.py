import streamlit as st


def hide_streamlit_chrome():
    st.markdown(
        """
        <style>
        #MainMenu, footer, [data-testid="stToolbar"],
        [data-testid="stAppDeployButton"], [data-testid="stDecoration"] {
            visibility: hidden !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def force_readable_colors():
    st.markdown(
        """
        <style>
        .stApp, .stApp p, .stApp label, .stApp li,
        .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] * {
            color: #18323b;
        }
        input, textarea { color: #18323b !important; background: #ffffff !important; }
        ::placeholder { color: #73858a !important; opacity: 1; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_base_home():
    hide_streamlit_chrome()
    st.markdown(
        """
        <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: #f5f7f4 !important;
        }
        [data-testid="stMainBlockContainer"] { max-width: 920px; padding-top: 2rem; }
        .brand-lockup { display:flex; align-items:center; gap:12px; margin: 0 0 3rem; }
        .brand-mark { display:inline-flex; width:42px; height:42px; align-items:center;
            justify-content:center; border-radius:14px; background:#087f75; color:#fff;
            font:800 15px 'Outfit',sans-serif; letter-spacing:-1px; }
        .brand-name { color:#18323b; font:750 24px 'Outfit',sans-serif; letter-spacing:-.7px; }
        .brand-name span { color:#087f75; }
        .hero-copy { max-width:700px; margin:0 auto 2.2rem; text-align:center; }
        .eyebrow, .portal-kicker { color:#087f75; font:700 11px 'Outfit',sans-serif;
            letter-spacing:1.7px; }
        .hero-copy h1 { color:#18323b; font:750 clamp(2.5rem,6vw,4rem)/1.04 'Outfit',sans-serif;
            letter-spacing:-2px; margin:.75rem 0 1rem; }
        .hero-copy h1 span { color:#087f75; }
        .hero-copy p { max-width:560px; margin:0 auto; color:#61747a; font-size:1.08rem; line-height:1.65; }
        .portal-card { min-height:205px; box-sizing:border-box; padding:1.5rem;
            background:#fff; border:1px solid #dce6e2; border-radius:18px;
            box-shadow:0 8px 26px rgba(24,50,59,.05); }
        .portal-icon { display:flex; width:38px; height:38px; align-items:center; justify-content:center;
            border-radius:12px; background:#e3f3ef; color:#087f75; font-size:21px; }
        .student-icon { background:#eef0e7; color:#627b48; }
        .portal-card .portal-kicker { margin-top:1.1rem; }
        .portal-card h2 { margin:.25rem 0 .5rem; color:#18323b; font:700 1.55rem 'Outfit',sans-serif; }
        .portal-card p { margin:0; color:#61747a; line-height:1.5; }
        [data-testid="stColumn"] [data-testid="stButton"] { margin-top:.8rem; }
        .home-note { display:flex; justify-content:center; flex-wrap:wrap; gap:.6rem;
            margin:2rem auto 1.5rem; color:#718187; font:500 13px 'Outfit',sans-serif; }
        @media (max-width: 640px) {
            .brand-lockup { margin-bottom:2rem; }
            .portal-card { min-height:0; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_background_dashboard():
    hide_streamlit_chrome()
    st.markdown(
        """
        <style>
        .stApp, [data-testid="stAppViewContainer"] { background:#f5f7f4 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_base_layout():
    hide_streamlit_chrome()
    force_readable_colors()
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');
        h1,h2,h3,h4,p,button,[data-testid="stHeading"] * {
            font-family:'Outfit',sans-serif !important;
        }
        h1,h2 { letter-spacing:-.5px; }
        button[kind="primary"], button[data-testid="stBaseButton-primary"] {
            background:#087f75 !important; border:1px solid #087f75 !important;
            color:#fff !important; border-radius:11px !important; font-weight:650 !important;
            transition:background .15s ease, transform .15s ease !important;
        }
        button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {
            background:#066b63 !important; transform:translateY(-1px) !important;
        }
        button[kind="secondary"], button[data-testid="stBaseButton-secondary"] {
            background:#fff !important; border:1px solid #cbd9d5 !important;
            color:#18323b !important; border-radius:11px !important;
        }
        button[kind="tertiary"], button[data-testid="stBaseButton-tertiary"] {
            background:transparent !important; color:#34545a !important; border-radius:10px !important;
        }
        [data-testid="stTextInputRootElement"], [data-testid="stTextInput"] [data-baseweb="input"] {
            border:1px solid #cbd9d5 !important; border-radius:10px !important; background:#fff !important;
        }
        [data-testid="stTextInputRootElement"]:focus-within,
        [data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
            border-color:#087f75 !important;
        }
        [data-testid="stTextInput"] button { background:transparent !important; color:#52676c !important; }
        [data-testid="stHeaderActionElements"] { display:none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
