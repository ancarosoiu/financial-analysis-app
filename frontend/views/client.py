import streamlit as st
import pandas as pd
import ast
import plotly.express as px
from html import escape
from datetime import datetime,date, timedelta

from api import (
    create_company,
    get_client_dashboard,
    upload_financial_file,
    get_upload_history,
    download_upload_file,
    get_standard_reports,
    download_standard_report,
    create_report_request,
    get_client_report_requests,
    download_custom_report,
)

def _safe_float(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default

def _init_onboarding_state():
    company_id = st.session_state.get("company_id")

    if "onboarding_step" not in st.session_state:
        if company_id:
            st.session_state.onboarding_step = 2
        else:
            st.session_state.onboarding_step = 1

    if "onboarding_company_id" not in st.session_state:
        st.session_state.onboarding_company_id = company_id

    if "onboarding_company_name" not in st.session_state:
        st.session_state.onboarding_company_name = ""

    if "onboarding_uploaded_file" not in st.session_state:
        st.session_state.onboarding_uploaded_file = ""

def _render_onboarding_styles_override():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(59, 130, 246, 0.14), transparent 30%),
                radial-gradient(circle at bottom right, rgba(14, 165, 233, 0.10), transparent 32%),
                linear-gradient(180deg, #eaf1fb 0%, #f4f7fb 52%, #edf4fb 100%) !important;
        }

        .block-container {
            max-width: 1080px !important;
            padding-top: 0.7rem !important;
            padding-bottom: 1.2rem !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_stepper(step: int):
    steps = [
        {"number": 1, "label": "Date firmă"},
        {"number": 2, "label": "Încărcare date"},
        {"number": 3, "label": "Confirmare"},
    ]

    html = '<div class="onboarding-stepper">'

    for item in steps:
        number = item["number"]

        if number < step:
            circle_class = "step-circle done"
            symbol = "✓"
        elif number == step:
            circle_class = "step-circle active"
            symbol = str(number)
        else:
            circle_class = "step-circle idle"
            symbol = str(number)

        html += f"""
        <div class="step-item">
            <div class="{circle_class}">{symbol}</div>
            <div class="step-text">{item["label"]}</div>
        </div>
        """

        if number < 3:
            line_class = "step-line active-line" if number < step else "step-line"
            html += f'<div class="{line_class}"></div>'

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

def render_company_step():
    st.markdown(
        """
        <div class="onboarding-card">
            <div class="onboarding-icon">▤</div>
            <div class="onboarding-card-title">Informații companie</div>
            <div class="onboarding-card-subtitle">
                Completează datele de identificare ale firmei tale
            </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("company_form", clear_on_submit=False):
        name = st.text_input(
            "Denumire companie",
            placeholder="SC Exemplu SRL"
        )

        cui = st.text_input(
            "CUI / Cod unic de înregistrare",
            placeholder="RO12345678"
        )

        address = st.text_input(
            "Adresă sediu social",
            placeholder="Str. Exemplu nr. 1, București"
        )

        industry = st.selectbox(
            "Domeniu de activitate",
            [
                "Selectează...",
                "IT & Software",
                "Comerț",
                "Producție",
                "Servicii financiare",
                "Construcții",
                "Transport",
                "HoReCa",
                "Sănătate",
                "Educație",
                "Alt domeniu",
            ],
        )

        col1, col2 = st.columns(2)

        with col1:
            phone = st.text_input(
                "Telefon",
                placeholder="0712345678"
            )

        with col2:
            email_contact = st.text_input(
                "Email contact",
                placeholder="office@firma.ro"
            )

        submitted = st.form_submit_button("Continuă", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not name or not cui:
            st.error("Denumirea companiei și CUI-ul sunt obligatorii.")
            return

        if industry == "Selectează...":
            st.error("Selectează domeniul de activitate.")
            return

        payload = {
            "name": name,
            "cui": cui,
            "industry": industry,
            "address": address,
            "phone_number": phone,
            "email_contact": email_contact,
        }

        with st.spinner("Se creează compania..."):
            result = create_company(payload, st.session_state.access_token)

        if result.get("success"):
            data = result.get("data", {})

            st.session_state.company_id = data.get("company_id")
            st.session_state.onboarding_company_id = data.get("company_id")
            st.session_state.onboarding_company_name = data.get("company_name", name)

            if data.get("is_onboarded"):
                st.session_state.is_onboarded = True
                st.session_state.page = "client_dashboard"
            else:
                st.session_state.onboarding_step = 2

            st.success(data.get("message", "Compania a fost salvată cu succes."))
            st.rerun()

        else:
            st.error(result.get("message", "Datele companiei nu au putut fi salvate."))
            return

def render_upload_step():
    st.html(
        """
        <div class="onboarding-upload-card">
            <div class="onboarding-upload-icon">↑</div>
            <div class="onboarding-upload-title">Încărcare date financiare</div>
            <div class="onboarding-upload-subtitle">
                Încarcă fișierul Excel cu bilanț contabil și cont de profit și pierdere.
            </div>

            <div class="onboarding-upload-note">
                <div class="onboarding-upload-note-title">Fișier necesar pentru analiză</div>
                <div class="onboarding-upload-note-text">
                    Selectează un fișier Excel în format .xlsx sau .xls.
                    Datele vor fi trimise către analist pentru validare înainte de calculul KPI-urilor.
                </div>
            </div>
        </div>
        """
    )

    upload_left, upload_center, upload_right = st.columns([0.55, 4.9, 0.55])

    with upload_center:
        uploaded_file = st.file_uploader(
            "",
            type=["xlsx", "xls"],
            key="onboarding_financial_file",
            help="Încarcă fișierul cu date financiare. Format acceptat: .xlsx sau .xls.",
            label_visibility="collapsed",
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Înapoi", use_container_width=True):
                st.session_state.onboarding_step = 1
                st.rerun()

        with col2:
            upload_clicked = st.button("Trimite spre validare", use_container_width=True)

    if upload_clicked:
        if uploaded_file is None:
            st.error("Încarcă un fișier Excel înainte de trimitere.")
            return

        company_id = st.session_state.company_id or st.session_state.onboarding_company_id

        if not company_id:
            st.error("Nu există companie asociată contului.")
            return

        with st.spinner("Se încarcă fișierul..."):
            result = upload_financial_file(
                company_id=company_id,
                file=uploaded_file,
                access_token=st.session_state.access_token,
            )

        if result.get("success"):
            st.session_state.onboarding_uploaded_file = uploaded_file.name
            st.session_state.onboarding_step = 3
            st.success("Fișierul a fost trimis spre validare.")
            st.rerun()
        else:
            errors = result.get("errors", {})

            if errors.get("code") == "monthly_approved_upload_exists":
                st.warning(
                    "Nu poți încărca un import nou deoarece există deja un import aprobat pentru luna curentă."
                )
            else:
                st.error(result.get("message", "Încărcarea fișierului a eșuat."))

def render_confirm_step():
    company_name = st.session_state.onboarding_company_name or "Companie înregistrată"
    uploaded_file = st.session_state.onboarding_uploaded_file or "Fișier încărcat"

    st.html(
        f"""
        <div class="onboarding-card">
            <div class="onboarding-icon success">✓</div>
            <div class="onboarding-card-title">Confirmare și finalizare</div>
            <div class="onboarding-card-subtitle">
                Datele au fost trimise către fluxul de validare.
            </div>
        </div>
        """
    )

    left, center, right = st.columns([1, 2.2, 1])

    with center:
        st.html(
            f"""
            <div class="confirm-panel">
                <div class="confirm-title">Rezumat trimitere</div>

                <div class="confirm-summary">
                    <div class="confirm-row">
                        <span>Companie</span>
                        <strong>{company_name}</strong>
                    </div>

                    <div class="confirm-row">
                        <span>Fișier încărcat</span>
                        <strong>{uploaded_file}</strong>
                    </div>

                    <div class="confirm-row">
                        <span>Status</span>
                        <strong>În așteptare validare</strong>
                    </div>
                </div>

                <div class="validation-note">
                    Datele tale vor fi procesate și validate de un analist financiar.
                    Vei primi o notificare când analiza este completă.
                </div>
            </div>
            """
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Înapoi la încărcare", use_container_width=True):
                st.session_state.onboarding_step = 2
                st.session_state.show_finalize_message = False
                st.rerun()

        with col2:
            if st.button("Finalizează", use_container_width=True):
                st.session_state.show_finalize_message = True

        if st.session_state.get("show_finalize_message", False):
            st.success(
                "Importul a fost trimis spre validare. "
                "După aprobare, dashboard-ul va deveni activ."
            )

def render_upload_history():
    st.markdown(
        '<div class="history-title">Istoric importuri</div>',
        unsafe_allow_html=True,
    )

    company_id = st.session_state.company_id or st.session_state.onboarding_company_id

    if not company_id:
        st.info("Istoricul importurilor va fi disponibil după crearea companiei.")
        return

    result = get_upload_history(
        company_id=company_id,
        access_token=st.session_state.access_token,
    )

    if not result.get("success"):
        st.warning(result.get("message", "Istoricul importurilor nu a putut fi încărcat."))
        return

    data = result.get("data", [])

    if not data:
        st.info("Nu există încă importuri.")
        return

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_client_onboarding():
    _render_onboarding_styles_override()
    _init_onboarding_state()

    render_stepper(st.session_state.onboarding_step)

    if st.session_state.onboarding_step == 1:
        render_company_step()
    elif st.session_state.onboarding_step == 2:
        render_upload_step()
    elif st.session_state.onboarding_step == 3:
        render_confirm_step()

def _upload_status_label(status: str):
    labels = {
        "pending": "În așteptare",
        "approved": "Aprobat",
        "rejected": "Respins",
    }
    return labels.get(status, status)

def _upload_status_badge(status: str):
    label = _upload_status_label(status)

    if status == "approved":
        css_class = "client-import-status-approved"
    elif status == "rejected":
        css_class = "client-import-status-rejected"
    else:
        css_class = "client-import-status-pending"

    return f'<span class="client-import-status-badge {css_class}">{label}</span>'

def _clean_rejection_reason(reason):
    if not reason:
        return ""

    text = str(reason).strip()

    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list) and parsed:
            text = str(parsed[0])
    except Exception:
        pass

    text = text.strip().strip("'").strip('"')
    text = text.replace("\\n", "\n")
    return text.strip()

def _friendly_column_name(column_name):
    labels = {
        "reporting_date": "Data raportării",
        "net_profit": "Profit net",
        "ebit": "EBIT",
        "sales_revenue": "Venituri din vânzări",
        "depreciation": "Amortizare",
        "operating_expenses": "Cheltuieli operaționale",
        "total_assets": "Active totale",
        "current_assets": "Active curente",
        "inventory": "Stocuri",
        "cash": "Numerar",
        "total_liabilities": "Datorii totale",
        "short_term_liabilities": "Datorii pe termen scurt",
        "equity": "Capitaluri proprii",
        "retained_earnings": "Profit reținut",
        "short_term_securities": "Titluri pe termen scurt",
        "receivables": "Creanțe",
        "gross_profit": "Profit brut",
        "extraordinary_items": "Elemente extraordinare",
        "financial_expenses": "Cheltuieli financiare",
        "interest": "Dobânzi",
        "share_capital": "Capital social",
        "profit_on_operating_activities": "Profit din activitatea operațională",
        "gross_profit_3_years": "Profit brut cumulat pe 3 ani",
        "cost_of_products_sold": "Costul produselor vândute",
        "profit_on_sales": "Profit din vânzări",
        "total_costs": "Costuri totale",
        "previous_period_sales": "Vânzările perioadei anterioare",
    }

    clean_name = str(column_name).strip().strip("'").strip('"').strip()
    return labels.get(clean_name, clean_name)

def _extract_missing_columns(reason):
    text = _clean_rejection_reason(reason)

    if "Lipsesc coloanele:" not in text:
        return []

    _, after = text.split("Lipsesc coloanele:", 1)

    for separator in ["Te rugăm", "Te rugam"]:
        if separator in after:
            after = after.split(separator, 1)[0]

    after = after.replace("[", "").replace("]", "")
    after = after.replace("'", "").replace('"', "")
    after = after.replace("\n", ",")

    return [
        _friendly_column_name(col)
        for col in after.split(",")
        if col.strip()
    ]

def _rejection_summary(reason):
    text = _clean_rejection_reason(reason)
    missing_columns = _extract_missing_columns(reason)

    if missing_columns:
        return {
            "title": "Fișier incomplet",
            "short": f"Lipsesc {len(missing_columns)} coloane financiare obligatorii.",
            "details": missing_columns,
            "type": "columns",
        }

    if not text:
        return {
            "title": "Import respins",
            "short": "Importul a fost respins de analist.",
            "details": [],
            "type": "text",
        }

    short_text = text
    if len(short_text) > 70:
        short_text = short_text[:70].rstrip() + "..."

    return {
        "title": "Import respins",
        "short": short_text,
        "details": [text],
        "type": "text",
    }

@st.dialog("Adauga import nou", width="large")
def render_add_import_modal():
    st.markdown(
        """
        <div class="review-modal-header">
            <div class="review-modal-icon">↑</div>
            <div>
                <div class="review-modal-title">Adaugă import financiar</div>
                <div class="review-modal-subtitle">
                    Încarcă un fișier Excel cu date financiare noi.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="review-warning-box">
            <div class="review-warning-title">Regulă import</div>
            <div class="review-warning-text">
                Poți încărca un import nou doar dacă nu există un import în așteptare
                și dacă a trecut cel puțin o lună de la ultimul import aprobat.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Fișier Excel",
        type=["xlsx", "xls"],
    )

    col_cancel, col_submit = st.columns([1, 1])

    with col_cancel:
        if st.button("Anulează", use_container_width=True):
            st.rerun()

    with col_submit:
        submit_clicked = st.button("Trimite importul", use_container_width=True)

    if submit_clicked:
        if uploaded_file is None:
            st.warning("Selectează un fișier Excel înainte de trimitere.")
            return

        company_id = st.session_state.company_id

        if not company_id:
            st.error("Nu există companie asociată contului.")
            return

        with st.spinner("Se încarcă importul..."):
            result = upload_financial_file(
                company_id=company_id,
                file=uploaded_file,
                access_token=st.session_state.access_token,
            )

        if result.get("success"):
            st.success("Importul a fost încărcat și trimis spre validare.")
            st.rerun()
            return

        errors = result.get("errors", {})
        code = errors.get("code")

        if code == "pending_import_exists":
            st.warning(result.get("message"))
        elif code == "too_soon_after_last_approved_import":
            st.warning(result.get("message"))
        else:
            st.error(result.get("message", "Încărcarea importului a eșuat."))

@st.dialog("Detalii respingere import", width="large")
def render_client_rejection_details_modal(upload: dict):
    summary = _rejection_summary(upload.get("motiv_respingere"))
    file_name = escape(str(upload.get("nume_fisier") or "Fișier necunoscut"))
    upload_date = escape(str(upload.get("data_incarcare") or "—"))

    st.markdown(
        f"""
        <div class="client-reject-modal-content">
            <div class="client-reject-modal-eyebrow">Import respins</div>
            <div class="client-reject-modal-title">{escape(summary["title"])}</div>
            <div class="client-reject-modal-subtitle">
                Fișier: <strong>{file_name}</strong><br>
                Data încărcării: <strong>{upload_date}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if summary["type"] == "columns":
        items_html = "".join(
            f"<li>{escape(item)}</li>"
            for item in summary["details"]
        )

        st.markdown(
            f"""
            <div class="client-reject-modal-box">
                <div class="client-reject-modal-box-title">
                    Coloane lipsă în fișier
                </div>
                <div class="client-reject-modal-box-text">
                    Fișierul nu conține toate coloanele financiare obligatorii.
                    Revizuiește structura fișierului Excel și reîncarcă un import valid.
                </div>
                <ul class="client-reject-modal-list">
                    {items_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        detail_text = summary["details"][0] if summary["details"] else "Importul a fost respins de analist."

        st.markdown(
            f"""
            <div class="client-reject-modal-box">
                <div class="client-reject-modal-box-title">
                    Motiv respingere
                </div>
                <div class="client-reject-modal-box-text">
                    {escape(detail_text)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_client_import_row(upload: dict):
    status = upload.get("status")
    file_name = escape(str(upload.get("nume_fisier") or "Fișier necunoscut"))
    upload_date = escape(str(upload.get("data_incarcare") or "—"))

    col_file, col_date, col_status, col_obs, col_action = st.columns(
        [2.05, 1.25, 0.95, 2.1, 0.95],
        vertical_alignment="center",
    )

    with col_file:
        st.markdown(
            f"""
            <div class="client-import-main">{file_name}</div>
            """,
            unsafe_allow_html=True,
        )

    with col_date:
        st.markdown(
            f"""
            <div class="client-import-main">{upload_date}</div>
            """,
            unsafe_allow_html=True,
        )

    with col_status:
        st.markdown(
            _upload_status_badge(status),
            unsafe_allow_html=True,
        )

    with col_obs:
        if status == "approved":
            st.markdown(
                """
                <div class="client-import-observation">
                    <div class="client-import-observation-title approved">Date procesate</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        elif status == "pending":
            st.markdown(
                """
                <div class="client-import-observation">
                    <div class="client-import-observation-title pending">În verificare</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            summary = _rejection_summary(upload.get("motiv_respingere"))

            st.markdown(
                f"""
                <div class="client-import-observation">
                    <div class="client-import-observation-title rejected">
                        {escape(summary["title"])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="client-details-button-anchor"></div>',
                unsafe_allow_html=True,
            )

            if st.button(
                    "Vezi detalii",
                    key=f"client_rejection_details_{upload.get('id')}",
                    use_container_width=True,
            ):
                render_client_rejection_details_modal(upload)

    with col_action:
        upload_id = upload.get("id")

        if not upload_id:
            st.markdown(
                '<span class="client-import-download-disabled">Indisponibil</span>',
                unsafe_allow_html=True,
            )
        else:
            download_result = download_upload_file(
                upload_id=upload_id,
                access_token=st.session_state.access_token,
            )

            if download_result.get("success"):
                st.download_button(
                    label="Descarcă",
                    data=download_result.get("content"),
                    file_name=upload.get("nume_fisier") or f"import_{upload_id}.xlsx",
                    mime=download_result.get(
                        "content_type",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    ),
                    use_container_width=True,
                    key=f"client_download_upload_{upload_id}",
                )
            else:
                st.markdown(
                    '<span class="client-import-download-disabled">Indisponibil</span>',
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="client-import-row-divider"></div>', unsafe_allow_html=True)

def render_client_imports_table(uploads: list):
    if not uploads:
        st.markdown(
            """
            <div class="client-import-empty-row">
                Nu există importuri pentru filtrul selectat.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for upload in uploads:
        render_client_import_row(upload)

def render_client_imports_header(status_options: list):
    with st.container():
        st.markdown(
            '<div class="client-import-card-anchor"></div>',
            unsafe_allow_html=True,
        )

        top_left, top_right = st.columns([2.6, 1], vertical_alignment="bottom")

        with top_left:
            st.markdown(
                """
                <div class="client-import-table-top">
                    <div class="client-import-table-title">Istoric importuri</div>
                    <div class="client-import-table-subtitle">
                        Importurile aprobate sunt incluse în calculele KPI și în dashboard.
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
                    status_options.index(st.session_state.client_upload_status_filter)
                    if st.session_state.client_upload_status_filter in status_options
                    else 0
                ),
                key="client_upload_status_filter",
            )

        st.markdown(
            """
            <div class="client-import-header">
                <div>Fișier</div>
                <div>Data încărcării</div>
                <div>Status</div>
                <div>Observații</div>
                <div>Acțiuni</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected_status_label

def render_client_imports_page():
    _render_client_imports_styles_override()

    header_left, header_right = st.columns([2.4, 1], vertical_alignment="center")

    with header_left:
        st.markdown(
            """
            <div class="dashboard-header compact-header">
                <div>
                    <div class="page-title-dark">Importuri financiare</div>
                    <div class="page-subtitle-dark">
                        Vizualizează istoricul fișierelor încărcate și adaugă importuri noi.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with header_right:
        st.markdown(
            '<div class="client-import-action-space"></div>',
            unsafe_allow_html=True,
        )

        if st.button("Adaugă import nou", use_container_width=True):
            render_add_import_modal()

    company_id = st.session_state.company_id

    if not company_id:
        st.info("Nu există companie asociată contului.")
        return

    result = get_upload_history(
        company_id=company_id,
        access_token=st.session_state.access_token,
    )

    if not result.get("success"):
        st.error(result.get("message", "Importurile nu au putut fi încărcate."))
        return

    uploads = result.get("data", [])

    status_map = {
        "Toate": "all",
        "În așteptare": "pending",
        "Aprobat": "approved",
        "Respins": "rejected",
    }

    status_options = list(status_map.keys())

    if "client_upload_status_filter" not in st.session_state:
        st.session_state.client_upload_status_filter = "Toate"

    selected_status_label = render_client_imports_header(status_options)
    selected_status = status_map.get(selected_status_label, "all")

    if selected_status != "all":
        uploads = [
            upload for upload in uploads
            if upload.get("status") == selected_status
        ]

    render_client_imports_table(uploads)

def _fmt_money(value):
    value = _safe_float(value)
    return f"{value:,.0f} RON"

def _fmt_percent(value):
    value = _safe_float(value)
    return f"{value * 100:.1f}%"

def _normalize_risk(value):
    value = _safe_float(value)

    if 0 <= value <= 1:
        return value * 100

    return value

def _fmt_percent_direct(value):
    value = _normalize_risk(value)
    return f"{value:.1f}%"

def _fmt_ratio(value):
    value = _safe_float(value)
    return f"{value:.2f}"

def _get_delta(current, previous):
    current = _safe_float(current)
    previous = _safe_float(previous)

    if previous == 0:
        return None

    return ((current - previous) / abs(previous)) * 100

def _fmt_delta(delta):
    if delta is None:
        return "N/A"

    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.1f}%"

def _risk_level(risk):
    risk = _normalize_risk(risk)

    if risk < 30:
        return "Risc scăzut", "risk-low"
    if risk < 60:
        return "Risc mediu", "risk-medium"
    return "Risc ridicat", "risk-high"

def _risk_page_level(risk):
    risk = _normalize_risk(risk)

    if risk < 30:
        return (
            "Risc scăzut",
            "risk-low",
            "Firma are o probabilitate redusă de dificultate financiară pe baza datelor analizate.",
        )
    if risk < 60:
        return (
            "Risc mediu",
            "risk-medium",
            "Firma necesită monitorizare atentă a indicatorilor financiari.",
        )
    return (
        "Risc ridicat",
        "risk-high",
        "Firma prezintă semnale financiare care necesită atenție rapidă.",
    )

def _indicator_label(indicator_code):
    labels = {
        "x1": "Profit net / active totale",
        "x2": "Datorii totale / active totale",
        "x3": "Capital de lucru / active totale",
        "x4": "Active curente / datorii curente",
        "x5": "Lichiditate defensivă ajustată",
        "x6": "Profit reținut / active totale",
        "x7": "EBIT / active totale",
        "x8": "Capitaluri proprii / datorii totale",
        "x9": "Vânzări / active totale",
        "x10": "Capitaluri proprii / active totale",
        "x11": "Rezultat brut ajustat / active",
        "x12": "Profit brut / datorii curente",
        "x13": "Profit brut + amortizare / vânzări",
        "x14": "Profit brut + dobânzi / active",
        "x15": "Datorii raportate la fluxul brut",
        "x16": "Profit brut + amortizare / datorii",
        "x17": "Active totale / datorii totale",
        "x18": "Profit brut / active totale",
        "x19": "Profit brut / vânzări",
        "x20": "Durata rotației stocurilor",
        "x21": "Evoluția vânzărilor",
        "x22": "Profit operațional / active",
        "x23": "Marja profitului net",
        "x24": "Profit brut cumulat / active",
        "x25": "Capitaluri ajustate / active",
        "x26": "Profit net + amortizare / datorii",
        "x27": "Profit operațional / cheltuieli financiare",
        "x28": "Capital de lucru / active fixe",
        "x29": "Dimensiunea firmei",
        "x30": "Datorii nete / vânzări",
        "x31": "Profit brut + dobânzi / vânzări",
        "x32": "Datorii curente / costul vânzărilor",
        "x33": "Cheltuieli operaționale / datorii curente",
        "x34": "Cheltuieli operaționale / datorii totale",
        "x35": "Profit din vânzări / active",
        "x36": "Vânzări / active totale",
        "x37": "Active curente fără stocuri / datorii lungi",
        "x38": "Capital permanent / active",
        "x39": "Profit din vânzări / vânzări",
        "x40": "Lichiditate rapidă ajustată",
        "x41": "Presiunea datoriilor asupra rezultatului operațional",
        "x42": "Profit operațional / vânzări",
        "x43": "Rotația creanțelor și stocurilor",
        "x44": "Durata încasării creanțelor",
        "x45": "Profit net / stocuri",
        "x46": "Active curente fără stocuri / datorii curente",
        "x47": "Durata stocurilor în costul vânzărilor",
        "x48": "EBITDA / active totale",
        "x49": "EBITDA / vânzări",
        "x50": "Active curente / datorii totale",
        "x51": "Datorii curente / active totale",
        "x52": "Datorii curente / costul vânzărilor",
        "x53": "Capitaluri proprii / active fixe",
        "x54": "Capital permanent / active fixe",
        "x55": "Capital de lucru",
        "x56": "Marja brută",
        "x57": "Capital de lucru ajustat",
        "x58": "Costuri totale / vânzări",
        "x59": "Datorii pe termen lung / capitaluri proprii",
        "x60": "Vânzări / stocuri",
        "x61": "Vânzări / creanțe",
        "x62": "Datorii curente / vânzări",
        "x63": "Vânzări / datorii curente",
        "x64": "Vânzări / active fixe",
        "x65": "Profit reținut / datorii totale",
        "x66": "Cash-flow raportat la capitalul de lucru",
    }

    return labels.get(indicator_code, indicator_code)

def _get_shap_rows(shap_data, key):
    if not isinstance(shap_data, dict):
        return []

    if shap_data.get("method") != "local_shap":
        return []

    rows = shap_data.get(key, [])

    if not isinstance(rows, list):
        return []

    return rows

def _fmt_shap_value(value):
    value = _safe_float(value)
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.4f}"

def _fmt_feature_value(value):
    value = _safe_float(value)

    if abs(value) >= 1000:
        return f"{value:,.0f}"

    return f"{value:.4f}"

def _shap_direction_text(direction):
    if direction == "increase_risk":
        return "Crește riscul"
    if direction == "reduce_risk":
        return "Reduce riscul"
    return "Impact neutru"

def _render_shap_factor_card(title, subtitle, factors, card_type):
    if not factors:
        return f"""
        <div class="shap-factor-card">
            <div class="shap-factor-card-title">{title}</div>
            <div class="shap-factor-card-subtitle">{subtitle}</div>
            <div class="shap-empty">Nu există factori relevanți în această categorie.</div>
        </div>
        """

    html = f"""
    <div class="shap-factor-card">
        <div class="shap-factor-card-title">{title}</div>
        <div class="shap-factor-card-subtitle">{subtitle}</div>
    """

    for factor in factors[:5]:
        indicator = factor.get("indicator", "")
        name = _indicator_label(indicator)
        feature_value = _fmt_feature_value(factor.get("feature_value"))
        shap_value = _fmt_shap_value(factor.get("shap_value"))

        html += f"""
        <div class="shap-factor-row">
            <div class="shap-factor-left">
                <div class="shap-factor-code">{indicator.upper()}</div>
                <div class="shap-factor-name">{name}</div>
                <div class="shap-factor-value">Valoare indicator: {feature_value}</div>
            </div>
            <div class="shap-impact {card_type}">
                {shap_value}
            </div>
        </div>
        """

    html += "</div>"
    return html

def render_dashboard_card(title, value, subtitle, delta=None, accent="blue"):
    delta_html = ""

    if delta is not None:
        delta_class = "positive" if delta >= 0 else "negative"
        delta_html = f"""
        <div class="dash-delta {delta_class}">
            {_fmt_delta(delta)}
        </div>
        """

    return f"""
<div class="dash-card accent-{accent}">
    <div class="dash-card-header">
        <div class="dash-card-title">{title}</div>
        {delta_html}
    </div>
    <div class="dash-card-value">{value}</div>
    <div class="dash-card-caption">{subtitle}</div>
</div>
"""

def _risk_metric_card(title, value, subtitle, accent="blue"):
    return f"""
<div class="risk-metric-card accent-{accent}">
    <div class="risk-metric-title">{title}</div>
    <div class="risk-metric-value">{value}</div>
    <div class="risk-metric-subtitle">{subtitle}</div>
</div>
"""

PLOTLY_CONFIG = {
    "displayModeBar": False,
    "scrollZoom": False,
    "doubleClick": "reset",
}

def _apply_dark_chart_layout(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font=dict(
            color="#cbd5e1",
            family="Inter, Segoe UI, Arial, sans-serif",
            size=13,
        ),
        title_font=dict(
            color="#f8fafc",
            family="Inter, Segoe UI, Arial, sans-serif",
            size=18,
        ),
        margin=dict(l=24, r=24, t=58, b=30),
        xaxis=dict(
            gridcolor="rgba(148, 163, 184, 0.14)",
            zerolinecolor="rgba(148, 163, 184, 0.18)",
            color="#8fa3c4",
            title_text=None,
        ),
        yaxis=dict(
            gridcolor="rgba(148, 163, 184, 0.14)",
            zerolinecolor="rgba(148, 163, 184, 0.18)",
            color="#8fa3c4",
            title_text=None,
        ),
        legend=dict(
            font=dict(color="#8fa3c4"),
            bgcolor="rgba(0,0,0,0)",
        ),
    )

    fig.update_xaxes(title_text=None)
    fig.update_yaxes(title_text=None)

    return fig

def _add_risk_thresholds(fig):
    fig.add_hline(
        y=30,
        line_dash="dash",
        line_width=1,
        line_color="rgba(249, 115, 22, 0.65)",
        annotation_text="Prag risc mediu 30%",
        annotation_position="top left",
        annotation_font_size=11,
        annotation_font_color="#fbbf24",
    )

    fig.add_hline(
        y=60,
        line_dash="dash",
        line_width=1,
        line_color="rgba(239, 68, 68, 0.65)",
        annotation_text="Prag risc ridicat 60%",
        annotation_position="top left",
        annotation_font_size=11,
        annotation_font_color="#f87171",
    )

    fig.update_yaxes(
        range=[0, 70],
        ticksuffix="%",
    )

    return fig

def _render_client_dashboard_styles_override():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(59, 130, 246, 0.18), transparent 30%),
                radial-gradient(circle at top right, rgba(14, 165, 233, 0.10), transparent 30%),
                linear-gradient(180deg, #020617 0%, #07111f 48%, #0b1220 100%) !important;
        }

        .block-container {
            max-width: 1380px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 2.4rem !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        .page-title-dark,
        .page-subtitle-dark {
            color: white !important;
        }

        .page-subtitle-dark {
            color: #8fa3c4 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _render_client_imports_styles_override():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(59, 130, 246, 0.18), transparent 30%),
                radial-gradient(circle at top right, rgba(14, 165, 233, 0.10), transparent 30%),
                linear-gradient(180deg, #020617 0%, #07111f 48%, #0b1220 100%) !important;
        }

        .block-container {
            max-width: 1380px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 2.4rem !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        .page-title-dark {
            color: #f8fafc !important;
        }

        .page-subtitle-dark {
            color: #8fa3c4 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _get_period_delta(df, months):
    if len(df) <= 1:
        return None

    current = _normalize_risk(df.iloc[-1].get("probabilitate_faliment"))
    start_df = df.tail(months)

    if start_df.empty:
        return None

    start = _normalize_risk(start_df.iloc[0].get("probabilitate_faliment"))

    return current - start

def _fmt_risk_delta(delta):
    if delta is None:
        return "N/A"

    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.1f} pp"

def _risk_delta_label(delta):
    if delta is None:
        return "Nu există suficiente date"

    if delta < 0:
        return "Risc în scădere"
    if delta > 0:
        return "Risc în creștere"
    return "Risc stabil"

def render_client_risk_page():
    _render_client_dashboard_styles_override()

    result = get_client_dashboard(
        company_id=st.session_state.company_id,
        access_token=st.session_state.access_token,
    )

    if not result.get("success"):
        st.error(result.get("message", "Nu s-au putut încărca datele de risc."))
        return

    data = result.get("data", {})
    company_name = data.get("company_name", "Companie")
    history = data.get("history", [])
    model_info = data.get("model") or {}

    st.html(
        f"""
        <div class="client-dash-header">
            <div>
                <div class="client-dash-title">Predicție risc ML</div>
                <div class="client-dash-subtitle">
                    {company_name} • Analiză predictivă bazată pe indicatorii financiari calculați
                </div>
            </div>
        </div>
        """
    )

    if not history:
        st.info("Nu există date financiare aprobate pentru calcularea predicției.")
        return

    df = pd.DataFrame(history)
    df = df.sort_values("date")

    if "probabilitate_faliment" not in df.columns:
        st.warning("Nu există predicții ML disponibile.")
        return

    df["probabilitate_faliment"] = df["probabilitate_faliment"].apply(_safe_float)
    df["risk_display"] = df["probabilitate_faliment"].apply(_normalize_risk)

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else latest

    risk = latest.get("probabilitate_faliment")
    risk_display = _normalize_risk(risk)
    risk_label, risk_class = _risk_level(risk)

    if risk_display < 30:
        risk_description = "Firma are o probabilitate redusă de dificultate financiară."
    elif risk_display < 60:
        risk_description = "Firma necesită monitorizare atentă a indicatorilor financiari."
    else:
        risk_description = "Firma prezintă semnale financiare care necesită atenție rapidă."

    previous_risk = previous.get("probabilitate_faliment")
    previous_risk_display = _normalize_risk(previous_risk)

    risk_change = risk_display - previous_risk_display if len(df) > 1 else None

    delta_3 = _get_period_delta(df, 3)
    delta_6 = _get_period_delta(df, 6)
    delta_12 = _get_period_delta(df, 12)

    max_risk = df["risk_display"].max()
    avg_risk = df["risk_display"].mean()

    st.html(
        f"""
        <div class="risk-page-hero">
            <div>
                <div class="risk-page-eyebrow">Predicție curentă</div>
                <div class="risk-page-title">{risk_label} • {_fmt_percent_direct(risk)}</div>
                <div class="risk-page-subtitle">
                    {risk_description}
                </div>
            </div>
            <div class="risk-page-score {risk_class}">
                <div class="risk-page-score-value">{_fmt_percent_direct(risk)}</div>
                <div class="risk-page-score-label">probabilitate faliment</div>
            </div>
        </div>
        """
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.html(_risk_metric_card("Risc curent", _fmt_percent_direct(risk), "Ultima lună analizată", "blue"))

    with c2:
        st.html(_risk_metric_card("Schimbare lunară", _fmt_risk_delta(risk_change), _risk_delta_label(risk_change), "purple"))

    with c3:
        st.html(_risk_metric_card("Risc maxim", f"{max_risk:.1f}%", "Maxim istoric în datele procesate", "orange"))

    with c4:
        st.html(_risk_metric_card("Risc mediu", f"{avg_risk:.1f}%", "Media perioadelor disponibile", "green"))

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    c5, c6, c7 = st.columns(3)

    with c5:
        st.html(_risk_metric_card("Trend 3 luni", _fmt_risk_delta(delta_3), _risk_delta_label(delta_3), "blue"))

    with c6:
        st.html(_risk_metric_card("Trend 6 luni", _fmt_risk_delta(delta_6), _risk_delta_label(delta_6), "purple"))

    with c7:
        st.html(_risk_metric_card("Trend 12 luni", _fmt_risk_delta(delta_12), _risk_delta_label(delta_12), "green"))

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([1.35, 1], gap="large")

    with left_col:
        fig_risk = px.area(
            df,
            x="date",
            y="risk_display",
            title="Trend risc faliment - toate lunile",
            markers=True,
        )

        _apply_dark_chart_layout(fig_risk, height=390)
        _add_risk_thresholds(fig_risk)

        fig_risk.update_traces(
            hovertemplate=(
                "Perioadă: %{x}<br>"
                "Risc estimat: %{y:.1f}%"
                "<extra></extra>"
            )
        )

        st.plotly_chart(fig_risk, use_container_width=True, config=PLOTLY_CONFIG)

    with right_col:
        st.html(
            f"""
            <div class="risk-explain-card">
                <div class="risk-explain-title">Interpretare predicție</div>
                <div class="risk-explain-main {risk_class}">
                    {risk_label}
                </div>
                <div class="risk-explain-text">
                    Modelul a estimat o probabilitate de {_fmt_percent_direct(risk)} pe baza indicatorilor calculați
                    din ultima perioadă financiară validată.
                </div>
                <div class="risk-explain-note">
                    Predicția este un semnal analitic, nu o decizie financiară absolută.
                </div>
            </div>
            """
        )

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3, gap="large")

    with col_a:
        df_3 = df.tail(3)
        fig_3 = px.line(df_3, x="date", y="risk_display", markers=True, title="Ultimele 3 luni")
        _apply_dark_chart_layout(fig_3, height=300)
        _add_risk_thresholds(fig_3)
        fig_3.update_traces(
            hovertemplate=(
                "Perioadă: %{x}<br>"
                "Risc estimat: %{y:.1f}%"
                "<extra></extra>"
            )
        )
        st.plotly_chart(fig_3, use_container_width=True, config=PLOTLY_CONFIG)

    with col_b:
        df_6 = df.tail(6)
        fig_6 = px.line(df_6, x="date", y="risk_display", markers=True, title="Ultimele 6 luni")
        _apply_dark_chart_layout(fig_6, height=300)
        _add_risk_thresholds(fig_6)
        fig_6.update_traces(
            hovertemplate=(
                "Perioadă: %{x}<br>"
                "Risc estimat: %{y:.1f}%"
                "<extra></extra>"
            )
        )
        st.plotly_chart(fig_6, use_container_width=True, config=PLOTLY_CONFIG)

    with col_c:
        df_12 = df.tail(12)
        fig_12 = px.line(df_12, x="date", y="risk_display", markers=True, title="Ultimele 12 luni")
        _apply_dark_chart_layout(fig_12, height=300)
        _add_risk_thresholds(fig_12)
        fig_12.update_traces(
            hovertemplate=(
                "Perioadă: %{x}<br>"
                "Risc estimat: %{y:.1f}%"
                "<extra></extra>"
            )
        )
        st.plotly_chart(fig_12, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    shap_data = latest.get("importanta_indicatori", {}) or {}

    top_factors = _get_shap_rows(shap_data, "top_factors")
    risk_factors = _get_shap_rows(shap_data, "risk_factors")
    protective_factors = _get_shap_rows(shap_data, "protective_factors")

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    if shap_data.get("method") == "local_shap" and top_factors:
        st.html(
            f"""
            <div class="shap-section-header">
                <div>
                    <div class="shap-section-eyebrow">Explicație individuală a predicției</div>
                    <div class="shap-section-title">Analiză SHAP locală pentru {latest.get("date")}</div>
                    <div class="shap-section-subtitle">
                        Factorii de mai jos explică predicția pentru perioada selectată,
                        nu importanța generală a modelului pentru toate firmele.
                    </div>
                </div>
                <div class="shap-local-badge">SHAP local</div>
            </div>
            """
        )

        shap_chart_df = pd.DataFrame(
            [
                {
                    "Indicator": factor.get("indicator", "").upper(),
                    "Denumire": _indicator_label(factor.get("indicator", "")),
                    "Impact SHAP": _safe_float(factor.get("shap_value")),
                    "Sens": _shap_direction_text(factor.get("direction")),
                }
                for factor in top_factors
            ]
        ).sort_values("Impact SHAP", ascending=True)

        left_shap, right_shap = st.columns([1.35, 1], gap="large")

        with left_shap:
            fig_shap = px.bar(
                shap_chart_df,
                x="Impact SHAP",
                y="Denumire",
                color="Sens",
                orientation="h",
                title="Factorii care au influențat predicția curentă",
                color_discrete_map={
                    "Crește riscul": "#ef4444",
                    "Reduce riscul": "#22c55e",
                    "Impact neutru": "#64748b",
                },
            )

            _apply_dark_chart_layout(fig_shap, height=430)

            fig_shap.update_layout(
                legend_title_text="Efect asupra riscului",
            )

            fig_shap.update_traces(
                marker_line_width=0,
            )

            st.plotly_chart(
                fig_shap,
                use_container_width=True,
                config=PLOTLY_CONFIG,
            )

        with right_shap:
            base_value = shap_data.get("base_value")
            explained_class = "Risc de faliment"

            st.html(
                f"""
                <div class="shap-summary-card">
                    <div class="shap-summary-title">Cum citim explicația?</div>

                    <div class="shap-summary-row">
                        <span>Predicție explicată</span>
                        <strong>{explained_class}</strong>
                    </div>

                    <div class="shap-summary-row">
                        <span>Probabilitate estimată</span>
                        <strong>{_fmt_percent_direct(risk)}</strong>
                    </div>

                    <div class="shap-summary-row">
                        <span>Scor de bază SHAP</span>
                        <strong>{_fmt_shap_value(base_value)}</strong>
                    </div>

                    <div class="shap-summary-info">
                        Valorile pozitive împing predicția către risc de faliment.
                        Valorile negative reduc scorul de risc.
                        Impactul SHAP este exprimat în scorul intern al modelului,
                        nu în puncte procentuale.
                    </div>
                </div>
                """
            )

        st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

        risk_col, protection_col = st.columns(2, gap="large")

        with risk_col:
            st.html(
                _render_shap_factor_card(
                    "Factori care cresc riscul",
                    "Indicatori care au împins predicția către clasa FALIMENT.",
                    risk_factors,
                    "risk",
                )
            )

        with protection_col:
            st.html(
                _render_shap_factor_card(
                    "Factori care reduc riscul",
                    "Indicatori care au diminuat scorul de risc estimat.",
                    protective_factors,
                    "protective",
                )
            )

    else:
        st.info(
            "Pentru această perioadă nu există încă o explicație SHAP locală. "
            "Aceasta va apărea pentru importurile procesate după activarea noii logici ML."
        )

    model_name = model_info.get("name", "Model ML activ")
    model_version = model_info.get("version", "N/A")
    accuracy = model_info.get("accuracy")
    f1_score = model_info.get("f1_score")

    st.html(
        f"""
<div class="model-meta-card">
    <div>
        <div class="model-meta-title">{model_name}</div>
        <div class="model-meta-subtitle">Versiune: {model_version}</div>
    </div>
    <div class="model-meta-stats">
        <div>
            <span>Acuratețe</span>
            <strong>{round(accuracy * 100, 2) if accuracy is not None else "N/A"}%</strong>
        </div>
        <div>
            <span>F1-score</span>
            <strong>{round(f1_score * 100, 2) if f1_score is not None else "N/A"}%</strong>
        </div>
    </div>
</div>
"""
    )

def render_client_dashboard():
    _render_client_dashboard_styles_override()

    result = get_client_dashboard(
        company_id=st.session_state.company_id,
        access_token=st.session_state.access_token,
    )

    if not result.get("success"):
        st.error(result.get("message", "Nu s-au putut încărca datele dashboard-ului."))
        return

    data = result.get("data", {})
    company_name = data.get("company_name", "Dashboard financiar")
    history = data.get("history", [])

    st.html(
        f"""
        <div class="client-dash-header">
            <div>
                <div class="client-dash-title">Financial Dashboard</div>
                <div class="client-dash-subtitle">
                    {company_name} • Monitorizare KPI, risc financiar și evoluție în timp
                </div>
            </div>
        </div>
        """
    )

    if not history:
        st.info("Nu există încă date aprobate pentru această companie.")
        return

    df = pd.DataFrame(history)

    numeric_columns = [
        "profit",
        "venituri",
        "ebit",
        "cheltuieli_operationale",
        "active_totale",
        "active_curente",
        "cash",
        "stocuri",
        "datorii_totale",
        "datorii_curente",
        "capitaluri_proprii",
        "profit_retinut",
        "probabilitate_faliment",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(_safe_float)

    df = df.sort_values("date")
    df["risk_display"] = df["probabilitate_faliment"].apply(_normalize_risk)

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else latest

    latest_kpis = latest.get("kpis", {}) if isinstance(latest.get("kpis", {}), dict) else {}

    liquidity = latest_kpis.get("lichiditate_curenta") or latest_kpis.get("lichiditate")
    profitability = latest_kpis.get("rentabilitate_active") or latest_kpis.get("profitabilitate")
    leverage = latest_kpis.get("grad_indatorare") or latest_kpis.get("leverage")
    solvability = latest_kpis.get("solvabilitate")

    risk = latest.get("probabilitate_faliment")
    risk_label, risk_class = _risk_level(risk)

    revenue_delta = _get_delta(latest.get("venituri"), previous.get("venituri"))
    profit_delta = _get_delta(latest.get("profit"), previous.get("profit"))
    assets_delta = _get_delta(latest.get("active_totale"), previous.get("active_totale"))
    debt_delta = _get_delta(latest.get("datorii_totale"), previous.get("datorii_totale"))

    st.html(
        f"""
        <div class="dash-hero">
            <div>
                <div class="dash-hero-eyebrow">Ultima perioadă analizată</div>
                <div class="dash-hero-title">{latest.get("date")}</div>
                <div class="dash-hero-subtitle">
                    Date financiare validate și procesate automat prin modelul ML.
                </div>
            </div>
            <div class="dash-risk-pill {risk_class}">
                {risk_label} • {_fmt_percent_direct(risk)}
            </div>
        </div>
        """
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.html(
            render_dashboard_card(
                "Venituri",
                _fmt_money(latest.get("venituri")),
                "Venituri totale în ultima perioadă",
                revenue_delta,
                "blue",
            )
        )

    with c2:
        st.html(
            render_dashboard_card(
                "Profit net",
                _fmt_money(latest.get("profit")),
                "Rezultat net raportat",
                profit_delta,
                "green",
            )
        )

    with c3:
        st.html(
            render_dashboard_card(
                "Active totale",
                _fmt_money(latest.get("active_totale")),
                "Dimensiunea economică a firmei",
                assets_delta,
                "purple",
            )
        )

    with c4:
        st.html(
            render_dashboard_card(
                "Datorii totale",
                _fmt_money(latest.get("datorii_totale")),
                "Expunere financiară totală",
                debt_delta,
                "orange",
            )
        )

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    c5, c6, c7, c8 = st.columns(4)

    with c5:
        st.html(
            render_dashboard_card(
                "Lichiditate curentă",
                _fmt_ratio(liquidity),
                "Active curente / datorii curente",
                None,
                "blue",
            )
        )

    with c6:
        st.html(
            render_dashboard_card(
                "Rentabilitate active",
                _fmt_percent(profitability),
                "Profit net / active totale",
                None,
                "green",
            )
        )

    with c7:
        st.html(
            render_dashboard_card(
                "Grad îndatorare",
                _fmt_percent(leverage),
                "Datorii totale / active totale",
                None,
                "orange",
            )
        )

    with c8:
        st.html(
            render_dashboard_card(
                "Solvabilitate",
                _fmt_percent(solvability),
                "Capitaluri proprii / active",
                None,
                "purple",
            )
        )

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([1.35, 1], gap="large")

    with left_col:
        fig_revenue_profit = px.area(
            df,
            x="date",
            y="venituri",
            title="Evoluție venituri și profit net",
        )

        fig_revenue_profit.update_traces(
            name="Venituri",
            hovertemplate=(
                "Perioadă: %{x}<br>"
                "Venituri: %{y:,.0f} RON"
                "<extra></extra>"
            ),
        )

        fig_revenue_profit.add_scatter(
            x=df["date"],
            y=df["profit"],
            mode="lines+markers",
            name="Profit net",
            hovertemplate=(
                "Perioadă: %{x}<br>"
                "Profit net: %{y:,.0f} RON"
                "<extra></extra>"
            ),
        )

        _apply_dark_chart_layout(fig_revenue_profit, height=390)

        fig_revenue_profit.update_yaxes(
            tickprefix="",
            ticksuffix=" RON",
        )

        st.plotly_chart(fig_revenue_profit, use_container_width=True, config=PLOTLY_CONFIG)

    with right_col:
        st.html(
            f"""
            <div class="dash-risk-card">
                <div class="dash-risk-title">Scor curent de risc</div>
                <div class="dash-risk-subtitle">Probabilitate estimată de faliment</div>
            
                <div class="dash-risk-circle {risk_class}">
                    <div class="dash-risk-value">{_fmt_percent_direct(risk)}</div>
                    <div class="dash-risk-label">{risk_label}</div>
                </div>
            
                <div class="dash-risk-note">
                    Modelul ML analizează indicatorii financiari calculați din datele validate.
                </div>
            </div>
            """
        )

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        structure_df = pd.DataFrame({
            "Categorie": ["Active totale", "Datorii totale", "Capitaluri proprii", "Cash"],
            "Valoare": [
                latest.get("active_totale"),
                latest.get("datorii_totale"),
                latest.get("capitaluri_proprii"),
                latest.get("cash"),
            ],
        })

        fig_structure = px.bar(
            structure_df,
            x="Categorie",
            y="Valoare",
            title="Structura financiară curentă",
            text="Valoare",
        )

        _apply_dark_chart_layout(fig_structure, height=360)

        fig_structure.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            hovertemplate=(
                "%{x}<br>"
                "Valoare: %{y:,.0f} RON"
                "<extra></extra>"
            ),
        )

        fig_structure.update_yaxes(
            ticksuffix=" RON",
        )

        st.plotly_chart(fig_structure, use_container_width=True, config=PLOTLY_CONFIG)

    with col_b:
        fig_risk = px.area(
            df,
            x="date",
            y="risk_display",
            title="Evoluția riscului de faliment",
            markers=True,
        )

        _apply_dark_chart_layout(fig_risk, height=360)
        _add_risk_thresholds(fig_risk)

        fig_risk.update_traces(
            hovertemplate=(
                "Perioadă: %{x}<br>"
                "Risc estimat: %{y:.1f}%"
                "<extra></extra>"
            )
        )

        st.plotly_chart(fig_risk, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    shap_data = latest.get("importanta_indicatori", {}) or {}
    top_factors = _get_shap_rows(shap_data, "top_factors")

    if shap_data.get("method") == "local_shap" and top_factors:
        preview_df = pd.DataFrame(
            [
                {
                    "Indicator": _indicator_label(factor.get("indicator", "")),
                    "Impact SHAP": _safe_float(factor.get("shap_value")),
                    "Sens": _shap_direction_text(factor.get("direction")),
                }
                for factor in top_factors[:5]
            ]
        ).sort_values("Impact SHAP", ascending=True)

        fig_imp = px.bar(
            preview_df,
            x="Impact SHAP",
            y="Indicator",
            orientation="h",
            color="Sens",
            title="Principalii factori ai riscului din ultima perioadă",
            color_discrete_map={
                "Crește riscul": "#ef4444",
                "Reduce riscul": "#22c55e",
                "Impact neutru": "#64748b",
            },
        )

        _apply_dark_chart_layout(fig_imp, height=360)
        fig_imp.update_layout(legend_title_text="Efect asupra riscului")

        st.plotly_chart(
            fig_imp,
            use_container_width=True,
            config=PLOTLY_CONFIG,
        )
    with st.expander("Istoric financiar detaliat", expanded=False):
        st.markdown(
            """
            <div class="dark-section-title">Date financiare procesate</div>
            """,
            unsafe_allow_html=True,
        )

        columns_to_show = [
            "date",
            "venituri",
            "profit",
            "active_totale",
            "datorii_totale",
            "capitaluri_proprii",
            "risk_display",
            "eticheta",
        ]

        columns_to_show = [col for col in columns_to_show if col in df.columns]

        st.dataframe(
            df[columns_to_show],
            use_container_width=True,
            hide_index=True,
        )

def _client_report_status_label(status: str):
    labels = {
        "pending": "În așteptare",
        "in_progress": "În lucru",
        "completed": "Finalizat",
    }
    return labels.get(status, status or "—")

def _client_report_status_badge(status: str):
    label = _client_report_status_label(status)

    if status == "completed":
        css_class = "client-report-status-completed"
    elif status == "in_progress":
        css_class = "client-report-status-progress"
    else:
        css_class = "client-report-status-pending"

    return f'<span class="client-report-status-badge {css_class}">{label}</span>'

def _fmt_report_probability(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"

    return f"{value:.2f}%"

@st.dialog("Solicitare raport personalizat", width="large")
def render_client_report_request_modal(standard_reports: list):
    st.markdown(
        """
        <div class="review-modal-header">
            <div class="review-modal-icon">✎</div>
            <div>
                <div class="review-modal-title">Solicitare raport personalizat</div>
                <div class="review-modal-subtitle">
                    Selectează raportul standard de referință și transmite cerințele pentru analist.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not standard_reports:
        st.warning(
            "Nu există rapoarte standard disponibile. Solicitarea personalizată poate fi creată după generarea unui raport standard."
        )
        return

    report_options = {}

    for report in standard_reports:
        report_id = report.get("id")
        balance_date = report.get("data_bilant") or "—"
        risk_status = report.get("status_risc") or "—"
        probability = _fmt_report_probability(report.get("probabilitate_faliment"))

        label = f"{balance_date} • {risk_status} • Probabilitate {probability}"
        report_options[label] = report_id

    selected_report_label = st.selectbox(
        "Raport standard de referință",
        options=list(report_options.keys()),
    )

    selected_base_report_id = report_options.get(selected_report_label)

    st.markdown(
        """
        <div class="review-warning-box">
            <div class="review-warning-title">Recomandare</div>
            <div class="review-warning-text">
                Raportul personalizat va porni de la perioada selectată mai sus.
                Scrie clar ce vrei să urmărească analistul: lichiditate, profitabilitate,
                îndatorare, risc financiar, evoluția veniturilor sau recomandări de îmbunătățire.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    focus_area = st.selectbox(
        "Zona principală de interes",
        [
            "Analiză generală",
            "Lichiditate",
            "Profitabilitate",
            "Îndatorare și solvabilitate",
            "Risc financiar",
            "Evoluția veniturilor și profitului",
            "Recomandări de îmbunătățire",
        ],
    )

    message = st.text_area(
        "Cerința pentru analist",
        placeholder=(
            "Exemplu: Aș dori o interpretare a riscului financiar pentru perioada selectată "
            "și recomandări privind îmbunătățirea lichidității."
        ),
        height=170,
    )

    col_cancel, col_submit = st.columns([1, 1])

    with col_cancel:
        if st.button("Anulează", use_container_width=True):
            st.rerun()

    with col_submit:
        submit_clicked = st.button("Trimite solicitarea", use_container_width=True)

    if submit_clicked:
        company_id = st.session_state.company_id

        if not company_id:
            st.error("Nu există companie asociată contului.")
            return

        clean_message = message.strip()

        if not clean_message:
            st.warning("Completează cerința pentru analist înainte de trimitere.")
            return

        final_message = (
            f"Raport standard de referință: {selected_report_label}\n\n"
            f"Zonă principală de interes: {focus_area}\n\n"
            f"Cerință client:\n{clean_message}"
        )

        with st.spinner("Se trimite solicitarea către analist..."):
            result = create_report_request(
                company_id=company_id,
                message=final_message,
                access_token=st.session_state.access_token,
                base_report_id=selected_base_report_id,
            )

        if result.get("success"):
            st.success("Solicitarea a fost trimisă cu succes către analist.")
            st.rerun()
            return

        st.error(result.get("message", "Solicitarea nu a putut fi trimisă."))

def render_client_standard_report_row(report: dict):
    report_id = report.get("id")
    balance_date = escape(str(report.get("data_bilant") or "—"))
    generated_at = escape(str(report.get("data_generare") or "—"))
    risk_status = escape(str(report.get("status_risc") or "—"))
    probability = _fmt_report_probability(report.get("probabilitate_faliment"))

    col_period, col_risk, col_generated, col_action = st.columns(
        [1.35, 1.25, 1.15, 0.95],
        vertical_alignment="center",
    )

    with col_period:
        st.markdown(
            f"""
            <div class="client-report-main">Raport standard</div>
            <div class="client-report-sub">Perioadă bilanțieră: {balance_date}</div>
            """,
            unsafe_allow_html=True,
        )

    with col_risk:
        st.markdown(
            f"""
            <div class="client-report-main">{risk_status}</div>
            <div class="client-report-sub">Probabilitate: {probability}</div>
            """,
            unsafe_allow_html=True,
        )

    with col_generated:
        st.markdown(
            f"""
            <div class="client-report-main">{generated_at}</div>
            <div class="client-report-sub">Generat automat</div>
            """,
            unsafe_allow_html=True,
        )

    with col_action:
        if not report_id:
            st.markdown(
                '<span class="client-import-download-disabled">Indisponibil</span>',
                unsafe_allow_html=True,
            )
        else:
            download_result = download_standard_report(
                report_id=report_id,
                access_token=st.session_state.access_token,
            )

            if download_result.get("success"):
                st.download_button(
                    label="Descarcă PDF",
                    data=download_result.get("content"),
                    file_name=f"raport_standard_{report_id}.pdf",
                    mime=download_result.get("content_type", "application/pdf"),
                    use_container_width=True,
                    key=f"client_download_standard_report_{report_id}",
                )
            else:
                st.markdown(
                    '<span class="client-import-download-disabled">Indisponibil</span>',
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="client-report-row-divider"></div>', unsafe_allow_html=True)

def render_client_standard_reports_section(reports: list, period_options: list):
    with st.container():
        st.markdown(
            '<div class="client-report-card-anchor"></div>',
            unsafe_allow_html=True,
        )

        top_left, top_right = st.columns([2.6, 1], vertical_alignment="bottom")

        with top_left:
            st.markdown(
                """
                <div class="client-report-section-top">
                    <div class="client-report-table-title">Rapoarte standard</div>
                    <div class="client-report-table-subtitle">
                        Rapoarte PDF generate automat pe baza KPI-urilor și predicției de risc.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with top_right:
            selected_period = st.selectbox(
                "Filtrează după perioadă",
                options=period_options,
                index=(
                    period_options.index(st.session_state.client_report_period_filter)
                    if st.session_state.client_report_period_filter in period_options
                    else 0
                ),
                key="client_report_period_filter",
            )

        st.markdown(
            """
            <div class="client-report-header client-report-standard-header">
                <div>Raport</div>
                <div>Risc estimat</div>
                <div>Data generării</div>
                <div>Acțiuni</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    filtered_reports = _filter_standard_reports_by_period(
        reports,
        selected_period,
    )

    if not filtered_reports:
        st.markdown(
            """
            <div class="client-report-empty-row">
                Nu există rapoarte standard pentru perioada selectată.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return selected_period

    for report in filtered_reports:
        render_client_standard_report_row(report)

    return selected_period

def render_client_custom_request_row(request_item: dict):
    request_id = request_item.get("id")
    status = request_item.get("status")
    created_at = escape(str(request_item.get("created_at") or "—"))
    analyst_username = escape(str(request_item.get("analyst_username") or "—"))
    message = escape(str(request_item.get("client_message") or "—"))

    if len(message) > 120:
        message = message[:120].rstrip() + "..."

    custom_report_id = request_item.get("custom_report_id")

    col_request, col_date, col_status, col_action = st.columns(
        [2.15, 1.15, 0.95, 0.95],
        vertical_alignment="center",
    )

    with col_request:
        st.markdown(
            f"""
            <div class="client-report-main">Solicitare #{request_id}</div>
            <div class="client-report-sub">{message}</div>
            <div class="client-report-sub">Analist: {analyst_username}</div>
            """,
            unsafe_allow_html=True,
        )

    with col_date:
        st.markdown(
            f"""
            <div class="client-report-main">{created_at}</div>
            <div class="client-report-sub">Data solicitării</div>
            """,
            unsafe_allow_html=True,
        )

    with col_status:
        st.markdown(
            _client_report_status_badge(status),
            unsafe_allow_html=True,
        )

    with col_action:
        if status == "completed" and custom_report_id:
            download_result = download_custom_report(
                report_id=custom_report_id,
                access_token=st.session_state.access_token,
            )

            if download_result.get("success"):
                st.download_button(
                    label="Descarcă PDF",
                    data=download_result.get("content"),
                    file_name=f"raport_personalizat_{custom_report_id}.pdf",
                    mime=download_result.get("content_type", "application/pdf"),
                    use_container_width=True,
                    key=f"client_download_custom_report_{custom_report_id}",
                )
            else:
                st.markdown(
                    '<span class="client-import-download-disabled">Indisponibil</span>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                """
                <div class="client-report-muted-action">
                    În așteptare
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="client-report-row-divider"></div>', unsafe_allow_html=True)

def render_client_custom_requests_section(requests_list: list):
    st.markdown(
        """
        <div class="client-report-card-anchor"></div>
        <div class="client-report-section-top">
            <div>
                <div class="client-report-table-title">Solicitări personalizate</div>
                <div class="client-report-table-subtitle">
                    Istoricul cererilor transmise către analist și rapoartele personalizate disponibile.
                </div>
            </div>
        </div>

        <div class="client-report-header client-report-custom-header">
            <div>Solicitare</div>
            <div>Data cererii</div>
            <div>Status</div>
            <div>Acțiuni</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not requests_list:
        st.markdown(
            """
            <div class="client-report-empty-row">
                Nu există încă solicitări de rapoarte personalizate.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for request_item in requests_list:
        render_client_custom_request_row(request_item)

def _parse_ro_date(value):
    if not value:
        return None

    text = str(value).strip()

    formats = [
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    return None

def _is_in_selected_period(value, selected_period: str):
    parsed_date = _parse_ro_date(value)

    if selected_period == "Toate":
        return True

    if parsed_date is None:
        return False

    today = date.today()

    if selected_period == "Ultimele 30 zile":
        return parsed_date >= today - timedelta(days=30)

    if selected_period == "Ultimele 3 luni":
        return parsed_date >= today - timedelta(days=90)

    if selected_period == "Ultimele 6 luni":
        return parsed_date >= today - timedelta(days=180)

    if selected_period == "Ultimele 12 luni":
        return parsed_date >= today - timedelta(days=365)

    if selected_period == "Anul curent":
        return parsed_date.year == today.year

    return True

def _filter_standard_reports_by_period(reports: list, selected_period: str):
    return [
        report for report in reports
        if _is_in_selected_period(report.get("data_bilant"), selected_period)
    ]

def _filter_custom_requests_by_period(requests_list: list, selected_period: str):
    return [
        request_item for request_item in requests_list
        if _is_in_selected_period(request_item.get("created_at"), selected_period)
    ]

def render_client_reports_page():
    _render_client_imports_styles_override()

    report_period_options = [
        "Toate",
        "Ultimele 30 zile",
        "Ultimele 3 luni",
        "Ultimele 6 luni",
        "Ultimele 12 luni",
        "Anul curent",
    ]

    if "client_report_period_filter" not in st.session_state:
        st.session_state.client_report_period_filter = "Toate"

    company_id = st.session_state.company_id

    if not company_id:
        st.info("Nu există companie asociată contului.")
        return

    standard_result = get_standard_reports(
        company_id=company_id,
        access_token=st.session_state.access_token,
    )

    requests_result = get_client_report_requests(
        company_id=company_id,
        access_token=st.session_state.access_token,
    )

    if not standard_result.get("success"):
        st.error(standard_result.get("message", "Rapoartele standard nu au putut fi încărcate."))
        return

    if not requests_result.get("success"):
        st.error(requests_result.get("message", "Solicitările de rapoarte nu au putut fi încărcate."))
        return

    standard_reports = standard_result.get("data", [])
    custom_requests = requests_result.get("data", [])

    header_left, header_right = st.columns([2.4, 1], vertical_alignment="center")

    with header_left:
        st.markdown(
            """
            <div class="dashboard-header compact-header">
                <div>
                    <div class="page-title-dark">Rapoarte financiare</div>
                    <div class="page-subtitle-dark">
                        Descarcă rapoarte standard sau solicită o interpretare personalizată de la analist.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with header_right:
        st.markdown(
            '<div class="client-import-action-space"></div>',
            unsafe_allow_html=True,
        )

        if st.button("Solicită raport personalizat", use_container_width=True):
            render_client_report_request_modal(standard_reports)

    st.markdown(
        """
        <div class="client-report-hero">
            <div class="client-report-hero-eyebrow">Centru rapoarte</div>
            <div class="client-report-hero-title">Analiză automată și recomandări personalizate</div>
            <div class="client-report-hero-text">
                Raportul standard sintetizează rezultatele calculate automat de sistem.
                Pentru interpretări suplimentare, poți transmite o solicitare către analistul financiar.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_period = render_client_standard_reports_section(
        standard_reports,
        report_period_options,
    )

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    filtered_custom_requests = _filter_custom_requests_by_period(
        custom_requests,
        selected_period,
    )

    render_client_custom_requests_section(filtered_custom_requests)