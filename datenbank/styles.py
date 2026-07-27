import streamlit as st

def lade_app_design():
    theme = st.session_state.get("app_theme", "Premium Dark")
    
    # 1. Farb-Definitionen je nach Theme
    if theme == "Premium Light":
        bg_main = "#ffffff"
        bg_sidebar = "#f1f5f9"
        text_color = "#0f172a"
        bg_card = "#ffffff"
        bg_element = "#f8fafc"
        border_color = "#cbd5e1"
        dropdown_bg = "#ffffff"
        dropdown_hover = "#e2e8f0"
    elif theme == "Premium Cashmere":
        bg_main = "#f9f6f0"
        bg_sidebar = "#eee8dc"
        text_color = "#2c2621"
        bg_card = "#fdfbf7"
        bg_element = "#f0eae1"
        border_color = "#d6ccc2"
        dropdown_bg = "#ffffff"
        dropdown_hover = "#e6dfd5"
    elif theme == "Premium Business":
        bg_main = "#0a192f"
        bg_sidebar = "#112240"
        text_color = "#e2e8f0"
        bg_card = "rgba(17, 34, 64, 0.7)"
        bg_element = "#1d3557"
        border_color = "rgba(255, 255, 255, 0.1)"
        dropdown_bg = "#112240"
        dropdown_hover = "#1d3557"
    elif theme == "Premium Slate":
        bg_main = "#1e293b"
        bg_sidebar = "#0f172a"
        text_color = "#f1f5f9"
        bg_card = "rgba(15, 23, 42, 0.6)"
        bg_element = "#334155"
        border_color = "rgba(255, 255, 255, 0.1)"
        dropdown_bg = "#0f172a"
        dropdown_hover = "#334155"
    else:  # Premium Dark (Standard)
        bg_main = "#0e1117"
        bg_sidebar = "#262730"
        text_color = "#fafafa"
        bg_card = "rgba(128, 128, 128, 0.04)"
        bg_element = "#262730"
        border_color = "rgba(128, 128, 128, 0.2)"
        dropdown_bg = "#262730"
        dropdown_hover = "#3d3e42"

    # 2. Globales CSS, das alle Komponenten weltweit einfärbt
    st.markdown(
        f"""
        <style>
        /* Allgemeine App-Hintergründe & Textfarben */
        .stApp {{
            background-color: {bg_main} !important;
            color: {text_color} !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: {bg_sidebar} !important;
        }}
        
        /* Globale Text- und Label-Farben erzwingen */
        p, span, label, div, h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
        }}

        /* GLOBALE FIXES FÜR INPUTS, DROPDOWNS & SELECTIONS (Schwarze Boxen eliminieren) */
        input, textarea {{
            background-color: {dropdown_bg} !important;
            color: {text_color} !important;
            border-color: {border_color} !important;
        }}

        /* Streamlit Selectbox / Multiselect Hauptbox */
        div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {{
            background-color: {dropdown_bg} !important;
            color: {text_color} !important;
            border-color: {border_color} !important;
        }}

        /* Dropdown Popup-Menüs (Die aufgeklappte Liste) */
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {{
            background-color: {dropdown_bg} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
        }}

        /* Einzelne Elemente in Auswahllisten */
        ul[role="listbox"] li, li[role="option"] {{
            background-color: {dropdown_bg} !important;
            color: {text_color} !important;
        }}

        /* Hover-Effekt in Dropdowns lesbar machen */
        ul[role="listbox"] li:hover,
        ul[role="listbox"] li[aria-selected="true"],
        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {{
            background-color: {dropdown_hover} !important;
            color: {text_color} !important;
        }}

        /* Container & Karten global anpassen */
        div[data-testid="stVerticalBlock"] div[data-testid="stContainer"] {{
            background-color: {bg_card} !important;
            border-color: {border_color} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
