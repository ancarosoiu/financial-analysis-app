import streamlit as st
from api import login_request, register_client, register_analyst
from session import login_user


def render_login_form():
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(
            "Username",
            placeholder="nume_utilizator",
        )

        password = st.text_input(
            "Parolă",
            type="password",
            placeholder="••••••••",
        )

        submitted = st.form_submit_button(
            "Autentificare",
            use_container_width=True
        )

    if submitted:
        if not username or not password:
            st.error("Completează username-ul și parola.")
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
    with st.form("register_form", clear_on_submit=False):
        role = st.selectbox("Tip utilizator", ["client", "analyst"])

        full_name = st.text_input(
            "Nume complet",
            placeholder="ex. Anca Popescu",
        )

        username = st.text_input(
            "Username",
            placeholder="ex. anca.popescu",
        )

        email = st.text_input(
            "Email",
            placeholder="nume@exemplu.ro",
        )

        password = st.text_input(
            "Parolă",
            type="password",
            placeholder="••••••••",
        )

        confirm_password = st.text_input(
            "Confirmă parola",
            type="password",
            placeholder="••••••••",
        )

        submitted = st.form_submit_button(
            "Creează cont",
            use_container_width=True
        )

    if submitted:
        if not full_name or not username or not email or not password or not confirm_password:
            st.error("Completează toate câmpurile.")
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
    left_col, right_col = st.columns([1.05, 1], gap="large")

    with left_col:
        st.markdown(
            """
            <div class="auth-brand-row">
                <div class="auth-brand-icon">▥</div>
                <div class="auth-brand-name">Financial Insight Pro</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="auth-brand-title">
                Platformă de Analiză<br>
                Financiară Automată
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="auth-brand-subtitle">
                Monitorizare KPI-uri • Predicții ML • Rapoarte automate •<br>
                Evaluare risc faliment
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        tab_login, tab_register = st.tabs(["Login", "Register"])

        with tab_login:
            render_login_form()

        with tab_register:
            render_register_form()