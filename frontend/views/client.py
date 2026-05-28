import streamlit as st
import pandas as pd
import plotly.express as px

from api import (
    create_company,
    get_client_dashboard,
    upload_financial_file,
    get_upload_history,
)

from views.styles import (
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
            background: #f4f7fb !important;
        }

        .block-container {
            max-width: 1120px !important;
            padding-top: 1.2rem !important;
            padding-bottom: 2rem !important;
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


def render_upload_step():
    st.markdown(
        """
        <div class="onboarding-card">
            <div class="onboarding-icon upload">↑</div>
            <div class="onboarding-card-title">Încărcare date financiare</div>
            <div class="onboarding-card-subtitle">
                Încarcă fișierul Excel cu bilanț contabil și cont de profit și pierdere
            </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Alege fișier Excel",
        type=["xlsx", "xls"],
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="upload-box">
            <div class="upload-big-icon">⇧</div>
            <div class="upload-title">Drag & drop fișierul Excel aici</div>
            <div class="upload-subtitle">sau folosește selectorul de fișier de mai sus</div>
            <div class="upload-format">Format acceptat: .xlsx, .xls | minimum 12 luni</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Înapoi", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()

    with col2:
        upload_clicked = st.button("Trimite spre validare", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if upload_clicked:
        if uploaded_file is None:
            st.error("Încarcă un fișier înainte de trimitere.")
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
                st.warning("Nu poți încărca un import nou deoarece există deja un import aprobat pentru luna curentă.")
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
        css_class = "status-badge-approved"
    elif status == "rejected":
        css_class = "status-badge-rejected"
    else:
        css_class = "status-badge-pending"

    return f'<span class="status-badge {css_class}">{label}</span>'


@st.dialog("Adaugă import nou", width="large")
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
        else:
            errors = result.get("errors", {})
            code = errors.get("code")

            if code == "pending_import_exists":
                st.warning(result.get("message"))
            elif code == "too_soon_after_last_approved_import":
                st.warning(result.get("message"))
            else:
                st.error(result.get("message", "Încărcarea importului a eșuat."))


def render_client_import_row(upload: dict):
    status = upload.get("status")

    with st.container(border=True):
        col_file, col_date, col_status, col_reason = st.columns(
            [2.4, 1.5, 1.2, 2.4],
            vertical_alignment="center",
        )

        with col_file:
            st.markdown(
                f"""
                <div class="table-main-text">{upload.get("nume_fisier")}</div>
                <div class="table-sub-text">ID import: {upload.get("id")}</div>
                """,
                unsafe_allow_html=True,
            )

        with col_date:
            st.markdown(
                f"""
                <div class="table-main-text">{upload.get("data_incarcare")}</div>
                <div class="table-sub-text">Data încărcării</div>
                """,
                unsafe_allow_html=True,
            )

        with col_status:
            st.markdown(_upload_status_badge(status), unsafe_allow_html=True)

        with col_reason:
            reason = upload.get("motiv_respingere")

            if status == "rejected" and reason:
                st.markdown(
                    f"""
                    <div class="table-sub-text">
                        <strong>Motiv:</strong> {reason}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif status == "approved":
                st.markdown(
                    """
                    <div class="table-sub-text">Date procesate și incluse în dashboard.</div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div class="table-sub-text">În așteptarea validării analistului.</div>
                    """,
                    unsafe_allow_html=True,
                )


def render_client_imports_page():
    _render_onboarding_styles_override()

    st.markdown(
        f"""
        <div class="dashboard-header">
            <div>
                <div class="page-title-dark">Importuri financiare</div>
                <div class="page-subtitle-dark">
                    Vizualizează istoricul fișierelor încărcate și adaugă importuri noi.
                </div>
            </div>
            <div class="user-chip">{st.session_state.username}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns([2.4, 1], vertical_alignment="center")

    with top_left:
        st.markdown(
            """
            <div class="analyst-section-header">
                <div class="analyst-section-title">Istoric importuri</div>
                <div class="analyst-section-subtitle">
                    Importurile aprobate sunt incluse în calculele KPI și în dashboard.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_right:
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

    if not uploads:
        st.info("Nu există importuri încărcate.")
        return

    st.markdown(
        """
        <div class="client-imports-table-header">
            <div>Fișier</div>
            <div>Data încărcării</div>
            <div>Status</div>
            <div>Observații</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for upload in uploads:
        render_client_import_row(upload)

def _fmt_money(value):
    value = _safe_float(value)
    return f"{value:,.0f} RON"


def _fmt_percent(value):
    value = _safe_float(value)
    return f"{value * 100:.1f}%"


def _normalize_risk(value):
    value = _safe_float(value)

    # Dacă modelul returnează 0.12, îl tratăm ca 12%.
    # Dacă returnează deja 12.0, îl păstrăm.
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
        "x1": "Rentabilitate active",
        "x2": "Grad de îndatorare",
        "x3": "Capital de lucru / active",
        "x4": "Lichiditate curentă",
        "x5": "Cash-flow operațional estimat",
        "x6": "Profit reținut / active",
        "x7": "EBIT / active",
        "x8": "Capitaluri proprii / datorii",
        "x9": "Rotația activelor",
        "x10": "Solvabilitate",
        "x11": "Profit + amortizare / datorii",
        "x12": "Profit / datorii curente",
        "x13": "Profit + amortizare / vânzări",
        "x14": "Profit + EBIT / active",
        "x15": "Datorii raportate la cash-flow",
        "x16": "Cash-flow / datorii totale",
        "x17": "Active / datorii",
        "x18": "Profit / active",
        "x19": "Profit / vânzări",
        "x20": "Stocuri raportate la vânzări",
        "x21": "Evoluție vânzări",
        "x22": "EBIT / active",
        "x23": "Marja profitului net",
        "x24": "Profit pe active",
        "x25": "Capital ajustat / active",
        "x26": "Profit + amortizare / datorii",
        "x27": "EBIT / cheltuieli operaționale",
        "x28": "Capital de lucru / active fixe",
        "x29": "Dimensiunea firmei",
        "x30": "Datorii nete / vânzări",
        "x31": "Profit + EBIT / vânzări",
        "x32": "Datorii curente raportate la costuri",
        "x33": "Datorii curente / datorii totale",
        "x34": "Cheltuieli operaționale / datorii",
        "x35": "Profit operațional / active",
        "x36": "Vânzări / active",
        "x37": "Active curente ajustate / datorii lungi",
        "x38": "Capital permanent / active",
        "x39": "Profit pe vânzări",
        "x40": "Lichiditate rapidă ajustată",
        "x41": "Presiune datorii / cash-flow",
        "x42": "Profit operațional / vânzări",
        "x43": "Creanțe raportate la vânzări",
        "x44": "Cash-flow / datorii",
        "x45": "Profit / stocuri",
        "x46": "Active curente fără stocuri / datorii curente",
        "x47": "Viteză rotație stocuri",
        "x48": "EBITDA / active",
        "x49": "EBITDA / vânzări",
        "x50": "Active curente / datorii totale",
        "x51": "Datorii curente / active",
        "x52": "Datorii curente raportate la costuri",
        "x53": "Capitaluri proprii / active fixe",
        "x54": "Capital permanent / active fixe",
        "x55": "Capital de lucru",
        "x56": "Marja brută",
        "x57": "Capital de lucru ajustat",
        "x58": "Cheltuieli / vânzări",
        "x59": "Datorii pe termen lung / capital",
        "x60": "Vânzări / stocuri",
        "x61": "Vânzări / active curente",
        "x62": "Datorii curente / vânzări",
        "x63": "Vânzări / datorii curente",
        "x64": "Vânzări / active fixe",
        "x65": "Profit reținut / datorii",
        "x66": "Cash-flow raportat la capital de lucru",
    }

    return labels.get(indicator_code, indicator_code)


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
    <div class="client-user-pill">{st.session_state.username}</div>
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
        )
        _apply_dark_chart_layout(fig_risk, height=390)
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
        st.plotly_chart(fig_3, use_container_width=True, config=PLOTLY_CONFIG)

    with col_b:
        df_6 = df.tail(6)
        fig_6 = px.line(df_6, x="date", y="risk_display", markers=True, title="Ultimele 6 luni")
        _apply_dark_chart_layout(fig_6, height=300)
        st.plotly_chart(fig_6, use_container_width=True, config=PLOTLY_CONFIG)

    with col_c:
        df_12 = df.tail(12)
        fig_12 = px.line(df_12, x="date", y="risk_display", markers=True, title="Ultimele 12 luni")
        _apply_dark_chart_layout(fig_12, height=300)
        st.plotly_chart(fig_12, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    importances = latest.get("importanta_indicatori", {})

    if isinstance(importances, dict) and importances:
        imp_df = pd.DataFrame(
            [
                {
                    "Indicator": key,
                    "Denumire": _indicator_label(key),
                    "Importanță": value,
                }
                for key, value in importances.items()
            ]
        ).sort_values("Importanță", ascending=True)

        left_imp, right_imp = st.columns([1.35, 1], gap="large")

        with left_imp:
            fig_imp = px.bar(
                imp_df,
                x="Importanță",
                y="Denumire",
                orientation="h",
                title="Top factori care au influențat predicția",
            )
            _apply_dark_chart_layout(fig_imp, height=390)
            st.plotly_chart(fig_imp, use_container_width=True, config=PLOTLY_CONFIG)

        with right_imp:
            top_rows = imp_df.sort_values("Importanță", ascending=False).head(5)

            html = """
<div class="feature-card">
    <div class="feature-card-title">Feature importance</div>
    <div class="feature-card-subtitle">
        Ce indicatori au contat cel mai mult în decizia modelului.
    </div>
"""

            for _, row in top_rows.iterrows():
                html += f"""
    <div class="feature-row">
        <div>
            <div class="feature-code">{row["Indicator"]}</div>
            <div class="feature-name">{row["Denumire"]}</div>
        </div>
        <div class="feature-value">{row["Importanță"]}</div>
    </div>
"""

            html += "</div>"

            st.html(html)

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
    <div class="client-user-pill">{st.session_state.username}</div>
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
            title="Evoluție venituri",
        )
        fig_revenue_profit.add_scatter(
            x=df["date"],
            y=df["profit"],
            mode="lines+markers",
            name="Profit",
        )
        _apply_dark_chart_layout(fig_revenue_profit, height=390)
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
            text_auto=".2s",
        )
        _apply_dark_chart_layout(fig_structure, height=360)
        st.plotly_chart(fig_structure, use_container_width=True, config=PLOTLY_CONFIG)

    with col_b:
        fig_risk = px.area(
            df,
            x="date",
            y="risk_display",
            title="Evoluția riscului de faliment",
        )
        _apply_dark_chart_layout(fig_risk, height=360)
        st.plotly_chart(fig_risk, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

    importances = latest.get("importanta_indicatori", {})

    if isinstance(importances, dict) and importances:
        imp_df = pd.DataFrame(
            [
                {
                    "Indicator": key,
                    "Denumire": _indicator_label(key),
                    "Importanță": value,
                }
                for key, value in importances.items()
            ]
        ).sort_values("Importanță", ascending=True)

        fig_imp = px.bar(
            imp_df,
            x="Importanță",
            y="Denumire",
            orientation="h",
            title="Top indicatori care au influențat predicția ML",
        )
        _apply_dark_chart_layout(fig_imp, height=360)
        st.plotly_chart(fig_imp, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown(
        """
        <div class="dark-section-title">Istoric financiar</div>
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