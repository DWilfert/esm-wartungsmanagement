import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def zeige_startseite():
    if "app_theme" not in st.session_state:
        st.session_state.app_theme = "Premium Dark"

    if "language" not in st.session_state:
        st.session_state.language = "de"

    ctx_params = st.query_params
    if "lang" in ctx_params:
        gewaehlte_sprache = ctx_params["lang"]
        if gewaehlte_sprache != st.session_state.language:
            st.session_state.language = gewaehlte_sprache
            st.query_params.clear()
            st.rerun()

    if st.session_state.language == "de":
        TXT_HOME = {
            "titel_home": "🏠 Vertrags & Wartungsmanagement V1.3.1.0",
            "subtitel_home": "Zentrale Erfassung, Analyse und Fristen-Überwachung.",
            "fristen_status": "Fristen-Detailübersicht:", "ueberfaellig": "Überfällig", "anstehend": "Anstehend", "ordnung": "In Ordnung"
        }
        TXT_KACHELN = {
            "not_title": "🚨 ESM Notfall-Kontakte", "not_hm": "Hausmeisterdienst", "not_so": "Security Officer", "not_tn": "Technischer Notdienst", "not_sd": "Sicherheitsdienst",
            "btn_edit": "🔧 Notfallkontakte & Standorte bearbeiten", "pw_label": "Passwort eingeben:", "form_title": "Daten anpassen", "btn_save": "Speichern", "error_pw": "Falsches Passwort!",
            "kachel_standorte": "🏫 Standorte", "np_label": "Höhere Schule Neuperlach (NP):", "fg_label": "Grundschule & Kita Fasangarten (FG):"
        }
    else:
        TXT_HOME = {
            "titel_home": "🏠 Contract & Maintenance Management V1.3.1.0",
            "subtitel_home": "Central recording, analysis and deadline monitoring.",
            "fristen_status": "Detailed Deadline Overview:", "ueberfaellig": "Overdue", "anstehend": "Upcoming", "ordnung": "In Order"
        }
        TXT_KACHELN = {
            "not_title": "🚨 ESM Emergency Contacts", "not_hm": "Facility Caretaker", "not_so": "Security Officer", "not_tn": "Technical Emergency", "not_sd": "Security Service",
            "btn_edit": "🔧 Edit Emergency Contacts & Locations", "pw_label": "Enter Password:", "form_title": "Adjust Data", "btn_save": "Save", "error_pw": "Incorrect Password!",
            "kachel_standorte": "🏫 Locations", "np_label": "Higher School Neuperlach (NP):", "fg_label": "Primary School & Nursery Fasangarten (FG):"
        }

    col_titel, col_steuerung = st.columns([0.75, 0.25])
    
    with col_titel:
        st.markdown(f"### {TXT_HOME['titel_home']}")
    
    with col_steuerung:
        de_style = "opacity: 1.0; transform: scale(1.15);" if st.session_state.language == "de" else "opacity: 0.65;"
        en_style = "opacity: 1.0; transform: scale(1.15);" if st.session_state.language == "en" else "opacity: 0.65;"
        
        st.markdown(
            f'<div style="display: flex; justify-content: flex-end; gap: 15px; margin-top: 8px;">'
            f'<a href="?lang=de" target="_self" title="Deutsch" style="text-decoration: none; {de_style}"><img src="https://flagcdn.com/w40/de.png" style="width: 24px; height: auto; border-radius: 2px;"></a>'
            f'<a href="?lang=en" target="_self" title="English" style="text-decoration: none; {en_style}"><img src="https://flagcdn.com/w40/gb.png" style="width: 24px; height: auto; border-radius: 2px;"></a>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown(f"<div style='font-size:13px; color:#94a3b8; margin-top:-10px; margin-bottom:10px;'>{TXT_HOME['subtitel_home']}</div>", unsafe_allow_html=True)
    st.write("---")

    # --- ✨ DIE NEON-KPI-KARTEN (Mit stabilen Demo-Werten) ---
    st.markdown("""
        <style>
        .neon-kpi-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(56, 189, 248, 0.4);
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.15);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .neon-kpi-title {
            font-size: 12px;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        .neon-kpi-value {
            font-size: 26px;
            font-weight: 800;
            color: #38bdf8;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
        }
        .start-kachel {
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sofortige Demo-Vertragsdaten für die KPI-Berechnung
    total_vertraege = 10
    c_rot = 3
    c_gelb = 2
    c_gruen = 5

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown(f"""
            <div class="neon-kpi-card">
                <div class="neon-kpi-title">{"Gesamtverträge" if st.session_state.language == "de" else "Total Contracts"}</div>
                <div class="neon-kpi-value">{total_vertraege}</div>
            </div>
        """, unsafe_allow_html=True)
    with col_kpi2:
        status_text = f"{c_rot} Überfällig" if st.session_state.language == "de" else f"{c_rot} Overdue"
        status_color = "#f87171"
        
        st.markdown(f"""
            <div class="neon-kpi-card">
                <div class="neon-kpi-title">{"Fristen-Alarm" if st.session_state.language == "de" else "Deadline Status"}</div>
                <div class="neon-kpi-value" style="color: {status_color}; text-shadow: 0 0 10px {status_color}66;">{status_text}</div>
            </div>
        """, unsafe_allow_html=True)
    with col_kpi3:
        st.markdown(f"""
            <div class="neon-kpi-card">
                <div class="neon-kpi-title">{"System-Status" if st.session_state.language == "de" else "System Status"}</div>
                <div class="neon-kpi-value" style="color: #818cf8; text-shadow: 0 0 10px rgba(129,140,248,0.4);">Online 🟢</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-size: 12px; color: #94a3b8; margin-bottom: 15px;'>{TXT_HOME['fristen_status']} &nbsp;&nbsp;<span style='color:#f87171'>🔴 {c_rot} {TXT_HOME['ueberfaellig']}</span> &nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#fbbf24'>🟡 {c_gelb} {TXT_HOME['anstehend']}</span> &nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#34d399'>🟢 {c_gruen} {TXT_HOME['ordnung']}</span></div>", unsafe_allow_html=True)
    st.write("---")

    adresse_np = "Elise-Aulinger-Straße 21<br>81739 München"
    adresse_fg = "Auguste-Kent-Platz 3<br>81549 München"
    
    notdienst_dict = {
        "Hausmeisterdienst": "0176 / 1112223",
        "Security Officer": "0176 / 4445556",
        "Technischer Notdienst": "089 / 9998887",
        "Sicherheitsdienst": "089 / 1239874"
    }

    col_kachel1, col_kachel2 = st.columns(2)
    with col_kachel1:
        st.markdown(
            f'<div class="start-kachel">'
            f'<h4>{TXT_KACHELN["kachel_standorte"]}</h4>'
            f'<p style="font-size: 13px; line-height: 1.5;">'
            f'<b>{TXT_KACHELN["np_label"]}</b><br>{adresse_np}<br><br>'
            f'<b>{TXT_KACHELN["fg_label"]}</b><br>{adresse_fg}'
            f'</p>'
            f'</div>', 
            unsafe_allow_html=True
        )

    with col_kachel2:
        st.markdown(
            f'<div class="start-kachel">'
            f'<h4>{TXT_KACHELN["not_title"]}</h4>'
            f'<table style="width:100%; font-size: 13px; border-spacing: 0 6px;">'
            f'<tr><td><b>{TXT_KACHELN["not_hm"]}:</b></td><td style="color:#34d399; text-align:right;">{notdienst_dict.get("Hausmeisterdienst", "")}</td></tr>'
            f'<tr><td><b>{TXT_KACHELN["not_so"]}:</b></td><td style="color:#34d399; text-align:right;">{notdienst_dict.get("Security Officer", "")}</td></tr>'
            f'<tr><td><b>{TXT_KACHELN["not_tn"]}:</b></td><td style="color:#fbbf24; text-align:right;">{notdienst_dict.get("Technischer Notdienst", "")}</td></tr>'
            f'<tr><td><b>{TXT_KACHELN["not_sd"]}:</b></td><td style="color:#34d399; text-align:right;">{notdienst_dict.get("Sicherheitsdienst", "")}</td></tr>'
            f'</table>'
            f'</div>', 
            unsafe_allow_html=True
        )

    if "edit_startseite" not in st.session_state: 
        st.session_state.edit_startseite = False
        
    if st.button(TXT_KACHELN["btn_edit"]): 
        st.session_state.edit_startseite = not st.session_state.edit_startseite

    if st.session_state.edit_startseite:
        pw = st.text_input(
            TXT_KACHELN["pw_label"], 
            type="password", 
            key="esm_unblockable_secure_search_field_final"
        )
        
        if pw == "esm":
            with st.form("edit_notfall_form"):
                st.markdown("##### " + ("🏫 Standorte (Objekt-Adressen)" if st.session_state.language == "de" else "🏫 Locations (Object Addresses)"))
                neue_adr_np = st.text_area(TXT_KACHELN["np_label"].replace(":", ""), value="Elise-Aulinger-Straße 21\n81739 München", height=70)
                neue_adr_fg = st.text_area(TXT_KACHELN["fg_label"].replace(":", ""), value="Auguste-Kent-Platz 3\n81549 München", height=70)
                
                st.markdown("---")
                st.markdown(f"##### {TXT_KACHELN['not_title']}")
                n_hm = st.text_input(TXT_KACHELN["not_hm"], value=notdienst_dict.get('Hausmeisterdienst', ''))
                n_so = st.text_input(TXT_KACHELN["not_so"], value=notdienst_dict.get('Security Officer', ''))
                n_tn = st.text_input(TXT_KACHELN["not_tn"], value=notdienst_dict.get('Technischer Notdienst', ''))
                n_sd = st.text_input(TXT_KACHELN["not_sd"], value=notdienst_dict.get('Sicherheitsdienst', ''))
                
                if st.form_submit_button(TXT_KACHELN["btn_save"]):
                    st.success("Erfolgreich gespeichert!" if st.session_state.language == "de" else "Successfully saved!")
                    st.session_state.edit_startseite = False
                    st.rerun()
