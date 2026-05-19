import streamlit as st

from page.auth import show_login
from page.register import show_register
from page.dashboard import show_dashboard

st.set_page_config(
    page_title="AMCHO Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── init session state ─────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "login"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None


# ── CSS global ─────────────────────────────────────
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        #MainMenu, footer, header { visibility: hidden; }

        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #f1f1f1; }
        ::-webkit-scrollbar-thumb { background: #c8a97e; border-radius: 4px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── ROUTING UNIQUE (IMPORTANT) ─────────────────────

if not st.session_state.authenticated:

    if st.session_state.page == "login":
        show_login()

    elif st.session_state.page == "register":
        show_register()

else:
    show_dashboard()