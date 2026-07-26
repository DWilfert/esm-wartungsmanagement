import streamlit as st
import pandas as pd

def zeige_auffaelligkeiten():
    # Einheitlicher Design-Fix für Radio-Buttons, Toolbars und Tabellen
    st.markdown("""
        <style>
        /* Kompakte Schriftgröße in allen Eingabefeldern und Formularen */
        input, select, textarea, div[data-baseweb="select"] span, label {
            font-size: 0.82rem !important;
        }
        
        /* Blendet den automatischen Streamlit-Hinweis aus */
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        
        /* Placeholder in leicht grauer Schrift und Kursiv */
        input::placeholder, textarea::placeholder {
            color: #94a3b8 !important;
            font-style: italic !important;
            opacity: 1 !important;
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
        
        ul[role="listbox"] li:hover,
        ul[role="listbox"] li[aria-selected="true"],
        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {
            background-color: rgba(128, 128, 128, 0.2) !important;
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

        /* Automatischer Hintergrund- und Rahmen-Fix für st.dataframe */
        div[data-testid="stDataFrame"] {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.language == "de":
        TXT_AUF = {
            "title": "Mängel & Protokoll-Auffälligkeiten",
            "desc": "Zentrale Erfassung von sicherheitsrelevanten Mängeln, offenen Prüfpunkten und Abweichungen aus Wartungsprotokollen.",
            "act_lbl": "Aktion wählen:", 
            "act_doc": "Offene Mängel einsehen", 
            "act_manage": "Neuen Mangel erfassen",
            "form_std": "Standort:", "form_vrt": "Zugehöriger Vertrag:", "form_anl": "Anlagenbezeichnung:", "form_prt": "Protokoll-Nummer:", "form_com": "Mängelbeschreibung / Kommentar:",
            "btn_save": "Mangel im System registrieren", "success_doc": "Mangel erfolgreich dokumentiert!"
        }
    else:
        TXT_AUF = {
            "title": "Defects & Protocol Anomalies",
            "desc": "Central registration of safety-relevant defects, open inspection items, and deviations from maintenance protocols.",
            "act_lbl": "Select Action:", 
            "act_doc": "View Open Defects", 
            "act_manage": "Register New Defect",
            "form_std": "Location:", "form_vrt": "Associated Contract:", "form_anl": "Asset Designation:", "form_prt": "Protocol Number:", "form_com": "Defect Description / Comment:",
            "btn_save": "Register Defect in System", "success_doc": "Defect successfully documented!"
        }

    st.subheader(TXT_AUF["title"])
    st.markdown(f"<div style='font-size: 13px; color: #64748b; margin-bottom: 25px;'>{TXT_AUF['desc']}</div>", unsafe_allow_html=True)

    # Verwendung von st.radio für saubere, lesbare Buttons
    auf_aktion = st.radio(
        TXT_AUF["act_lbl"],
        options=[TXT_AUF["act_doc"], TXT_AUF["act_manage"]],
        horizontal=True,
        key="auf_main_navigation_radio_v9"
    )
    st.write("")

    if auf_aktion == TXT_AUF["act_manage"]:
        vertrag_optionen = ["", "[ID: 1] Vollwartungsvertrag Objekt 1", "[ID: 2] Vollwartungsvertrag Objekt 2", "[ID: 3] Vollwartungsvertrag Objekt 3"]
              
        with st.form("auf_form_einmalig", clear_on_submit=True):
            col_auf1, col_auf2, col_auf3, col_auf4 = st.columns(4)
            with col_auf1: a_standort = st.selectbox(TXT_AUF["form_std"], ["", "FG", "NP"], key="auf_std_field")
            with col_auf2: a_vertrag = st.selectbox(TXT_AUF["form_vrt"], vertrag_optionen, key="auf_vrt_field")
            with col_auf3: a_anlage = st.text_input(TXT_AUF["form_anl"], placeholder="Beispiel: Aufzug Hauptgebäude" if st.session_state.language == "de" else "e.g. Main Building Elevator", key="auf_anl_field")
            with col_auf4: a_protokoll = st.text_input(TXT_AUF["form_prt"], placeholder="Beispiel: PR-2026-04" if st.session_state.language == "de" else "e.g. PR-2026-04", key="auf_prt_field")
            a_kommentar = st.text_area(TXT_AUF["form_com"], placeholder="Beispiel: Schleifgeräusche im 2. OG, bitte Seilspannung prüfen." if st.session_state.language == "de" else "e.g. Grinding noise on 2nd floor, please check rope tension.", key="auf_com_field")
            
            if st.form_submit_button(TXT_AUF["btn_save"]):
                if not a_standort or not a_anlage: 
                    st.error("Bitte Pflichtfelder ausfüllen!" if st.session_state.language == "de" else "Please fill in required fields!")
                else:
                    st.success(TXT_AUF["success_doc"])
                    st.rerun()

    elif auf_aktion == TXT_AUF["act_doc"]:
        # Sofortige Demo-Mängel mit Ampelstatus bereitstellen
        df_auf = pd.DataFrame({
            "id": [1, 2, 3],
            "standort": ["NP", "FG", "NP"],
            "bezeichnung": ["Personenaufzug Hauptgebäude", "Lüftungsanlage Bibliothek", "Brandschutztür Flur Ost"],
            "bemerkung": ["🔴 Schleifgeräusche im Schacht, Seilprüfung erforderlich", "🟡 Filterwechsel überfällig und Luftstrom zu gering", "🟢 Dichtung beschädigt, Austausch anstehend"],
            "firma": ["Otis GmbH", "Stulz GmbH", "Siemens AG"],
            "protokoll": ["PR-2026-01", "PR-2026-02", "PR-2026-03"]
        })

        if not df_auf.empty:
            df_anzeige_auf = df_auf.copy()
            spalten_mapping_auf = {
                "id": "ID",
                "standort": "Standort" if st.session_state.language == "de" else "Location",
                "bezeichnung": "Anlage / Bezeichnung" if st.session_state.language == "de" else "Asset / Designation",
                "bemerkung": "Mängelbeschreibung & Status" if st.session_state.language == "de" else "Defect Description & Status",
                "firma": "Vertrag / Firma" if st.session_state.language == "de" else "Contract / Company",
                "protokoll": "Protokoll-Nr." if st.session_state.language == "de" else "Protocol No."
            }
            df_anzeige_auf.rename(columns=spalten_mapping_auf, inplace=True)
              
            st.dataframe(df_anzeige_auf, use_container_width=True, hide_index=True)
              
            auf_del_id = st.selectbox("Eintrag löschen anhand ID:" if st.session_state.language == "de" else "Delete entry by ID:", [""] + [str(i) for i in df_auf["id"].tolist()], key="auf_del_select")
              
            if auf_del_id:
                bestätigt = st.checkbox(
                    "Sicherheitsabfrage: Wirklich löschen?" if st.session_state.language == "de" else "Security check: Really delete?",
                    key="auf_sicherheits_checkbox"
                )
                if bestätigt:
                    if st.button("Ausgewählten Mangel löschen" if st.session_state.language == "de" else "Delete selected defect", key="auf_del_action_btn"):
                        st.success("Mangel erfolgreich gelöscht!" if st.session_state.language == "de" else "Defect successfully deleted!")
                        st.rerun()
        else:
            st.info("Keine Mängel oder Auffälligkeiten in der Datenbank hinterlegt." if st.session_state.language == "de" else "No defects or anomalies recorded in the database.")
