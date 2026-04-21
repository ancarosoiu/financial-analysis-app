import streamlit as st
from session import init_session, logout
from views.auth import render_auth_page
from views.client import render_client_dashboard, render_client_onboarding
from views.analyst import render_analyst_dashboard
from views.styles import load_global_styles

st.set_page_config(
    page_title="Financial Insight Pro",
    page_icon="📊",
    layout="wide"
)

init_session()
load_global_styles()

if st.session_state.authenticated:
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

            if st.button("Onboarding / Upload", use_container_width=True):
                st.session_state.page = "client_onboarding"

        elif st.session_state.role == "analyst":
            st.write("---")
            if st.button("Analyst Dashboard", use_container_width=True):
                st.session_state.page = "analyst_dashboard"

        st.write("---")
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

if not st.session_state.authenticated:
    render_auth_page()
else:
    if st.session_state.role == "client":
        if st.session_state.page == "client_onboarding":
            render_client_onboarding()
        else:
            render_client_dashboard()

    elif st.session_state.role == "analyst":
        render_analyst_dashboard()