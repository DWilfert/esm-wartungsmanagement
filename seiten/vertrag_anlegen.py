import streamlit as st
import pandas as pd
from datenbank.befehle import hole_datenbank_verbindung

def zeige_vertragsanalyse(v_id_auswahl=""):
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
        </style>
    """, unsafe_allow_html=True)

    if 'language' not in st.session_state:
        st.session_state.language = "de"

    if st.session_state.language == "de":
        TXT_VA = {
            "title": "Neuen Wartungsvertrag registrieren",
            "desc": "Erfassung von neuen Dienstleistungs- und Wartungsverträgen inklusive DIN 276 Zuordnung und Fristen-Clusterung.",
            "act_lbl": "Aktion wählen:", "act_new": "Neuen Vertrag erfassen",
            "v_bez": "Vertragsbezeichnung / Gewerk:", "v_firma": "Wartungsfirma / Dienstleister:", "din276": "Kostengruppe DIN 276",
            "kosten": "Kosten pro Jahr (€):", "standort": "Standort:", "anzahl": "Anzahl Einheiten:", "bench_ep": "Benchmark Einzelpreis (€):",
            "protokoll": "Protokoll-Status:", "v_grund": "Gesetzliche Grundlage / Wartungsumfang:", "v_hinw": "Besondere Hinweise / Auflagen:",
            "form_title": "Formular: Neuer Wartungsvertrag"
        }
    else:
        TXT_VA = {
            "title": "Register New Maintenance Contract",
            "desc": "Registration of new service and maintenance contracts including DIN 276 classification and deadline clustering.",
            "act_lbl": "Select Action:", "act_new": "Register New Contract",
            "v_bez": "Contract Designation / Trade:", "v_firma": "Maintenance Company / Provider:", "din276": "Cost Group DIN 276",
            "kosten": "Cost p.a. (€):", "location": "Location:", "anzahl": "Number of Units:", "bench_ep": "Benchmark Unit Price (€):",
            "protokoll": "Protocol Status:", "v_grund": "Legal Basis / Maintenance Scope:", "v_hinw": "Special Notes / Requirements:",
            "form_title": "Form: New Maintenance Contract"
        }

    st.subheader(TXT_VA["title"])
    st.markdown(f"<div style='font-size: 13px; color: #64748b; margin-bottom: 25px;'>{TXT_VA['desc']}</div>", unsafe_allow_html=True)
    va_aktion = TXT_VA["act_new"]

    if va_aktion == TXT_VA["act_new"]:
        with st.form("form_neuer_vertrag", clear_on_submit=True):
            if st.session_state.language == "de":
                din276_optionen = [
                    "",
                    "100 - Grundstück",
                    "110 - Grundstückswert",
                    "120 - Grundstücksnebenkosten",
                    "130 - Rechte Dritter",
                    "200 - Vorbereitende Maßnahmen",
                    "210 - Herrichten",
                    "220 - Öffentliche Erschließung",
                    "230 - Nichtöffentliche Erschließung",
                    "240 - Ausgleichsmaßnahmen und -abgaben",
                    "250 - Übergangsmaßnahmen",
                    "300 - Bauwerk - Baukonstruktion",
                    "310 - Baugrube / Erdbau",
                    "320 - Gründung, Unterbau",
                    "330 - Außenwände / Vertikale Baukonstruktionen, außen",
                    "340 - Innenwände / Vertikale Baukonstruktionen, innen",
                    "350 - Decken / Horizontale Baukonstruktionen",
                    "360 - Dächer",
                    "370 - Infrastrukturanlagen",
                    "380 - Baukonstruktive Einbauten",
                    "390 - Sonstige Maßnahmen für Baukonstruktionen",
                    "400 - Bauwerk - Technische Anlagen",
                    "410 - Abwasser-, Wasser-, Gasanlagen",
                    "420 - Wärmeversorgungsanlage",
                    "430 - Raumlufttechnische Anlagen",
                    "440 - Elektrische Anlagen",
                    "450 - Kommunikations-, sicherheits- und informationstechnische Anlagen",
                    "460 - Förderanlagen",
                    "470 - Nutzungsspezifische und verfahrenstechnische Anlagen",
                    "480 - Gebäude- und Anlagenautomation",
                    "490 - Sonstige Maßnahmen für technische Anlagen",
                    "500 - Außenanlagen und Freiflächen",
                    "510 - Erdbau",
                    "520 - Gründung, Unterbau",
                    "530 - Oberbau, Deckschichten",
                    "540 - Baukonstruktionen",
                    "550 - Technische Anlagen",
                    "560 - Einbauten in Außenanlagen und Freiflächen",
                    "570 - Vegetationsflächen",
                    "580 - Wasserflächen",
                    "590 - Sonstige Maßnahmen für Außenanlagen und Freiflächen",
                    "600 - Ausstattung und Kunstwerke",
                    "610 - Allgemeine Ausstattung",
                    "620 - Besondere Ausstattung",
                    "630 - Informationstechnische Ausstattung",
                    "640 - Künstlerische Ausstattung",
                    "690 - Sonstige Ausstattung",
                    "700 - Baunebenkosten",
                    "710 - Bauherrenaufgaben",
                    "720 - Vorbereitung der Objektplanung",
                    "730 - Objektplanung",
                    "740 - Fachplanung",
                    "750 - Künstlerische Leistungen",
                    "760 - Allgemeine Baunebenkosten",
                    "790 - Sonstige Baunebenkosten",
                    "800 - Finanzierung",
                    "810 - Finanzierungsnebenkosten",
                    "820 - Fremdkapitalzinsen",
                    "830 - Eigenkapitalzinsen",
                    "840 - Bürgschaften",
                    "890 - Sonstige Finanzierungskosten"
                ]
            else:
                din276_optionen = [
                    "",
                    "100 - Site",
                    "110 - Site Value",
                    "120 - Incidental Site Costs",
                    "130 - Rights of Third Parties",
                    "200 - Preparatory Measures",
                    "210 - Site Preparation",
                    "220 - Public Utility Connections",
                    "230 - Private Utility Connections",
                    "240 - Mitigation Measures and Fees",
                    "250 - Transitional Measures",
                    "300 - Building - Construction",
                    "310 - Excavation / Earthworks",
                    "320 - Foundation, Substructure",
                    "330 - Exterior Walls / Vertical Structures, Exterior",
                    "340 - Interior Walls / Vertical Structures, Interior",
                    "350 - Ceilings / Horizontal Structures",
                    "360 - Roofs",
                    "370 - Infrastructure Facilities",
                    "380 - Structural Fixtures",
                    "390 - Other Measures for Structures",
                    "400 - Building - Technical Installations",
                    "410 - Drainage, Water, Gas Systems",
                    "420 - Heat Supply Systems",
                    "430 - HVAC Systems",
                    "440 - Electrical Installations",
                    "450 - Communication, Safety and IT Systems",
                    "460 - Conveying Systems",
                    "470 - Use-Specific and Process Systems",
                    "480 - Building and Plant Automation",
                    "490 - Other Measures for Technical Installations",
                    "500 - Outdoor Facilities and Open Spaces",
                    "510 - Earthworks",
                    "520 - Foundation, Substructure",
                    "530 - Superstructure, Surfacing",
                    "540 - Structural Elements",
                    "550 - Technical Installations",
                    "560 - Fixtures in Outdoor Facilities",
                    "570 - Vegetation Areas",
                    "580 - Water Areas",
                    "590 - Other Measures for Outdoor Facilities",
                    "600 - Equipment and Artworks",
                    "610 - General Equipment",
                    "620 - Special Equipment",
                    "630 - IT Equipment",
                    "640 - Artistic Equipment",
                    "690 - Other Equipment",
                    "700 - Non-Construction Costs",
                    "710 - Client Tasks",
                    "720 - Preparation of Design",
                    "730 - General Planning",
                    "740 - Specialized Planning",
                    "750 - Artistic Services",
                    "760 - General Non-Construction Costs",
                    "790 - Other Non-Construction Costs",
                    "800 - Financing",
                    "810 - Incidental Financing Costs",
                    "820 - Debt Capital Interest",
                    "830 - Equity Capital Interest",
                    "840 - Guarantees",
                    "890 - Other Financing Costs"
                ]

            c1, c2, c3 = st.columns([4.0, 4.0, 2.0])
            with c1: v_bez = st.text_input(TXT_VA["v_bez"], key="v_bez_new")
            with c2: v_firma = st.text_input(TXT_VA["v_firma"], key="v_firma_new")
            with c3: v_din = st.selectbox(TXT_VA["din276"], options=din276_optionen, index=0, key="v_din_new")

            st.write("")
            c_s1, c_std, c_s2, c_s3, c_s4, c_s5 = st.columns([1.5, 1.2, 1.2, 1.5, 1.2, 1.4])
            with c_s1: v_kosten = st.number_input(TXT_VA["kosten"], min_value=0.0, step=100.0, key="v_kosten_new")
            with c_std: v_std = st.selectbox(TXT_VA["standort"], ["NP", "FG"], key="v_std_new")
            with c_s2: v_anz = st.number_input(TXT_VA["anzahl"], min_value=1, step=1, value=1, key="v_anz_new")
            with c_s3: v_bep = st.number_input(TXT_VA["bench_ep"], min_value=0.0, step=10.0, key="v_bep_new")
            with c_s4: 
                intervall_lbl = "Intervall" if st.session_state.language == "de" else "Interval"
                v_zmon = st.number_input(intervall_lbl, min_value=1, step=1, value=12, key="v_zmon_new")
            with c_s5: 
                if st.session_state.language == "de":
                    prot_options = ["", "Ja", "Nein", "Prüfung"]
                else:
                    prot_options = ["", "Yes", "No", "Inspection"]
                v_prot = st.selectbox(TXT_VA["protokoll"], prot_options, key="v_prot_new")

            st.write("")
            lbl_l = "Letzte Wartung" if st.session_state.language == "de" else "Last Maintenance"
            lbl_nw = "Nächste Wartung" if st.session_state.language == "de" else "Next Maintenance"
            lbl_np = "Nächste Prüfung" if st.session_state.language == "de" else "Next Inspection"

            c_d1, c_date2, c_date3, c_date4, _ = st.columns([2.0, 2.0, 2.0, 1.0, 3.0])
            with c_d1: v_last_w = st.date_input(lbl_l, value=None, format="DD.MM.YYYY", key="v_lw_new")
            with c_date2: v_next_w = st.date_input(lbl_nw, value=None, format="DD.MM.YYYY", key="v_nw_new")
            with c_date3: v_next_p = st.date_input(lbl_np, value=None, format="DD.MM.YYYY", key="v_np_new")
            with c_date4: v_cluster = st.text_input("Cluster", value="A", key="v_cl_new")

            st.write("")
            c_t1, c_text2 = st.columns(2)
            with c_t1: v_grund = st.text_area(TXT_VA["v_grund"], height=110, key="v_grund_new")
            with c_text2: v_hinw = st.text_area(TXT_VA["v_hinw"], height=110, key="v_hinw_new")
            v_bem = st.text_area("Anmerkung" if st.session_state.language == "de" else "Notes", height=110, key="v_bem_new")

            btn_text_new = "Neuen Vertrag im System anlegen" if st.session_state.language == "de" else "Create New Contract"
            if st.form_submit_button(f"➕ {btn_text_new}"):
                if not v_bez or not v_firma:
                    st.error("Pflichtfelder (Bezeichnung & Wartungsfirma) ausfüllen!" if st.session_state.language == "de" else "Please fill out required fields!")
                else:
                    conn = hole_datenbank_verbindung()
                    if conn is not None:
                        try:
                            cursor = conn.cursor()
                            v_bpa = int(v_anz) * float(v_bep)
                            db_lw = v_last_w.strftime('%Y-%m-%d') if v_last_w else None
                            db_nw = v_next_w.strftime('%Y-%m-%d') if v_next_w else None
                            db_np = v_next_p.strftime('%Y-%m-%d') if v_next_p else None
                            db_din_zahl = v_din.split(" - ")[0].strip() if v_din else ""

                            sql_ins = "INSERT INTO `wartungsvertraege` (bezeichnung, firma, standort, kostenpa, anzahl, benchmarkep, benchmarkpa, protokollvorhanden, zyklusmonate, din276, grundlage, hinweise, bemerkung, letztewartung, naechstewartung, weiterewartung, gewaehrleistung) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(sql_ins, (v_bez, v_firma, v_std, v_kosten, v_anz, v_bep, v_bpa, v_prot, v_zmon, db_din_zahl, v_grund, v_hinw, v_bem, db_lw, db_nw, db_np, v_cluster))
                            conn.commit()
                            cursor.close()
                            st.success("✅ Neuer Vertrag erfolgreich registriert!" if st.session_state.language == "de" else "✅ New contract successfully registered!")
                            st.rerun()
                        except Exception as e: 
                            err_prefix = "Fehler:" if st.session_state.language == "de" else "Error:"
                            st.error(f"{err_prefix} {str(e)}")
                        finally: 
                            conn.close()
