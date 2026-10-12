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
            background:radial-gradient(ellipse at 10% 4%,#eee9ff 0,transparent 42%),radial-gradient(ellipse at 92% 12%,#fff0e8 0,transparent 32%),#f8f7fb !important;
        }
        [data-testid="stMainBlockContainer"] { max-width: 920px; padding-top: 2rem; }
        .brand-lockup { display:flex; align-items:center; gap:12px; margin: 0 0 3rem; }
        .brand-mark { display:inline-flex; width:42px; height:42px; align-items:center;
            justify-content:center; border-radius:14px; background:linear-gradient(135deg,#6546f5,#8b5cf6); color:#fff;
            font:800 15px 'Outfit',sans-serif; letter-spacing:-1px; }
        .brand-name { color:#18323b; font:750 24px 'Outfit',sans-serif; letter-spacing:-.7px; }
        .brand-name span { color:#7653ef; }
        .hero-copy { max-width:700px; margin:0 auto 2.2rem; text-align:center; }
        .eyebrow, .portal-kicker { color:#7653ef; font:700 11px 'Outfit',sans-serif;
            letter-spacing:1.7px; }
        .hero-copy h1 { color:#18323b; font:750 clamp(2.5rem,6vw,4rem)/1.04 'Outfit',sans-serif;
            letter-spacing:-2px; margin:.75rem 0 1rem; }
        .hero-copy h1 span { color:#7653ef; }
        .hero-copy p { max-width:560px; margin:0 auto; color:#61747a; font-size:1.08rem; line-height:1.65; }
        .portal-card { min-height:205px; box-sizing:border-box; padding:1.5rem;
            background:#fff; border:1px solid #dce6e2; border-radius:18px;
            box-shadow:0 12px 34px rgba(24,50,59,.07); transition:transform .2s ease,box-shadow .2s ease; }
        .portal-card:hover { transform:translateY(-3px); box-shadow:0 18px 42px rgba(24,50,59,.11); }
        .portal-icon { display:flex; width:38px; height:38px; align-items:center; justify-content:center;
            border-radius:12px; background:#eee9ff; color:#7653ef; font-size:21px; }
        .student-icon { background:#fff0e8; color:#ed784b; }
        .portal-card .portal-kicker { margin-top:1.1rem; }
        .portal-card h2 { margin:.25rem 0 .5rem; color:#18323b; font:700 1.55rem 'Outfit',sans-serif; }
        .portal-card p { margin:0; color:#61747a; line-height:1.5; }
        [data-testid="stColumn"] [data-testid="stButton"] { margin-top:.8rem; }
        .home-note { display:flex; justify-content:center; flex-wrap:wrap; gap:.6rem;
            margin:2rem auto 1.5rem; color:#718187; font:500 13px 'Outfit',sans-serif; }
        [data-testid="stColumn"] [data-testid="stButton"] button { min-height:2.8rem; }
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
        .stApp, [data-testid="stAppViewContainer"] {
            background:radial-gradient(ellipse at 8% 0%, #eee9ff 0, transparent 34%),
                       radial-gradient(ellipse at 96% 8%, #fff0e8 0, transparent 30%), #f8f7fb !important;
        }
        [data-testid="stMainBlockContainer"] { max-width:1120px; padding-top:1.5rem; padding-bottom:3rem; }
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
        .brand-lockup { display:flex; align-items:center; gap:12px; margin:0 0 1.4rem; }
        .brand-mark { display:inline-flex; width:42px; height:42px; align-items:center; justify-content:center;
            border-radius:14px; background:linear-gradient(135deg,#6546f5,#8b5cf6); color:#fff;
            font:800 15px 'Outfit',sans-serif; letter-spacing:-1px; }
        .brand-name { color:#18323b; font:750 24px 'Outfit',sans-serif; letter-spacing:-.7px; }
        .brand-name span { color:#7653ef; }
        h1,h2,h3,h4,p,button,[data-testid="stHeading"] * {
            font-family:'Outfit',sans-serif !important;
        }
        h1,h2 { letter-spacing:-.7px; color:#18323b; }
        h3,h4 { color:#25434a; }
        [data-testid="stSubheader"] { color:#18323b; }
        [data-testid="stVerticalBlockBorderWrapper"] {
            background:rgba(255,255,255,.82); border:1px solid #e1eae6 !important;
            border-radius:18px !important; box-shadow:0 10px 30px rgba(24,50,59,.045);
        }
        [data-testid="stMetric"] { background:#fff; border:1px solid #e1eae6; border-radius:15px; padding:1rem 1.1rem; }
        [data-testid="stMetricLabel"] { color:#64777c !important; }
        [data-testid="stMetricValue"] { color:#7653ef !important; font-family:'Outfit',sans-serif !important; }
        [data-testid="stTabs"] [data-baseweb="tab-list"] { gap:.4rem; }
        [data-testid="stTabs"] [data-baseweb="tab"] { border-radius:10px 10px 0 0; }
        [data-testid="stDataFrame"] { border:1px solid #e1eae6; border-radius:14px; overflow:hidden; }
        [data-testid="stAlert"] { border-radius:13px; }
        [data-testid="stCameraInput"] { border-radius:16px; overflow:hidden; }
        button[kind="primary"], button[data-testid="stBaseButton-primary"] {
            background:linear-gradient(120deg,#6546f5,#8b5cf6) !important; border:1px solid #6546f5 !important;
            color:#fff !important; border-radius:12px !important; font-weight:650 !important;
            box-shadow:0 6px 16px rgba(101,70,245,.23) !important;
            transition:background .15s ease, transform .15s ease !important;
        }
        button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {
            background:linear-gradient(120deg,#5434dc,#7541e8) !important; transform:translateY(-1px) !important;
        }
        button[kind="secondary"], button[data-testid="stBaseButton-secondary"] {
            background:linear-gradient(120deg,#f27b50,#f49a55) !important; border:1px solid #ef794d !important;
            color:#fff !important; border-radius:12px !important; font-weight:650 !important;
            box-shadow:0 6px 15px rgba(239,121,77,.18) !important;
        }
        button[kind="tertiary"], button[data-testid="stBaseButton-tertiary"] {
            background:#eee9ff !important; color:#6444dc !important; border:1px solid #e0d8ff !important; border-radius:10px !important;
        }
        button[kind="primary"], button[kind="secondary"], button[kind="tertiary"] {
            transition:transform .16s ease, box-shadow .16s ease, filter .16s ease !important;
        }
        button[kind="primary"]:hover, button[kind="secondary"]:hover, button[kind="tertiary"]:hover {
            transform:translateY(-1px) !important; filter:saturate(1.08) !important;
        }
        [data-testid="stTextInputRootElement"], [data-testid="stTextInput"] [data-baseweb="input"] {
            border:1px solid #ded9ea !important; border-radius:10px !important; background:#fff !important;
        }
        [data-testid="stTextInputRootElement"]:focus-within,
        [data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
            border-color:#7653ef !important;
        }
        [data-testid="stTextInput"] button { background:transparent !important; color:#52676c !important; }
        [data-testid="stHeaderActionElements"] { display:none !important; }
        .dashboard-welcome { color:#64777c; font-size:.92rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )
