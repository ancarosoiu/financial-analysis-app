import streamlit as st
import pandas as pd

from api import (
    get_analyst_dashboard_stats,
    get_companies,
    get_analyst_uploads,
    review_upload,
)

from views.styles import metric_card


def _render_analyst_styles_override():
    st.markdown(
        """
        <style>
        .stApp {
            background: #f4f7fb !important;
        }

        .block-container {
            max-width: 1280px !important;
            padding-top: 1.4rem !important;
            padding-bottom: 2rem !important;
        }

        /* Pe pagina analistului NU vrem tab-uri înguste ca la login */
        .stTabs {
            max-width: 100% !important;
            width: 100% !important;
            margin: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            padding: 0 !important;
            border-radius: 0 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            max-width: 520px !important;
            background: white !important;
            padding: 6px !important;
            border-radius: 14px !important;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06) !important;
            margin-bottom: 1.3rem !important;
        }

        .stTabs [data-baseweb="tab"] {
            height: 44px !important;
            border-radius: 10px !important;
            font-weight: 750 !important;
        }

        .stTabs [aria-selected="true"] {
            background: #2563eb !important;
            color: white !important;
        }

        .stTabs [aria-selected="true"] p {
            color: white !important;
        }

        /* Rândurile din tabel să fie mai aerisite */
        div[data-testid="stHorizontalBlock"] {
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _status_label(status: str):
    labels = {
        "pending": "În așteptare",
        "approved": "Aprobat",
        "rejected": "Respins",
    }
    return labels.get(status, status)


def _status_badge(status: str):
    label = _status_label(status)

    if status == "approved":
        css_class = "status-badge-approved"
    elif status == "rejected":
        css_class = "status-badge-rejected"
    else:
        css_class = "status-badge-pending"

    return f'<span class="status-badge {css_class}">{label}</span>'

@st.dialog("Review Financial Import", width="large")
def render_review_import_modal(upload: dict):
    upload_id = upload.get("id")

    st.markdown(
        f"""
        <div class="review-modal-header">
            <div class="review-modal-icon">▤</div>
            <div>
                <div class="review-modal-title">Verificare import financiar</div>
                <div class="review-modal-subtitle">
                    Aprobă sau respinge fișierul încărcat de client.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="review-modal-section-title">Detalii import</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="review-details-box">
            <div class="review-detail-row">
                <span>Companie</span>
                <strong>{upload.get("company_name")}</strong>
            </div>
            <div class="review-detail-row">
                <span>CUI</span>
                <strong>{upload.get("cui")}</strong>
            </div>
            <div class="review-detail-row">
                <span>Client</span>
                <strong>{upload.get("client_username")}</strong>
            </div>
            <div class="review-detail-row">
                <span>Fișier</span>
                <strong>{upload.get("file_name")}</strong>
            </div>
            <div class="review-detail-row">
                <span>Încărcat la</span>
                <strong>{upload.get("uploaded_at")}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="review-warning-box">
            <div class="review-warning-title">Acțiune necesară</div>
            <div class="review-warning-text">
                Acest import este în așteptarea validării. Dacă îl aprobi, sistemul va procesa fișierul,
                va calcula indicatorii financiari și va activa dashboard-ul clientului.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reason = st.text_area(
        "Motiv respingere",
        key=f"modal_reject_reason_{upload_id}",
        placeholder="Completează motivul respingerii doar dacă vrei să respingi importul...",
        height=110,
    )

    st.caption("Motivul este obligatoriu doar pentru respingerea importului.")

    col_cancel, col_reject, col_approve = st.columns([1, 1, 1])

    with col_cancel:
        if st.button("Anulează", use_container_width=True, key=f"cancel_modal_{upload_id}"):
            st.rerun()

    with col_reject:
        reject_clicked = st.button(
            "Respinge",
            use_container_width=True,
            key=f"modal_reject_{upload_id}",
        )

    with col_approve:
        approve_clicked = st.button(
            "Aprobă importul",
            use_container_width=True,
            key=f"modal_approve_{upload_id}",
        )

    if approve_clicked:
        with st.spinner("Se procesează fișierul și se calculează KPI-urile..."):
            response = review_upload(
                upload_id=upload_id,
                decision="approve",
                access_token=st.session_state.access_token,
            )

        if response.get("success"):
            st.success("Import aprobat. KPI-urile au fost calculate.")
            st.rerun()
        else:
            st.error(response.get("message", "Aprobarea importului a eșuat."))

    if reject_clicked:
        if not reason:
            st.warning("Completează motivul respingerii.")
            return

        with st.spinner("Se respinge importul..."):
            response = review_upload(
                upload_id=upload_id,
                decision="reject",
                access_token=st.session_state.access_token,
                reason=reason,
            )

        if response.get("success"):
            st.success("Import respins.")
            st.rerun()
        else:
            st.error(response.get("message", "Respingerea importului a eșuat."))


def render_upload_actions(upload: dict):
    status = upload.get("status")

    if status != "pending":
        st.caption("Procesat")
        return

    if st.button(
        "Acțiuni",
        key=f"actions_{upload.get('id')}",
        use_container_width=True,
    ):
        render_review_import_modal(upload)

def render_upload_row(upload: dict):
    status = upload.get("status")

    with st.container(border=True):
        col_company, col_file, col_date, col_status, col_actions = st.columns(
            [2.4, 2.6, 1.5, 1.3, 1.7],
            vertical_alignment="center",
        )

        with col_company:
            st.markdown(
                f"""
                <div class="table-main-text">{upload.get("company_name")}</div>
                <div class="table-sub-text">
                    CUI: {upload.get("cui")} · Client: {upload.get("client_username")}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_file:
            st.markdown(
                f"""
                <div class="table-main-text">{upload.get("file_name")}</div>
                <div class="table-sub-text">
                    Domeniu: {upload.get("industry") or "N/A"}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_date:
            st.markdown(
                f"""
                <div class="table-main-text">{upload.get("uploaded_at")}</div>
                <div class="table-sub-text">
                    Procesat: {upload.get("processed_at") or "—"}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_status:
            st.markdown(_status_badge(status), unsafe_allow_html=True)

        with col_actions:
            render_upload_actions(upload)

    if status == "rejected" and upload.get("rejection_reason"):
        st.markdown(
            f"""
            <div class="reject-reason-box">
                <strong>Motiv respingere:</strong> {upload.get("rejection_reason")}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_uploads_table(uploads: list):
    st.markdown(
        """
        <div class="uploads-table-header">
            <div>Companie</div>
            <div>Fișier</div>
            <div>Data încărcării</div>
            <div>Status</div>
            <div>Acțiuni</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for upload in uploads:
        render_upload_row(upload)


def render_uploads_section():
    st.markdown(
        """
        <div class="analyst-section-header">
            <div>
                <div class="analyst-section-title">Importuri financiare</div>
                <div class="analyst-section-subtitle">
                    Verifică și procesează fișierele încărcate de clienți. Importurile în așteptare apar implicit primele.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns([2.4, 1], vertical_alignment="bottom")

    with top_left:
        st.markdown(
            """
            <div class="small-section-title">Lista importurilor</div>
            """,
            unsafe_allow_html=True,
        )

    with top_right:
        selected_status_label = st.selectbox(
            "Filtrează după status",
            [
                "În așteptare",
                "Aprobat",
                "Respins",
                "Toate",
            ],
        )

    status_map = {
        "În așteptare": "pending",
        "Aprobat": "approved",
        "Respins": "rejected",
        "Toate": "all",
    }

    selected_status = status_map[selected_status_label]

    result = get_analyst_uploads(
        access_token=st.session_state.access_token,
        status=selected_status,
    )

    if not result.get("success"):
        st.error(result.get("message", "Nu s-au putut încărca importurile."))
        return

    uploads = result.get("data", [])

    if not uploads:
        st.info("Nu există importuri pentru filtrul selectat.")
        return

    render_uploads_table(uploads)


def render_companies_table():
    st.markdown(
        """
        <div class="analyst-section-title small">Firme asignate</div>
        """,
        unsafe_allow_html=True,
    )

    result = get_companies(st.session_state.access_token)

    if not result.get("success"):
        st.warning(result.get("message", "Companiile nu au putut fi încărcate."))
        return

    companies = result.get("data", [])

    if not companies:
        st.info("Nu există firme asignate.")
        return

    df = pd.DataFrame(companies)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_analyst_dashboard():
    _render_analyst_styles_override()

    st.markdown(
        f"""
        <div class="dashboard-header">
            <div>
                <div class="page-title-dark">Dashboard analist</div>
                <div class="page-subtitle-dark">
                    Gestionează importurile, firmele asignate și cererile de raportare.
                </div>
            </div>
            <div class="user-chip">{st.session_state.username}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stats_result = get_analyst_dashboard_stats(st.session_state.access_token)

    if stats_result.get("success"):
        stats = stats_result.get("data", {})
    else:
        stats = {}

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            metric_card("Firme asignate", stats.get("total_firme", 0), "Portofoliu curent"),
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            metric_card("Importuri noi", stats.get("importuri_noi", 0), "În așteptare"),
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            metric_card("Cereri rapoarte", stats.get("cereri_rapoarte_noi", 0), "Pending"),
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            metric_card("Firme risc ridicat", stats.get("firme_risc_ridicat", 0), "Monitorizare"),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Importuri", "Firme asignate"])

    with tab1:
        render_uploads_section()

    with tab2:
        render_companies_table()