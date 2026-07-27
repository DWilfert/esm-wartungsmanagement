import streamlit as st
import pandas as pd
from datenbank.befehle import hole_datenbank_verbindung, schreibe_datenbank_daten

def zeige_auffalligkeiten():
    st.markdown("""
        <style>
        input, select, textarea, div[data-baseweb="select"] span, label {
            font-size: 0.82rem !important;
        }
        div[data-testid="InputInstructions"] { display: none !important; }
        div[data-testid="stDataFrame"] {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }
        .auffallig-card {
            background-color: var(--secondary-background-color);
            border: 1px solid var(--primary-color);
            border-radius: 8px;
            padding: 18px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            color: var(--text-color);
        }
        </style>
    """, unsafe_allow_html=True)

    if 'language' not in st.session_state:
        st.session_state.language = "de"

    if st.session_state.language == "de":
        TXT_AUF = {
            "title": "⚠️ Auffälligkeiten & Mängelmanagement",
            "desc": "Erfassung und Bearbeitung von technischen Mängeln, Fristüberschreitungen und Unstimmigkeiten.",
            "sec_uebersicht": "🔍 1. Thema: Aktuelle Auffälligkeiten",
            "sec_loeschen": "🗑️ 2. Thema: Eintrag löschen",
            "lbl_id_loeschen": "Eintrag löschen anhand ID:",
            "btn_loeschen": "Löschen ausführen"
        }
    else:
        TXT_AUF = {
            "title": "⚠️ Anomalies & Defect Management",
            "desc": "Recording and processing of technical defects, deadline overruns, and discrepancies.",
            "sec_uebersicht": "🔍 1. Theme: Current Anomalies",
            "sec_loeschen": "🗑️ 2. Theme: Delete Entry",
            "lbl_id_loeschen": "Delete entry by ID:",
            "btn_loeschen": "Execute Deletion"
        }

    st.subheader(TXT_AUF["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 20px;'>{TXT_AUF['desc']}</div>", unsafe_allow_html=True)

    df_auffalligkeiten = pd.DataFrame({
        "id": [1, 2, 3],
        "anlagenid": [17501, 17504, 17508],
        "bereich": ["Fördertechnik", "Elektrotechnik", "Wärmeversorgung"],
        "beschreibung": ["Notruf-Einrichtung defekt", "Prüfprotokoll unvollständig", "Druckverlust gemeldet"],
        "status": ["Offen", "In Bearbeitung", "Offen"],
        "datum": ["2026-05-10", "2026-06-01", "2026-07-15"]
    })

    # -------------------------------------------------------------
    # BEREICH 1: ÜBERSICHT
    # -------------------------------------------------------------
    with st.container(border=True):
        st.markdown(f"**{TXT_AUF['sec_uebersicht']}**")
        st.markdown("<hr style='border: none; height: 1px; background-color: rgba(128, 128, 128, 0.3); margin: 10px 0;'>", unsafe_allow_html=True)
        
        st.dataframe(df_auffalligkeiten, use_container_width=True, hide_index=True)

    st.write("")

    # -------------------------------------------------------------
    # BEREICH 2: EINTRAG LÖSCHEN
    # -------------------------------------------------------------
    with st.container(border=True):
        st.markdown(f"**{TXT_AUF['sec_loeschen']}**")
        st.markdown("<hr style='border: none; height: 1px; background-color: rgba(128, 128, 128, 0.3); margin: 10px 0;'>", unsafe_allow_html=True)
        
        col_id_sel, col_btn_del, col_space = st.columns([2.5, 2.5, 5.0])
        
        with col_id_sel:
            id_optionen = [""] + df_auffalligkeiten["id"].tolist()
            ausgewaehlte_id = st.selectbox(
                TXT_AUF["lbl_id_loeschen"],
                options=id_optionen,
                key="auffallig_loesch_id"
            )
            
        with col_btn_del:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True) 
            if st.button(TXT_AUF["btn_loeschen"], key="btn_auffallig_loeschen", use_container_width=True):
                if ausgewaehlte_id:
                    st.success(f"Eintrag mit ID {ausgewaehlte_id} wurde erfolgreich gelöscht!")
                else:
                    st.warning("Bitte wählen Sie zuerst eine gültige ID aus.")
