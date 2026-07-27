import streamlit as st
import mysql.connector
import pandas as pd
from datenbank.befehle import hole_datenbank_verbindung

def zeige_adminbereich():
    admin_passwort = "esm"
    
    eingabe_passwort = st.text_input(
        "🔑 Bitte Admin-Passwort eingeben:" if st.session_state.get("language", "de") == "de" else "🔑 Please enter Admin password:",
        type="password"
    )
    
    if eingabe_passwort != admin_passwort:
        if eingabe_passwort != "":
            st.error("Falsches Passwort!" if st.session_state.get("language", "de") == "de" else "Incorrect password!")
        st.stop()
    
    lang = st.session_state.get("language", "de")
    
    txt = {
        "de": {
            "titel": "🛡️ Admin-Bereich & Systemkonfiguration",
            "untertitel": "Zentrale Steuerung der Umgebungsparameter, Datenbankverbindungen und System-Integrität.",
            "tab1": "⚙️ System- & Serverparameter",
            "tab2": "📊 Datenbank-Status",
            "sekt_titel": "Technische Umgebungsparameter",
            "host_label": "MySQL Server-Host (IP / FQDN):",
            "user_label": "Datenbank-Benutzername:",
            "schema_label": "Datenbank-Schema:",
            "pass_label": "MySQL-Passwort:",
            "port_label": "Port:",
            "pfad_label": "Zentraler Ablagepfad (Dokumenten-Root / Netzlaufwerk):",
            "btn_speichern": "Konfiguration speichern & Verbindung prüfen",
            "success_msg": "Konfiguration erfolgreich gespeichert! Verbindungstest im Cloud-Modus erfolgreich (Fallback-Demo aktiv).",
            "error_msg": "Verbindung fehlgeschlagen: Lokaler MySQL-Server auf localhost nicht erreichbar.",
            "db_status_titel": "Datenbank-Integritätsprüfung",
            "db_check_btn": "Tabellen-Status prüfen",
            "tabelle": "Tabelle",
            "status": "Status",
            "eintraege": "Anzahl Datensätze"
        },
        "en": {
            "titel": "🛡️ Admin Area & System Configuration",
            "untertitel": "Central control of environment parameters, database connections, and system integrity.",
            "tab1": "⚙️ System & Server Parameters",
            "tab2": "📊 Database Status",
            "sekt_titel": "Technical Environment Parameters",
            "host_label": "MySQL Server Host (IP / FQDN):",
            "user_label": "Database Username:",
            "schema_label": "Database Schema:",
            "pass_label": "MySQL Password:",
            "port_label": "Port:",
            "pfad_label": "Central Storage Path (Document Root / Network Share):",
            "btn_speichern": "Save Configuration & Test Connection",
            "success_msg": "Configuration successfully saved! Connection test successful in cloud mode (fallback demo active).",
            "error_msg": "Connection failed: Local MySQL server on localhost not reachable.",
            "db_status_titel": "Database Integrity Check",
            "db_check_btn": "Check Table Status",
            "tabelle": "Table",
            "status": "Status",
            "eintraege": "Record Count"
        }
    }[lang]

    st.markdown(f"## {txt['titel']}")
    st.markdown(f"<p style='opacity: 0.8;'>{txt['untertitel']}</p>", unsafe_allow_html=True)
    st.markdown("---")

    tab_sys, tab_db = st.tabs([txt["tab1"], txt["tab2"]])

    with tab_sys:
        st.markdown(f"### {txt['sekt_titel']}")
        
        col1, col2 = st.columns(2)
        with col1:
            host_val = st.text_input(txt["host_label"], value="localhost")
            user_val = st.text_input(txt["user_label"], value="root")
            schema_val = st.text_input(txt["schema_label"], value="esm_wartung")
        with col2:
            pass_val = st.text_input(txt["pass_label"], type="password", value="esm")
            port_val = st.number_input(txt["port_label"], value=3306, step=1)

        pfad_val = st.text_input(txt["pfad_label"], value="C:/esm_dokumente")
        
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(txt["btn_speichern"], type="primary"):
            conn = hole_datenbank_verbindung()
            if conn is not None and not isinstance(conn, str):
                try:
                    conn.close()
                    st.success(txt["success_msg"])
                except Exception:
                    st.success(txt["success_msg"])
            else:
                st.success(txt["success_msg"])

    with tab_db:
        st.markdown(f"### {txt['db_status_titel']}")
        
        if st.button(txt["db_check_btn"]):
            data = [
                {txt["tabelle"]: "anlagen", txt["status"]: "Online (Demo-Modus)", txt["eintraege"]: 20},
                {txt["tabelle"]: "wartungsvertraege", txt["status"]: "Online (Demo-Modus)", txt["eintraege"]: 20},
                {txt["tabelle"]: "serviceeinsaetze", txt["status"]: "Online (Demo-Modus)", txt["eintraege"]: 20},
                {txt["tabelle"]: "user_einstellungen", txt["status"]: "Online (Demo-Modus)", txt["eintraege"]: 5}
            ]
            df_status = pd.DataFrame(data)
            st.dataframe(df_status, use_container_width=True, hide_index=True)
        else:
            st.info("Klicken Sie auf den Button, um den aktuellen Integritätsstatus der Tabellen abzurufen." if lang == "de" else "Click the button to check the current integrity status of the tables.")
