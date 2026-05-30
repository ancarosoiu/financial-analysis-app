import streamlit as st


def load_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        html, body, [class*="css"], .stApp {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        }

        /* =========================
           BASE STREAMLIT
        ========================= */
        .stApp {
            background: #111827;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 6rem;
            padding-bottom: 2rem;
        }

        .divider-space {
            height: 18px;
        }

        /* =========================
           SIDEBAR
        ========================= */
        [data-testid="stSidebar"] {
            background: #0f172a;
        }

        [data-testid="stSidebar"] * {
            color: white;
        }

        /* =========================
           AUTH
        ========================= */
        .auth-brand-row {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 3.2rem;
            margin-bottom: 24px;
        }

        .auth-brand-icon {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 900;
            font-size: 20px;
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.35);
        }

        .auth-brand-name {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: #ffffff;
        }

        .auth-brand-title {
            font-size: 2.05rem;
            line-height: 1.18;
            font-weight: 850;
            letter-spacing: -0.03em;
            color: #f8fafc;
            margin-bottom: 22px;
        }

        .auth-brand-subtitle {
            color: #cbd5e1;
            font-size: 0.98rem;
            line-height: 1.7;
            font-weight: 500;
        }

        .stTabs {
            background: #ffffff;
            border-radius: 12px;
            padding: 1.25rem;
            max-width: 430px;
            margin: 0 auto;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.32);
        }

        .stTabs [data-baseweb="tab-list"] {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            background: transparent;
            margin-bottom: 1.15rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 7px;
            background: #eef2f7;
            color: #334155;
            font-weight: 750;
            justify-content: center;
            border: none;
            padding: 0;
        }

        .stTabs [data-baseweb="tab"] p {
            font-size: 0.92rem;
            margin: 0;
        }

        .stTabs [aria-selected="true"] {
            background: #2563eb !important;
            color: white !important;
        }

        .stTabs [aria-selected="true"] p {
            color: white !important;
        }

        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {
            display: none;
        }

        /* =========================
           FORM CONTROLS
        ========================= */
        label[data-testid="stWidgetLabel"] p {
            font-size: 0.82rem;
            font-weight: 700;
            color: #334155;
            margin-bottom: 0.25rem;
        }

        div[data-testid="stForm"] {
            border: none;
            padding: 0;
        }

        .stTextInput > div > div {
            border: none !important;
            border-radius: 7px !important;
            background: transparent !important;
            box-shadow: none !important;
            overflow: visible !important;
        }

        .stTextInput [data-baseweb="input"] {
            height: 42px !important;
            border: 1px solid #d9e1ec !important;
            border-radius: 7px !important;
            background: white !important;
            box-shadow: none !important;
            overflow: hidden !important;
        }

        .stTextInput [data-baseweb="input"]:focus-within {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12) !important;
        }

        .stTextInput [data-baseweb="input"] > div,
        .stTextInput [data-baseweb="input"] button {
            background: white !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }

        .stTextInput input {
            height: 40px !important;
            font-size: 0.92rem !important;
            color: #111827 !important;
            background: white !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            border-radius: 7px !important;
        }

        .stTextInput input::placeholder {
            color: #a0aec0 !important;
        }

        .stTextInput [data-baseweb="input"] button {
            color: #64748b !important;
            height: 38px !important;
            width: 38px !important;
            min-width: 38px !important;
            padding: 0 !important;
            margin: 0 3px 0 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            opacity: 1 !important;
            border-radius: 6px !important;
        }

        .stTextInput [data-baseweb="input"] button:hover {
            background: #f8fafc !important;
            color: #334155 !important;
            transform: none !important;
        }

        .stTextInput [data-baseweb="input"] button svg {
            color: #64748b !important;
            stroke: #64748b !important;
            fill: none !important;
            opacity: 1 !important;
        }

        .stTextInput [data-baseweb="input"] button:hover svg {
            color: #334155 !important;
            stroke: #334155 !important;
        }

        .stTextArea textarea {
            background: white !important;
            border: 1px solid #d9e1ec !important;
            border-radius: 12px !important;
            color: #101828 !important;
            font-size: 0.92rem !important;
            box-shadow: none !important;
        }

        .stTextArea textarea::placeholder {
            color: #98a2b3 !important;
        }

        .stSelectbox [data-baseweb="select"] {
            background: white !important;
        }

        .stSelectbox [data-baseweb="select"] > div {
            min-height: 42px !important;
            border-radius: 7px !important;
            border: 1px solid #d9e1ec !important;
            background: white !important;
            box-shadow: none !important;
        }

        .stSelectbox [data-baseweb="select"] div {
            background: white !important;
        }

        .stSelectbox [data-baseweb="select"] *,
        .stSelectbox [data-baseweb="select"] span,
        .stSelectbox [data-baseweb="select"] input,
        .stSelectbox [data-baseweb="select"] div[role="combobox"],
        .stSelectbox [data-baseweb="select"] div[aria-selected] {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            opacity: 1 !important;
            visibility: visible !important;
            font-weight: 600 !important;
        }

        .stSelectbox [data-baseweb="select"] svg,
        .stSelectbox [data-baseweb="select"] svg path {
            color: #64748b !important;
            fill: #64748b !important;
            stroke: #64748b !important;
        }

        div[data-baseweb="popover"] {
            background: white !important;
            z-index: 999999 !important;
        }

        div[data-baseweb="popover"] ul {
            background: white !important;
            border-radius: 10px !important;
            border: 1px solid #e5e7eb !important;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12) !important;
            padding: 6px !important;
        }

        div[data-baseweb="popover"] li,
        div[data-baseweb="popover"] li * {
            color: #111827 !important;
            background: white !important;
            font-weight: 500 !important;
        }

        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="popover"] li[aria-selected="true"] {
            background: #eef4ff !important;
            color: #111827 !important;
        }

        div[data-testid="stFormSubmitButton"] button,
        .stButton > button {
            height: 44px;
            border-radius: 7px;
            background: #2563eb;
            color: white;
            border: none;
            font-weight: 800;
            font-size: 0.92rem;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.22);
            transition: 0.18s ease;
        }

        div[data-testid="stFormSubmitButton"] button:hover,
        .stButton > button:hover {
            background: #1d4ed8;
            color: white;
            transform: translateY(-1px);
        }

        .stAlert {
            border-radius: 10px;
            font-size: 0.9rem;
        }

        /* =========================
           LIGHT GENERIC COMPONENTS
        ========================= */
        .metric-card {
            background: white;
            border-radius: 18px;
            padding: 18px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
            min-height: 128px;
        }

        .metric-title {
            font-size: 0.9rem;
            color: #667085;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .metric-value {
            font-size: 1.75rem;
            font-weight: 800;
            color: #101828;
            margin-bottom: 4px;
        }

        .metric-caption {
            font-size: 0.85rem;
            color: #98a2b3;
        }

        .page-title {
            text-align: center;
            font-size: 1.8rem;
            font-weight: 800;
            color: #101828;
            margin-top: 0.5rem;
        }

        .page-subtitle {
            text-align: center;
            color: #667085;
            margin-bottom: 1.2rem;
        }

        .page-title-dark {
            font-size: 1.7rem;
            font-weight: 800;
            color: #101828;
        }

        .page-subtitle-dark {
            color: #667085;
            margin-top: 0.25rem;
        }

        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.2rem;
        }

        .user-chip {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 999px;
            padding: 9px 14px;
            color: #344054;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        }

        .analyst-section-header {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 20px 22px;
            margin-bottom: 1rem;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
        }

        .analyst-section-title {
            color: #101828;
            font-weight: 850;
            font-size: 1.25rem;
            margin-bottom: 4px;
        }

        .analyst-section-title.small {
            font-size: 1.05rem;
            margin-bottom: 0.8rem;
        }

        .analyst-section-subtitle {
            color: #667085;
            font-size: 0.92rem;
        }

        .small-section-title {
            color: #101828;
            font-weight: 850;
            font-size: 1.08rem;
            margin-bottom: 0.8rem;
        }

        .table-main-text {
            color: #101828;
            font-weight: 800;
            font-size: 0.95rem;
            line-height: 1.35;
        }

        .table-sub-text {
            color: #667085;
            font-size: 0.82rem;
            margin-top: 0.2rem;
            line-height: 1.35;
        }

        .client-imports-table-header,
        .uploads-table-header {
            display: grid;
            gap: 1rem;
            color: #667085;
            font-size: 0.8rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.02em;
            padding: 0.75rem 1rem;
            margin-top: 0.5rem;
            margin-bottom: 0.35rem;
        }

        .client-imports-table-header {
            grid-template-columns: 2.4fr 1.5fr 1.2fr 2.4fr;
        }

        .uploads-table-header {
            grid-template-columns: 2.4fr 2.6fr 1.5fr 1.3fr 1.7fr;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            padding: 6px 11px;
            font-size: 0.78rem;
            font-weight: 850;
            white-space: nowrap;
        }

        .status-badge-pending {
            background: #fff7ed;
            color: #c2410c;
            border: 1px solid #fed7aa;
        }

        .status-badge-approved {
            background: #dcfce7;
            color: #166534;
            border: 1px solid #bbf7d0;
        }

        .status-badge-rejected {
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }

        .reject-reason-box {
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #991b1b;
            border-radius: 14px;
            padding: 12px 14px;
            margin: 0.35rem 0 1rem 0;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* =========================
           DARK CLIENT DASHBOARD / RISK
        ========================= */
        .client-dash-header,
        .dash-hero,
        .risk-page-hero,
        .shap-section-header,
        .model-meta-card {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 24px;
        }

        .client-dash-header {
            margin-bottom: 1.6rem;
        }

        .client-dash-title {
            color: #f8fafc;
            font-size: 2.55rem;
            font-weight: 800;
            letter-spacing: -0.045em;
            line-height: 1.05;
            margin-bottom: 0.55rem;
        }

        .client-dash-subtitle {
            color: #8fa3c4;
            font-size: 1.02rem;
            font-weight: 500;
            letter-spacing: -0.01em;
        }

        .client-user-pill {
            background: rgba(255, 255, 255, 0.96);
            color: #0f172a;
            border-radius: 999px;
            padding: 11px 18px;
            font-weight: 600;
            box-shadow: 0 18px 38px rgba(0, 0, 0, 0.25);
        }

        .dash-hero,
        .risk-page-hero,
        .shap-section-header,
        .model-meta-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.22), transparent 34%),
                linear-gradient(135deg, #0b1730 0%, #102f76 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 24px;
            padding: 30px 34px;
            margin-bottom: 1.6rem;
            box-shadow:
                0 24px 60px rgba(15, 23, 42, 0.30),
                0 0 60px rgba(37, 99, 235, 0.14);
        }

        .dash-hero {
            align-items: center;
        }

        .dash-hero-eyebrow,
        .risk-page-eyebrow,
        .shap-section-eyebrow {
            color: #93c5fd;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 9px;
        }

        .dash-hero-title,
        .risk-page-title {
            color: #ffffff;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            margin-bottom: 8px;
        }

        .dash-hero-subtitle,
        .risk-page-subtitle,
        .shap-section-subtitle {
            color: #cbd5e1;
            font-size: 0.98rem;
            font-weight: 500;
            line-height: 1.5;
            max-width: 760px;
        }

        .dash-risk-pill,
        .risk-explain-main,
        .shap-local-badge {
            display: inline-flex;
            border-radius: 999px;
            padding: 10px 15px;
            font-weight: 800;
            white-space: nowrap;
            border: 1px solid rgba(255, 255, 255, 0.20);
        }

        .dash-risk-pill {
            padding: 13px 18px;
        }

        .risk-low {
            background: rgba(34, 197, 94, 0.16);
            color: #4ade80;
            border-color: rgba(34, 197, 94, 0.35);
        }

        .risk-medium {
            background: rgba(249, 115, 22, 0.16);
            color: #fb923c;
            border-color: rgba(249, 115, 22, 0.35);
        }

        .risk-high {
            background: rgba(239, 68, 68, 0.16);
            color: #f87171;
            border-color: rgba(239, 68, 68, 0.35);
        }

        .dash-card,
        .dash-risk-card,
        .risk-metric-card,
        .risk-explain-card,
        .shap-summary-card,
        .shap-factor-card,
        .feature-card,
        .model-meta-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.14), transparent 34%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 22px;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.10);
            box-sizing: border-box;
        }

        .dash-card,
        .risk-metric-card {
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .dash-card {
            padding: 22px 24px;
            height: 210px;
            min-height: 210px;
            max-height: 210px;
        }

        .risk-metric-card {
            padding: 22px;
            height: 178px;
            min-height: 178px;
            max-height: 178px;
            justify-content: space-between;
        }

        .dash-card::before,
        .risk-metric-card::before {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: inherit;
            pointer-events: none;
            border: 1px solid transparent;
        }

        .accent-blue::before {
            border-color: rgba(59, 130, 246, 0.30);
        }

        .accent-green::before {
            border-color: rgba(34, 197, 94, 0.28);
        }

        .accent-orange::before {
            border-color: rgba(249, 115, 22, 0.30);
        }

        .accent-purple::before {
            border-color: rgba(124, 58, 237, 0.30);
        }

        .dash-card-header {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: flex-start;
            position: relative;
            z-index: 2;
            min-height: 38px;
        }

        .dash-card-title,
        .risk-metric-title {
            color: #a7bad8;
            font-weight: 650;
            font-size: 0.95rem;
            line-height: 1.3;
            position: relative;
            z-index: 2;
        }

        .dash-card-title {
            margin-bottom: 12px;
            max-width: 68%;
        }

        .dash-card-value,
        .risk-metric-value {
            color: #f8fafc;
            font-weight: 800;
            font-size: 1.85rem;
            letter-spacing: -0.045em;
            line-height: 1.15;
            white-space: nowrap;
            position: relative;
            z-index: 2;
        }

        .dash-card-value {
            margin: 8px 0 10px 0;
        }

        .dash-card-caption,
        .risk-metric-subtitle {
            color: #8fa3c4;
            font-size: 0.88rem;
            line-height: 1.4;
            font-weight: 500;
            position: relative;
            z-index: 2;
        }

        .dash-card-caption {
            margin-top: auto;
            min-height: 38px;
        }

        .dash-delta,
        .shap-impact {
            border-radius: 999px;
            padding: 6px 11px;
            font-size: 0.78rem;
            font-weight: 800;
            text-align: center;
            white-space: nowrap;
            flex-shrink: 0;
            position: relative;
            z-index: 2;
        }

        .dash-delta.positive,
        .shap-impact.protective {
            background: rgba(34, 197, 94, 0.16);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.35);
        }

        .dash-delta.negative,
        .shap-impact.risk {
            background: rgba(239, 68, 68, 0.16);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.35);
        }

        .dash-risk-card {
            padding: 28px;
            min-height: 390px;
            text-align: center;
        }

        .dash-risk-title,
        .risk-explain-title,
        .shap-summary-title,
        .shap-factor-card-title,
        .feature-card-title,
        .model-meta-title {
            color: #f8fafc;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .dash-risk-title {
            font-size: 1.3rem;
            margin-bottom: 5px;
        }

        .dash-risk-subtitle,
        .risk-explain-note,
        .shap-summary-row span,
        .feature-card-subtitle,
        .model-meta-subtitle {
            color: #8fa3c4;
        }

        .dash-risk-subtitle {
            font-size: 0.9rem;
            margin-bottom: 26px;
        }

        .dash-risk-circle,
        .risk-page-score {
            border-radius: 999px;
            background: #07111f;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 12px solid rgba(96, 165, 250, 0.20);
        }

        .dash-risk-circle {
            width: 175px;
            height: 175px;
            margin: 0 auto 26px auto;
            border-width: 14px;
        }

        .risk-page-score {
            width: 165px;
            height: 165px;
            flex-shrink: 0;
        }

        .dash-risk-circle.risk-low,
        .risk-page-score.risk-low {
            border-color: #22c55e;
            box-shadow: 0 0 38px rgba(34, 197, 94, 0.18);
        }

        .dash-risk-circle.risk-medium,
        .risk-page-score.risk-medium {
            border-color: #f97316;
            box-shadow: 0 0 38px rgba(249, 115, 22, 0.18);
        }

        .dash-risk-circle.risk-high,
        .risk-page-score.risk-high {
            border-color: #ef4444;
            box-shadow: 0 0 38px rgba(239, 68, 68, 0.18);
        }

        .dash-risk-value,
        .risk-page-score-value {
            color: #ffffff;
            font-weight: 800;
            font-size: 2.1rem;
            letter-spacing: -0.04em;
        }

        .dash-risk-label,
        .risk-page-score-label {
            color: #a7bad8;
            font-size: 0.85rem;
            font-weight: 700;
            text-align: center;
        }

        .dash-risk-note,
        .risk-explain-text {
            color: #cbd5e1;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .dark-section-title {
            color: #f8fafc;
            font-size: 1.2rem;
            font-weight: 800;
            margin: 1.2rem 0 0.8rem 0;
        }

        .risk-page-title {
            color: #f8fafc;
        }

        .risk-page-score-label {
            color: #8fa3c4;
            font-size: 0.78rem;
        }

        .risk-explain-card {
            padding: 28px;
            height: 390px;
            min-height: 390px;
        }

        .risk-explain-title {
            font-size: 1.25rem;
            margin-bottom: 18px;
        }

        .risk-explain-main {
            margin-bottom: 18px;
        }

        .risk-explain-text {
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 18px;
        }

        /* =========================
           SHAP
        ========================= */
        .shap-section-header {
            align-items: center;
            margin: 0.4rem 0 1.25rem 0;
            padding: 24px 28px;
        }

        .shap-section-eyebrow {
            color: #60a5fa;
        }

        .shap-section-title {
            color: #f8fafc;
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 6px;
        }

        .shap-local-badge {
            background: rgba(59, 130, 246, 0.16);
            color: #60a5fa;
            border-color: rgba(96, 165, 250, 0.34);
            font-size: 0.82rem;
        }

        .shap-summary-card {
            padding: 25px;
            height: 430px;
            min-height: 430px;
            max-height: 430px;
        }

        .shap-summary-title {
            font-size: 1.22rem;
            margin-bottom: 20px;
        }

        .shap-summary-row,
        .feature-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            padding: 14px 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.14);
        }

        .shap-summary-row:last-child,
        .feature-row:last-child {
            border-bottom: none;
        }

        .shap-summary-row span {
            font-size: 0.9rem;
            font-weight: 500;
        }

        .shap-summary-row strong {
            color: #f8fafc;
            font-size: 0.95rem;
            font-weight: 800;
            text-align: right;
        }

        .shap-summary-info {
            margin-top: 22px;
            background: rgba(59, 130, 246, 0.08);
            border: 1px solid rgba(96, 165, 250, 0.16);
            border-radius: 14px;
            padding: 15px;
            color: #cbd5e1;
            font-size: 0.88rem;
            line-height: 1.55;
        }

        .shap-factor-card {
            padding: 24px;
            height: 485px;
            min-height: 485px;
            max-height: 485px;
            overflow: hidden;
        }

        .shap-factor-card-title {
            font-size: 1.18rem;
            margin-bottom: 6px;
        }

        .shap-factor-card-subtitle {
            color: #8fa3c4;
            font-size: 0.86rem;
            line-height: 1.45;
            margin-bottom: 16px;
            min-height: 40px;
        }

        .shap-factor-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 14px;
            min-height: 68px;
            padding: 10px 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.14);
        }

        .shap-factor-row:last-child {
            border-bottom: none;
        }

        .shap-factor-left {
            min-width: 0;
            flex: 1;
        }

        .shap-factor-code,
        .feature-code {
            color: #60a5fa;
            font-weight: 800;
            font-size: 0.76rem;
            margin-bottom: 3px;
        }

        .shap-factor-name,
        .feature-name {
            color: #e2e8f0;
            font-weight: 600;
            font-size: 0.84rem;
            line-height: 1.32;
        }

        .shap-factor-value {
            color: #7187aa;
            font-size: 0.76rem;
            margin-top: 3px;
        }

        .shap-impact {
            min-width: 72px;
        }

        .shap-empty {
            color: #8fa3c4;
            font-size: 0.9rem;
            margin-top: 22px;
        }

        .feature-card {
            padding: 24px;
            height: 390px;
            min-height: 390px;
        }

        .feature-card-title {
            font-size: 1.25rem;
            margin-bottom: 6px;
        }

        .feature-card-subtitle {
            font-size: 0.9rem;
            line-height: 1.5;
            margin-bottom: 18px;
        }

        .feature-value {
            color: #f8fafc;
            font-weight: 800;
        }

        .model-meta-card {
            border-radius: 20px;
            padding: 22px 24px;
            margin-top: 1.2rem;
            align-items: center;
        }

        .model-meta-title {
            font-size: 1.1rem;
        }

        .model-meta-stats {
            display: flex;
            gap: 28px;
        }

        .model-meta-stats span {
            display: block;
            color: #8fa3c4;
            font-size: 0.8rem;
            margin-bottom: 4px;
        }

        .model-meta-stats strong {
            color: #f8fafc;
            font-size: 1.05rem;
        }

        /* =========================
           ONBOARDING
        ========================= */
        .onboarding-stepper {
            max-width: 560px;
            margin: 0 auto 1.7rem auto;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .step-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 90px;
        }

        .step-circle {
            width: 34px;
            height: 34px;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.9rem;
            margin-bottom: 8px;
        }

        .step-circle.active,
        .step-circle.done {
            background: #2563eb;
            color: white;
        }

        .step-circle.active {
            box-shadow: 0 8px 18px rgba(37, 99, 235, 0.28);
        }

        .step-circle.idle {
            background: white;
            color: #98a2b3;
            border: 1px solid #cbd5e1;
        }

        .step-text {
            color: #64748b;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .step-line {
            height: 2px;
            width: 90px;
            background: #cbd5e1;
            margin: 0 -8px 22px -8px;
        }

        .step-line.active-line {
            background: #2563eb;
        }

        .onboarding-card,
        .confirm-panel {
            background: white;
            border-radius: 18px;
            border: 1px solid #eef2f6;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
        }

        .onboarding-card {
            padding: 28px 34px;
            max-width: 720px;
            margin: 0 auto 1.5rem auto;
        }

        .onboarding-icon {
            width: 54px;
            height: 54px;
            border-radius: 999px;
            background: #eaf2ff;
            color: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 14px auto;
            font-size: 26px;
            font-weight: 900;
        }

        .onboarding-icon.upload,
        .onboarding-icon.success {
            background: #dcfce7;
            color: #16a34a;
        }

        .onboarding-card-title {
            text-align: center;
            color: #101828;
            font-size: 1.35rem;
            font-weight: 850;
            margin-bottom: 6px;
        }

        .onboarding-card-subtitle {
            text-align: center;
            color: #667085;
            font-size: 0.95rem;
            margin-bottom: 1.25rem;
        }

        .upload-box {
            border: 1.5px dashed #cbd5e1;
            border-radius: 16px;
            background: #f8fafc;
            padding: 34px 20px;
            text-align: center;
            margin: 0.9rem 0 1rem 0;
        }

        .upload-big-icon {
            color: #94a3b8;
            font-size: 2.2rem;
            font-weight: 900;
            margin-bottom: 8px;
        }

        .upload-title {
            color: #344054;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .upload-subtitle {
            color: #667085;
            font-size: 0.9rem;
            margin-bottom: 10px;
        }

        .upload-format {
            color: #98a2b3;
            font-size: 0.8rem;
        }

        .confirm-panel {
            padding: 22px 24px;
            border-color: #e5e7eb;
            margin-top: -1rem;
            color: #101828;
        }

        .confirm-title {
            color: #101828;
            font-size: 1.15rem;
            font-weight: 850;
            margin-bottom: 14px;
        }

        .confirm-summary {
            background: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            overflow: hidden;
            margin-bottom: 18px;
        }

        .confirm-row,
        .review-detail-row {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            padding: 14px 16px;
            border-bottom: 1px solid #e5e7eb;
        }

        .confirm-row:last-child,
        .review-detail-row:last-child {
            border-bottom: none;
        }

        .confirm-row span,
        .review-detail-row span {
            color: #667085;
            font-weight: 600;
        }

        .confirm-row strong,
        .review-detail-row strong {
            color: #101828;
            font-weight: 800;
            text-align: right;
        }

        .validation-note {
            background: #fffbeb;
            border: 1px solid #fde68a;
            color: #92400e;
            border-radius: 12px;
            padding: 13px 15px;
            font-size: 0.92rem;
            line-height: 1.5;
            font-weight: 600;
        }

        /* =========================
           MODALS
        ========================= */
        dialog::backdrop {
            background: rgba(15, 23, 42, 0.55) !important;
            backdrop-filter: blur(6px) !important;
        }

        div[data-testid="stDialog"] div[role="dialog"] {
            border-radius: 20px !important;
            border: 1px solid #e5e7eb !important;
            box-shadow: 0 30px 80px rgba(15, 23, 42, 0.28) !important;
            background: white !important;
            padding: 0 !important;
        }

        div[data-testid="stDownloadButton"] button {
            height: 44px !important;
            border-radius: 12px !important;
            background: #0f172a !important;
            color: #ffffff !important;
            border: 1px solid #1e293b !important;
            font-weight: 800 !important;
            font-size: 0.92rem !important;
            box-shadow: 0 12px 24px rgba(15, 23, 42, 0.18) !important;
            transition: 0.18s ease !important;
            margin-bottom: 0.9rem !important;
        }

        div[data-testid="stDownloadButton"] button:hover {
            background: #1e293b !important;
            color: #ffffff !important;
            border-color: #334155 !important;
            transform: translateY(-1px) !important;
        }

        .review-modal-header {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 22px 26px 18px 26px;
            border-bottom: 1px solid #e5e7eb;
        }

        .review-modal-icon {
            width: 52px;
            height: 52px;
            border-radius: 14px;
            background: #eaf2ff;
            color: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 900;
        }

        .review-modal-title {
            color: #101828;
            font-size: 1.35rem;
            font-weight: 850;
            line-height: 1.2;
        }

        .review-modal-subtitle {
            color: #667085;
            font-size: 0.95rem;
            margin-top: 4px;
        }

        .review-modal-section-title {
            color: #344054;
            font-size: 1rem;
            font-weight: 850;
            margin: 20px 0 10px 0;
        }

        .review-details-box {
            background: #f8fafc;
            border-radius: 16px;
            border: 1px solid #edf2f7;
            overflow: hidden;
            margin-bottom: 18px;
        }

        .review-warning-box {
            background: #fffbeb;
            border: 1px solid #fde68a;
            border-radius: 16px;
            padding: 15px 16px;
            margin: 18px 0;
        }

        .review-warning-title {
            color: #92400e;
            font-weight: 850;
            margin-bottom: 5px;
        }

        .review-warning-text {
            color: #92400e;
            font-size: 0.92rem;
            line-height: 1.5;
        }

        div[data-testid="stDialog"] textarea {
            background: white !important;
            border: 1px solid #d9e1ec !important;
            border-radius: 12px !important;
            color: #101828 !important;
            font-size: 0.92rem !important;
        }

        div[data-testid="stDialog"] textarea::placeholder {
            color: #98a2b3 !important;
        }

        div[data-testid="stDialog"] button {
            border-radius: 12px !important;
            height: 44px !important;
            font-weight: 800 !important;
        }
        
                /* =========================
           CLIENT IMPORTS DARK TABLE
        ========================= */
        .compact-header {
            margin-bottom: 0.8rem;
        }

        .client-import-action-space {
            height: 44px;
        }

        .client-import-table-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.10), transparent 34%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.22);
            border-radius: 22px;
            padding: 22px 24px 18px 24px;
            margin-top: 1.3rem;
            margin-bottom: 10px;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.08);
            overflow: hidden;
        }

        .client-import-table-title {
            color: #f8fafc;
            font-size: 1.25rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            margin-bottom: 5px;
        }

        .client-import-table-subtitle {
            color: #8fa3c4;
            font-size: 0.92rem;
            line-height: 1.45;
            margin-bottom: 18px;
        }

        .client-import-header {
            display: grid;
            grid-template-columns: 2.05fr 1.25fr 0.95fr 2.1fr 0.95fr;
            gap: 18px;
            align-items: center;
            padding: 12px 2px 14px 2px;
            border-top: 1px solid rgba(148, 163, 184, 0.16);
            border-bottom: 1px solid rgba(148, 163, 184, 0.22);
            color: #93a7c5;
            font-size: 0.76rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            background: transparent !important;
            box-shadow: none !important;
        }

        .client-import-row-divider {
            height: 1px;
            background: rgba(148, 163, 184, 0.15);
            margin: 14px 0;
        }

        .client-import-main {
            color: #f8fafc;
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.35;
            word-break: break-word;
        }

        .client-import-status-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            padding: 7px 12px;
            font-size: 0.78rem;
            font-weight: 900;
            white-space: nowrap;
        }

        .client-import-status-pending {
            background: rgba(249, 115, 22, 0.16);
            color: #fb923c;
            border: 1px solid rgba(249, 115, 22, 0.35);
        }

        .client-import-status-approved {
            background: rgba(34, 197, 94, 0.16);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.35);
        }

        .client-import-status-rejected {
            background: rgba(239, 68, 68, 0.16);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.35);
        }

        .client-import-observation {
            color: #8fa3c4;
            font-size: 0.84rem;
            line-height: 1.45;
        }

        .client-import-observation-title {
            color: #f8fafc;
            font-weight: 850;
            margin-bottom: 4px;
        }

        .client-import-observation-title.approved {
            color: #4ade80;
        }

        .client-import-observation-title.pending {
            color: #fb923c;
        }

        .client-import-observation-title.rejected {
            color: #f87171;
        }

        .client-import-observation-text {
            color: #8fa3c4;
            line-height: 1.45;
        }

        .client-import-empty-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.10), transparent 34%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.22);
            border-radius: 22px;
            padding: 24px;
            margin-top: 1.3rem;
            color: #cbd5e1;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.08);
        }

        .client-detail-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.08), transparent 34%),
                linear-gradient(180deg, #0f223a 0%, #0b1728 100%);
            border: 1px solid rgba(96, 165, 250, 0.24);
            border-radius: 16px;
            padding: 14px 16px;
            margin-top: 8px;
            color: #cbd5e1;
        }

        .client-detail-card-title {
            color: #f8fafc;
            font-size: 0.92rem;
            font-weight: 850;
            margin-bottom: 10px;
        }

        .client-detail-text {
            color: #cbd5e1;
            font-size: 0.88rem;
            line-height: 1.5;
        }

        .client-detail-list {
            margin: 0;
            padding-left: 18px;
            color: #cbd5e1;
        }

        .client-detail-list li {
            margin-bottom: 6px;
            line-height: 1.45;
            font-size: 0.88rem;
        }

        div[data-testid="stExpander"] {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        div[data-testid="stExpander"] details {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        div[data-testid="stExpander"] summary {
            background: rgba(15, 23, 42, 0.78) !important;
            border: 1px solid rgba(96, 165, 250, 0.24) !important;
            border-radius: 14px !important;
            color: #f8fafc !important;
            font-weight: 800 !important;
            min-height: 38px !important;
            padding: 0.35rem 0.8rem !important;
        }

        div[data-testid="stExpander"] summary:hover {
            background: rgba(30, 41, 59, 0.92) !important;
            border-color: rgba(147, 197, 253, 0.45) !important;
        }

        div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
            color: #cbd5e1 !important;
        }

        div[data-testid="stDownloadButton"] button {
            min-height: 42px !important;
            border-radius: 999px !important;
            background: rgba(37, 99, 235, 0.18) !important;
            color: #bfdbfe !important;
            border: 1px solid rgba(96, 165, 250, 0.34) !important;
            font-size: 0.78rem !important;
            font-weight: 900 !important;
            box-shadow: none !important;
            padding: 8px 14px !important;
            margin-bottom: 0 !important;
        }

        div[data-testid="stDownloadButton"] button:hover {
            background: rgba(37, 99, 235, 0.30) !important;
            color: #ffffff !important;
            border-color: rgba(147, 197, 253, 0.55) !important;
            transform: translateY(-1px);
        }

        .client-import-download-disabled {
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 700;
        }

        /* =========================
           SOFTER MODAL LOOK
        ========================= */
        dialog::backdrop {
            background: rgba(2, 6, 23, 0.68) !important;
            backdrop-filter: blur(8px) !important;
        }

        div[data-testid="stDialog"] div[role="dialog"] {
            border-radius: 22px !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            box-shadow:
                0 30px 90px rgba(2, 6, 23, 0.55),
                0 0 55px rgba(37, 99, 235, 0.16) !important;
            background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%) !important;
            padding: 0 !important;
        }

        div[data-testid="stDialog"] h2 {
            color: #0f172a !important;
            opacity: 0.04 !important;
        }

        .review-modal-header {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 24px 28px 18px 28px;
            border-bottom: 1px solid rgba(148, 163, 184, 0.22);
        }

        .review-modal-icon {
            width: 52px;
            height: 52px;
            border-radius: 16px;
            background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
            color: #2563eb !important;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 900;
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.14);
        }

        .review-modal-title {
            color: #0f172a !important;
            font-size: 1.35rem;
            font-weight: 900;
            line-height: 1.2;
        }

        .review-modal-subtitle {
            color: #64748b !important;
            font-size: 0.95rem;
            margin-top: 4px;
        }

        .review-warning-box {
            background: #fff8e6;
            border: 1px solid #fde68a;
            border-radius: 16px;
            padding: 15px 16px;
            margin: 18px 0;
        }

        .review-warning-title {
            color: #92400e !important;
            font-weight: 850;
            margin-bottom: 5px;
        }

        .review-warning-text {
            color: #92400e !important;
            font-size: 0.92rem;
            line-height: 1.5;
        }
        /* =========================
           RESPONSIVE
        ========================= */
        @media (max-width: 900px) {
            .block-container {
                padding-top: 2rem;
            }

            .auth-brand-row {
                justify-content: center;
                margin-top: 0;
            }

            .auth-brand-title,
            .auth-brand-subtitle {
                text-align: center;
            }

            .auth-brand-title {
                font-size: 1.75rem;
            }

            .stTabs {
                max-width: 100%;
            }

            .uploads-table-header,
            .client-imports-table-header,
            .client-import-header {
                display: none;
            }

            .client-dash-header,
            .dash-hero,
            .risk-page-hero,
            .shap-section-header,
            .model-meta-card {
                flex-direction: column;
                align-items: flex-start;
            }

            .risk-page-score {
                margin-top: 12px;
            }

            .model-meta-stats {
                width: 100%;
                justify-content: space-between;
            }

            .dash-card,
            .risk-metric-card,
            .risk-explain-card,
            .shap-summary-card,
            .shap-factor-card {
                height: auto;
                max-height: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_analyst_styles():
    st.markdown(
        """
        <style>
        /* =========================
           ANALYST BASE
        ========================= */
        .stApp {
            background: #07111f !important;
        }

        .block-container {
            max-width: 1320px !important;
            padding-top: 2.2rem !important;
            padding-bottom: 2.5rem !important;
        }

        .analyst-page-header {
            margin-bottom: 1.6rem;
        }

        .analyst-page-title {
            color: #f8fafc;
            font-size: 2.45rem;
            font-weight: 900;
            letter-spacing: -0.045em;
            line-height: 1.05;
            margin-bottom: 0.45rem;
        }

        .analyst-page-subtitle {
            color: #8fa3c4;
            font-size: 1rem;
            font-weight: 500;
            line-height: 1.55;
        }

        .analyst-hero {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.28), transparent 34%),
                linear-gradient(135deg, #0b1730 0%, #102f76 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 24px;
            padding: 28px 32px;
            margin-bottom: 1.5rem;
            box-shadow:
                0 24px 60px rgba(15, 23, 42, 0.30),
                0 0 60px rgba(37, 99, 235, 0.14);
        }

        .analyst-hero-spaced {
            margin-top: 1.6rem;
        }

        .analyst-hero-eyebrow {
            color: #93c5fd;
            font-size: 0.78rem;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            margin-bottom: 8px;
        }

        .analyst-hero-title {
            color: #ffffff;
            font-size: 1.65rem;
            font-weight: 900;
            letter-spacing: -0.035em;
            margin-bottom: 8px;
        }

        .analyst-hero-text {
            color: #cbd5e1;
            font-size: 0.96rem;
            line-height: 1.55;
            max-width: 900px;
        }

        /* =========================
           ANALYST CARDS
        ========================= */
        .analyst-stat-card,
        .analyst-table-card,
        .analyst-company-table-card,
        .analyst-empty-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.12), transparent 34%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.22);
            border-radius: 22px;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.08);
        }

        .analyst-stat-card {
            padding: 22px 24px;
            height: 155px;
            min-height: 155px;
            box-sizing: border-box;
        }

        .analyst-stat-title {
            color: #a7bad8;
            font-weight: 700;
            font-size: 0.92rem;
            margin-bottom: 14px;
        }

        .analyst-stat-value {
            color: #f8fafc;
            font-weight: 900;
            font-size: 2rem;
            letter-spacing: -0.04em;
            margin-bottom: 10px;
        }

        .analyst-stat-caption {
            color: #8fa3c4;
            font-size: 0.88rem;
            line-height: 1.35;
        }

        .analyst-empty-card {
            padding: 24px;
            color: #cbd5e1;
        }

        .analyst-section-title-dark {
            color: #f8fafc;
            font-size: 1.35rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            margin-bottom: 0.25rem;
        }

        .analyst-section-subtitle-dark {
            color: #8fa3c4;
            font-size: 0.92rem;
            line-height: 1.45;
        }

        .analyst-main-text,
        .analyst-company-main {
            color: #f8fafc;
            font-weight: 850;
            font-size: 0.94rem;
            line-height: 1.35;
            word-break: break-word;
        }

        .analyst-sub-text,
        .analyst-company-sub {
            color: #8fa3c4;
            font-size: 0.82rem;
            margin-top: 4px;
            line-height: 1.35;
            word-break: break-word;
        }

        .analyst-muted-action {
            color: #8fa3c4;
            font-size: 0.86rem;
            font-weight: 600;
        }

        /* =========================
           ANALYST TABLES
        ========================= */
        .analyst-table-card {
            padding: 18px 20px 12px 20px;
            overflow: hidden;
        }

        .analyst-import-header,
        .analyst-import-row {
            display: grid;
            grid-template-columns: 2.1fr 2.5fr 1.45fr 1.15fr 1.25fr;
            gap: 18px;
            align-items: center;
        }

        .analyst-import-header,
        .analyst-company-header {
            color: #93a7c5;
            font-size: 0.76rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .analyst-import-header {
            padding: 12px 8px 14px 8px;
            border-bottom: 1px solid rgba(148, 163, 184, 0.20);
        }

        .analyst-import-row {
            padding: 18px 8px;
            border-bottom: 1px solid rgba(148, 163, 184, 0.14);
        }

        .analyst-import-row:last-child {
            border-bottom: none;
        }

        .analyst-company-table-card {
            padding: 22px 24px 10px 24px;
            margin-top: 1.4rem;
            overflow: hidden;
        }

        .analyst-company-table-title {
            color: #f8fafc;
            font-size: 1.25rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            margin-bottom: 5px;
        }

        .analyst-company-table-subtitle {
            color: #8fa3c4;
            font-size: 0.92rem;
            line-height: 1.45;
            margin-bottom: 18px;
        }

        .analyst-company-header,
        .analyst-company-row {
            display: grid;
            grid-template-columns: 2fr 1.1fr 2.1fr 2fr 1.2fr;
            gap: 18px;
            align-items: center;
        }

        .analyst-company-header {
            padding: 12px 2px 14px 2px;
            border-top: 1px solid rgba(148, 163, 184, 0.16);
            border-bottom: 1px solid rgba(148, 163, 184, 0.22);
        }

        .analyst-company-row {
            padding: 18px 2px;
            border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        }

        .analyst-company-row:last-child {
            border-bottom: none;
        }

        .reject-reason-box {
            background: rgba(239, 68, 68, 0.11);
            border: 1px solid rgba(239, 68, 68, 0.25);
            color: #fecaca;
            border-radius: 14px;
            padding: 12px 14px;
            margin: 0.1rem 0 0.8rem 0;
            font-size: 0.86rem;
            line-height: 1.5;
        }

        /* =========================
           ANALYST BADGES
        ========================= */
        .status-badge,
        .company-status-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            padding: 7px 12px;
            font-size: 0.78rem;
            font-weight: 900;
            white-space: nowrap;
        }

        .status-badge-pending,
        .company-status-pending {
            background: rgba(249, 115, 22, 0.16);
            color: #fb923c;
            border: 1px solid rgba(249, 115, 22, 0.35);
        }

        .status-badge-approved,
        .company-status-active {
            background: rgba(34, 197, 94, 0.16);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.35);
        }

        .status-badge-rejected {
            background: rgba(239, 68, 68, 0.16);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.35);
        }

        /* =========================
           ANALYST SELECTBOX
        ========================= */
        div[data-testid="stSelectbox"] label p {
            color: #a7bad8 !important;
            font-weight: 850 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
            min-height: 46px !important;
            border-radius: 12px !important;
            border: 1px solid rgba(96, 165, 250, 0.28) !important;
            background: #10233c !important;
            box-shadow: none !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] div {
            background: #10233c !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] *,
        div[data-testid="stSelectbox"] [data-baseweb="select"] span,
        div[data-testid="stSelectbox"] [data-baseweb="select"] input,
        div[data-testid="stSelectbox"] [data-baseweb="select"] div[role="combobox"] {
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
            opacity: 1 !important;
            visibility: visible !important;
            font-weight: 700 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] svg,
        div[data-testid="stSelectbox"] [data-baseweb="select"] svg path {
            color: #8fa3c4 !important;
            fill: #8fa3c4 !important;
            stroke: #8fa3c4 !important;
        }

        div[data-baseweb="popover"],
        div[data-baseweb="popover"] ul {
            background: #10233c !important;
        }

        div[data-baseweb="popover"] ul {
            border-radius: 12px !important;
            border: 1px solid rgba(96, 165, 250, 0.28) !important;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.45) !important;
            padding: 6px !important;
        }

        div[data-baseweb="popover"] li,
        div[data-baseweb="popover"] li *,
        div[data-baseweb="popover"] [role="option"],
        div[data-baseweb="popover"] [role="option"] * {
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
            background: #10233c !important;
            opacity: 1 !important;
            font-weight: 600 !important;
        }

        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="popover"] li[aria-selected="true"],
        div[data-baseweb="popover"] [role="option"]:hover,
        div[data-baseweb="popover"] [role="option"][aria-selected="true"] {
            background: #1e3a5f !important;
            color: #ffffff !important;
        }

        /* =========================
           RESPONSIVE
        ========================= */
        @media (max-width: 950px) {
            .analyst-page-header {
                flex-direction: column;
                align-items: flex-start;
            }

            .analyst-import-header,
            .analyst-company-header {
                display: none;
            }

            .analyst-import-row,
            .analyst-company-row {
                grid-template-columns: 1fr;
                gap: 10px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str, caption: str):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-caption">{caption}</div>
    </div>
    """


def status_pill(text: str, color: str):
    color_map = {
        "green": ("#dcfce7", "#166534"),
        "orange": ("#ffedd5", "#9a3412"),
        "red": ("#fee2e2", "#991b1b"),
    }

    bg, fg = color_map.get(color, ("#dcfce7", "#166534"))

    return f"""
    <div style="
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-top: 10px;
        background: {bg};
        color: {fg};
    ">
        {text}
    </div>
    """


def render_hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 24px 28px;
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.08);
            margin-bottom: 22px;
            border: 1px solid #e5e7eb;
        ">
            <div style="
                font-size: 1.8rem;
                font-weight: 850;
                color: #101828;
                margin-bottom: 6px;
            ">
                {title}
            </div>
            <div style="
                color: #667085;
                font-size: 1rem;
                line-height: 1.6;
            ">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
