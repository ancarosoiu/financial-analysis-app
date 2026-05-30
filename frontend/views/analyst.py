import streamlit as st
import pandas as pd

from api import (
    get_analyst_dashboard_stats,
    get_companies,
    get_analyst_uploads,
    review_upload,
    download_upload_file,
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

        div[data-testid="stHorizontalBlock"] {
            align-items: center;
        }

        /* =========================
           FIX SELECTBOX ANALIST
           Face textul selectat vizibil în căsuța de filtrare
        ========================= */

        div[data-testid="stSelectbox"] {
            color: #111827 !important;
        }

        div[data-testid="stSelectbox"] label p {
            color: #111827 !important;
            font-weight: 800 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] {
            background: #ffffff !important;
            border-radius: 10px !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
            min-height: 46px !important;
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
            box-shadow: none !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] div {
            background: #ffffff !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] *,
        div[data-testid="stSelectbox"] [data-baseweb="select"] span,
        div[data-testid="stSelectbox"] [data-baseweb="select"] input,
        div[data-testid="stSelectbox"] [data-baseweb="select"] div[role="combobox"] {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            opacity: 1 !important;
            visibility: visible !important;
            font-weight: 650 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] input::placeholder {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            opacity: 1 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
            color: #64748b !important;
            fill: #64748b !important;
            stroke: #64748b !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] svg path {
            fill: #64748b !important;
            stroke: #64748b !important;
        }

        div[data-baseweb="popover"] {
            background: #ffffff !important;
            z-index: 999999 !important;
        }

        div[data-baseweb="popover"] ul {
            background: #ffffff !important;
            border-radius: 10px !important;
            border: 1px solid #cbd5e1 !important;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18) !important;
            padding: 6px !important;
        }

        div[data-baseweb="popover"] li,
        div[data-baseweb="popover"] li *,
        div[data-baseweb="popover"] [role="option"],
        div[data-baseweb="popover"] [role="option"] * {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            background: #ffffff !important;
            opacity: 1 !important;
            font-weight: 500 !important;
        }

        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="popover"] li[aria-selected="true"],
        div[data-baseweb="popover"] [role="option"]:hover,
        div[data-baseweb="popover"] [role="option"][aria-selected="true"] {
            background: #eef4ff !important;
            color: #111827 !important;
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


def _close_review_modal():
    st.session_state.selected_review_upload = None


def _clear_review_modal_on_filter_change():
    st.session_state.selected_review_upload = None


def _set_flash_message(message: str, message_type: str = "success"):
    st.session_state.analyst_flash_message = message
    st.session_state.analyst_flash_type = message_type


def _show_flash_message():
    message = st.session_state.pop("analyst_flash_message", None)
    message_type = st.session_state.pop("analyst_flash_type", "success")

    if not message:
        return

    if message_type == "success":
        st.success(message)
    elif message_type == "warning":
        st.warning(message)
    else:
        st.error(message)


@st.dialog("Verificare import financiar", width="large")
def render_review_import_modal(upload: dict):
    upload_id = upload.get("id")

    if upload.get("status") != "pending":
        _close_review_modal()
        _set_flash_message(
            "Acest import a fost deja procesat și nu mai poate fi aprobat sau respins manual.",
            "warning",
        )
        st.rerun()

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

    st.markdown(
        '<div class="review-modal-section-title">Detalii import</div>',
        unsafe_allow_html=True,
    )

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

    download_result = download_upload_file(
        upload_id=upload_id,
        access_token=st.session_state.access_token,
    )

    if download_result.get("success"):
        st.download_button(
            label="Descarcă fișierul Excel",
            data=download_result.get("content"),
            file_name=upload.get("file_name") or f"import_{upload_id}.xlsx",
            mime=download_result.get(
                "content_type",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            use_container_width=True,
            key=f"download_upload_{upload_id}",
        )
    else:
        st.warning(
            download_result.get(
                "message",
                "Fișierul nu poate fi descărcat.",
            )
        )

    st.markdown(
        """
        <div class="review-warning-box">
            <div class="review-warning-title">Acțiune necesară</div>
            <div class="review-warning-text">
                Acest import este în așteptarea validării. Descarcă fișierul Excel,
                verifică datele încărcate de client, apoi aprobă sau respinge importul.
                Dacă îl aprobi, sistemul va procesa fișierul, va calcula indicatorii financiari
                și va actualiza dashboard-ul clientului. Dacă îl respingi, clientul va vedea
                motivul respingerii în istoricul importurilor.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reason = st.text_area(
        "Motiv respingere",
        key=f"modal_reject_reason_{upload_id}",
        placeholder="Completează motivul doar dacă vrei să respingi importul...",
        height=110,
    )

    st.caption("Motivul este obligatoriu doar pentru respingerea importului.")

    col_cancel, col_reject, col_approve = st.columns([1, 1, 1])

    with col_cancel:
        cancel_clicked = st.button(
            "Anulează",
            use_container_width=True,
            key=f"cancel_modal_{upload_id}",
        )

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

    if cancel_clicked:
        _close_review_modal()
        st.rerun()

    if reject_clicked:
        clean_reason = reason.strip()

        if not clean_reason:
            st.warning("Completează motivul respingerii.")
            return

        with st.spinner("Se respinge importul..."):
            response = review_upload(
                upload_id=upload_id,
                decision="reject",
                access_token=st.session_state.access_token,
                reason=clean_reason,
            )

        if response.get("success"):
            _close_review_modal()
            _set_flash_message("Importul a fost respins cu succes.", "success")
            st.rerun()

        message = response.get("message", "Respingerea importului a eșuat.")
        _close_review_modal()
        _set_flash_message(
            f"Importul nu mai poate fi respins manual. Detalii: {message}",
            "error",
        )
        st.rerun()

    if approve_clicked:
        with st.spinner("Se procesează fișierul și se calculează KPI-urile..."):
            response = review_upload(
                upload_id=upload_id,
                decision="approve",
                access_token=st.session_state.access_token,
            )

        if response.get("success"):
            _close_review_modal()
            _set_flash_message(
                "Importul a fost aprobat. KPI-urile au fost calculate și dashboard-ul clientului a fost actualizat.",
                "success",
            )
            st.rerun()

        message = response.get("message", "Aprobarea importului a eșuat.")
        _close_review_modal()
        _set_flash_message(
            f"Procesarea importului a eșuat. Importul a fost respins automat. Detalii: {message}",
            "error",
        )
        st.rerun()


def render_upload_actions(upload: dict):
    status = upload.get("status")

    if status != "pending":
        status_text = _status_label(status).lower()
        st.markdown(
            f"""
            <div class="table-sub-text">
                Import {status_text}
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if st.button(
        "Acțiuni",
        key=f"actions_{upload.get('id')}",
        use_container_width=True,
    ):
        st.session_state.selected_review_upload = upload
        st.rerun()


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

    _show_flash_message()

    top_left, top_right = st.columns([2.4, 1], vertical_alignment="bottom")

    with top_left:
        st.markdown(
            """
            <div class="small-section-title">Lista importurilor</div>
            """,
            unsafe_allow_html=True,
        )

    status_map = {
        "În așteptare": "pending",
        "Aprobat": "approved",
        "Respins": "rejected",
        "Toate": "all",
    }

    status_options = list(status_map.keys())

    if "analyst_upload_status_filter" not in st.session_state:
        st.session_state.analyst_upload_status_filter = "În așteptare"

    with top_right:
        selected_status_label = st.selectbox(
            "Filtrează după status",
            options=status_options,
            index=(
                status_options.index(st.session_state.analyst_upload_status_filter)
                if st.session_state.analyst_upload_status_filter in status_options
                else 0
            ),
            key="analyst_upload_status_filter",
            on_change=_clear_review_modal_on_filter_change,
        )

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

    selected_upload = st.session_state.get("selected_review_upload")

    if selected_upload and selected_upload.get("status") == "pending":
        render_review_import_modal(selected_upload)
    else:
        st.session_state.selected_review_upload = None


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
            metric_card(
                "Firme asignate",
                stats.get("total_firme", 0),
                "Portofoliu curent",
            ),
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            metric_card(
                "Importuri noi",
                stats.get("importuri_noi", 0),
                "În așteptare",
            ),
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            metric_card(
                "Cereri rapoarte",
                stats.get("cereri_rapoarte_noi", 0),
                "Pending",
            ),
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            metric_card(
                "Firme risc ridicat",
                stats.get("firme_risc_ridicat", 0),
                "Monitorizare",
            ),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Importuri", "Firme asignate"])

    with tab1:
        render_uploads_section()

    with tab2:
        render_companies_table()