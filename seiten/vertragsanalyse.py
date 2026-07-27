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
            border: 1px solid rgba(56, 189, 248, 0.5);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            border-radius: 8px;
            padding: 14px 18px;
            height: 100%;
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
            "no_data": "Keine Vertragsdaten für das gewählte Wirtschaftsjahr vorhanden.",
            "filter_all": "Alle",
            "info_title": "📋 Maßnahmen-Leitfaden & Clusterung einblenden",
            "a": "Abweichungen zwischen Anlagenbestand, Verträgen und Wartungsprotokollen",
            "b": "Unvollständige oder fehlende Wartungs- und Prüfprotokolle",
            "c": "Abweichungen bei Wartungs- und Prüfintervallen",
            "d": "Unklare Zuordnung von Anlagen zu Wartungsverträgen",
            "e": "Mängel und technische Auffälligkeiten aus der Anlagenerfassung und Wartungsprotokollen",
            "lbl_standort": "Standort-Filter:",
            "lbl_jahr": "Wirtschaftsjahr (5-Jahres-Plan):",
            "select_placeholder": "-- Vertrag für Enterprise-Details wählen --"
        }
    else:
        TXT_VA = {
            "title": "📊 Contract Analysis",
            "desc": "Commercial evaluation of maintenance, service, warranty, and repair contracts.",
            "stat_total": "Total Cost p.a.",
            "stat_count": "Total Contracts",
            "stat_avg": "Ø Value per Contract",
            "no_data": "No contract data available for the selected fiscal year.",
            "filter_all": "All",
            "info_title": "📋 Show Action Guide & Clustering",
            "a": "Discrepancies between asset inventory, contracts, and maintenance logs",
            "b": "Incomplete or missing maintenance and inspection protocols",
            "c": "Deviations in maintenance and inspection intervals",
            "d": "Unclear assignment of assets to maintenance contracts",
            "e": "Defects and technical abnormalities from asset registration and maintenance logs",
            "lbl_standort": "Location Filter:",
            "lbl_jahr": "Fiscal Year (5-Year Plan):",
            "select_placeholder": "-- Select contract for enterprise details --"
        }

    st.subheader(TXT_VA["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 15px;'>{TXT_VA['desc']}</div>", unsafe_allow_html=True)

    # Demodaten über den 5-Jahres-Horizont (2026 bis 2030) verteilt
    df = pd.DataFrame({
        "id": [i+1 for i in range(10)],
        "anlagenid": [17501 + i for i in range(10)],
        "vertragsnummer": ["V-2026-001", "V-2026-142", "V-2027-089", "V-2028-012", "V-2026-331", "V-2029-055", "V-2027-190", "V-2030-811", "V-2028-402", "V-2026-009"],
        "bezeichnung": [
            "Vollwartung Personenaufzug A", "Wartungsvertrag RLT-Anlage", "Servicevertrag Heizung", 
            "Prüfvertrag Brandmeldeanlage", "Wartung Klima Serverraum", "Vollwartung Rollstuhlhebebühne", 
            "Wartung Rauchabzug", "Servicevertrag Trafo-Station", "Wartung Notstromaggregat", "Wartungsvertrag Sanitärpumpe"
        ],
        "firma": ["Otis GmbH", "Stulz GmbH", "Viessmann Werke", "Siemens AG", "Stulz GmbH", "Schindler AG", "Siemens AG", "Siemens AG", "Viessmann Werke", "Stulz GmbH"],
        "standort": ["NP", "FG", "NP", "FG", "NP", "FG", "NP", "FG", "NP", "FG"],
        "wirtschaftsjahr": ["2026", "2026", "2027", "2028", "2026", "2029", "2027", "2030", "2028", "2026"],
        "kostenpa": [2400.0, 1800.0, 3200.0, 1500.0, 2100.0, 1200.0, 950.0, 4500.0, 2800.0, 800.0],
        "benchmarkpa": [2500.0, 1900.0, 3000.0, 1600.0, 2000.0, 1250.0, 1000.0, 4200.0, 2700.0, 850.0],
        "gewerksbez": ["Fördertechnik", "Raumlufttechnik", "Wärmeversorgung", "Elektrotechnik", "Klimatechnik", "Fördertechnik", "Brandschutz", "Elektrotechnik", "Notstrom", "Sanitär"],
        "gewaehrleistung": ["A", "B", "A", "C", "A", "B", "A", "C", "B", "A"],
        "laufzeit_start": ["01.01.2026", "15.03.2026", "01.07.2027", "01.01.2028", "01.06.2026", "15.02.2029", "01.09.2027", "01.01.2030", "15.10.2028", "01.01.2026"],
        "laufzeit_ende": ["31.12.2028", "14.03.2029", "30.06.2030", "31.12.2030", "31.05.2029", "14.02.2032", "31.08.2030", "31.12.2032", "14.10.2031", "31.12.2028"],
        "kuendigung": ["3 Monate zum Jahresende", "6 Monate zum Laufzeitende", "3 Monate zum Quartalsende", "3 Monate zum Jahresende", "6 Monate zum Laufzeitende", "3 Monate zum Jahresende", "3 Monate zum Quartalsende", "6 Monate zum Jahresende", "3 Monate zum Jahresende", "3 Monate zum Quartalsende"],
        "ansprechpartner": ["Herr Müller (Tel. 089/1234-1)", "Frau Huber (Tel. 089/1234-2)", "Herr Schmidt (Tel. 089/1234-3)", "Service-Center (Tel. 0800-555)", "Frau Huber (Tel. 089/1234-2)", "Herr Wagner (Tel. 089/1234-6)", "Service-Center (Tel. 0800-555)", "Herr Bauer (Tel. 089/1234-8)", "Herr Schmidt (Tel. 089/1234-3)", "Frau Huber (Tel. 089/1234-2)"]
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
            # 5-Jahres-Horizont für die Planung (2026 bis 2030)
            jahr_optionen = [TXT_VA["filter_all"], "2026", "2027", "2028", "2029", "2030"]
            ausgewaehltes_jahr = st.radio(
                TXT_VA["lbl_jahr"],
                options=jahr_optionen,
                horizontal=True,
                key="va_jahr_radio"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # Filter anwenden (Standort)
    if ausgewaehlter_standort != TXT_VA["filter_all"] and ausgewaehlter_standort is not None:
        df = df[df["standort"] == ausgewaehlter_standort]

    # Filter anwenden (Wirtschaftsjahr)
    if ausgewaehltes_jahr != TXT_VA["filter_all"] and ausgewaehltes_jahr is not None:
        df = df[df["wirtschaftsjahr"] == ausgewaehltes_jahr]

    if df.empty:
        st.info(TXT_VA["no_data"])
        return
        
    total_kosten = pd.to_numeric(df["kostenpa"], errors="coerce").fillna(0.0).sum()
    anzahl_vertraege = len(df)
    avg_kosten = total_kosten / anzahl_vertraege if anzahl_vertraege > 0 else 0.0

    if st.session_state.language == "de":
        lbl_tbl = ["Bezeichnung", "Firma", "Standort", "Jahr", "Kosten p.a.", "Benchmark p.a.", "Clusterung"]
    else:
        lbl_tbl = ["Designation", "Company", "Location", "Year", "Cost p.a.", "Benchmark p.a.", "Clustering"]

    df_filtered = df.copy().reset_index(drop=True)
    df_display = df_filtered[["bezeichnung", "firma", "standort", "wirtschaftsjahr", "kostenpa", "benchmarkpa", "gewaehrleistung"]].copy()
    
    df_display["kostenpa"] = pd.to_numeric(df_display["kostenpa"], errors="coerce").fillna(0.0).map('{:,.2f} €'.format)
    df_display["benchmarkpa"] = pd.to_numeric(df_display["benchmarkpa"], errors="coerce").fillna(0.0).map('{:,.2f} €'.format)
    df_display.columns = lbl_tbl

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

    st.dataframe(
        df_display,
        width="stretch",
        height=400,
        hide_index=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_icon, col_select, col_card = st.columns([0.5, 3.5, 8])
    
    with col_icon:
        st.markdown("""
            <div style="font-size: 1.1rem; text-align: right; padding-top: 7px; padding-right: 5px;">
                ℹ️
            </div>
        """, unsafe_allow_html=True)

    with col_select:
        vertrag_namen = [TXT_VA["select_placeholder"]] + df_filtered["bezeichnung"].tolist()
        ausgewaehlter_vertrag = st.selectbox("", options=vertrag_namen, index=0, key="enterprise_direct_select", label_visibility="collapsed")

    with col_card:
        if ausgewaehlter_vertrag and ausgewaehlter_vertrag != TXT_VA["select_placeholder"]:
            gew_vertrag = df_filtered[df_filtered["bezeichnung"] == ausgewaehlter_vertrag].iloc[0]
            st.markdown(f"""
                <div class="enterprise-detail-card">
                    <div style="font-size: 13px; font-weight: bold; color: #38bdf8; margin-bottom: 6px; display: flex; justify-content: space-between; border-bottom: 1px solid rgba(56, 189, 248, 0.3); padding-bottom: 4px;">
                        <span>📋 {gew_vertrag['bezeichnung']}</span>
                        <span style="font-size: 11px; color: #94a3b8; font-weight: normal;">Vertrags-Nr: {gew_vertrag['vertragsnummer']}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 11.5px; line-height: 1.5; color: #f8fafc;">
                        <div><strong>🏢 Standort & ID:</strong> {gew_vertrag['standort']} (Anlagen-ID: {gew_vertrag['anlagenid']})</div>
                        <div><strong>🤝 Auftragnehmer:</strong> {gew_vertrag['firma']}</div>
                        <div><strong>⚙️ Gewerk & Cluster:</strong> {gew_vertrag['gewerksbez']} (Klasse <span style="color: #34d399; font-weight: bold;">{gew_vertrag['gewaehrleistung']}</span>)</div>
                        <div><strong>💰 Kosten p.a.:</strong> <span style="color: #38bdf8; font-weight: bold;">{gew_vertrag['kostenpa']:,.2f} €</span> (Benchmark: {gew_vertrag['benchmarkpa']:,.2f} €)</div>
                        <div><strong>📅 Laufzeit:</strong> {gew_vertrag['laufzeit_start']} bis {gew_vertrag['laufzeit_ende']} (GJ {gew_vertrag['wirtschaftsjahr']})</div>
                        <div><strong>⏱️ Kündigungsfrist:</strong> {gew_vertrag['kuendigung']}</div>
                        <div style="grid-column: span 2; margin-top: 4px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 4px; color: #cbd5e1;">
                            <strong>📞 Ansprechpartner / Service:</strong> {gew_vertrag['ansprechpartner']}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="enterprise-detail-card" style="opacity: 0.5; display: flex; align-items: center; justify-content: center; font-size: 11.5px; font-style: italic; min-height: 105px; color: #94a3b8;">
                    Kein Vertrag ausgewählt – bitte wählen Sie links einen Eintrag aus, um die vollständigen Enterprise-Details anzuzeigen.
                </div>
            """, unsafe_allow_html=True)
