import streamlit as st


def hide_streamlit_chrome():
    # Hides the top-right toolbar (Rerun / Always rerun, three-dot menu,
    # Deploy button), the footer and the top colour strip
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        [data-testid="stToolbar"] {display: none !important;}
        [data-testid="stAppDeployButton"] {display: none !important;}
        [data-testid="stMainMenu"] {display: none !important;}
        [data-testid="stStatusWidget"] {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
        </style>
    """, unsafe_allow_html=True)


def style_base_home():
    hide_streamlit_chrome()
    st.markdown("""
        <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #1e1b4b !important;
        }

        /* make both boxes the same height */
        [data-testid="stHorizontalBlock"] {
            align-items: stretch !important;
        }

        /* the box */
        [data-testid="stColumn"] {
            background-color: #E0E3FF !important;
            border: 3px solid #1e1e5a !important;
            border-radius: 1.5rem !important;
            padding: 2rem 1.5rem !important;
            box-sizing: border-box !important;
        }

        /* center everything inside the box */
        [data-testid="stColumn"] [data-testid="stVerticalBlock"] {
            align-items: center !important;
            text-align: center !important;
        }
        [data-testid="stColumn"] [data-testid="stImage"],
        [data-testid="stColumn"] [data-testid="stButton"] {
            display: flex !important;
            justify-content: center !important;
        }

        /* readable heading inside the box */
        [data-testid="stColumn"] h2,
        [data-testid="stColumn"] [data-testid="stHeading"] * {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
            font-size: 1.8rem !important;
            color: #1e1e5a !important;
            text-align: center !important;
        }

        /* hide the little link icon next to headings */
        [data-testid="stHeaderActionElements"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    hide_streamlit_chrome()
    st.markdown("""
        <style>
        .stApp {
            background-color: #f0f2f6 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    hide_streamlit_chrome()
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

h1, h2,
[data-testid="stHeading"],
[data-testid="stHeading"] * {
    font-family: 'Outfit', sans-serif !important;
    font-size: 2rem !important;
    line-height: 1 !important;
    margin-bottom: 0rem !important;
}

/* "span" removed so the eye icon font is not overridden */
h3, h4, p,
[data-testid="stMarkdownContainer"] p,
[data-testid="stHeadingWithActionElements"] h3,
[data-testid="stHeadingWithActionElements"] h4,
button p {
    font-family: 'Outfit', sans-serif !important;
}

/* all buttons (primary = purple) */
button {
    border-radius: 1.5rem !important;
    background: purple !important;
    color: white !important;
    padding: 10px 20px !important;
    border: none !important;
    transition: transform 0.2s ease-in-out !important;
}

/* secondary = pink */
button[kind="secondary"],
button[data-testid="stBaseButton-secondary"] {
    background: #Eb459e !important;
    color: white !important;
}

/* tertiary = black */
button[kind="tertiary"],
button[data-testid="stBaseButton-tertiary"] {
    background: black !important;
    color: white !important;
}

/* password eye button: transparent icon, not a purple pill */
[data-testid="stTextInput"] button {
    background: transparent !important;
    color: #555 !important;
    padding: 0 8px !important;
}
/* border around text boxes */
[data-testid="stTextInputRootElement"],
[data-testid="stTextInput"] [data-baseweb="input"] {
    border: 2px solid #7b4fa0 !important;
    border-radius: 0.75rem !important;
    background: white !important;
}

/* darker border when typing */
[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
    border: 2px solid purple !important;
}

button:hover {
    transform: scale(1.05) !important;
}
</style>
""", unsafe_allow_html=True)
