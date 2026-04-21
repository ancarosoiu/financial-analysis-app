import streamlit as st


def load_global_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                linear-gradient(135deg, rgba(8, 21, 58, 0.90), rgba(24, 71, 170, 0.78)),
                url('https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=1600&q=80');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 0.8rem;
            padding-bottom: 1rem;
        }

        .auth-logo-wrap {
            text-align: center;
            margin-top: 0.1rem;
            margin-bottom: 0.9rem;
        }

        .brand-badge {
            width: 58px;
            height: 58px;
            margin: 0 auto 12px auto;
            border-radius: 16px;
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.18);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            backdrop-filter: blur(8px);
            box-shadow: 0 10px 24px rgba(5, 20, 53, 0.18);
        }

        .center-brand-title {
            font-size: 2.3rem;
            font-weight: 800;
            color: white;
            line-height: 1.05;
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
        }

        .center-brand-subtitle {
            font-size: 1rem;
            color: rgba(255,255,255,0.88);
            line-height: 1.4;
        }

        .auth-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #10234b;
            margin-bottom: 0.15rem;
        }

        .auth-subtitle {
            color: #667085;
            font-size: 0.95rem;
            line-height: 1.45;
            margin-bottom: 0.55rem;
        }

        .auth-note {
            background: #f7f9fc;
            border: 1px solid #e8edf5;
            color: #475467;
            border-radius: 14px;
            padding: 10px 12px;
            font-size: 0.89rem;
            line-height: 1.45;
            margin-top: 0.65rem;
        }

        /* card-ul real al zonei centrale, aplicat pe tabs container */
        .stTabs {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid rgba(255,255,255,0.45);
            border-radius: 24px;
            padding: 0.95rem 1rem 0.85rem 1rem;
            box-shadow: 0 20px 50px rgba(4, 15, 44, 0.22);
            backdrop-filter: blur(10px);
            max-width: 760px;
            margin: 0 auto;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: #f3f6fb;
            border-radius: 14px;
            padding: 4px;
            margin-bottom: 0.9rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 10px;
            padding: 0 18px;
            font-weight: 700;
            color: #475467;
        }

        .stTabs [aria-selected="true"] {
            background: white !important;
            color: #1d4ed8 !important;
            box-shadow: 0 2px 8px rgba(15, 37, 84, 0.08);
        }

        label[data-testid="stWidgetLabel"] p {
            color: #24324a !important;
            font-weight: 600;
            font-size: 0.93rem;
        }

        .stTextInput > div > div,
        .stSelectbox > div > div,
        .stTextInput input {
            border-radius: 12px !important;
        }

        .stTextInput input {
            padding-top: 0.72rem !important;
            padding-bottom: 0.72rem !important;
        }

        .stSelectbox [data-baseweb="select"] > div {
            border-radius: 12px !important;
            min-height: 46px !important;
        }

        .stButton > button,
        .stForm button[kind="primary"] {
            width: 100%;
            height: 46px;
            border: 0;
            border-radius: 12px;
            background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%);
            color: white;
            font-weight: 700;
            font-size: 0.96rem;
            box-shadow: 0 10px 20px rgba(37, 99, 235, 0.20);
            transition: all 0.18s ease;
        }

        .stButton > button:hover,
        .stForm button[kind="primary"]:hover {
            background: linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%);
            color: white;
            transform: translateY(-1px);
        }

        [data-testid="stSuccess"],
        [data-testid="stAlert"] {
            border-radius: 14px;
        }

        [data-testid="stSidebar"] {
            background: rgba(9, 20, 52, 0.96);
        }

        @media (max-width: 768px) {
            .block-container {
                padding-top: 0.6rem;
                padding-bottom: 0.6rem;
            }

            .center-brand-title {
                font-size: 1.8rem;
            }

            .center-brand-subtitle {
                font-size: 0.92rem;
            }

            .stTabs {
                max-width: 100%;
                padding: 0.85rem 0.85rem 0.75rem 0.85rem;
                border-radius: 20px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.96);
            border-radius: 24px;
            padding: 24px 28px;
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
            margin-bottom: 22px;
        ">
            <div style="
                font-size: 2rem;
                font-weight: 800;
                color: #0f172a;
                margin-bottom: 6px;
            ">
                {title}
            </div>
            <div style="
                color: #475467;
                font-size: 1rem;
                line-height: 1.6;
            ">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str, caption: str):
    return f"""
    <div style="
        background: rgba(255,255,255,0.97);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.10);
        min-height: 140px;
    ">
        <div style="
            font-size: 0.95rem;
            color: #475467;
            margin-bottom: 10px;
            font-weight: 600;
        ">
            {title}
        </div>
        <div style="
            font-size: 2rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 8px;
        ">
            {value}
        </div>
        <div style="
            font-size: 0.86rem;
            color: #667085;
        ">
            {caption}
        </div>
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