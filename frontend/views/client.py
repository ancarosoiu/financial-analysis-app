import streamlit as st
import pandas as pd
import plotly.express as px

from api import (
    get_client_dashboard,
    upload_financial_file,
    get_upload_history,
)

from views.styles import (
    load_global_styles,
    render_hero,
    metric_card,
    status_pill,
)

def _safe_float(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def render_client_onboarding():
    load_global_styles()

    render_hero(
        "Client Onboarding",
        "Încarcă minimum 12 luni de date financiare pentru a activa dashboard-ul companiei."
    )

    st.markdown(
        '<div class="section-title">Încărcare fișier financiar</div>',
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Alege fișier Excel",
            type=["xlsx", "xls"]
        )

        if uploaded_file is not None:
            st.info(
                "Fișierul va intra în fluxul de validare și va fi aprobat de analistul alocat."
            )

            if st.button("Trimite pentru validare", use_container_width=True):
                result = upload_financial_file(
                    company_id=st.session_state.company_id,
                    file=uploaded_file,
                    access_token=st.session_state.access_token,
                )

                if result.get("success"):
                    st.success(
                        "Fișier încărcat cu succes. Așteaptă aprobarea analistului."
                    )
                else:
                    st.error(result.get("message", "Încărcarea a eșuat."))

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Istoric importuri</div>',
        unsafe_allow_html=True
    )

    result = get_upload_history(
        company_id=st.session_state.company_id,
        access_token=st.session_state.access_token,
    )

    if result.get("success"):
        data = result.get("data", [])

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nu există încă importuri.")
    else:
        st.warning(result.get("message", "Istoricul importurilor nu a putut fi încărcat."))


def render_client_dashboard():
    load_global_styles()

    result = get_client_dashboard(
        company_id=st.session_state.company_id,
        access_token=st.session_state.access_token,
    )

    if not result.get("success"):
        st.error(result.get("message", "Nu s-au putut încărca datele dashboard-ului."))
        return

    data = result.get("data", {})
    company_name = data.get("company_name", "Client Dashboard")
    summary = data.get("summary", "")
    history = data.get("history", [])

    render_hero(
        company_name,
        summary if summary else "Vizualizare KPI, istoric financiar și indicatori de risc."
    )

    if not history:
        st.info("Nu există încă date aprobate pentru această companie.")
        return

    df = pd.DataFrame(history)

    if "profit" in df.columns:
        df["profit"] = df["profit"].apply(_safe_float)
    if "venituri" in df.columns:
        df["venituri"] = df["venituri"].apply(_safe_float)
    if "probabilitate_faliment" in df.columns:
        df["probabilitate_faliment"] = df["probabilitate_faliment"].apply(_safe_float)

    if "date" in df.columns:
        df = df.sort_values("date")

    latest = df.iloc[-1]

    latest_kpis = latest.get("kpis", {}) if isinstance(latest.get("kpis", {}), dict) else {}
    latest_liquidity = latest_kpis.get("lichiditate")
    latest_profitability = latest_kpis.get("profitabilitate")
    latest_leverage = latest_kpis.get("leverage")
    risk = _safe_float(latest.get("probabilitate_faliment", 0))

    if risk < 30:
        risk_label = status_pill("Risc scăzut", "green")
    elif risk < 60:
        risk_label = status_pill("Risc mediu", "orange")
    else:
        risk_label = status_pill("Risc ridicat", "red")

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        st.markdown(
            metric_card(
                "Venituri curente",
                f"{_safe_float(latest.get('venituri')):,.0f}",
                "Ultima perioadă aprobată"
            ),
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            metric_card(
                "Profit curent",
                f"{_safe_float(latest.get('profit')):,.0f}",
                "Ultima perioadă aprobată"
            ),
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            metric_card(
                "Lichiditate",
                f"{_safe_float(latest_liquidity):.2f}",
                "Current ratio estimat"
            ),
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            metric_card(
                "Prob. faliment",
                f"{risk:.1f}%",
                "Model ML"
            ),
            unsafe_allow_html=True,
        )
        st.markdown(risk_label, unsafe_allow_html=True)

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["KPI Overview", "Risk & Prediction", "Istoric Tabelar"])

    with tab1:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            fig_revenue = px.line(
                df,
                x="date",
                y="venituri",
                markers=True,
                title="Tendință venituri"
            )
            fig_revenue.update_layout(
                template="plotly_white",
                height=360,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_revenue, use_container_width=True)

        with col2:
            fig_profit = px.line(
                df,
                x="date",
                y="profit",
                markers=True,
                title="Tendință profit"
            )
            fig_profit.update_layout(
                template="plotly_white",
                height=360,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_profit, use_container_width=True)

        kpi_rows = []
        for _, row in df.iterrows():
            kpis = row.get("kpis", {}) if isinstance(row.get("kpis", {}), dict) else {}
            kpi_rows.append({
                "date": row.get("date"),
                "lichiditate": _safe_float(kpis.get("lichiditate")),
                "profitabilitate": _safe_float(kpis.get("profitabilitate")),
                "leverage": _safe_float(kpis.get("leverage")),
            })

        kpi_df = pd.DataFrame(kpi_rows)

        col3, col4 = st.columns(2, gap="large")

        with col3:
            fig_liq = px.line(
                kpi_df,
                x="date",
                y="lichiditate",
                markers=True,
                title="Lichiditate în timp"
            )
            fig_liq.update_layout(
                template="plotly_white",
                height=340,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_liq, use_container_width=True)

        with col4:
            fig_lev = px.line(
                kpi_df,
                x="date",
                y="leverage",
                markers=True,
                title="Leverage în timp"
            )
            fig_lev.update_layout(
                template="plotly_white",
                height=340,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_lev, use_container_width=True)

    with tab2:
        fig_risk = px.area(
            df,
            x="date",
            y="probabilitate_faliment",
            title="Evoluția riscului de faliment"
        )
        fig_risk.update_layout(
            template="plotly_white",
            height=360,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig_risk, use_container_width=True)

        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown("### Ultima predicție")
        st.write(f"**Etichetă model:** {latest.get('eticheta', 'N/A')}")
        st.write(f"**Probabilitate faliment:** {_safe_float(latest.get('probabilitate_faliment')):.2f}%")

        importances = latest.get("importanta_indicatori", {})
        if isinstance(importances, dict) and importances:
            imp_df = pd.DataFrame(
                [{"indicator": k, "importance": v} for k, v in importances.items()]
            ).sort_values("importance", ascending=False).head(10)

            fig_imp = px.bar(
                imp_df,
                x="importance",
                y="indicator",
                orientation="h",
                title="Top factori de influență"
            )
            fig_imp.update_layout(
                template="plotly_white",
                height=380,
                margin=dict(l=20, r=20, t=50, b=20),
                yaxis=dict(categoryorder="total ascending"),
            )
            st.plotly_chart(fig_imp, use_container_width=True)
        else:
            st.info("Nu există încă date de explainability disponibile pentru ultima predicție.")

        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        columns_to_show = [
            col for col in ["date", "venituri", "profit", "probabilitate_faliment", "eticheta"]
            if col in df.columns
        ]
        show_df = df[columns_to_show].copy()
        st.dataframe(show_df, use_container_width=True, hide_index=True)