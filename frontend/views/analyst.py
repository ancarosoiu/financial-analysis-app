import streamlit as st
import pandas as pd
from api import get_analyst_dashboard_stats, get_companies
from views.styles import load_global_styles, render_hero, metric_card


def render_analyst_dashboard():
    load_global_styles()

    render_hero(
        "Analyst Control Center",
        "Vizualizare portofoliu, task-uri prioritare și firmele alocate."
    )

    stats_response = get_analyst_dashboard_stats(st.session_state.access_token)

    total_firme = 0
    importuri_noi = 0
    cereri_rapoarte_noi = 0
    firme_risc_ridicat = 0

    if stats_response.status_code == 200:
        stats = stats_response.json()
        total_firme = stats.get("total_firme", 0)
        importuri_noi = stats.get("importuri_noi", 0)
        cereri_rapoarte_noi = stats.get("cereri_rapoarte_noi", 0)
        firme_risc_ridicat = stats.get("firme_risc_ridicat", 0)

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        st.markdown(metric_card("Firme alocate", str(total_firme), "Portofoliu activ"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("Importuri noi", str(importuri_noi), "În așteptare aprobare"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("Cereri rapoarte", str(cereri_rapoarte_noi), "Task-uri noi"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("Risc ridicat", str(firme_risc_ridicat), "Companii monitorizate"), unsafe_allow_html=True)

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.45, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-title">Lista clienților alocați</div>', unsafe_allow_html=True)
        companies_response = get_companies(st.session_state.access_token)

        if companies_response.status_code == 200:
            companies = companies_response.json()
            if companies:
                df = pd.DataFrame(companies)
                wanted_cols = [
                    "nume", "cui", "industrie", "status_onboarded",
                    "analist_nume", "owner_username", "data_inregistrare"
                ]
                existing_cols = [c for c in wanted_cols if c in df.columns]
                st.dataframe(df[existing_cols], use_container_width=True, hide_index=True)
            else:
                st.info("Nu există firme alocate momentan.")
        else:
            st.warning("Lista firmelor nu a putut fi încărcată.")

    with col_right:
        st.markdown('<div class="section-title">Work Queue</div>', unsafe_allow_html=True)

        queue_rows = [
            {"Prioritate": "Ridicată", "Task": "Revizuire importuri pending", "Status": importuri_noi},
            {"Prioritate": "Medie", "Task": "Cereri raport personalizat", "Status": cereri_rapoarte_noi},
            {"Prioritate": "Ridicată", "Task": "Monitorizare firme cu risc", "Status": firme_risc_ridicat},
        ]

        qdf = pd.DataFrame(queue_rows)
        st.dataframe(qdf, use_container_width=True, hide_index=True)

        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown("### Rezumat operațional")
        st.write(
            """
            Acest dashboard centralizează companiile alocate analistului și oferă o
            vedere rapidă asupra task-urilor curente: importuri în așteptare, cereri
            noi de raport și companii care necesită monitorizare prioritară.
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)