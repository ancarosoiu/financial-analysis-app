import streamlit as st


def init_session():
    defaults = {
        "authenticated": False,
        "access_token": None,
        "refresh_token": None,
        "username": None,
        "role": None,
        "is_onboarded": False,
        "company_id": None,
        "page": "auth",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_user(data: dict):
    st.session_state.authenticated = True
    st.session_state.access_token = data.get("access")
    st.session_state.refresh_token = data.get("refresh")
    st.session_state.username = data.get("username")
    st.session_state.role = data.get("role")
    st.session_state.is_onboarded = data.get("is_onboarded", False)
    st.session_state.company_id = data.get("company_id")

    if st.session_state.role == "client":
        st.session_state.page = (
            "client_dashboard"
            if st.session_state.is_onboarded
            else "client_onboarding"
        )
    elif st.session_state.role == "analyst":
        st.session_state.page = "analyst_dashboard"
    else:
        st.session_state.page = "auth"


def logout():
    keys = [
        "authenticated",
        "access_token",
        "refresh_token",
        "username",
        "role",
        "is_onboarded",
        "company_id",
        "page",
    ]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]

    init_session()