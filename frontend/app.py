import streamlit as st

from textwrap import dedent
from session import init_session, logout
from views.auth import render_auth_page
from views.client import (
    render_client_dashboard,
    render_client_onboarding,
    render_client_imports_page,
    render_client_risk_page,
    render_client_reports_page,
)
from views.analyst import (
    render_analyst_portfolio_page,
    render_analyst_imports_page,
    render_analyst_reports_page,
)
from views.styles import load_global_styles


st.set_page_config(
    page_title="Financial Insight",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
)

init_session()
load_global_styles()

def go_to_page(page_name: str):
    st.session_state.page = page_name

    st.session_state.selected_review_upload = None
    st.session_state.selected_report_request = None

    st.rerun()

def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand-card">
                <div class="sidebar-brand-icon">FI</div>
                <div>
                    <div class="sidebar-brand-title">Financial Insight</div>
                    <div class="sidebar-brand-subtitle">Financial analytics</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        is_client_onboarding = (
            st.session_state.role == "client"
            and (
                not st.session_state.get("is_onboarded", False)
                or st.session_state.get("page") == "client_onboarding"
            )
        )

        if is_client_onboarding:
            st.write("---")

            if st.button("Logout", use_container_width=True):
                logout()
                st.rerun()

            return

        if st.session_state.role == "client":
            st.write("---")

            if st.button("Dashboard KPI", use_container_width=True):
                go_to_page("client_dashboard")

            if st.button("Predicție Risc", use_container_width=True):
                go_to_page("client_risk")

            if st.button("Importuri", use_container_width=True):
                go_to_page("client_imports")

            if st.button("Rapoarte", use_container_width=True):
                go_to_page("client_reports")

        elif st.session_state.role == "analyst":
            st.write("---")

            if st.button("Portofoliu firme", use_container_width=True):
                go_to_page("analyst_portfolio")

            if st.button("Importuri", use_container_width=True):
                go_to_page("analyst_imports")

            if st.button("Rapoarte", use_container_width=True):
                go_to_page("analyst_reports")

        st.write("---")

        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

def render_mobile_menu():
    if not st.session_state.authenticated:
        return

    st.markdown('<div class="mobile-menu-safe-anchor"></div>', unsafe_allow_html=True)

    with st.expander("Financial Insight", expanded=False):
        if st.session_state.role == "client":
            is_client_onboarding = (
                not st.session_state.get("is_onboarded", False)
                or st.session_state.get("page") == "client_onboarding"
            )

            if is_client_onboarding:
                st.info("Finalizează onboarding-ul pentru a accesa paginile aplicației.")
            else:
                if st.button("Dashboard KPI", key="mobile_client_dashboard", use_container_width=True):
                    go_to_page("client_dashboard")

                if st.button("Predicție Risc", key="mobile_client_risk", use_container_width=True):
                    go_to_page("client_risk")

                if st.button("Importuri", key="mobile_client_imports", use_container_width=True):
                    go_to_page("client_imports")

                if st.button("Rapoarte", key="mobile_client_reports", use_container_width=True):
                    go_to_page("client_reports")

        elif st.session_state.role == "analyst":
            if st.button("Portofoliu firme", key="mobile_analyst_portfolio", use_container_width=True):
                go_to_page("analyst_portfolio")

            if st.button("Importuri", key="mobile_analyst_imports", use_container_width=True):
                go_to_page("analyst_imports")

            if st.button("Rapoarte", key="mobile_analyst_reports", use_container_width=True):
                go_to_page("analyst_reports")

        st.divider()

        if st.button("Logout", key="mobile_logout", use_container_width=True):
            logout()
            st.rerun()

if not st.session_state.authenticated:
    render_auth_page()

else:
    render_sidebar()
    render_mobile_menu()

    if st.session_state.role == "client":
        if st.session_state.page == "client_onboarding":
            render_client_onboarding()
        elif st.session_state.page == "client_imports":
            render_client_imports_page()
        elif st.session_state.page == "client_risk":
            render_client_risk_page()
        elif st.session_state.page == "client_reports":
            render_client_reports_page()
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