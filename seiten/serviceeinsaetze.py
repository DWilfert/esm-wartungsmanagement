import streamlit as st
import pandas as pd

def zeige_serviceeinsaetze():
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
            padding: 2px;
            background-image: linear-gradient(to right, rgba(128, 128, 128, 0.08) 1px, transparent 1px),
                              linear-gradient(to bottom, rgba(128, 128, 128, 0.08) 1px, transparent 1px);
            background-size: 15px 15px;
        }
        
        div[data-testid="stDataFrame"] td {
            padding-top: 2px !important;
            padding-bottom: 2px !important;
            font-size: 0.78rem !important;
        }

        .enterprise-card {
            background-color: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 0.5rem;
            padding: 15px;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'language' not in st.session_state:
        st.session_state.language = "de"

    if st.session_state.language == "de":
        TXT_SRV = {
            "title": "🛠️ Serviceeinsätze", "act_lbl": "Aktion:", "act_hist": "Historie / Suche", "act_add": "Bericht erfassen",
            "filter_lbl": "Standort filtern:", "opt_all": "Alle", "src_lbl": "🔍 Schnell-Suche (Echtzeit):",
            "src_ph": "Gewerk, Kurzbericht oder ID...", "empty_table": "Keine Einträge entsprechen deinen Filter-Kriterien.",
            "empty_db": "Keine Serviceberichte in der operationalen Database vorhanden.", "sel_id": "ID wählen für Details / Löschen:",
            "det_title": "Details zu Serviceeinsatz-ID", "anl_id": "Anlagen-ID:", "gewerk": "Gewerbeklassifizierung:",
            "kurz": "Kurfassung / Ergebnis:", "zyklus": "Intervall:", "hinweis": "Hinweis:", "btn_del": "Diesen Bericht löschen", "succ_del": "Bericht erfolgreich gelöscht.",
            "loc_lbl": "Standort", "asset_id_lbl": "Anlagen-ID", "class_lbl": "Klasse", "asset_type_lbl": "Anlagenart",
            "kenn1_lbl": "Kennzeichnung 1", "kenn2_lbl": "Kennzeichnung 2", "class_desc_lbl": "Bezeichnung Klasse",
            "summary_res_lbl": "Kurzfassung / Ergebnis", "equipment_lbl": "Benötigtes Ersatzequipment / Spezialwerkzeug",
            "interval_lbl": "Intervall", "note_lbl": "Hinweis", "legal_basis_lbl": "Gesetzliche Grundlage", "legal_text_lbl": "Gesetzliche Textstelle",
            "qual_lbl": "Qualifikation", "initial_insp_lbl": "Erstabnahme", "recurring_lbl": "Wiederkehrend", "relief_lbl": "Entlastung im Schadensfall",
            "btn_save_report": "Servicebericht speichern", "err_valid": "🔴 Fehler: Bitte gib eine gültige Anlagen-ID größer als 0 sowie einen Standort!",
            "succ_saved": "✅ Servicebericht erfolgreich gespeichert!"
        }
    else:
        TXT_SRV = {
            "title": "🛠️ Service Deployments", "act_lbl": "Action:", "act_hist": "History / Search", "act_add": "Log New Report",
            "filter_lbl": "Filter Location:", "opt_all": "All", "src_lbl": "🔍 Quick Search (Real-time):",
            "src_ph": "Trade, summary or ID...", "empty_table": "No entries match your filter criteria.",
            "empty_db": "No service reports available in the operational database.", "sel_id": "Select ID for Details / Deletion:",
            "det_title": "Details for Service ID", "anl_id": "Asset ID:", "gewerk": "Trade Classification:",
            "kurz": "Summary / Result:", "zyklus": "Interval:", "hinweis": "Note:", "btn_del": "Delete this report", "succ_del": "Report successfully deleted.",
            "loc_lbl": "Location", "asset_id_lbl": "Asset ID", "class_lbl": "Class", "asset_type_lbl": "Asset Type",
            "kenn1_lbl": "Identification 1", "kenn2_lbl": "Identification 2", "class_desc_lbl": "Class Designation",
            "summary_res_lbl": "Summary / Result", "equipment_lbl": "Required Spare Equipment / Special Tool",
            "interval_lbl": "Interval", "note_lbl": "Note", "legal_basis_lbl": "Legal Basis", "legal_text_lbl": "Legal Provision",
            "qual_lbl": "Qualification", "initial_insp_lbl": "Initial Inspection", "recurring_lbl": "Recurring", "relief_lbl": "Relief in Case of Damage",
            "btn_save_report": "Save Service Report", "err_valid": "🔴 Error: Please provide a valid Asset ID greater than 0 and a location!",
            "succ_saved": "✅ Service report successfully saved!"
        }

    st.subheader(TXT_SRV["title"])
    srv_aktion = st.radio(TXT_SRV["act_lbl"], [TXT_SRV["act_hist"], TXT_SRV["act_add"]], horizontal=True, key="srv_haupt_aktion_v7")
    
    if srv_aktion == TXT_SRV["act_hist"]:
        df_service = pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "anlagenid": [17501, 17502, 17503, 17504, 17505],
            "standort": ["NP", "FG", "NP", "FG", "NP"],
            "klasse": [460, 430, 420, 440, 450],
            "klassebez": ["Fördertechnik", "Raumlufttechnik", "Wärmeversorgung", "Elektrotechnik", "Sicherheitstechnik"],
            "kurz": ["🔴 Quartalswartung überfällig", "🟡 Filterwechsel anstehend", "🟢 Jahreswartung erfolgreich", "🔴 Hauptprüfung ausstehend", "🟢 Funktionsprüfung bestanden"],
            "intervall": ["12M", "6M", "12M", "24M", "12M"],
            "hinweis": ["Dringend veranlassen", "Material vorbestellen", "Erledigt", "Termin vereinbaren", "Dokumentiert"]
        })
            
        if df_service.empty:
            st.info(TXT_SRV["empty_db"])
        else:
            s_filter = st.radio(TXT_SRV["filter_lbl"], [TXT_SRV["opt_all"], "NP (Neuperlach)", "FG (Fasangarten)"], horizontal=True, key="srv_standort_filter_v7")
            col_src_srv, _ = st.columns([3.5, 6.5])
            with col_src_srv: 
                s_suche = st.text_input(TXT_SRV["src_lbl"], placeholder=TXT_SRV["src_ph"], autocomplete="off", key="srv_src_inp_v7")

            df_srv_f = df_service.copy()
            if s_filter != TXT_SRV["opt_all"]:
                krz = "NP" if "NP" in s_filter else "FG"
                df_srv_f = df_srv_f[df_srv_f["standort"] == krz]
                
            if s_suche:
                sl = s_suche.lower()
                df_srv_f = df_srv_f[df_srv_f["anlagenid"].astype(str).str.contains(sl, na=False) | df_srv_f["klassebez"].str.lower().str.contains(sl, na=False) | df_srv_f["kurz"].str.lower().str.contains(sl, na=False)] 
            
            if not df_srv_f.empty:
                df_anzeige_srv = df_srv_f[["id", "anlagenid", "standort", "klassebez", "kurz", "intervall", "hinweis"]].copy()
                spalten_srv_live = {
                    "id": "ID", "anlagenid": "Anlagen-ID" if st.session_state.language == "de" else "Asset-ID",
                    "standort": "Standort" if st.session_state.language == "de" else "Location",
                    "klassebez": "Gewerk" if st.session_state.language == "de" else "Trade",
                    "kurz": "Kurzbericht" if st.session_state.language == "de" else "Summary",
                    "intervall": "Zyklus" if st.session_state.language == "de" else "Interval", "hinweis": "Status"
                }
                df_anzeige_srv.rename(columns=spalten_srv_live, inplace=True)
                st.dataframe(df_anzeige_srv, use_container_width=True, hide_index=True)
                
                col_srv_id, _ = st.columns([2.0, 8.0])
                with col_srv_id: 
                    srv_sel_id = st.selectbox(TXT_SRV["sel_id"], [""] + [str(i) for i in df_srv_f["id"].tolist()], key="srv_sel_id_selectbox_v7")
                
                if srv_sel_id:
                    df_srv_target = df_srv_f[df_srv_f["id"] == int(srv_sel_id)]
                    if not df_srv_target.empty:
                        s_det = df_srv_target.iloc[0]
                        
                        st.markdown(f"##### {TXT_SRV['det_title']} {srv_sel_id}")
                        st.markdown(f"""
                        <div class="enterprise-card">
                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; font-size: 0.85rem;">
                                <div><b>{TXT_SRV['anl_id']}</b><br>{s_det['anlagenid']} ({s_det['standort']})</div>
                                <div><b>{TXT_SRV['gewerk']}</b><br>{s_det.get('klasse', '-')} - {s_det['klassebez']}</div>
                                <div><b>{TXT_SRV['kurz']}</b><br>{s_det['kurz']}</div>
                                <div><b>{TXT_SRV['zyklus']}</b><br>{s_det['intervall']}</div>
                                <div style="grid-column: span 2;"><b>{TXT_SRV['hinweis']}</b><br>{s_det['hinweis']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        bestätigt = st.checkbox(
                            "Sicherheitsabfrage: Wirklich löschen?" if st.session_state.language == "de" else "Security check: Really delete?",
                            key="srv_sicherheits_checkbox"
                        )
                        if bestätigt:
                            if st.button(TXT_SRV["btn_del"], key="srv_del_btn_action"):
                                st.success(TXT_SRV["succ_del"])
                                st.rerun()
            else: 
                st.info(TXT_SRV["empty_table"])
    elif srv_aktion == TXT_SRV["act_add"]:
        with st.form("srv_form_n_einmalig", clear_on_submit=True):
            col_s1, col_s2, col_s3, col_s4 = st.columns([1.0, 1.5, 1.5, 6.0])
            with col_s1: s_standort = st.selectbox(TXT_SRV["loc_lbl"], ["", "NP", "FG"], key="srv_standort_sel_v7")
            with col_s2: 
                s_id_raw = st.text_input(TXT_SRV["asset_id_lbl"], max_chars=6, placeholder="17501", autocomplete="off", key="srv_id_input_v7")
                s_id = int("".join(filter(str.isdigit, s_id_raw))) if any(c.isdigit() for c in s_id_raw) else 0
            with col_s3: 
                s_kl_raw = st.text_input(TXT_SRV["class_lbl"], max_chars=6, placeholder="4610", autocomplete="off", key="srv_klasse_input_v7")
                s_kl = int("".join(filter(str.isdigit, s_kl_raw))) if any(c.isdigit() for c in s_kl_raw) else 0
            with col_s4: s_anl_typ = st.text_input(TXT_SRV["asset_type_lbl"], placeholder="Ex. Personenaufzug Seil" if st.session_state.language == "en" else "z. B. Personenaufzug Seil", autocomplete="off", key="srv_art_input_v7")
            
            col_s5, col_s6, col_s7 = st.columns([2.0, 2.0, 6.0])
            with col_s5: s_k1 = st.text_input(TXT_SRV["kenn1_lbl"], placeholder="Ex. Haupt" if st.session_state.language == "en" else "z. B. Haupt", autocomplete="off", key="srv_k1_input_v7")
            with col_s6: s_k2 = st.text_input(TXT_SRV["kenn2_lbl"], placeholder="Ex. Bauteil A" if st.session_state.language == "en" else "z. B. Bauteil A", autocomplete="off", key="srv_k2_input_v7")
            with col_s7: s_kl_bez = st.text_input(TXT_SRV["class_desc_lbl"], placeholder="Ex. Aufzugstechnik" if st.session_state.language == "en" else "z. B. Aufzugstechnik", autocomplete="off", key="srv_klbez_input_v7")
            
            col_s8, col_s9 = st.columns([5.0, 5.0])
            with col_s8: s_kurz = st.text_input(TXT_SRV["summary_res_lbl"], placeholder="Ex. Quartalswartung mangelfrei durchgeführt" if st.session_state.language == "en" else "z. B. Quartalswartung mangelfrei durchgeführt", autocomplete="off", key="srv_kurz_input_v7")
            with col_s9: s_ersatzequip = st.text_input(TXT_SRV["equipment_lbl"], placeholder="Ex. Schmieröl Typ C, keine Ersatzteile" if st.session_state.language == "en" else "z. B. Schmieröl Typ C, keine Ersatzteile", autocomplete="off", key="srv_equip_input_v7")

            col_zz5, col_zz6 = st.columns([2.0, 8.0])
            with col_zz5: s_int = st.text_input(TXT_SRV["interval_lbl"], placeholder="Ex. 6M" if st.session_state.language == "en" else "z. B. 6M", autocomplete="off", key="srv_int_input_v7")
            with col_zz6: s_hinw = st.text_input(TXT_SRV["note_lbl"], placeholder="Ex. Nächste Prüfung durch TÜV im Folgemonat" if st.session_state.language == "en" else "z. B. Nächste Prüfung durch TÜV im Folgemonat", autocomplete="off", key="srv_hinw_input_v7")

            col_uu1, col_uu2 = st.columns([5.0, 5.0])
            with col_uu1: s_gg = st.text_input(TXT_SRV["legal_basis_lbl"], placeholder="Ex. BetrSichV" if st.session_state.language == "en" else "z. B. BetrSichV", autocomplete="off", key="srv_gg_input_v7")
            with col_uu2: s_gt = st.text_input(TXT_SRV["legal_text_lbl"], placeholder="Ex. Anhang 1, Ziff. 4" if st.session_state.language == "en" else "z. B. Anhang 1, Ziff. 4", autocomplete="off", key="srv_gt_input_v7")
            
            col_uu3, col_uu4, col_uu5, col_uu6 = st.columns([3.0, 2.0, 2.0, 3.0])
            with col_uu3: s_qual = st.text_input(TXT_SRV["qual_lbl"], placeholder="Ex. Sachkundiger / Befähigte Person" if st.session_state.language == "en" else "z. B. Sachkundiger / Befähigte Person", autocomplete="off", key="srv_qual_input_v7")
            with col_uu4: 
                erst_options = ["", "Ja", "Nein"] if st.session_state.language == "de" else ["", "Yes", "No"]
                s_erst = st.selectbox(TXT_SRV["initial_insp_lbl"], erst_options, key="srv_erst_sel_v7")
            with col_uu5: 
                wied_options = ["", "Ja", "Nein"] if st.session_state.language == "de" else ["", "Yes", "No"]
                s_wied = st.selectbox(TXT_SRV["recurring_lbl"], wied_options, key="srv_wied_sel_v7")
            with col_uu6: s_entl = st.text_input(TXT_SRV["relief_lbl"], placeholder="Ex. Ja (Dokumentiert)" if st.session_state.language == "en" else "z. B. Ja (Dokumentiert)", autocomplete="off", key="srv_entl_input_v7")
            
            if st.form_submit_button(TXT_SRV["btn_save_report"]):
                if not s_standort or s_id <= 0: 
                    st.error(TXT_SRV["err_valid"])
                else:
                    st.success(TXT_SRV["succ_saved"])
                    st.rerun()
