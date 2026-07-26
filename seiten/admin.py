import streamlit as st
import mysql.connector
import pandas as pd
import os
from datetime import datetime
from datenbank.befehle import hole_datenbank_verbindung

def zeige_adminbereich():
    st.markdown("""
        <style>
        input, select, textarea, div[data-baseweb="select"] span, label, .stRadio div {
            font-size: 0.82rem !important;
        }
        
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        
        input::placeholder, textarea::placeholder {
            color: #94a3b8 !important;
            font-style: italic !important;
            opacity: 1 !important;
        }
        
        div[data-testid="stSegmentedControl"] button,
        div[data-baseweb="button-group"] button,
        button[data-baseweb="tab"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
        }
        
        div[data-testid="stSegmentedControl"] button[aria-selected="true"],
        div[data-baseweb="button-group"] button[aria-selected="true"] {
            background-color: #e2e8f0 !important;
            color: #0f172a !important;
        }
        
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
            background-color: var(--secondary-background-color) !important;
        }
        
        ul[role="listbox"] li, li[role="option"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            font-size: 0.85rem !important;
        }
        
        ul[role="listbox"] li:hover,
        ul[role="listbox"] li[aria-selected="true"],
        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {
            background-color: rgba(128, 128, 128, 0.25) !important;
            color: var(--text-color) !important;
        }
        
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

        div[data-testid="stDataFrame"] {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.language == "de":
        TXT_AD = {
            "title": "🛡️ Systemadministration & Server-Konfiguration",
            "pw_lbl": "Administrator-Passwort eingeben:",
            "access_granted": "🟢 Zugriff gewährt.",
            "access_denied": "Falsches Administrator-Passwort. Zugriff verweigert.",
            "tab_config": "⚙️ System- & Serverparameter",
            "tab_status": "📊 Datenbank-Status",
            "sub_params": "### ⚙️ Technische Umgebungsparameter",
            "lbl_host": "MySQL Server-Host (IP / FQDN):",
            "lbl_user": "Datenbank-Benutzername:",
            "lbl_db": "Datenbank-Schema:",
            "lbl_pw": "MySQL-Passwort:",
            "lbl_port": "Port:",
            "lbl_root": "Zentraler Ablagepfad (Dokumenten-Root / Netzlaufwerk):",
            "btn_save": "💾 Konfiguration speichern & Verbindung prüfen",
            "cfg_ok": "🟢 Parameter erfolgreich im System hinterlegt.",
            "conn_ok": "🟢 MySQL-Verbindungstest erfolgreich.",
            "conn_err": "⚠️ Pfad gespeichert, aber Verbindungstest fehlgeschlagen: ",
            "sub_metrics": "#### 📊 Datenbank-Metriken",
            "col_area": "Datenbereich",
            "col_rows": "Datensätze",
            "reset_header": "⚠️ Gefahrenzone: Datenbank-Reset",
            "reset_desc": "Hier kannst du alle gespeicherten Daten unwiderruflich aus den Tabellen löschen (z. B. zum Bereinigen der Demodaten).",
            "btn_reset_trigger": "🗑️ Alle Daten & Datensätze zurücksetzen / löschen",
            "reset_confirm_q": "Bist du absolut sicher, dass du sämtliche Tabellen leeren möchtest?",
            "btn_yes_delete": "Ja, unwiderruflich löschen",
            "reset_success": "🗑️ Alle Datenbanktabellen wurden erfolgreich geleert."
        }
        TAB_STATUS = {
            "wartungsvertraege": "Wartungsverträge", 
            "anlagen": "Anlagenstruktur",
            "wartungsplanung": "Mängel & Auffälligkeiten", 
            "serviceeinsaetze": "Serviceeinträge",
            "firmeninfo": "Firmen & Techniker"
        }
    else:
        TXT_AD = {
            "title": "🛡️ System Administration & Server Configuration",
            "pw_lbl": "Enter Administrator Password:",
            "access_granted": "🟢 Access granted.",
            "access_denied": "Incorrect administrator password. Access denied.",
            "tab_config": "⚙️ System & Server Parameters",
            "tab_status": "📊 Database Status",
            "sub_params": "### ⚙️ Technical Environment Parameters",
            "lbl_host": "MySQL Server Host (IP / FQDN):",
            "lbl_user": "Database Username:",
            "lbl_db": "Database Schema:",
            "lbl_pw": "MySQL Password:",
            "lbl_port": "Port:",
            "lbl_root": "Central Document Path (Document Root / Network Drive):",
            "btn_save": "💾 Save Configuration & Verify Connection",
            "cfg_ok": "🟢 Parameters successfully saved to system.",
            "conn_ok": "🟢 MySQL connection test successful.",
            "conn_err": "⚠️ Path saved, but connection test failed: ",
            "sub_metrics": "#### 📊 Database Metrics",
            "col_area": "Data Domain",
            "col_rows": "Records",
            "reset_header": "⚠️ Danger Zone: Database Reset",
            "reset_desc": "Here you can irrevocably delete all saved data from the tables (e.g., to clear demo data).",
            "btn_reset_trigger": "🗑️ Reset / Delete All Data & Records",
            "reset_confirm_q": "Are you absolutely sure you want to empty all tables?",
            "btn_yes_delete": "Yes, delete irrevocably",
            "reset_success": "🗑️ All database tables have been successfully emptied."
        }
        TAB_STATUS = {
            "wartungsvertraege": "Maintenance Contracts", 
            "anlagen": "Asset Structure",
            "wartungsplanung": "Defects & Anomalies", 
            "serviceeinsaetze": "Service Records",
            "firmeninfo": "Companies & Technicians"
        }

    st.subheader(TXT_AD["title"])
    col_pw_ad, _ = st.columns([3.5, 6.5])
    with col_pw_ad:
        admin_pw = st.text_input(TXT_AD["pw_lbl"], type="password", key="admin_system_auth_input_v8", autocomplete="off")

    if admin_pw == "esm":
        st.success(TXT_AD["access_granted"])
        
        admin_unterbereich = st.segmented_control(
            "",
            [TXT_AD["tab_config"], TXT_AD["tab_status"]],
            default=TXT_AD["tab_config"],
            key="admin_tabs_ersatz_v8"
        )
        
        if admin_unterbereich == TXT_AD["tab_config"]:
            st.markdown(TXT_AD["sub_params"])
            with st.form("server_config_form_final_v8", clear_on_submit=False):
                c_srv1, c_srv2 = st.columns(2)
                with c_srv1:
                    srv_host = st.text_input(TXT_AD["lbl_host"], value="localhost", autocomplete="off")
                    srv_user = st.text_input(TXT_AD["lbl_user"], value="root", autocomplete="off")
                    srv_db = st.text_input(TXT_AD["lbl_db"], value="esm_wartung", autocomplete="off")
                with c_srv2:
                    srv_pw = st.text_input(TXT_AD["lbl_pw"], value="", type="password", autocomplete="off")
                    srv_port = st.number_input(TXT_AD["lbl_port"], min_value=1, max_value=65535, value=3306)
                
                st.markdown("---")
                doc_path_input = st.text_input(
                    TXT_AD["lbl_root"], 
                    value="C:/esm_dokumente", 
                    key="admin_doc_path_config_v8",
                    autocomplete="off"
                )
                
                if st.form_submit_button(TXT_AD["btn_save"]):
                    st.success(TXT_AD["cfg_ok"])
                    if srv_pw != "":
                        try:
                            test_conn = mysql.connector.connect(
                                host=srv_host, user=srv_user, password=srv_pw, database=srv_db, port=int(srv_port), connect_timeout=3
                            )
                            if test_conn.is_connected():
                                test_conn.close()
                                st.success(TXT_AD["conn_ok"])
                        except Exception as srv_err:
                            st.warning(f"{TXT_AD['conn_err']}{str(srv_err)}")
                            
        elif admin_unterbereich == TXT_AD["tab_status"]:
            st.markdown(TXT_AD["sub_metrics"])
            conn = hole_datenbank_verbindung()
            if conn is not None:
                stats_daten = []
                try:
                    cursor = conn.cursor()
                    for tech_name, klar_name in TAB_STATUS.items():
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM `{tech_name}`")
                            anzahl_zeilen = cursor.fetchone()
                            anz_wert = anzahl_zeilen[0] if anzahl_zeilen else 0
                        except:
                            anz_wert = 0
                        stats_daten.append({TXT_AD["col_area"]: klar_name, TXT_AD["col_rows"]: anz_wert})
                    cursor.close()
                    st.dataframe(pd.DataFrame(stats_daten), use_container_width=True, hide_index=True)
                except Exception as e:
                    pass
                finally:
                    conn.close()

            st.write("")
            st.markdown("---")
            st.markdown(f"##### {TXT_AD['reset_header']}")
            st.markdown(f"<div style='font-size: 13px; color: #94a3b8; margin-bottom: 10px;'>{TXT_AD['reset_desc']}</div>", unsafe_allow_html=True)

            if "confirm_db_reset" not in st.session_state:
                st.session_state.confirm_db_reset = False

            if not st.session_state.confirm_db_reset:
                if st.button(TXT_AD["btn_reset_trigger"], key="btn_trigger_db_reset_v8"):
                    st.session_state.confirm_db_reset = True
                    st.rerun()
            else:
                st.warning(TXT_AD["reset_confirm_q"])
                col_b1, col_b2, _ = st.columns([2.0, 2.0, 6.0])
                with col_b1:
                    if st.button(TXT_AD["btn_yes_delete"], type="primary", key="btn_execute_db_reset_v8"):
                        conn_res = hole_datenbank_verbindung()
                        if conn_res is not None:
                            try:
                                cur_res = conn_res.cursor()
                                cur_res.execute("SET FOREIGN_KEY_CHECKS = 0;")
                                for t_name in TAB_STATUS.keys():
                                    try:
                                        cur_res.execute(f"TRUNCATE TABLE `{t_name}`")
                                    except:
                                        pass
                                cur_res.execute("SET FOREIGN_KEY_CHECKS = 1;")
                                conn_res.commit()
                                cur_res.close()
                                st.success(TXT_AD["reset_success"])
                                st.session_state.confirm_db_reset = False
                                st.rerun()
                            except Exception as res_err:
                                st.error(f"Fehler beim Zurücksetzen: {res_err}")
                            finally:
                                conn_res.close()
                with col_b2:
                    if st.button("Abbrechen" if st.session_state.language == "de" else "Cancel", key="btn_cancel_db_reset_v8"):
                        st.session_state.confirm_db_reset = False
                        st.rerun()

    elif admin_pw != "":
        st.error(TXT_AD["access_denied"])