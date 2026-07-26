import streamlit as st
import pandas as pd

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

        div[data-testid="stDataFrame"] {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }

        .buchhaltung-info-zeile {
            display: flex;
            gap: 30px;
            background-color: var(--secondary-background-color);
            padding: 8px 14px;
            border-radius: 6px;
            border: 1px solid rgba(128, 128, 128, 0.15);
            font-size: 11px;
            font-style: italic;
            color: var(--text-color);
            opacity: 0.85;
            margin-bottom: 15px;
            align-items: center;
        }
        
        .filter-container {
            background-color: transparent !important;
            padding: 0px !important;
            border: none !important;
            margin-bottom: 15px;
        }
        
        .enterprise-detail-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
            border: 1px solid rgba(56, 189, 248, 0.4);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.language == "de":
        TXT_VA = {
            "title": "📊 Vertragsanalyse",
            "desc": "Kaufmännische Auswertung von Wartungs-, Service-, Garantie- und Reparaturverträgen.",
            "stat_total": "Gesamtkosten p.a.",
            "stat_count": "Verträge Gesamt",
            "stat_avg": "Ø-Wert pro Vertrag",
            "no_data": "Keine Vertragsdaten zur Analyse vorhanden.",
            "filter_all": "Alle",
            "info_title": "📋 Maßnahmen-Leitfaden & Clusterung einblenden",
            "a": "Abweichungen zwischen Anlagenbestand, Verträgen und Wartungsprotokollen",
            "b": "Unvollständige oder fehlende Wartungs- und Prüfprotokolle",
            "c": "Abweichungen bei Wartungs- und Prüfintervallen",
            "d": "Unklare Zuordnung von Anlagen zu Wartungsverträgen",
            "e": "Mängel und technische Auffälligkeiten aus der Anlagenerfassung und Wartungsprotokollen",
            "view_mode": "Ansichtsmodus:",
            "lbl_standort": "Standort-Filter:",
            "lbl_ansicht": "Ansicht:",
            "lbl_select_row": "🎛️ Enterprise-Schnellauswahl für Vertrags-Detailanalyse:"
        }
    else:
        TXT_VA = {
            "title": "📊 Contract Analysis",
            "desc": "Commercial evaluation of maintenance, service, warranty, and repair contracts.",
            "stat_total": "Total Cost p.a.",
            "stat_count": "Total Contracts",
            "stat_avg": "Ø Value per Contract",
            "no_data": "No contract data available for analysis.",
            "filter_all": "All",
            "info_title": "📋 Show Action Guide & Clustering",
            "a": "Discrepancies between asset inventory, contracts, and maintenance logs",
            "b": "Incomplete or missing maintenance and inspection protocols",
            "c": "Deviations in maintenance and inspection intervals",
            "d": "Unclear assignment of assets to maintenance contracts",
            "e": "Defects and technical abnormalities from asset registration and maintenance logs",
            "view_mode": "View Mode:",
            "lbl_standort": "Location Filter:",
            "lbl_ansicht": "View:",
            "lbl_select_row": "🎛️ Enterprise Quick Selection for Contract Detail Analysis:"
        }

    st.subheader(TXT_VA["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 15px;'>{TXT_VA['desc']}</div>", unsafe_allow_html=True)

    # Sofortige, stabile Demo-Verträge bereitstellen
    df = pd.DataFrame({
        "id": [i+1 for i in range(10)],
        "anlagenid": [17501 + i for i in range(10)],
        "bezeichnung": [
            "Vollwartung Personenaufzug A", "Wartungsvertrag RLT-Anlage", "Servicevertrag Heizung", 
            "Prüfvertrag Brandmeldeanlage", "Wartung Klima Serverraum", "Vollwartung Rollstuhlhebebühne", 
            "Wartung Rauchabzug", "Servicevertrag Trafo-Station", "Wartung Notstromaggregat", "Wartungsvertrag Sanitärpumpe"
        ],
        "firma": ["Otis GmbH", "Stulz GmbH", "Viessmann Werke", "Siemens AG", "Stulz GmbH", "Schindler AG", "Siemens AG", "Siemens AG", "Viessmann Werke", "Stulz GmbH"],
        "standort": ["NP", "FG", "NP", "FG", "NP", "FG", "NP", "FG", "NP", "FG"],
        "kostenpa": [2400.0, 1800.0, 3200.0, 1500.0, 2100.0, 1200.0, 950.0, 4500.0, 2800.0, 800.0],
        "benchmarkpa": [2500.0, 1900.0, 3000.0, 1600.0, 2000.0, 1250.0, 1000.0, 4200.0, 2700.0, 850.0],
        "gewerksbez": ["Fördertechnik", "Raumlufttechnik", "Wärmeversorgung", "Elektrotechnik", "Klimatechnik", "Fördertechnik", "Brandschutz", "Elektrotechnik", "Notstrom", "Sanitär"],
        "gewaehrleistung": ["A", "B", "A", "C", "A", "B", "A", "C", "B", "A"]
    })

    with st.container():
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        col_ctrl1, col_ctrl2 = st.columns(2)
        
        with col_ctrl1:
            standort_optionen = [TXT_VA["filter_all"], "NP", "FG"]
            ausgewaehlter_standort = st.radio(
                TXT_VA["lbl_standort"], 
                options=standort_optionen, 
                horizontal=True,
                key="va_standort_radio"
            )

        with col_ctrl2:
            opt_ansicht = ["📊 Dashboard", "🖥️ Fullscreen"]
            gewaehlte_ansicht = st.radio(
                TXT_VA["lbl_ansicht"],
                options=opt_ansicht,
                horizontal=True,
                key="va_view_mode_radio"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    if ausgewaehlter_standort != TXT_VA["filter_all"] and ausgewaehlter_standort is not None:
        df = df[df["standort"] == ausgewaehlter_standort]

    if df.empty:
        st.info(TXT_VA["no_data"])
        return
        
    if "kostenpa" in df.columns:
        total_kosten = pd.to_numeric(df["kostenpa"], errors="coerce").fillna(0.0).sum()
    else:
        total_kosten = 0.0
        
    anzahl_vertraege = len(df)
    avg_kosten = total_kosten / anzahl_vertraege if anzahl_vertraege > 0 else 0.0

    if st.session_state.language == "de":
        lbl_tbl = ["Bezeichnung", "Firma", "Standort", "Kosten p.a.", "Benchmark p.a.", "Clusterung"]
    else:
        lbl_tbl = ["Designation", "Company", "Location", "Cost p.a.", "Benchmark p.a.", "Clustering"]

    df_filtered = df[["anlagenid", "bezeichnung", "firma", "standort", "kostenpa", "benchmarkpa", "gewaehrleistung"]].copy().reset_index(drop=True)
    df_display = df_filtered[["bezeichnung", "firma", "standort", "kostenpa", "benchmarkpa", "gewaehrleistung"]].copy()
    
    if "kostenpa" in df_display.columns:
        df_display["kostenpa"] = pd.to_numeric(df_display["kostenpa"], errors="coerce").fillna(0.0)
        df_display["kostenpa"] = df_display["kostenpa"].map('{:,.2f} €'.format)
        
    if "benchmarkpa" in df_display.columns:
        df_display["benchmarkpa"] = pd.to_numeric(df_display["benchmarkpa"], errors="coerce").fillna(0.0)
        df_display["benchmarkpa"] = df_display["benchmarkpa"].map('{:,.2f} €'.format)
        
    df_display.columns = lbl_tbl

    # Dashboard-Ansicht oder Fullscreen-Ansicht der Tabelle
    if gewaehlte_ansicht == "🖥️ Fullscreen":
        st.dataframe(
            df_display,
            width="stretch",
            height=450, 
            hide_index=True
        )
    else:
        st.markdown(f'''
            <div class="buchhaltung-info-zeile">
                <div><strong>{TXT_VA["stat_total"]}:</strong> <em>{total_kosten:,.2f} €</em></div>
                <div><strong>{TXT_VA["stat_count"]}:</strong> <em>{anzahl_vertraege}</em></div>
                <div><strong>{TXT_VA["stat_avg"]}:</strong> <em>{avg_kosten:,.2f} €</em></div>
            </div>
        ''', unsafe_allow_html=True)

        with st.expander(TXT_VA['info_title'], expanded=False):
            st.markdown(f'''
                <div style='font-size: 12px; line-height: 1.6;'>
                    <strong>A:</strong> {TXT_VA['a']}<br>
                    <strong>B:</strong> {TXT_VA['b']}<br>
                    <strong>C:</strong> {TXT_VA['c']}<br>
                    <strong>D:</strong> {TXT_VA['d']}<br>
                    <strong>E:</strong> {TXT_VA['e']}
                </div>
            ''', unsafe_allow_html=True)
            
        st.markdown("---")

        st.dataframe(
            df_display,
            width="stretch",
            height=280,
            hide_index=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Professionelle Enterprise-Selectbox mit eleganter visueller Einbettung
    vertrag_optionen = ["-- Bitte wählen oder Vertrag aus Liste analysieren --" if st.session_state.language == "de" else "-- Please select contract for analysis --"] + df_filtered["bezeichnung"].tolist()
    
    col_sel1, col_sel2 = st.columns([7, 3])
    with col_sel1:
        ausgewaehlter_vertrag = st.selectbox(
            TXT_VA["lbl_select_row"], 
            options=vertrag_optionen, 
            key="enterprise_vertrag_selector"
        )

    # Elegante, designte Enterprise-Detailkarte (öffnet sich nur bei Auswahl)
    if ausgewaehlter_vertrag and not ausgewaehlter_vertrag.startswith("--"):
        gew_vertrag = df_filtered[df_filtered["bezeichnung"] == ausgewaehlter_vertrag].iloc[0]
        
        st.markdown(f"""
            <div class="enterprise-detail-card">
                <h4 style="color: #38bdf8; margin-top: 0; margin-bottom: 15px; border-bottom: 1px solid rgba(56,189,248,0.2); padding-bottom: 8px;">
                    🔍 Enterprise-Detailanalyse: {gew_vertrag['bezeichnung']}
                </h4>
                <div style="display: flex; justify-content: space-between; font-size: 13px; line-height: 1.8;">
                    <div>
                        <b>Anlagen-ID:</b> {gew_vertrag['anlagenid']}<br>
                        <b>Standort:</b> {gew_vertrag['standort']}<br>
                        <b>Wartungsfirma:</b> {gew_vertrag['firma']}
                    </div>
                    <div>
                        <b>Gewerk:</b> {gew_vertrag['gewerksbez']}<br>
                        <b>Kosten p.a.:</b> {gew_vertrag['kostenpa']:,.2f} €<br>
                        <b>Benchmark p.a.:</b> {gew_vertrag['benchmarkpa']:,.2f} €
                    </div>
                    <div>
                        <b>Clusterung / Gewährleistung:</b> <span style="color: #34d399; font-weight: bold;">Klasse {gew_vertrag['gewaehrleistung']}</span><br>
                        <b>Status:</b> <span style="color: #38bdf8;">Aktiv & Überwacht</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
