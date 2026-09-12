import base64

import streamlit as st

from .config import BASE_DIR

LOGO_PATH = BASE_DIR / "assets" / "logo_apiis.png"

_GRADIENT_BG = "linear-gradient(135deg, #2c6ea5 0%, #123657 45%, #081522 100%)"
_ACCENT = "#1C86C7"


def _build_css(dark: bool, wide: bool) -> str:
    if dark:
        card_bg = "#131b2e"
        text_color = "#f0f2f5"
        input_bg = "#1e2940"
        input_border = "#334166"
    else:
        card_bg = "#ffffff"
        text_color = "#1a2233"
        input_bg = "#f5f7fa"
        input_border = "#d0d7e2"

    max_width = "1100px" if wide else "900px"

    alert_overrides = ""
    if dark:
        alert_overrides = """
        .st-key-brand_card [data-testid="stAlert"] {
            background-color: #1f2a40 !important;
        }
        [data-testid="stAlertContentSuccess"], [data-testid="stAlertContentSuccess"] * {
            color: #6fe3a1 !important;
        }
        [data-testid="stAlertContentInfo"], [data-testid="stAlertContentInfo"] * {
            color: #7fc8f8 !important;
        }
        [data-testid="stAlertContentWarning"], [data-testid="stAlertContentWarning"] * {
            color: #ffd479 !important;
        }
        [data-testid="stAlertContentError"], [data-testid="stAlertContentError"] * {
            color: #ff8a8a !important;
        }
        """

    return f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: {_GRADIENT_BG} !important;
    }}
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}
    section[data-testid="stSidebar"] {{
        background: #0d2b4a !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: #ffffff !important;
    }}
    .block-container {{
        max-width: {max_width};
        margin: 1rem auto 3rem auto;
        background: transparent !important;
    }}

    /* Logo + tagline sit directly on the gradient, outside the card */
    .brand-header {{
        text-align: center;
        margin: 1.5rem 0 2rem 0;
    }}
    .brand-header img {{
        width: 340px;
        max-width: 80%;
    }}
    .brand-header .brand-tagline {{
        color: rgba(255, 255, 255, 0.85) !important;
        font-size: 0.95rem;
        margin-top: 0.6rem;
    }}

    /* The bordered container (st.container(border=True)) is styled as the card */
    .st-key-brand_card {{
        background: {card_bg} !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 25px 70px rgba(0,0,0,0.45) !important;
        padding: 2.5rem 2.5rem 2rem 2.5rem !important;
    }}
    .st-key-brand_card h1,
    .st-key-brand_card h2,
    .st-key-brand_card h3,
    .st-key-brand_card h4,
    .st-key-brand_card h5,
    .st-key-brand_card h6,
    .st-key-brand_card p,
    .st-key-brand_card span,
    .st-key-brand_card label,
    .st-key-brand_card li,
    .st-key-brand_card [data-testid="stMarkdownContainer"],
    .st-key-brand_card [data-testid="stCaptionContainer"] {{
        color: {text_color} !important;
    }}
    .st-key-brand_card [data-testid="stExpander"] {{
        background-color: {input_bg} !important;
        border-color: {input_border} !important;
        border-radius: 10px !important;
    }}
    .st-key-brand_card [data-testid="stExpander"] summary,
    .st-key-brand_card [data-testid="stExpander"] summary span,
    .st-key-brand_card [data-testid="stExpander"] summary p,
    .st-key-brand_card [data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
    }}
    .st-key-brand_card .stTextInput input,
    .st-key-brand_card .stTextArea textarea,
    .st-key-brand_card [data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border-color: {input_border} !important;
        border-radius: 8px !important;
    }}
    .st-key-brand_card [data-testid="stFileUploaderDropzone"] {{
        background-color: {input_bg} !important;
        border-color: {input_border} !important;
        border-radius: 8px !important;
    }}
    .st-key-brand_card [data-testid="stFileUploaderDropzone"] * {{
        color: {text_color} !important;
    }}
    .st-key-brand_card button {{
        border-radius: 8px !important;
    }}
    .st-key-brand_card button[kind="primary"],
    .st-key-brand_card [data-testid="baseButton-primary"] {{
        background-color: {_ACCENT} !important;
        color: #ffffff !important;
        border-color: {_ACCENT} !important;
    }}
    .st-key-brand_card a,
    .st-key-brand_card a:visited {{
        color: {_ACCENT} !important;
    }}
    .st-key-brand_card [data-testid="stAlert"] {{
        border-radius: 10px !important;
    }}
    .st-key-brand_card hr {{
        border-color: {input_border} !important;
    }}
    {alert_overrides}
    </style>
    """


def is_dark() -> bool:
    return st.session_state.get("dark_mode", False)


def apply_theme(wide: bool = False):
    st.markdown(_build_css(is_dark(), wide), unsafe_allow_html=True)


def render_logo_header(tagline: str = ""):
    if not LOGO_PATH.exists():
        return
    logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    tagline_html = f'<div class="brand-tagline">{tagline}</div>' if tagline else ""
    st.markdown(
        f"""
        <div class="brand-header">
            <img src="data:image/png;base64,{logo_b64}" />
            {tagline_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
