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
        subtle_text = "#9aa8c0"
    else:
        card_bg = "#ffffff"
        text_color = "#1a2233"
        input_bg = "#f5f7fa"
        input_border = "#d0d7e2"
        subtle_text = "#5b6b7c"

    max_width = "1100px" if wide else "700px"

    alert_overrides = ""
    if dark:
        alert_overrides = """
        [data-testid="stAlert"] { background-color: #1f2a40 !important; }
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
        margin: 2rem auto 3rem auto;
        background: {card_bg};
        border-radius: 20px;
        padding: 2.5rem 2.5rem 2rem 2.5rem;
        box-shadow: 0 25px 70px rgba(0,0,0,0.45);
    }}
    h1, h2, h3, h4, h5, h6, p, span, label, li,
    [data-testid="stMarkdownContainer"], [data-testid="stCaptionContainer"] {{
        color: {text_color} !important;
    }}
    .brand-header {{
        text-align: center;
        margin-bottom: 1.5rem;
    }}
    .brand-header img {{
        width: 88px;
    }}
    .brand-header .brand-tagline {{
        color: {subtle_text} !important;
        font-size: 0.85rem;
        margin-top: 0.35rem;
    }}
    [data-testid="stExpander"] {{
        background-color: {input_bg} !important;
        border-color: {input_border} !important;
        border-radius: 10px !important;
    }}
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
    }}
    .stTextInput input, .stTextArea textarea, [data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border-color: {input_border} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stFileUploaderDropzone"] {{
        background-color: {input_bg} !important;
        border-color: {input_border} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stFileUploaderDropzone"] * {{
        color: {text_color} !important;
    }}
    button {{
        border-radius: 8px !important;
    }}
    button[kind="primary"], [data-testid="baseButton-primary"] {{
        background-color: {_ACCENT} !important;
        color: #ffffff !important;
        border-color: {_ACCENT} !important;
    }}
    a, a:visited {{
        color: {_ACCENT} !important;
    }}
    [data-testid="stAlert"] {{
        border-radius: 10px !important;
    }}
    hr {{
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
