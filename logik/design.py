import streamlit as st

def lade_design_farben():
    if 'app_theme' not in st.session_state:
        st.session_state.app_theme = "Premium Dark"

    if st.session_state.app_theme == "Premium Cashmere":
        return {
            "bg_app": "linear-gradient(135deg, #f5f5f2 0%, #e8e8e3 100%)",
            "bg_sidebar": "#e8e8e3",          # Harmonisch an den Haupthintergrund angepasst
            "border_color": "#cbd5e1",
            "card_bg": "#ffffff",
            "text_main": "#1e293b",            # Dunkler Text für perfektes Lesen
            "text_muted": "#475569",
            "input_bg": "#ffffff",
            "accent_color": "#b45309"
        }
    elif st.session_state.app_theme == "Premium Business":
        return {
            "bg_app": "radial-gradient(circle at top left, #1e293b 0%, #0f172a 100%)",
            "bg_sidebar": "#0b1329",
            "border_color": "#1e293b",
            "card_bg": "#111b30",
            "text_main": "#f8fafc",
            "text_muted": "#94a3b8",
            "input_bg": "#1e293b",
            "accent_color": "#60a5fa"
        }
    else:  # Premium Dark
        return {
            "bg_app": "radial-gradient(circle at top left, #1a1f2c 0%, #0e1117 100%)",
            "bg_sidebar": "#111622",
            "border_color": "#232d42",
            "card_bg": "#161b26",
            "text_main": "#e2e8f0",
            "text_muted": "#94a3b8",
            "input_bg": "#1f293d",
            "accent_color": "#4a90e2"
        }

def korrigiere_menue_button():
    css_code = """
    <style>
        [data-testid="stSidebarCollapseButton"] {
            top: 20px !important;
        }
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)


def wende_design_an():
    """Liest die Farben aus und wendet das CSS dynamisch auf die gesamte App & Sidebar an."""
    farben = lade_design_farben()
    
    css = f"""
    <style>
        /* 1. Haupt-App Hintergrund & Schriftfarbe */
        .stApp {{
            background: {farben["bg_app"]};
            color: {farben["text_main"]};
        }}
        
        /* 2. Seitliches Menü (Sidebar) Hintergrund */
        [data-testid="stSidebar"] {{
            background-color: {farben["bg_sidebar"]} !important;
            border-right: 1px solid {farben["border_color"]};
        }}
        
        /* 3. Ausklappmenüs in der Sidebar (st.expander) */
        [data-testid="stSidebar"] .streamlit-expanderHeader {{
            background-color: {farben["card_bg"]} !important;
            color: {farben["text_main"]} !important;
            border: 1px solid {farben["border_color"]};
            border-radius: 8px;
        }}
        [data-testid="stSidebar"] .streamlit-expanderContent {{
            background-color: {farben["bg_sidebar"]} !important;
            color: {farben["text_main"]} !important;
            border: 1px solid {farben["border_color"]};
            border-top: none;
        }}
        
        /* 4. Texte, Labels, Pfeile & Überschriften in der Sidebar */
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] svg {{
            color: {farben["text_main"]} !important;
            fill: {farben["text_main"]} !important;
        }}
        
        /* 5. Eingabefelder in der Sidebar anpassen */
        [data-testid="stSidebar"] div[data-baseweb="input"],
        [data-testid="stSidebar"] div[data-baseweb="select"] {{
            background-color: {farben["input_bg"]} !important;
            border: 1px solid {farben["border_color"]};
            color: {farben["text_main"]} !important;
        }}
    </style>
    """
    # CSS in Streamlit injizieren
    st.markdown(css, unsafe_allow_html=True)
    
    # Deine Button-Korrektur direkt mit ausführen
    korrigiere_menue_button()