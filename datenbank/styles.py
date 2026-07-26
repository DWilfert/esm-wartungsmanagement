import streamlit as st

def lade_app_design():
    valid_themes = ["Premium Dark", "Premium Business", "Premium Slate", "Premium Light", "Premium Cashmere"]
    if 'app_theme' not in st.session_state or st.session_state.app_theme not in valid_themes:
        st.session_state.app_theme = "Premium Dark"

    theme = st.session_state.app_theme

    if theme == "Premium Business":
        bg_app = "radial-gradient(circle at top left, #1e293b 0%, #0f172a 100%)"
        solid_bg = "#0f172a"
        border_color = "rgba(96, 165, 250, 0.3)"
        card_bg = "rgba(17, 27, 48, 0.7)"
        text_main = "#f8fafc"
        text_muted = "#94a3b8"
        accent_color = "#60a5fa"
        input_bg = "rgba(15, 23, 42, 0.9)"
        
    elif theme == "Premium Slate":
        bg_app = "radial-gradient(circle at top left, #3f3f46 0%, #18181b 100%)"
        solid_bg = "#18181b"
        border_color = "rgba(161, 161, 170, 0.3)"
        card_bg = "rgba(39, 39, 42, 0.7)"
        text_main = "#f4f4f5"
        text_muted = "#a1a1aa"
        accent_color = "#a1a1aa"
        input_bg = "rgba(24, 24, 27, 0.9)"

    elif theme == "Premium Light":
        bg_app = "radial-gradient(circle at top left, #ffffff 0%, #f1f5f9 100%)"
        solid_bg = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.15)"
        card_bg = "rgba(255, 255, 255, 0.9)"
        text_main = "#0f172a"  
        text_muted = "#64748b"
        accent_color = "#3b82f6"
        input_bg = "#f8fafc" 

    elif theme == "Premium Cashmere":
        bg_app = "radial-gradient(circle at top left, #fdfbf7 0%, #e6e2d8 100%)"
        solid_bg = "#fdfbf7"
        border_color = "rgba(139, 115, 85, 0.3)"
        card_bg = "rgba(255, 255, 255, 0.8)"
        text_main = "#433422"  
        text_muted = "#8b7355"
        accent_color = "#8b7355"
        input_bg = "#ffffff" 

    else:
        bg_app = "radial-gradient(circle at top left, #1a1f2c 0%, #0e1117 100%)"
        solid_bg = "#0e1117"
        border_color = "rgba(74, 144, 226, 0.3)"
        card_bg = "rgba(22, 27, 38, 0.7)"
        text_main = "#e2e8f0"
        text_muted = "#94a3b8"
        accent_color = "#4a90e2"
        input_bg = "rgba(14, 17, 23, 0.9)"

    bg_sidebar = bg_app
    pfeil_farbe = accent_color

    st.markdown(f"""
        <style>
        :root, [data-testid="stAppViewContainer"] {{
            --primary-color: {accent_color};
            --background-color: {solid_bg};
            --secondary-background-color: {input_bg};
            --text-color: {text_main};
            --body-text-color: {text_main};
            --widget-background-color: {input_bg};
            --widget-text-color: {text_main};
        }}

        [data-testid="stHeader"] {{ background: transparent !important; }}
        [data-testid="stDecoration"] {{ display: none !important; }}
        [data-testid="stMainBlockContainer"] {{ padding-top: 3rem !important; }}
        
        .stApp {{ 
            background: {bg_app} !important; 
            font-family: 'Inter', sans-serif; 
        }}
        
        section[data-testid="stSidebar"] > div:first-child,
        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"] {{ 
            background: {bg_sidebar} !important; 
            background-color: transparent !important; 
            border-right: 1px solid {border_color} !important; 
        }}

        h1, h2, h3, h4, h5, h6, p, span, label, div {{
            color: {text_main} !important;
        }}

        div[data-testid="stForm"], .start-kachel {{
            background: {card_bg} !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid {border_color} !important;
            border-radius: 12px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15) !important;
        }}
        
        /* RADIKALER FIX FÜR SEGMENTED CONTROLS & AUSWAHL-BUTTONS */
        div[data-testid="stSegmentedControl"] div[role="button"],
        div[data-testid="stSegmentedControl"] button,
        div[data-testid="stSegmentedControl"] span,
        div[data-testid="stSegmentedControl"] p {{
            background-color: {input_bg} !important;
            color: {text_main} !important;
        }}
        
        div[data-testid="stSegmentedControl"] div[role="button"]:hover,
        div[data-testid="stSegmentedControl"] button:hover {{
            background-color: {border_color} !important;
            color: {accent_color} !important;
        }}

        /* TABELLEN */
        [data-testid="stDataFrame"], [data-testid="stTable"] {{
            background-color: {card_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px;
        }}
        
        [data-testid="stDataFrame"] div[data-baseweb="base-input"] input,
        [data-testid="stDataFrame"] table {{
            color: {text_main} !important;
        }}

        /* MENÜS & DROPDOWNS */
        [data-baseweb="popover"] > div,
        [data-baseweb="menu"],
        ul[role="listbox"],
        li[role="option"] {{
            background-color: {input_bg} !important;
            color: {text_main} !important;
        }}
        
        li[role="option"]:hover {{
            background-color: {border_color} !important;
        }}
        
        input, textarea, [data-baseweb="select"] div, [data-baseweb="base-input"] {{
            background-color: {input_bg} !important;
            color: {text_main} !important;
            border-color: {border_color} !important;
        }}

        /* STANDARD-BUTTONS */
        div[data-testid="stButton"] button,
        div[data-testid="stFormSubmitButton"] button,
        div[data-testid="stDownloadButton"] button {{
            background-color: {card_bg} !important;
            color: {text_main} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px !important;
            transition: all 0.3s ease;
        }}
        
        div[data-testid="stButton"] button:hover,
        div[data-testid="stFormSubmitButton"] button:hover,
        div[data-testid="stDownloadButton"] button:hover {{
            border-color: {accent_color} !important;
            color: {accent_color} !important;
        }}
        
        [data-testid="stButton"] button:has(strong) p,
        [data-testid="stButton"] button:has(em) p {{
            display: none !important;
        }}
        
        [data-testid="stSidebarCollapseButton"] {{
            display: inline-flex !important;
            visibility: visible !important;
            background-color: transparent !important;
            z-index: 999999 !important;
        }}
        [data-testid="stSidebarCollapseButton"] svg {{
            fill: {pfeil_farbe} !important;
            color: {pfeil_farbe} !important;
        }}
        </style>
    """, unsafe_allow_html=True)