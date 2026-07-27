import streamlit as st
from datenbank.befehle import hole_datenbank_verbindung
import json

def zeige_einstellungen():
    st.markdown("""
        <style>
        /* Kompakte Schriftgröße in allen Eingabefeldern, Radio-Buttons und Formularen */
        input, select, textarea, div[data-baseweb="select"] span, label, .stRadio div {
            font-size: 0.82rem !important;
        }
        
        /* Blendet den automatischen Streamlit-Hinweis aus */
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        
        /* Dropdown-Menüs und Popovers */
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
            background-color: var(--secondary-background-color) !important;
        }
        
        ul[role="listbox"] li, li[role="option"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            font-size: 0.85rem !important;
        }
        
        /* Dezenter, dunkler Hover-Zustand passend zum Dark-Mode */
        ul[role="listbox"] li:hover,
        ul[role="listbox"] li[aria-selected="true"],
        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {
            background-color: rgba(128, 128, 128, 0.25) !important;
            color: var(--text-color) !important;
        }
        
        /* Tooltips & Toolbar-Buttons */
        div[data-testid="stElementToolbar"], 
        div[data-testid="stElementToolbar"] button,
        span[data-testid="stTooltipHoverTarget"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
        }
        
        div[data-baseweb="tooltip"], div[role="tooltip"], div.stTooltipContent {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.3) !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.language == "de":
        TXT_E = {
            "title": "⚙️ Benutzer- & Systemeinstellungen",
            "desc": "Zentrale Steuerungseinheit für persönliche Ansichten, Präferenzen und das UI-Verhalten am Arbeitsplatz.",
            "card_ansicht": "🖥️ Ansichten & Filter-Verhalten",
            "card_design": "🎨 Design & Benutzeroberfläche",
            "radio_label": "Automatisches Speichern von Filtern:",
            "opt_manuell": "Persönliche Einstellungen dauerhaft merken",
            "opt_auto": "Standard / Automatisch entscheiden",
            "theme_label": "Design-Thema (Farbgebung):",
            "start_label": "Standard-Startseite beim Login:",
            "density_label": "Tabellen-Zeilendichte:",
            "opt_compact": "Kompakt (Maximale Übersicht)",
            "opt_comfort": "Komfortabel (Mehr Abstand)",
            "btn_save": "Änderungen speichern",
            "success": "Benutzer-Einstellungen erfolgreich aktualisiert!"
        }
    else:
        TXT_E = {
            "title": "⚙️ User & System Settings",
            "desc": "Central control unit for personal views, preferences, and UI behavior at the workstation.",
            "card_ansicht": "🖥️ Views & Filter Behavior",
            "card_design": "🎨 Design & User Interface",
            "radio_label": "Automatic saving of filters:",
            "opt_manuell": "Remember personal settings permanently",
            "opt_auto": "Standard / Decide automatically",
            "theme_label": "Design Theme (Color Scheme):",
            "start_label": "Default Landing Page upon login:",
            "density_label": "Table Row Density:",
            "opt_compact": "Compact (Maximum overview)",
            "opt_comfort": "Comfortable (More spacing)",
            "btn_save": "Save Changes",
            "success": "User settings successfully updated!"
        }

    st.subheader(TXT_E["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 25px;'>{TXT_E['desc']}</div>", unsafe_allow_html=True)

    # Werte aus Datenbank laden (oder Fallback auf Session State)
    aktueller_modus = "manuell"
    aktuelles_theme = st.session_state.get("app_theme", "Premium Dark")
    aktuelle_startseite = st.session_state.get("startseite", "Startseite")
    aktuelle_dichte = st.session_state.get("tabellen_dichte", "Kompakt")
    
    conn = hole_datenbank_verbindung()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT schluessel, wert FROM `user_einstellungen` WHERE schluessel IN ('speicher_modus', 'app_theme', 'startseite', 'tabellen_dichte')")
            ergebnisse = cursor.fetchall()
            for row in ergebnisse:
                val = json.loads(row["wert"])
                if row["schluessel"] == "speicher_modus":
                    aktueller_modus = val
                elif row["schluessel"] == "app_theme":
                    aktuelles_theme = val
                elif row["schluessel"] == "startseite":
                    aktuelle_startseite = val
                elif row["schluessel"] == "tabellen_dichte":
                    aktuelle_dichte = val
            cursor.close()
        except Exception as e:
            print(f"Lade-Fehler: {e}")
        finally:
            try:
                if conn is not None:
                    conn.close()
            except:
                pass

    # --- ENTERPRISE ZWEI-SPALTEN-GRID ---
    col_grid_1, col_grid_2 = st.columns(2, gap="medium")

    with col_grid_1:
        with st.container(border=True):
            st.markdown(f"##### {TXT_E['card_ansicht']}")
            st.write("")
            default_idx = 0 if aktueller_modus == "manuell" else 1
            wahl_modus = st.radio(
                TXT_E["radio_label"],
                options=[TXT_E["opt_manuell"], TXT_E["opt_auto"]],
                index=default_idx,
                key="einstellungen_speicher_radio"
            )

    with col_grid_2:
        with st.container(border=True):
            st.markdown(f"##### {TXT_E['card_design']}")
            st.write("")
            
            themen_optionen = ["Premium Dark", "Premium Business", "Premium Slate", "Premium Light", "Premium Cashmere"]
            try:
                theme_index = themen_optionen.index(aktuelles_theme)
            except ValueError:
                theme_index = 0

            startseiten_optionen = ["Startseite", "Globale Suche", "Vertragsanalyse", "Wartungsanalyse", "Jahresplan"]
            try:
                start_index = startseiten_optionen.index(aktuelle_startseite)
            except ValueError:
                start_index = 0

            dichte_optionen = [TXT_E["opt_compact"], TXT_E["opt_comfort"]]
            try:
                dichte_index = dichte_optionen.index(aktuelle_dichte)
            except ValueError:
                dichte_index = 0

            # Kompakte 50%-Spalten für die Dropdowns innerhalb der Karte
            col_dd1, _ = st.columns([6.0, 4.0])
            with col_dd1:
                wahl_theme = st.selectbox(TXT_E["theme_label"], options=themen_optionen, index=theme_index, key="einstellungen_theme_select")
                wahl_start = st.selectbox(TXT_E["start_label"], options=startseiten_optionen, index=start_index, key="einstellungen_start_select")
                wahl_dichte = st.selectbox(TXT_E["density_label"], options=dichte_optionen, index=dichte_index, key="einstellungen_dichte_select")

    st.write("")
    st.write("")
    if st.button(TXT_E["btn_save"], type="primary"):
        neuer_modus = "manuell" if wahl_modus == TXT_E["opt_manuell"] else "auto"
        
        # In Session State aktualisieren
        st.session_state.app_theme = wahl_theme
        st.session_state.startseite = wahl_start
        st.session_state.tabellen_dichte = wahl_dichte
        
        # In Datenbank speichern
        conn = hole_datenbank_verbindung()
        if conn is not None:
            try:
                cursor = conn.cursor()
                
                einstellungen_dict = {
                    'speicher_modus': neuer_modus,
                    'app_theme': wahl_theme,
                    'startseite': wahl_start,
                    'tabellen_dichte': wahl_dichte
                }
                
                for key, val in einstellungen_dict.items():
                    val_str = json.dumps(val)
                    cursor.execute(
                        "INSERT INTO `user_einstellungen` (schluessel, wert) VALUES (%s, %s) ON DUPLICATE KEY UPDATE wert = %s", 
                        (key, val_str, val_str)
                    )
                
                conn.commit()
                cursor.close()
                st.success(TXT_E["success"])
                st.rerun()
            except Exception as e:
                st.error(f"Fehler beim Speichern: {e}" if st.session_state.language == "de" else f"Error while saving: {e}")
            finally:
                try:
                    if conn is not None:
                        conn.close()
                except:
                    pass
        else:
            st.error("Keine Verbindung zur Datenbank." if st.session_state.language == "de" else "No database connection.")
