import streamlit as st
import base64
import os
import warnings
import json

# --- IMPORTE ---
from datenbank.befehle import initialisiere_beispieldaten, hole_datenbank_verbindung
from datenbank.styles import lade_app_design
from seiten.startseite import zeige_startseite
from seiten.admin import zeige_adminbereich
from seiten.vertragsanalyse import zeige_vertragsanalyse
from seiten.wartungsanalyse import zeige_wartungsanalyse
from seiten.auffaelligkeiten import zeige_auffaelligkeiten
from seiten.anlagenstruktur import zeige_anlagenstruktur
from seiten.serviceeinsaetze import zeige_serviceeinsaetze
from seiten.plan_5jahres import zeige_5jahresplan
from seiten.firmeninfo import zeige_firmeninfo
from seiten.import_export import zeige_import_export
from seiten.vertrag_dokumente import zeige_vertragsdokumente
from seiten.einstellungen import zeige_einstellungen
from seiten.kontakt import zeige_kontaktformular
from seiten.anlagen_history import zeige_anlagen_history
from seiten.globale_suche import zeige_globale_suche

warnings.filterwarnings("ignore", category=UserWarning)

# --- SESSION STATES & SICHERHEIT ---
if "language" not in st.session_state:
    st.session_state.language = "de"

if "app_theme" not in st.session_state:
    st.session_state.app_theme = "Premium Dark"

if "speicher_modus" not in st.session_state:
    st.session_state.speicher_modus = "manuell"

# Einstellungen beim Start laden (vollständig fehlergeschützt für die Cloud)
try:
    conn = hole_datenbank_verbindung()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT schluessel, wert FROM `user_einstellungen` WHERE schluessel IN ('app_theme', 'speicher_modus')")
        for row in cursor.fetchall():
            val = json.loads(row["wert"])
            if row["schluessel"] == "app_theme":
                st.session_state.app_theme = val
            elif row["schluessel"] == "speicher_modus":
                st.session_state.speicher_modus = val
        cursor.close()
        conn.close()
except Exception:
    pass

# --- BILINGUALES MENÜ-WÖRTERBUCH ---
TXT_MENU = {
    "de": {
        "hauptmenue": "### 🌟 HAUPTMENÜ",
        "m1": "🏠 Startseite",  
        "m16": "🔍 Globale Suche",  
        "m2": "📊 Vertragsanalyse", "m3": "📂 Vertragsdokumente",
        "m4": "📈 Wartungsanalyse", "m5": "⚠️ Auffälligkeiten", "m6": "🏫 Anlagen NP & FG",
        "m15": "🔄 360° Anlagen", 
        "m7": "🛠️ Service NP & FG", "m8": "📅 Jahresplan", "m9": "🏢 Firmeninfo",
        "m10": "📥 Import/Export", "m11": "🛡️ Admin", "m12": "⚙️ Einstellungen",
        "m13": "✉️ Support & Kontakt"
    },
    "en": {
        "hauptmenue": "### 🌟 MAIN MENU",
        "m1": "🏠 Home",  
        "m16": "🔍 Global Search",
        "m2": "📊 Contract Analysis", "m3": "📂 Contract Documents",
        "m4": "📈 Maintenance Analysis", "m5": "⚠️ Discrepancies", "m6": "Asset Structure NP & FG",
        "m15": "🔄 360° Assets", 
        "m7": "🛠️ Service NP & FG", "m8": "📅 Annual Plan", "m9": "🏢 Company Info",
        "m10": "📥 Import/Export", "m11": "🛡️ Admin", "m12": "⚙️ Settings",
        "m13": "✉️ Support & Contact"
    }
}[st.session_state.language]

if "app_seite_wechseln" not in st.session_state:
    st.session_state.app_seite_wechseln = False

if "app_ziel_seite" not in st.session_state:
    st.session_state.app_ziel_seite = None

if st.session_state.app_seite_wechseln:
    if st.session_state.app_ziel_seite is not None:
        st.session_state.haupt_navigation_final = st.session_state.app_ziel_seite
    else:
        st.session_state.haupt_navigation_final = TXT_MENU["m1"]  
    st.session_state.app_seite_wechseln = False
    st.session_state.app_ziel_seite = None

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ESM Wartungsmanagement V1.3.1.0 Enterprise",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME FARBEN ---
theme = st.session_state.app_theme

if theme == "Premium Business":
    bg_color = "#0a192f"         
    sidebar_color = "#112240"    
elif theme == "Premium Cashmere":
    bg_color = "#f9f6f0"         
    sidebar_color = "#eee8dc"    
elif theme == "Premium Slate":
    bg_color = "#1e293b"
    sidebar_color = "#0f172a"
elif theme == "Premium Light":
    bg_color = "#ffffff"
    sidebar_color = "#f1f5f9"
else:  
    bg_color = "#0e1117"         
    sidebar_color = "#262730"    

st.markdown(
    f"""
    <style>
    .stAppDeployButton {{ display: none !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    header {{ background: transparent !important; }}
    [data-testid="collapsedControl"] {{ top: 25px !important; left: 20px !important; z-index: 999999 !important; }}
    
    .stApp {{ background-color: {bg_color} !important; }}
    [data-testid="stSidebar"] {{ background-color: {sidebar_color} !important; }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- INITIALISIERUNG & LOGO ---
lade_app_design()
try:
    initialisiere_beispieldaten()
except Exception:
    pass

logo_pfad = "logo1.png"
try:
    if os.path.exists(logo_pfad):
        with open(logo_pfad, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.sidebar.markdown(
            f'<div style="text-align: center; margin-bottom: 20px;">'
            f'<img src="data:image/png;base64,{encoded_string}" style="max-width: 100%; height: auto; border-radius: 8px; display: block; margin: 0 auto;">'
            f'<div style="font-size: 0.72rem; color: var(--text-color); opacity: 0.6; margin-top: 3px; letter-spacing: 0.5px;">© D.Wilfert / 2026</div>'
            f'</div>', 
            unsafe_allow_html=True
        )
except Exception as e:
    pass

# --- SIDEBAR INTERFACE ---
st.sidebar.markdown(TXT_MENU["hauptmenue"])

ausgewaehlter_punkt = st.sidebar.radio(
    "Navigieren zu:" if st.session_state.language == "de" else "Navigate to:",
    [TXT_MENU[k] for k in ["m1", "m16", "m2", "m3", "m4", "m5", "m6", "m15", "m7", "m8", "m9", "m10", "m11", "m12", "m13"]], 
    key="haupt_navigation_final"
)

# --- ROUTING SYSTEM ---
if ausgewaehlter_punkt == TXT_MENU["m1"]:
    zeige_startseite()  
elif ausgewaehlter_punkt == TXT_MENU["m16"]:
    zeige_globale_suche()
elif ausgewaehlter_punkt == TXT_MENU["m2"]:
    zeige_vertragsanalyse("")
elif ausgewaehlter_punkt == TXT_MENU["m3"]:
    zeige_vertragsdokumente()
elif ausgewaehlter_punkt == TXT_MENU["m4"]:
    zeige_wartungsanalyse()
elif ausgewaehlter_punkt == TXT_MENU["m5"]:
    zeige_auffaelligkeiten()
elif ausgewaehlter_punkt == TXT_MENU["m6"]:
    zeige_anlagenstruktur()
elif ausgewaehlter_punkt == TXT_MENU["m15"]:
    zeige_anlagen_history()
elif ausgewaehlter_punkt == TXT_MENU["m7"]:
    zeige_serviceeinsaetze()
elif ausgewaehlter_punkt == TXT_MENU["m8"]:
    zeige_5jahresplan()
elif ausgewaehlter_punkt == TXT_MENU["m9"]:
    zeige_firmeninfo()
elif ausgewaehlter_punkt == TXT_MENU["m10"]:
    zeige_import_export()
elif ausgewaehlter_punkt == TXT_MENU["m11"]:
    zeige_adminbereich()
elif ausgewaehlter_punkt == TXT_MENU["m12"]:
    zeige_einstellungen()
elif ausgewaehlter_punkt == TXT_MENU["m13"]:
    zeige_kontaktformular()
