import streamlit as st

from session import init_session, logout
from views.auth import render_auth_page
from views.client import (
    render_client_dashboard,
    render_client_onboarding,
    render_client_imports_page,
    render_client_risk_page,
)
from views.analyst import (
    render_analyst_portfolio_page,
    render_analyst_imports_page,
    render_analyst_reports_page,
)
from views.styles import load_global_styles


st.set_page_config(
    page_title="Financial Insight Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session()
load_global_styles()


def render_sidebar():
    with st.sidebar:
        st.markdown("## Financial Insight Pro")
        st.caption(f"Logged in as {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role}")

        if st.session_state.role == "client":
            st.write("---")

            if st.button("Dashboard KPI", use_container_width=True):
                st.session_state.page = (
                    "client_dashboard"
                    if st.session_state.is_onboarded
                    else "client_onboarding"
                )
                st.rerun()

            if st.button("Predicție ML / Risc", use_container_width=True):
                st.session_state.page = "client_risk"
                st.rerun()

            if st.button("Importuri", use_container_width=True):
                st.session_state.page = "client_imports"
                st.rerun()

            if not st.session_state.is_onboarded:
                if st.button("Onboarding / Upload", use_container_width=True):
                    st.session_state.page = "client_onboarding"
                    st.rerun()

        elif st.session_state.role == "analyst":
            st.write("---")

            if st.button("Portofoliu firme", use_container_width=True):
                st.session_state.page = "analyst_portfolio"
                st.rerun()

            if st.button("Importuri", use_container_width=True):
                st.session_state.page = "analyst_imports"
                st.rerun()

            if st.button("Rapoarte", use_container_width=True):
                st.session_state.page = "analyst_reports"
                st.rerun()

        st.write("---")

        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()


if not st.session_state.authenticated:
    render_auth_page()

else:
    render_sidebar()

    if st.session_state.role == "client":
        if st.session_state.page == "client_onboarding":
            render_client_onboarding()
        elif st.session_state.page == "client_imports":
            render_client_imports_page()
        elif st.session_state.page == "client_risk":
            render_client_risk_page()
        else:
            render_client_dashboard()

    elif st.session_state.role == "analyst":
        if st.session_state.page == "analyst_imports":
            render_analyst_imports_page()
        elif st.session_state.page == "analyst_reports":
            render_analyst_reports_page()
        else:
            render_analyst_portfolio_page()

    else:
        st.error("Rol necunoscut. Te rog autentifică-te din nou.")
        logout()
        st.rerun()