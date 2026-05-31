import streamlit as st
from html import escape

from api import (
    get_analyst_dashboard_stats,
    get_companies,
    get_analyst_uploads,
    review_upload,
    download_upload_file,
)

from views.styles import load_analyst_styles


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


def _render_analyst_header(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="analyst-page-header">
            <div>
                <div class="analyst-page-title">{title}</div>
                <div class="analyst-page-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _analyst_stat_card(title: str, value, caption: str):
    return f"""
    <div class="analyst-stat-card">
        <div class="analyst-stat-title">{title}</div>
        <div class="analyst-stat-value">{value}</div>
        <div class="analyst-stat-caption">{caption}</div>
    </div>
    """


def _safe_company_value(company: dict, *keys, default="—"):
    for key in keys:
        value = company.get(key)
        if value not in [None, ""]:
            return escape(str(value))
    return default


def _render_companies_table(companies: list):
    rows_html = ""

    for company in companies:
        name = _safe_company_value(company, "nume", "name")
        cui = _safe_company_value(company, "cui")
        industry = _safe_company_value(company, "industrie", "industry")
        address = _safe_company_value(company, "adresa", "address")
        email = _safe_company_value(company, "email", "email_contact")
        phone = _safe_company_value(company, "telefon", "phone", "phone_number")
        owner = _safe_company_value(company, "owner_username", "client_username", "owner")
        onboarded = company.get("status_onboarded", company.get("is_onboarded", False))

        if onboarded:
            status_badge = '<span class="company-status-badge company-status-active">Activă</span>'
        else:
            status_badge = '<span class="company-status-badge company-status-pending">În configurare</span>'

        rows_html += f"""
        <div class="analyst-company-row">
            <div>
                <div class="analyst-company-main">{name}</div>
                <div class="analyst-company-sub">Client: {owner}</div>
            </div>

            <div>
                <div class="analyst-company-main">{cui}</div>
            </div>

            <div>
                <div class="analyst-company-main">{industry}</div>
                <div class="analyst-company-sub">{address}</div>
            </div>

            <div>
                <div class="analyst-company-main">{email}</div>
                <div class="analyst-company-sub">{phone}</div>
            </div>

            <div>
                {status_badge}
            </div>
        </div>
        """

    table_html = f"""
    <div class="analyst-company-table-card">
        <div class="analyst-company-table-title">Lista firmelor asignate</div>
        <div class="analyst-company-table-subtitle">
            Firmele monitorizate de analist și principalele informații de identificare.
        </div>

        <div class="analyst-company-table">
            <div class="analyst-company-header">
                <div>Companie</div>
                <div>CUI</div>
                <div>Domeniu</div>
                <div>Contact</div>
                <div>Status</div>
            </div>

            {rows_html}
        </div>
    </div>
    """

    st.html(table_html)


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
        """
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
    upload_id = upload.get("id")
    status = upload.get("status")

    if status == "pending":
        st.markdown(
            '<div class="analyst-action-button-anchor"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Acțiuni",
            key=f"actions_{upload_id}",
            use_container_width=True,
        ):
            st.session_state.selected_review_upload = upload
            st.rerun()

        return

    if not upload_id:
        st.markdown(
            """
            <div class="analyst-muted-action">
                Fișier indisponibil
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    download_result = download_upload_file(
        upload_id=upload_id,
        access_token=st.session_state.access_token,
    )

    if download_result.get("success"):
        st.download_button(
            label="Descarcă",
            data=download_result.get("content"),
            file_name=upload.get("file_name") or f"import_{upload_id}.xlsx",
            mime=download_result.get(
                "content_type",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            use_container_width=True,
            key=f"analyst_download_upload_{upload_id}",
        )
    else:
        st.markdown(
            """
            <div class="analyst-muted-action">
                Fișier indisponibil
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_upload_row(upload: dict):
    status = upload.get("status")

    company_name = escape(str(upload.get("company_name") or "—"))
    cui = escape(str(upload.get("cui") or "—"))
    client_username = escape(str(upload.get("client_username") or "—"))
    file_name = escape(str(upload.get("file_name") or "Fișier necunoscut"))
    industry = escape(str(upload.get("industry") or "N/A"))
    uploaded_at = escape(str(upload.get("uploaded_at") or "—"))
    processed_at = escape(str(upload.get("processed_at") or "—"))

    col_company, col_file, col_date, col_status, col_actions = st.columns(
        [2.05, 2.05, 1.35, 0.95, 1.1],
        vertical_alignment="center",
    )

    with col_company:
        st.markdown(
            f"""
            <div class="analyst-import-main">{company_name}</div>
            <div class="analyst-import-sub">
                CUI: {cui} · Client: {client_username}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_file:
        st.markdown(
            f"""
            <div class="analyst-import-main">{file_name}</div>
            <div class="analyst-import-sub">
                Domeniu: {industry}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_date:
        st.markdown(
            f"""
            <div class="analyst-import-main">{uploaded_at}</div>
            <div class="analyst-import-sub">
                Procesat: {processed_at}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_status:
        st.markdown(
            _status_badge(status),
            unsafe_allow_html=True,
        )

    with col_actions:
        render_upload_actions(upload)

    st.markdown(
        '<div class="analyst-import-row-divider"></div>',
        unsafe_allow_html=True,
    )


def render_analyst_imports_header(status_options: list):
    with st.container():
        st.markdown(
            '<div class="analyst-import-card-anchor"></div>',
            unsafe_allow_html=True,
        )

        top_left, top_right = st.columns([2.6, 1], vertical_alignment="bottom")

        with top_left:
            st.markdown(
                """
                <div class="analyst-import-table-top">
                    <div class="analyst-import-table-title">Lista importurilor</div>
                    <div class="analyst-import-table-subtitle">
                        Importurile în așteptare necesită verificare finală din partea analistului.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

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

        st.markdown(
            """
            <div class="analyst-import-header">
                <div>Companie</div>
                <div>Fișier</div>
                <div>Data încărcării</div>
                <div>Status</div>
                <div>Acțiuni</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected_status_label

def render_uploads_table(uploads: list):
    if not uploads:
        st.markdown(
            """
            <div class="analyst-import-empty-row">
                Nu există importuri pentru filtrul selectat.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for upload in uploads:
        render_upload_row(upload)


def render_analyst_imports_page():
    load_analyst_styles()

    _render_analyst_header(
        "Importuri financiare",
        "Verifică fișierele încărcate de clienți, descarcă documentele Excel și aprobă sau respinge importurile."
    )

    _show_flash_message()

    status_map = {
        "În așteptare": "pending",
        "Aprobat": "approved",
        "Respins": "rejected",
        "Toate": "all",
    }

    status_options = list(status_map.keys())

    if "analyst_upload_status_filter" not in st.session_state:
        st.session_state.analyst_upload_status_filter = "În așteptare"

    selected_status_label = render_analyst_imports_header(status_options)
    selected_status = status_map[selected_status_label]

    result = get_analyst_uploads(
        access_token=st.session_state.access_token,
        status=selected_status,
    )

    if not result.get("success"):
        st.error(result.get("message", "Nu s-au putut încărca importurile."))
        return

    uploads = result.get("data", [])

    render_uploads_table(uploads)

    selected_upload = st.session_state.get("selected_review_upload")

    if selected_upload and selected_upload.get("status") == "pending":
        render_review_import_modal(selected_upload)
    else:
        st.session_state.selected_review_upload = None


def render_analyst_portfolio_page():
    load_analyst_styles()

    _render_analyst_header(
        "Portofoliu firme",
        "Monitorizează firmele asignate, importurile active și situațiile care necesită atenție."
    )

    stats_result = get_analyst_dashboard_stats(st.session_state.access_token)

    if stats_result.get("success"):
        stats = stats_result.get("data", {})
    else:
        stats = {}

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            _analyst_stat_card(
                "Firme asignate",
                stats.get("total_firme", 0),
                "Portofoliu curent"
            ),
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            _analyst_stat_card(
                "Importuri noi",
                stats.get("importuri_noi", 0),
                "În așteptare"
            ),
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            _analyst_stat_card(
                "Cereri rapoarte",
                stats.get("cereri_rapoarte_noi", 0),
                "Solicitări client"
            ),
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            _analyst_stat_card(
                "Firme risc ridicat",
                stats.get("firme_risc_ridicat", 0),
                "Monitorizare"
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="analyst-hero analyst-hero-spaced">
            <div class="analyst-hero-eyebrow">Portofoliu</div>
            <div class="analyst-hero-title">Firme asignate analistului</div>
            <div class="analyst-hero-text">
                Această secțiune centralizează firmele aflate în responsabilitatea analistului.
                Poți urmări rapid firmele active, domeniul de activitate și datele principale de contact.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = get_companies(st.session_state.access_token)

    if not result.get("success"):
        st.error(result.get("message", "Companiile nu au putut fi încărcate."))
        return

    companies = result.get("data", [])

    if not companies:
        st.markdown(
            """
            <div class="analyst-empty-card">
                Nu există firme asignate acestui analist.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    _render_companies_table(companies)


def render_analyst_reports_page():
    load_analyst_styles()

    _render_analyst_header(
        "Rapoarte",
        "Gestionează solicitările de rapoarte și pregătește recomandări personalizate pentru clienți."
    )

    st.markdown(
        """
        <div class="analyst-hero">
            <div class="analyst-hero-eyebrow">În lucru</div>
            <div class="analyst-hero-title">Flux rapoarte personalizate</div>
            <div class="analyst-hero-text">
                Aici vom integra solicitările de rapoarte, completarea recomandărilor de către analist
                și generarea documentului PDF pentru client. Începem această secțiune după ce finalizăm pagina de importuri.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="analyst-empty-card">
            Pagina de rapoarte este pregătită ca structură. Următorul pas este integrarea logicii de backend pentru cereri,
            completare raport și generare PDF.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_analyst_dashboard():
    render_analyst_portfolio_page()