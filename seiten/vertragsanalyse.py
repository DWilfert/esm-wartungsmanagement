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
            border: 1px solid rgba(56, 189, 248, 0.4);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            border-radius: 8px;
            padding: 10px 15px;
            margin-top: 10px;
            margin-bottom: 10px;
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
            "lbl_standort": "Standort-Filter:",
            "lbl_ansicht": "Ansicht:",
            "lbl_detail": "Detailansicht"
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
            "lbl_standort": "Location Filter:",
            "lbl_ansicht": "View:",
            "lbl_detail": "Detailed View"
        }

    st.subheader(TXT_VA["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 15px;'>{TXT_VA['desc']}</div>", unsafe_allow_html=True)

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
        
    total_kosten = pd.to_numeric(df["kostenpa"], errors="coerce").fillna(0.0).sum()
    anzahl_vertraege = len(df)
    avg_kosten = total_kosten / anzahl_vertraege if anzahl_vertraege > 0 else 0.0

    if st.session_state.language == "de":
        lbl_tbl = ["Bezeichnung", "Firma", "Standort", "Kosten p.a.", "Benchmark p.a.", "Clusterung"]
    else:
        lbl_tbl = ["Designation", "Company", "Location", "Cost p.a.", "Benchmark p.a.", "Clustering"]

    df_filtered = df[["id", "anlagenid", "bezeichnung", "firma", "standort", "kostenpa", "benchmarkpa", "gewerksbez", "gewaehrleistung"]].copy().reset_index(drop=True)
    df_display = df_filtered[["bezeichnung", "firma", "standort", "kostenpa", "benchmarkpa", "gewaehrleistung"]].copy()
    
    df_display["kostenpa"] = pd.to_numeric(df_display["kostenpa"], errors="coerce").fillna(0.0).map('{:,.2f} €'.format)
    df_display["benchmarkpa"] = pd.to_numeric(df_display["benchmarkpa"], errors="coerce").fillna(0.0).map('{:,.2f} €'.format)
    df_display.columns = lbl_tbl

    if gewaehlte_ansicht != "🖥️ Fullscreen":
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
            
        # Dünne Trennlinie (st.markdown("---")) komplett entfernt für maximalen Platz!

    # Größeres Tabellenfenster ohne Scroll-Stress
    st.dataframe(
        df_display,
        width="stretch",
        height=520 if gewaehlte_ansicht == "🖥️ Fullscreen" else 420,
        hide_index=True
    )

    # Auswahlfeld extrem kompakt (70% kleiner / schmales Spaltenlayout) und passend beschriftet
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_space, col_select = st.columns([7, 3])
    with col_select:
        vertrag_namen = [""] + df_filtered["bezeichnung"].tolist()
        ausgewaehlter_vertrag = st.selectbox(TXT_VA["lbl_detail"], options=vertrag_namen, key="enterprise_direct_select")

    if ausgewaehlter_vertrag:
        gew_vertrag = df_filtered[df_filtered["bezeichnung"] == ausgewaehlter_vertrag].iloc[0]
        st.markdown(f"""
            <div class="enterprise-detail-card">
                <div style="font-size: 12px; font-weight: bold; color: #38bdf8; margin-bottom: 6px;">
                    🔍 Detailansicht: {gew_vertrag['bezeichnung']}
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 11px; line-height: 1.5;">
                    <div>
                        <b>ID:</b> {gew_vertrag['anlagenid']} | 
                        <b>Standort:</b> {gew_vertrag['standort']} | 
                        <b>Firma:</b> {gew_vertrag['firma']}
                    </div>
                    <div>
                        <b>Gewerk:</b> {gew_vertrag['gewerksbez']} | 
                        <b>Kosten p.a.:</b> {gew_vertrag['kostenpa']:,.2f} €
                    </div>
                    <div>
                        <b>Cluster:</b> <span style="color: #34d399; font-weight: bold;">{gew_vertrag['gewaehrleistung']}</span> | 
                        <b>Status:</b> <span style="color: #38bdf8;">Aktiv</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
