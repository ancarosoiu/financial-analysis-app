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
           GLOBAL
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

        /* =========================
           AUTH PAGE
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
           LABELS
        ========================= */
        label[data-testid="stWidgetLabel"] p {
            font-size: 0.82rem;
            font-weight: 700;
            color: #334155;
            margin-bottom: 0.25rem;
        }

        /* =========================
           INPUTS
        ========================= */
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

        .stTextInput [data-baseweb="input"] > div {
            border: none !important;
            background: white !important;
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
            background: white !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
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
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
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

        /* =========================
           SELECTBOX
        ========================= */
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

        .stSelectbox [data-baseweb="select"] span {
            color: #111827 !important;
            opacity: 1 !important;
        }

        .stSelectbox [data-baseweb="select"] input {
            color: #111827 !important;
            opacity: 1 !important;
        }

        .stSelectbox [data-baseweb="select"] svg {
            color: #64748b !important;
            fill: #64748b !important;
        }

        div[data-baseweb="popover"] {
            background: white !important;
        }

        div[data-baseweb="popover"] ul {
            background: white !important;
            border-radius: 10px !important;
            border: 1px solid #e5e7eb !important;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12) !important;
        }

        div[data-baseweb="popover"] li {
            color: #111827 !important;
            background: white !important;
        }

        div[data-baseweb="popover"] li:hover {
            background: #eef4ff !important;
            color: #111827 !important;
        }

        /* =========================
           FORMS
        ========================= */
        div[data-testid="stForm"] {
            border: none;
            padding: 0;
        }

        /* =========================
           BUTTONS
        ========================= */
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

        /* =========================
           ALERTS
        ========================= */
        .stAlert {
            border-radius: 10px;
            font-size: 0.9rem;
        }

        /* =========================
           GENERIC DASHBOARD HELPERS
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

        .divider-space {
            height: 18px;
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

        /* =========================
           CLIENT KPI DASHBOARD
        ========================= */
        .client-dash-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
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

        .dash-hero {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.28), transparent 32%),
                linear-gradient(135deg, #0b1730 0%, #102f76 100%);
            color: white;
            border-radius: 24px;
            padding: 30px 34px;
            margin-bottom: 1.6rem;
            border: 1px solid rgba(96, 165, 250, 0.22);
            box-shadow:
                0 24px 60px rgba(15, 23, 42, 0.30),
                0 0 60px rgba(37, 99, 235, 0.14);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
        }

        .dash-hero-eyebrow {
            color: #93c5fd;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 9px;
        }

        .dash-hero-title {
            font-size: 2rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.04em;
            margin-bottom: 8px;
        }

        .dash-hero-subtitle {
            color: #cbd5e1;
            font-size: 0.98rem;
            font-weight: 500;
        }

        .dash-risk-pill {
            border-radius: 999px;
            padding: 13px 18px;
            font-weight: 800;
            white-space: nowrap;
            border: 1px solid rgba(255, 255, 255, 0.20);
        }

        .dash-risk-pill.risk-low {
            background: rgba(34, 197, 94, 0.16);
            color: #4ade80;
            border-color: rgba(34, 197, 94, 0.35);
        }

        .dash-risk-pill.risk-medium {
            background: rgba(249, 115, 22, 0.16);
            color: #fb923c;
            border-color: rgba(249, 115, 22, 0.35);
        }

        .dash-risk-pill.risk-high {
            background: rgba(239, 68, 68, 0.16);
            color: #f87171;
            border-color: rgba(239, 68, 68, 0.35);
        }

        .dash-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.15), transparent 30%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 20px;
            padding: 22px 24px;
            height: 210px;
            min-height: 210px;
            max-height: 210px;
            box-sizing: border-box;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.08);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .dash-card::before {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 20px;
            pointer-events: none;
            border: 1px solid transparent;
        }

        .dash-card.accent-blue::before {
            border-color: rgba(59, 130, 246, 0.28);
        }

        .dash-card.accent-green::before {
            border-color: rgba(34, 197, 94, 0.28);
        }

        .dash-card.accent-orange::before {
            border-color: rgba(249, 115, 22, 0.28);
        }

        .dash-card.accent-purple::before {
            border-color: rgba(124, 58, 237, 0.28);
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

        .dash-card-title {
            color: #a7bad8;
            font-weight: 650;
            font-size: 0.95rem;
            margin-bottom: 12px;
            letter-spacing: -0.01em;
            max-width: 68%;
            line-height: 1.3;
        }

        .dash-card-value {
            color: #f8fafc;
            font-weight: 800;
            font-size: 1.78rem;
            letter-spacing: -0.045em;
            line-height: 1.15;
            margin-top: 8px;
            margin-bottom: 10px;
            position: relative;
            z-index: 2;
            white-space: nowrap;
        }

        .dash-card-caption {
            color: #8fa3c4;
            font-size: 0.88rem;
            line-height: 1.35;
            font-weight: 500;
            position: relative;
            z-index: 2;
            margin-top: auto;
            min-height: 38px;
        }

        .dash-delta {
            border-radius: 999px;
            padding: 6px 11px;
            font-size: 0.78rem;
            font-weight: 800;
            position: relative;
            z-index: 2;
            min-width: 58px;
            text-align: center;
            white-space: nowrap;
            flex-shrink: 0;
        }

        .dash-delta.positive {
            background: rgba(34, 197, 94, 0.16);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.35);
        }

        .dash-delta.negative {
            background: rgba(239, 68, 68, 0.16);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.35);
        }

        .dash-risk-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.15), transparent 34%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 22px;
            padding: 28px;
            min-height: 390px;
            text-align: center;
            box-sizing: border-box;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.10);
        }

        .dash-risk-title {
            color: #f8fafc;
            font-weight: 800;
            font-size: 1.3rem;
            margin-bottom: 5px;
            letter-spacing: -0.025em;
        }

        .dash-risk-subtitle {
            color: #8fa3c4;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 26px;
        }

        .dash-risk-circle {
            width: 175px;
            height: 175px;
            border-radius: 999px;
            margin: 0 auto 26px auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 14px solid rgba(96, 165, 250, 0.20);
            background: #07111f;
        }

        .dash-risk-circle.risk-low {
            border-color: #22c55e;
            box-shadow: 0 0 38px rgba(34, 197, 94, 0.18);
        }

        .dash-risk-circle.risk-medium {
            border-color: #f97316;
            box-shadow: 0 0 38px rgba(249, 115, 22, 0.18);
        }

        .dash-risk-circle.risk-high {
            border-color: #ef4444;
            box-shadow: 0 0 38px rgba(239, 68, 68, 0.18);
        }

        .dash-risk-value {
            color: #ffffff;
            font-weight: 800;
            font-size: 2.1rem;
            letter-spacing: -0.04em;
        }

        .dash-risk-label {
            color: #a7bad8;
            font-size: 0.85rem;
            font-weight: 700;
        }

        .dash-risk-note {
            color: #8fa3c4;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .dark-section-title {
            color: #f8fafc;
            font-size: 1.2rem;
            font-weight: 800;
            margin: 1.2rem 0 0.8rem 0;
        }

        /* =========================
           CLIENT RISK / ML PAGE
        ========================= */
        .risk-page-hero {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.26), transparent 34%),
                linear-gradient(135deg, #0b1730 0%, #102f76 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 24px;
            padding: 30px 34px;
            margin-bottom: 1.6rem;
            box-shadow:
                0 24px 60px rgba(15, 23, 42, 0.30),
                0 0 60px rgba(37, 99, 235, 0.14);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
        }

        .risk-page-eyebrow {
            color: #93c5fd;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 9px;
        }

        .risk-page-title {
            color: #f8fafc;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            margin-bottom: 8px;
        }

        .risk-page-subtitle {
            color: #cbd5e1;
            font-size: 0.98rem;
            line-height: 1.5;
            max-width: 720px;
        }

        .risk-page-score {
            width: 165px;
            height: 165px;
            border-radius: 999px;
            background: #07111f;
            border: 12px solid rgba(96, 165, 250, 0.20);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            flex-shrink: 0;
        }

        .risk-page-score.risk-low {
            border-color: #22c55e;
            box-shadow: 0 0 38px rgba(34, 197, 94, 0.18);
        }

        .risk-page-score.risk-medium {
            border-color: #f97316;
            box-shadow: 0 0 38px rgba(249, 115, 22, 0.18);
        }

        .risk-page-score.risk-high {
            border-color: #ef4444;
            box-shadow: 0 0 38px rgba(239, 68, 68, 0.18);
        }

        .risk-page-score-value {
            color: white;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.04em;
        }

        .risk-page-score-label {
            color: #8fa3c4;
            font-size: 0.78rem;
            font-weight: 700;
            text-align: center;
        }

        .risk-metric-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.15), transparent 30%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 20px;
            padding: 22px;
            height: 178px;
            min-height: 178px;
            max-height: 178px;
            box-sizing: border-box;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.08);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
        }

        .risk-metric-card::before {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 20px;
            pointer-events: none;
            border: 1px solid transparent;
        }

        .risk-metric-card.accent-blue::before {
            border-color: rgba(59, 130, 246, 0.30);
        }

        .risk-metric-card.accent-green::before {
            border-color: rgba(34, 197, 94, 0.28);
        }

        .risk-metric-card.accent-orange::before {
            border-color: rgba(249, 115, 22, 0.30);
        }

        .risk-metric-card.accent-purple::before {
            border-color: rgba(124, 58, 237, 0.30);
        }

        .risk-metric-title {
            color: #a7bad8;
            font-weight: 600;
            font-size: 0.95rem;
            line-height: 1.3;
            position: relative;
            z-index: 1;
            min-height: 24px;
        }

        .risk-metric-value {
            color: #f8fafc;
            font-weight: 800;
            font-size: 1.9rem;
            letter-spacing: -0.04em;
            line-height: 1.1;
            white-space: nowrap;
            position: relative;
            z-index: 1;
        }

        .risk-metric-subtitle {
            color: #8fa3c4;
            font-size: 0.88rem;
            line-height: 1.4;
            min-height: 38px;
            position: relative;
            z-index: 1;
        }

        .risk-explain-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.14), transparent 34%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 22px;
            padding: 28px;
            height: 390px;
            min-height: 390px;
            box-sizing: border-box;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.10);
        }

        .risk-explain-title {
            color: #f8fafc;
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 18px;
        }

        .risk-explain-main {
            display: inline-flex;
            padding: 10px 14px;
            border-radius: 999px;
            font-weight: 800;
            margin-bottom: 18px;
        }

        .risk-explain-main.risk-low {
            background: rgba(34, 197, 94, 0.16);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.35);
        }

        .risk-explain-main.risk-medium {
            background: rgba(249, 115, 22, 0.16);
            color: #fb923c;
            border: 1px solid rgba(249, 115, 22, 0.35);
        }

        .risk-explain-main.risk-high {
            background: rgba(239, 68, 68, 0.16);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.35);
        }

        .risk-explain-text {
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 18px;
        }

        .risk-explain-note {
            color: #8fa3c4;
            font-size: 0.88rem;
            line-height: 1.5;
        }

        /* =========================
           LOCAL SHAP EXPLANATION
        ========================= */
        .shap-section-header {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.18), transparent 32%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 22px;
            padding: 24px 28px;
            margin: 0.4rem 0 1.25rem 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 22px;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.10);
        }

        .shap-section-eyebrow {
            color: #60a5fa;
            font-size: 0.76rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            margin-bottom: 8px;
        }

        .shap-section-title {
            color: #f8fafc;
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 6px;
        }

        .shap-section-subtitle {
            color: #8fa3c4;
            font-size: 0.9rem;
            line-height: 1.5;
            max-width: 760px;
        }

        .shap-local-badge {
            background: rgba(59, 130, 246, 0.16);
            color: #60a5fa;
            border: 1px solid rgba(96, 165, 250, 0.34);
            border-radius: 999px;
            padding: 10px 15px;
            font-size: 0.82rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .shap-summary-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.13), transparent 34%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 22px;
            padding: 25px;
            height: 430px;
            min-height: 430px;
            max-height: 430px;
            box-sizing: border-box;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.10);
        }

        .shap-summary-title {
            color: #f8fafc;
            font-size: 1.22rem;
            font-weight: 800;
            margin-bottom: 20px;
            letter-spacing: -0.02em;
        }

        .shap-summary-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            padding: 14px 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.14);
        }

        .shap-summary-row span {
            color: #8fa3c4;
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
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.12), transparent 34%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 22px;
            padding: 24px;
            height: 485px;
            min-height: 485px;
            max-height: 485px;
            box-sizing: border-box;
            overflow: hidden;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.10);
        }

        .shap-factor-card-title {
            color: #f8fafc;
            font-size: 1.18rem;
            font-weight: 800;
            margin-bottom: 6px;
            letter-spacing: -0.02em;
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

        .shap-factor-code {
            color: #60a5fa;
            font-weight: 800;
            font-size: 0.76rem;
            margin-bottom: 3px;
        }

        .shap-factor-name {
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
            flex-shrink: 0;
            border-radius: 999px;
            padding: 7px 10px;
            font-size: 0.78rem;
            font-weight: 800;
            min-width: 72px;
            text-align: center;
        }

        .shap-impact.risk {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.32);
        }

        .shap-impact.protective {
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.32);
        }

        .shap-empty {
            color: #8fa3c4;
            font-size: 0.9rem;
            margin-top: 22px;
        }

        /* Stil rămas compatibil dacă încă există vreun bloc vechi feature-card */
        .feature-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.14), transparent 34%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 22px;
            padding: 24px;
            height: 390px;
            min-height: 390px;
            box-sizing: border-box;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.10);
        }

        .feature-card-title {
            color: #f8fafc;
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .feature-card-subtitle {
            color: #8fa3c4;
            font-size: 0.9rem;
            line-height: 1.5;
            margin-bottom: 18px;
        }

        .feature-row {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            padding: 12px 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.14);
        }

        .feature-row:last-child {
            border-bottom: none;
        }

        .feature-code {
            color: #93c5fd;
            font-weight: 800;
            font-size: 0.9rem;
        }

        .feature-name {
            color: #cbd5e1;
            font-size: 0.88rem;
            margin-top: 3px;
        }

        .feature-value {
            color: #f8fafc;
            font-weight: 800;
        }

        .model-meta-card {
            background:
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.12), transparent 34%),
                linear-gradient(180deg, #10233c 0%, #0b1b31 100%);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 20px;
            padding: 22px 24px;
            margin-top: 1.2rem;
            display: flex;
            justify-content: space-between;
            gap: 24px;
            align-items: center;
            box-shadow:
                0 14px 36px rgba(0, 0, 0, 0.25),
                0 0 34px rgba(37, 99, 235, 0.08);
        }

        .model-meta-title {
            color: #f8fafc;
            font-weight: 800;
            font-size: 1.1rem;
        }

        .model-meta-subtitle {
            color: #8fa3c4;
            margin-top: 4px;
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
           ONBOARDING PAGE
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

        .onboarding-card {
            background: white;
            border-radius: 18px;
            padding: 28px 34px;
            max-width: 720px;
            margin: 0 auto 1.5rem auto;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
            border: 1px solid #eef2f6;
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
            background: white;
            border-radius: 18px;
            padding: 22px 24px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
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

        .confirm-row {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            padding: 14px 16px;
            border-bottom: 1px solid #e5e7eb;
            color: #475467;
            font-size: 0.93rem;
        }

        .confirm-row:last-child {
            border-bottom: none;
        }

        .confirm-row span {
            color: #667085;
            font-weight: 600;
        }

        .confirm-row strong {
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
           ANALYST DASHBOARD
        ========================= */
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

        .uploads-table-header {
            display: grid;
            grid-template-columns: 2.4fr 2.6fr 1.5fr 1.3fr 1.7fr;
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
           REVIEW IMPORT MODAL
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

        .review-detail-row {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            padding: 13px 16px;
            border-bottom: 1px solid #e5e7eb;
        }

        .review-detail-row:last-child {
            border-bottom: none;
        }

        .review-detail-row span {
            color: #667085;
            font-weight: 600;
        }

        .review-detail-row strong {
            color: #101828;
            font-weight: 850;
            text-align: right;
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
           CLIENT IMPORTS PAGE
        ========================= */
        .client-imports-table-header {
            display: grid;
            grid-template-columns: 2.4fr 1.5fr 1.2fr 2.4fr;
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
            .client-imports-table-header {
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