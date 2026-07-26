import streamlit as st
from datenbank.befehle import hole_datenbank_verbindung
import json

def zeige_einstellungen():
    if st.session_state.language == "de":
        TXT_E = {
            "title": "⚙️ Systemeinstellungen & Präferenzen",
            "desc": "Verwalte hier das globale Systemverhalten, Designs und Ansichten.",
            "hdr_speicher": "💾 Automatisches Speichern von Ansichten & Filtern",
            "radio_label": "Wie soll das System mit deinen Ansichts- und Filter-Einstellungen umgehen?",
            "opt_manuell": "Persönliche Einstellungen dauerhaft speichern (Meine Ansichten merken)",
            "opt_auto": "Automatisch / Standard (Vom Programm entscheiden lassen)",
            "hdr_design": "🎨 Design & Farb-Thema",
            "theme_label": "Wähle dein bevorzugtes Design-Thema:",
            "btn_save": "Einstellungen speichern",
            "success": "Einstellungen erfolgreich in der Datenbank gespeichert!"
        }
    else:
        TXT_E = {
            "title": "⚙️ System Settings & Preferences",
            "desc": "Manage global system behavior, designs, and views here.",
            "hdr_speicher": "💾 Automatic Saving of Views & Filters",
            "radio_label": "How should the system handle your view and filter settings?",
            "opt_manuell": "Save personal settings permanently (Remember my views)",
            "opt_auto": "Automatic / Default (Let the program decide)",
            "hdr_design": "🎨 Design & Color Theme",
            "theme_label": "Choose your preferred design theme:",
            "btn_save": "Save Settings",
            "success": "Settings successfully saved to the database!"
        }

    st.subheader(TXT_E["title"])
    st.markdown(f"<div style='font-size: 13px; color: #64748b; margin-bottom: 25px;'>{TXT_E['desc']}</div>", unsafe_allow_html=True)

    # Werte aus Datenbank laden
    aktueller_modus = "manuell"
    aktuelles_theme = st.session_state.get("app_theme", "Premium Dark")
    
    conn = hole_datenbank_verbindung()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT schluessel, wert FROM `user_einstellungen` WHERE schluessel IN ('speicher_modus', 'app_theme')")
            ergebnisse = cursor.fetchall()
            for row in ergebnisse:
                val = json.loads(row["wert"])
                if row["schluessel"] == "speicher_modus":
                    aktueller_modus = val
                elif row["schluessel"] == "app_theme":
                    aktuelles_theme = val
            cursor.close()
        except Exception as e:
            print(f"Lade-Fehler: {e}" if st.session_state.language == "de" else f"Load Error: {e}")
        finally:
            conn.close()

    # --- SPEICHER-MODUS AUSWAHL ---
    st.markdown(f"##### {TXT_E['hdr_speicher']}")
    default_idx = 0 if aktueller_modus == "manuell" else 1
    wahl_modus = st.radio(
        TXT_E["radio_label"],
        options=[TXT_E["opt_manuell"], TXT_E["opt_auto"]],
        index=default_idx,
        key="einstellungen_speicher_radio"
    )

    st.write("")

    # --- THEME AUSWAHL (Alle 5 Designs aus dem Screenshot) ---
    st.markdown(f"##### {TXT_E['hdr_design']}")
    themen_optionen = ["Premium Dark", "Premium Business", "Premium Slate", "Premium Light", "Premium Cashmere"]
    try:
        theme_index = themen_optionen.index(aktuelles_theme)
    except ValueError:
        theme_index = 0

    col_theme_1, _ = st.columns([4.0, 6.0])
    with col_theme_1:
        wahl_theme = st.selectbox(
            TXT_E["theme_label"],
            options=themen_optionen,
            index=theme_index,
            key="einstellungen_theme_select"
        )

    st.write("")
    if st.button(TXT_E["btn_save"], use_container_width=False):
        neuer_modus = "manuell" if wahl_modus == TXT_E["opt_manuell"] else "auto"
        
        # In Session State aktualisieren
        st.session_state.app_theme = wahl_theme
        
        # In Datenbank speichern
        conn = hole_datenbank_verbindung()
        if conn is not None:
            try:
                cursor = conn.cursor()
                # Speicher-Modus sichern
                val_mod_str = json.dumps(neuer_modus)
                cursor.execute("INSERT INTO `user_einstellungen` (schluessel, wert) VALUES ('speicher_modus', %s) ON DUPLICATE KEY UPDATE wert = %s", (val_mod_str, val_mod_str))
                
                # Theme sichern
                val_thm_str = json.dumps(wahl_theme)
                cursor.execute("INSERT INTO `user_einstellungen` (schluessel, wert) VALUES ('app_theme', %s) ON DUPLICATE KEY UPDATE wert = %s", (val_thm_str, val_thm_str))
                
                conn.commit()
                cursor.close()
                st.success(TXT_E["success"])
                st.rerun()
            except Exception as e:
                st.error(f"Fehler beim Speichern: {e}" if st.session_state.language == "de" else f"Error while saving: {e}")
            finally:
                conn.close()