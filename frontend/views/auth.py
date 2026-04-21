import streamlit as st
from api import login_request, register_client, register_analyst
from session import login_user


def render_login_form():
    st.markdown(
        '<div class="auth-title">Autentificare</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="auth-subtitle">Accesează platforma folosind credențialele contului tău.</div>',
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="ex. anca.popescu")
        password = st.text_input("Parolă", type="password", placeholder="Introdu parola")
        btn_left, btn_center, btn_right = st.columns([1, 1, 1])

        with btn_center:
            submitted = st.form_submit_button("Continuă", use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Completează toate câmpurile.")
            return

        with st.spinner("Se realizează autentificarea..."):
            result = login_request(username, password)

        if result.get("success"):
            login_user(result)
            st.success("Autentificare reușită.")
            st.rerun()
        else:
            st.error(result.get("message", "Autentificarea a eșuat."))

def render_register_form():
    st.markdown(
        '<div class="auth-title">Creare cont</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="auth-subtitle">Înregistrează un cont nou și selectează rolul potrivit.</div>',
        unsafe_allow_html=True,
    )

    with st.form("register_form", clear_on_submit=False):
        role = st.selectbox("Tip utilizator", ["client", "analyst"])
        full_name = st.text_input("Nume complet", placeholder="ex. Anca Popescu")
        username = st.text_input("Username", placeholder="ex. anca.popescu")
        email = st.text_input("Email", placeholder="ex. anca@firma.ro")

        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Parolă", type="password")
        with col2:
            confirm_password = st.text_input("Confirmă parola", type="password")

        btn_left, btn_center, btn_right = st.columns([1, 1, 1])

        with btn_center:
            submitted = st.form_submit_button("Creează cont", use_container_width=True)

    if submitted:
        if not full_name or not username or not email or not password or not confirm_password:
            st.error("Completează toate câmpurile obligatorii.")
            return

        if password != confirm_password:
            st.error("Parolele nu coincid.")
            return

        payload = {
            "full_name": full_name,
            "username": username,
            "email": email,
            "password": password,
        }

        if role == "client":
            with st.spinner("Se creează contul de client..."):
                result = register_client(payload)
        else:
            with st.spinner("Se creează contul de analist..."):
                result = register_analyst(payload)

        if result.get("success"):
            st.success("Cont creat cu succes. Acum te poți autentifica.")
        else:
            st.error(result.get("message", "Înregistrarea a eșuat."))

def render_auth_page():
    left_spacer, center_col, right_spacer = st.columns([0.7, 1.6, 0.7])

    with center_col:
        st.markdown(
            """
            <div class="auth-logo-wrap">
                <div class="brand-badge">📊</div>
                <div class="center-brand-title">Financial Insight Pro</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_login, tab_register = st.tabs(["Login", "Register"])

        with tab_login:
            render_login_form()

        with tab_register:
            render_register_form()