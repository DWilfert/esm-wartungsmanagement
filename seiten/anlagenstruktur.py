import streamlit as st
import pandas as pd
from datenbank.befehle import hole_datenbank_verbindung

def zeige_anlagenstruktur():
    # CSS für kompakte Schriftgröße, Dropdown-Fix und kursive, hellgraue Placeholder
    st.markdown("""
        <style>
        /* Kompakte Schriftgröße in allen Eingabefeldern und Formularen */
        input, select, textarea, div[data-baseweb="select"] span, label {
            font-size: 0.82rem !important;
        }
        
        /* Blendet den automatischen Streamlit-Hinweis 'Press enter to submit form' aus */
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        
        /* Placeholder (Beispieltexte) in leicht grauer Schrift und Kursiv */
        input::placeholder, textarea::placeholder {
            color: #94a3b8 !important;
            font-style: italic !important;
            opacity: 1 !important;
        }
        
        /* Erzwingt einen sauberen Hintergrund für das gesamte Dropdown-Menü */
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
            background-color: var(--secondary-background-color) !important;
        }
        
        /* Jedes einzelne Listenelement im Dropdown */
        div[data-baseweb="popover"] ul li, 
        ul[data-baseweb="menu"] li,
        li[role="option"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            font-size: 0.85rem !important;
        }
        
        /* Markierter/ausgewählter Balken (Hover & Highlight) */
        div[data-baseweb="popover"] ul li:hover,
        div[data-baseweb="popover"] ul li[aria-selected="true"],
        ul[data-baseweb="menu"] li:hover,
        ul[data-baseweb="menu"] li[aria-selected="true"],
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

        /* Fix für st.dataframe Container */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("🏫 Anlagenstruktur" if st.session_state.language == "de" else "🏫 Asset Structure")
    
    if "ziel_vertrags_id" in st.session_state and st.session_state.ziel_vertrags_id is not None:
        st.session_state.showendlos = True

    df_anlagen = pd.DataFrame()
    conn = hole_datenbank_verbindung()
    if conn is not None:
        try: 
            df_anlagen = pd.read_sql("SELECT * FROM `anlagen`", conn)
        except Exception as e: 
            st.error(f"Fehler: {str(e)}" if st.session_state.language == "de" else f"Error: {str(e)}")
        finally: 
            conn.close()
            
    if "showendlos" not in st.session_state:
        st.session_state.showendlos = False
            
    # Umbenannter Button für Endlosliste & Neuerfassung
    btn_text = "🔄 Endlosliste & Neuerfassung umschalten" if st.session_state.language == "de" else "🔄 Toggle List & Registration"
    if st.button(btn_text, key="anl_toggle_btn_main"):
        st.session_state.showendlos = not st.session_state.showendlos
        if "ziel_vertrags_id" in st.session_state:
            st.session_state.ziel_vertrags_id = None
        st.rerun()

    if st.session_state.showendlos and not df_anlagen.empty:
        col_filt, col_src = st.columns([4.0, 6.0])
        with col_filt: anl_filter = st.radio("Standort filtern:" if st.session_state.language == "de" else "Filter Location:", ["Beide" if st.session_state.language == "de" else "Both", "NP", "FG"], horizontal=True, key="anl_std_filter_v7")
        with col_src: anl_suche = st.text_input("🔍 Echtzeit-Suche:" if st.session_state.language == "de" else "🔍 Real-time Search:", autocomplete="off", key="anl_src_input_v7")

        df_endlos = df_anlagen.copy()
        if_anl_filter = anl_filter != ("Beide" if st.session_state.language == "de" else "Both")
        if if_anl_filter: 
            df_endlos = df_endlos[df_endlos["standort"] == anl_filter]
        if anl_suche:
            s_l = anl_suche.lower()
            df_endlos = df_endlos[df_endlos["bezeichnung"].str.lower().str.contains(s_l, na=False)]
        
        st.dataframe(df_endlos[["id", "standort", "bezeichnung", "hersteller", "typ", "zustand"]], use_container_width=True, hide_index=True)

        id_liste = [""] + [str(i) for i in df_endlos["id"].tolist()]
        vorauswahl_index = 0
        
        if "ziel_vertrags_id" in st.session_state and st.session_state.ziel_vertrags_id is not None:
            gesuchte_id_str = str(st.session_state.ziel_vertrags_id)
            if gesuchte_id_str in id_liste:
                vorauswahl_index = id_liste.index(gesuchte_id_str)

        sel_id_raw = st.selectbox(
            "Anlage wählen für Details:" if st.session_state.language == "de" else "Select Asset for Details:", 
            options=id_liste, 
            index=vorauswahl_index, 
            key="anl_sel_id_dropdown_v7"
        )
        if sel_id_raw:
            sel_id = int(sel_id_raw)
            df_target = df_endlos[df_endlos["id"] == sel_id]
            if not df_target.empty:
                row_det = df_target.iloc[0].to_dict()
                st.markdown(f"**{'Zustandsampel' if st.session_state.language == 'de' else 'Condition Traffic Light'}:** {'🟡' if 'betriebsbereit' in str(row_det.get('zustand', '')).lower() else '🔴'}")
                
                t1, t2, t3, t4, t5 = st.tabs(["📋 Basis" if st.session_state.language == "de" else "📋 Basic", "🔧 Technik" if st.session_state.language == "de" else "🔧 Tech", "📍 Ort" if st.session_state.language == "de" else "📍 Location", "⏱️ Historie" if st.session_state.language == "de" else "⏱️ History", "📝 Bearbeiten" if st.session_state.language == "de" else "📝 Edit"])
                with t1:
                    st.write(f"**{'Anlagenart' if st.session_state.language == 'de' else 'Asset Type'}:** {row_det.get('anlagentyp', '-')}")
                    st.write(f"**{'Bauteil-ID' if st.session_state.language == 'de' else 'Component ID'}:** {row_det.get('bauteilid', '-')}")
                    st.write(f"**{'Untergewerk' if st.session_state.language == 'de' else 'Sub-Trade'}:** {row_det.get('untergewerk', '-')}")
                    st.write(f"**{'AKS-Bezeichnung' if st.session_state.language == 'de' else 'AKS Designation'}:** {row_det.get('aksbez', '-')}")
                    st.write(f"**DIN 276:** {row_det.get('din276', '-')}")
                    st.write(f"**{'Beschreibung' if st.session_state.language == 'de' else 'Description'}:** {row_det.get('beschreibung', '-')}")
                with t2:
                    st.write(f"**{'Hersteller' if st.session_state.language == 'de' else 'Manufacturer'}:** {row_det.get('hersteller', '-')}")
                    st.write(f"**{'Modell / Typ' if st.session_state.language == 'de' else 'Model / Type'}:** {row_det.get('typ', '-')}")
                    st.write(f"**{'Seriennummer' if st.session_state.language == 'de' else 'Serial Number'}:** {row_det.get('seriennummer', '-')}")
                    st.write(f"**{'Baujahr' if st.session_state.language == 'de' else 'Year of Construction'}:** {row_det.get('baujahr', '-')}")
                    st.write(f"**{'Lebensdauer / -ende' if st.session_state.language == 'de' else 'Lifespan / End'}:** {row_det.get('lebensdauer', '-')} / {row_det.get('lebensende', '-')}")
                with t3:
                    st.write(f"**{'Gebäudeteil' if st.session_state.language == 'de' else 'Building Section'}:** {row_det.get('gebaudeteil', '-')}")
                    st.write(f"**{'Etage' if st.session_state.language == 'de' else 'Floor'}:** {row_det.get('etage', '-')}")
                    st.write(f"**{'Raum / -bez.' if st.session_state.language == 'de' else 'Room / Descr.'}:** {row_det.get('raum', '-')} ({row_det.get('raumbezeichnung', '-')})")
                with t4:
                    conn_hist = hole_datenbank_verbindung()
                    if conn_hist is not None:
                        try:
                            sql_hist = "SELECT id, klassebez, kurz, intervall, hinweis FROM `serviceeinsaetze` WHERE anlagenid = %s"
                            df_hist = pd.read_sql(sql_hist, conn_hist, params=(sel_id,))
                            if not df_hist.empty: 
                                st.dataframe(df_hist, use_container_width=True, hide_index=True)
                            else: 
                                st.info("Keine Service-Einträge gefunden." if st.session_state.language == "de" else "No service entries found.")
                        except Exception as e_hist: 
                            st.error(f"Fehler: {str(e_hist)}" if st.session_state.language == "de" else f"Error: {str(e_hist)}")
                        finally: 
                            conn_hist.close()
                with t5:
                    with st.form(f"form_edit_anl_{sel_id}"):
                        u_bez = st.text_input("Bezeichnung" if st.session_state.language == "de" else "Designation", value=str(row_det.get('bezeichnung', '')), key=f"u_bez_anl_{sel_id}")
                        u_st = st.text_input("Zustand" if st.session_state.language == "de" else "Condition", value=str(row_det.get('zustand', '')), key=f"u_st_anl_{sel_id}")
                        if st.form_submit_button("Änderungen speichern" if st.session_state.language == "de" else "Save Changes"):
                            conn_up = hole_datenbank_verbindung()
                            if conn_up:
                                cursor = conn_up.cursor()
                                cursor.execute("UPDATE `anlagen` SET bezeichnung=%s, zustand=%s WHERE id=%s", (u_bez, u_st, sel_id))
                                conn_up.commit()
                                conn_up.close()
                                st.success("Aktualisiert!" if st.session_state.language == "de" else "Updated!")
                                st.rerun()

                st.markdown("---")
                df_t_check = pd.DataFrame()
                conn = hole_datenbank_verbindung()
                if conn is not None:
                    try:
                        cursor = conn.cursor(dictionary=True)
                        sql_t = "SELECT f.* FROM `firmeninfo` f JOIN `wartungsvertraege` v ON f.firmenname = v.firma WHERE v.anlagenid = %s"
                        cursor.execute(sql_t, (sel_id,))
                        df_t_check = pd.DataFrame(cursor.fetchall())
                        cursor.close()
                    except: 
                        pass
                    finally: 
                        conn.close()
                if not df_t_check.empty:
                    r_t = df_t_check.iloc[0]
                    werkzeug_info = row_det.get('merkc', '') if row_det.get('merkc', '') else ("Keine Spezialwerkzeuge erforderlich" if st.session_state.language == "de" else "No special tools required")
                    st.info(f"🏢 **{'Zugeordnete Wartungsfirma' if st.session_state.language == 'de' else 'Assigned Maintenance Company'}:** {r_t['firmenname']}\n\n👤 **{'Zuständiger Service-Techniker' if st.session_state.language == 'de' else 'Responsible Service Technician'}:** {r_t['technikername']} ({r_t['techniker_telefon']})\n\n🛠️ **{'Erforderliches Spezialwerkzeug / Equipment' if st.session_state.language == 'de' else 'Required Special Tool / Equipment'}:** {werkzeug_info}")
                
                st.write("")
                col_back, _ = st.columns([4.0, 6.0])
                with col_back:
                    if st.button("📊 Zurück zur kaufmännischen Vertragsanalyse" if st.session_state.language == "de" else "📊 Back to Commercial Contract Analysis", key="anl_btn_back_to_va", use_container_width=True):
                        st.session_state.app_ziel_seite = "📊 Vertragsanalyse" if st.session_state.language == "de" else "📊 Contract Analysis"
                        st.session_state.app_seite_wechseln = True
                        st.rerun()
                st.write("---")
                
        if "ziel_vertrags_id" in st.session_state and st.session_state.ziel_vertrags_id is not None:
            st.session_state.ziel_vertrags_id = None

    else:
        st.markdown("#### 📋 Neue Anlage erfassen" if st.session_state.language == "de" else "#### 📋 Register New Asset")
        with st.form("anl_form_n_einmalig", clear_on_submit=True):
            
            st.markdown("##### 1. Basisdaten & Kennzeichnung" if st.session_state.language == "de" else "##### 1. Basic Data & Identification")
            c1, c2, c3, c4, c5, c6 = st.columns([0.8, 1.5, 1.5, 2.0, 1.5, 4.0])
            with c1: anl_standort = st.selectbox("Standort *" if st.session_state.language == "de" else "Location *", ["", "FG", "NP"], key="anl_ins_std_v16")
            with c2: 
                anl_id_raw = st.text_input("Anlagen-ID *" if st.session_state.language == "de" else "Asset ID *", max_chars=6, placeholder="z. B. 17501" if st.session_state.language == "de" else "e.g. 17501", key="anl_ins_id_v16")
                anl_id = int("".join(filter(str.isdigit, anl_id_raw))) if any(c.isdigit() for c in anl_id_raw) else 0
            with c3: anl_bauteilid = st.text_input("Bauteil-ID" if st.session_state.language == "de" else "Component ID", placeholder="z. B. 123" if st.session_state.language == "de" else "e.g. 123", key="anl_ins_btid_v16")
            with c4: anl_anlagentyp = st.text_input("Anlagentyp" if st.session_state.language == "de" else "Asset Type", placeholder="z. B. Aufzug" if st.session_state.language == "de" else "e.g. Elevator", key="anl_ins_altyp_v16")
            with c5: anl_untergewerk = st.text_input("Untergewerk" if st.session_state.language == "de" else "Sub-Trade", placeholder="z. B. 1" if st.session_state.language == "de" else "e.g. 1", key="anl_ins_ugew_v16")
            with c6: anl_bez = st.text_input("Bezeichnung der Anlage *" if st.session_state.language == "de" else "Asset Designation *", placeholder="z. B. Personenaufzug A" if st.session_state.language == "de" else "e.g. Passenger Elevator A", key="anl_ins_bez_v16")

            c7, c8 = st.columns([3, 3])
            with c7: anl_aks = st.text_input("AKS-Bezeichnung" if st.session_state.language == "de" else "AKS Designation", placeholder="z. B. AK-10" if st.session_state.language == "de" else "e.g. AK-10", key="anl_ins_aks_v16")
            
            din_276_optionen = [
                "",
                "100 - Grundstück" if st.session_state.language == "de" else "100 - Site",
                "110 - Grundstückswert" if st.session_state.language == "de" else "110 - Site Value",
                "120 - Grundstücksnebenkosten" if st.session_state.language == "de" else "120 - Incidental Site Costs",
                "130 - Rechte Dritter" if st.session_state.language == "de" else "130 - Rights of Third Parties",
                "200 - Vorbereitende Maßnahmen" if st.session_state.language == "de" else "200 - Preparatory Measures",
                "210 - Herrichten" if st.session_state.language == "de" else "210 - Site Preparation",
                "220 - Öffentliche Erschließung" if st.session_state.language == "de" else "220 - Public Utility Connections",
                "230 - Nichtöffentliche Erschließung" if st.session_state.language == "de" else "230 - Private Utility Connections",
                "240 - Ausgleichsmaßnahmen und -abgaben" if st.session_state.language == "de" else "240 - Mitigation Measures and Fees",
                "250 - Übergangsmaßnahmen" if st.session_state.language == "de" else "250 - Transitional Measures",
                "300 - Bauwerk - Baukonstruktion" if st.session_state.language == "de" else "300 - Building - Construction",
                "310 - Baugrube / Erdbau" if st.session_state.language == "de" else "310 - Excavation / Earthworks",
                "320 - Gründung, Unterbau" if st.session_state.language == "de" else "320 - Foundation, Substructure",
                "330 - Außenwände / Vertikale Baukonstruktionen, außen" if st.session_state.language == "de" else "330 - Exterior Walls / Vertical Structures, Exterior",
                "340 - Innenwände / Vertikale Baukonstruktionen, innen" if st.session_state.language == "de" else "340 - Interior Walls / Vertical Structures, Interior",
                "350 - Decken / Horizontale Baukonstruktionen" if st.session_state.language == "de" else "350 - Ceilings / Horizontal Structures",
                "360 - Dächer" if st.session_state.language == "de" else "360 - Roofs",
                "370 - Infrastrukturanlagen" if st.session_state.language == "de" else "370 - Infrastructure Facilities",
                "380 - Baukonstruktive Einbauten" if st.session_state.language == "de" else "380 - Structural Fixtures",
                "390 - Sonstige Maßnahmen für Baukonstruktionen" if st.session_state.language == "de" else "390 - Other Measures for Structures",
                "400 - Bauwerk - Technische Anlagen" if st.session_state.language == "de" else "400 - Building - Technical Installations",
                "410 - Abwasser-, Wasser-, Gasanlagen" if st.session_state.language == "de" else "410 - Drainage, Water, Gas Systems",
                "420 - Wärmeversorgungsanlage" if st.session_state.language == "de" else "420 - Heat Supply Systems",
                "430 - Raumlufttechnische Anlagen" if st.session_state.language == "de" else "430 - HVAC Systems",
                "440 - Elektrische Anlagen" if st.session_state.language == "de" else "440 - Electrical Installations",
                "450 - Kommunikations-, sicherheits- und informationstechnische Anlagen" if st.session_state.language == "de" else "450 - Communication, Safety and IT Systems",
                "460 - Förderanlagen" if st.session_state.language == "de" else "460 - Conveying Systems",
                "470 - Nutzungsspezifische und verfahrenstechnische Anlagen" if st.session_state.language == "de" else "470 - Use-Specific and Process Systems",
                "480 - Gebäude- und Anlagenautomation" if st.session_state.language == "de" else "480 - Building and Plant Automation",
                "490 - Sonstige Maßnahmen für technische Anlagen" if st.session_state.language == "de" else "490 - Other Measures for Technical Installations",
                "500 - Außenanlagen und Freiflächen" if st.session_state.language == "de" else "500 - Outdoor Facilities and Open Spaces",
                "510 - Erdbau" if st.session_state.language == "de" else "510 - Earthworks",
                "520 - Gründung, Unterbau" if st.session_state.language == "de" else "520 - Foundation, Substructure",
                "530 - Oberbau, Deckschichten" if st.session_state.language == "de" else "530 - Superstructure, Surfacing",
                "540 - Baukonstruktionen" if st.session_state.language == "de" else "540 - Structural Elements",
                "550 - Technische Anlagen" if st.session_state.language == "de" else "550 - Technical Installations",
                "560 - Einbauten in Außenanlagen und Freiflächen" if st.session_state.language == "de" else "560 - Fixtures in Outdoor Facilities",
                "570 - Vegetationsflächen" if st.session_state.language == "de" else "570 - Vegetation Areas",
                "580 - Wasserflächen" if st.session_state.language == "de" else "580 - Water Areas",
                "590 - Sonstige Maßnahmen für Außenanlagen und Freiflächen" if st.session_state.language == "de" else "590 - Other Measures for Outdoor Facilities",
                "600 - Ausstattung und Kunstwerke" if st.session_state.language == "de" else "600 - Equipment and Artworks",
                "610 - Allgemeine Ausstattung" if st.session_state.language == "de" else "610 - General Equipment",
                "620 - Besondere Ausstattung" if st.session_state.language == "de" else "620 - Special Equipment",
                "630 - Informationstechnische Ausstattung" if st.session_state.language == "de" else "630 - IT Equipment",
                "640 - Künstlerische Ausstattung" if st.session_state.language == "de" else "640 - Artistic Equipment",
                "690 - Sonstige Ausstattung" if st.session_state.language == "de" else "690 - Other Equipment",
                "700 - Baunebenkosten" if st.session_state.language == "de" else "700 - Non-Construction Costs",
                "710 - Bauherrenaufgaben" if st.session_state.language == "de" else "710 - Client Tasks",
                "720 - Vorbereitung der Objektplanung" if st.session_state.language == "de" else "720 - Preparation of Design",
                "730 - Objektplanung" if st.session_state.language == "de" else "730 - General Planning",
                "740 - Fachplanung" if st.session_state.language == "de" else "740 - Specialized Planning",
                "750 - Künstlerische Leistungen" if st.session_state.language == "de" else "750 - Artistic Services",
                "760 - Allgemeine Baunebenkosten" if st.session_state.language == "de" else "760 - General Non-Construction Costs",
                "790 - Sonstige Baunebenkosten" if st.session_state.language == "de" else "790 - Other Non-Construction Costs",
                "800 - Finanzierung" if st.session_state.language == "de" else "800 - Financing",
                "810 - Finanzierungsnebenkosten" if st.session_state.language == "de" else "810 - Incidental Financing Costs",
                "820 - Fremdkapitalzinsen" if st.session_state.language == "de" else "820 - Debt Capital Interest",
                "830 - Eigenkapitalzinsen" if st.session_state.language == "de" else "830 - Equity Capital Interest",
                "840 - Bürgschaften" if st.session_state.language == "de" else "840 - Guarantees",
                "890 - Sonstige Finanzierungskosten" if st.session_state.language == "de" else "890 - Other Financing Costs"
            ]
            with c8: anl_din = st.selectbox("Kostengruppe DIN 276" if st.session_state.language == "de" else "Cost Group DIN 276", din_276_optionen, key="anl_ins_din_v16")

            st.markdown("##### 2. Technische Daten, Baujahr & Lebensdauer" if st.session_state.language == "de" else "##### 2. Technical Data, Year & Lifespan")
            t1, t2, t3, t4, t5, t6 = st.columns([2.25, 2.25, 2.25, 1.25, 0.84, 0.7])
            with t1: anl_hersteller = st.text_input("Hersteller" if st.session_state.language == "de" else "Manufacturer", placeholder="z. B. Otis" if st.session_state.language == "de" else "e.g. Otis", key="anl_ins_her_v16")
            with t2: anl_typ = st.text_input("Typ / Modell" if st.session_state.language == "de" else "Type / Model", placeholder="z. B. Gen2" if st.session_state.language == "de" else "e.g. Gen2", key="anl_ins_typ_v16")
            with t3: anl_sn = st.text_input("Seriennummer" if st.session_state.language == "de" else "Serial Number", placeholder="z. B. SN-98765" if st.session_state.language == "de" else "e.g. SN-98765", key="anl_ins_sn_v16")
            with t4: anl_baujahr = st.text_input("Baujahr" if st.session_state.language == "de" else "Year", placeholder="z. B. 2020" if st.session_state.language == "de" else "e.g. 2020", key="anl_ins_bj_v16")
            with t5: anl_lebensdauer = st.text_input("Lebensdauer" if st.session_state.language == "de" else "Lifespan", placeholder="z. B. 20J" if st.session_state.language == "de" else "e.g. 20Y", key="anl_ins_ld_v16")
            with t6: anl_lebensende = st.text_input("Ende" if st.session_state.language == "de" else "End", placeholder="z. B. 2040" if st.session_state.language == "de" else "e.g. 2040", key="anl_ins_le_v16")

            st.markdown("##### 3. Standort im Gebäude" if st.session_state.language == "de" else "##### 3. Location in Building")
            s1, s2, s3, s4, s5, s6 = st.columns([1.25, 0.75, 0.75, 0.75, 1.75, 2.4])
            with s1: anl_geb = st.text_input("Gebäudeteil" if st.session_state.language == "de" else "Building Section", placeholder="z. B. Hauptgeb." if st.session_state.language == "de" else "e.g. Main Bldg.", key="anl_ins_geb_v16")
            with s2: anl_etage = st.text_input("Etage" if st.session_state.language == "de" else "Floor", placeholder="z. B. OG 2" if st.session_state.language == "de" else "e.g. 2nd Fl.", key="anl_ins_etg_v16")
            with s3: anl_raum = st.text_input("Raum" if st.session_state.language == "de" else "Room", placeholder="z. B. 204" if st.session_state.language == "de" else "e.g. 204", key="anl_ins_raum_v16")
            with s4: anl_anzahl = st.text_input("Anzahl" if st.session_state.language == "de" else "Quantity", placeholder="z. B. 1" if st.session_state.language == "de" else "e.g. 1", key="anl_ins_anz_v16")
            with s5: anl_raumbez = st.text_input("Raumbezeichnung" if st.session_state.language == "de" else "Room Designation", placeholder="z. B. Büro Leitung" if st.session_state.language == "de" else "e.g. Management Office", key="anl_ins_rbez_v16")
            with s6: anl_werkzeug = st.text_input("Spezialwerkzeug" if st.session_state.language == "de" else "Special Tool", placeholder="z. B. Vierkant" if st.session_state.language == "de" else "e.g. Square Key", key="anl_ins_werk_v16")

            st.markdown("##### 4. Kenn-Felder & Merkmale (A bis K vollständig)" if st.session_state.language == "de" else "##### 4. ID Fields & Characteristics (A to K complete)")
            k1, k2, k3, k4, k5 = st.columns(5)
            with k1: anl_kenn1 = st.text_input("Kenn 1", placeholder="z. B. W1" if st.session_state.language == "de" else "e.g. W1", key="anl_ins_k1_v16")
            with k2: anl_kenn2 = st.text_input("Kenn 2", placeholder="z. B. W2" if st.session_state.language == "de" else "e.g. W2", key="anl_ins_k2_v16")
            with k3: anl_kenn3 = st.text_input("Kenn 3", placeholder="z. B. W3" if st.session_state.language == "de" else "e.g. W3", key="anl_ins_k3_v16")
            with k4: anl_kenn4 = st.text_input("Kenn 4", placeholder="z. B. W4" if st.session_state.language == "de" else "e.g. W4", key="anl_ins_k4_v16")
            with k5: anl_kenn5 = st.text_input("Kenn 5", placeholder="z. B. W5" if st.session_state.language == "de" else "e.g. W5", key="anl_ins_k5_v16")

            m1, m2, m3, m4, m5 = st.columns(5)
            with m1: anl_merka = st.text_input("Merk A", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_ma_v16")
            with m2: anl_merkb = st.text_input("Merk B", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_mb_v16")
            with m3: anl_merkc = st.text_input("Merk C", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_mc_v16")
            with m4: anl_merkd = st.text_input("Merk D", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_md_v16")
            with m5: anl_merke = st.text_input("Merk E", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_me_v16")

            mk1, mk2, mk3, mk4, mk5, mk6 = st.columns(6)
            with mk1: anl_merkf = st.text_input("Merk F", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_mf_v16")
            with mk2: anl_merkg = st.text_input("Merk G", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_mg_v16")
            with mk3: anl_merkh = st.text_input("Merk H", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_mh_v16")
            with mk4: anl_merki = st.text_input("Merk I", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_mi_v16")
            with mk5: anl_merkj = st.text_input("Merk J", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_mj_v16")
            with mk6: anl_merkk = st.text_input("Merk K", placeholder="z. B. Info" if st.session_state.language == "de" else "e.g. Info", key="anl_ins_mk_v16")

            anl_beschreibung = st.text_area("Beschreibung / Details" if st.session_state.language == "de" else "Description / Details", placeholder="z. B. Zusätzliche Hinweise zur Anlage..." if st.session_state.language == "de" else "e.g. Additional notes on the asset...", key="anl_ins_desc_v16")
            
            st.write("")
            if st.form_submit_button("Anlage im System speichern" if st.session_state.language == "de" else "Save Asset in System"):
                if not anl_standort or anl_id <= 0 or not anl_bez: 
                    st.error("🔴 Bitte Pflichtfelder (Standort, Anlagen-ID, Bezeichnung) ausfüllen!" if st.session_state.language == "de" else "🔴 Please fill in required fields (Location, Asset ID, Designation)!")
                else:
                    conn = hole_datenbank_verbindung()
                    if conn is not None:
                        try:
                            cursor = conn.cursor()
                            sql_ins = """
                                INSERT INTO `anlagen` 
                                (id, standort, anlagentyp, bauteilid, bezeichnung, untergewerk, aksbez, din276, beschreibung, baujahr, anzahl, hersteller, typ, seriennummer, gebaudeteil, etage, raum, raumbezeichnung, lebensdauer, lebensende, kenn1, kenn2, kenn3, kenn4, kenn5, merka, merkb, merkc, merkd, merke, merkf, merkg, merkh, merki, merkj, merkk, zustand) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Betriebsbereit')
                            """
                            bt_id = int(anl_bauteilid) if anl_bauteilid.isdigit() else None
                            ugew = int(anl_untergewerk) if anl_untergewerk.isdigit() else None
                            bj = int(anl_baujahr) if anl_baujahr.isdigit() else None
                            anz = int(anl_anzahl) if anl_anzahl.isdigit() else 1

                            val = (
                                anl_id, anl_standort, anl_anlagentyp, bt_id, anl_bez, ugew, 
                                anl_aks, anl_din, anl_beschreibung, bj, anz, anl_hersteller, 
                                anl_typ, anl_sn, anl_geb, anl_etage, anl_raum, anl_raumbez, 
                                anl_lebensdauer, anl_lebensende, anl_kenn1, anl_kenn2, anl_kenn3, 
                                anl_kenn4, anl_kenn5, anl_merka, anl_merkb, anl_merkc, anl_merkd, anl_merke,
                                anl_merkf, anl_merkg, anl_merkh, anl_merki, anl_merkj, anl_merkk
                            )
                            cursor.execute(sql_ins, val)
                            conn.commit()
                            cursor.close()
                            st.success("✅ Anlage erfolgreich in der Datenbank registriert!" if st.session_state.language == "de" else "✅ Asset successfully registered in the database!")
                            st.rerun()
                        except Exception as e_ins: 
                            st.error(f"Fehler: {str(e_ins)}" if st.session_state.language == "de" else f"Error: {str(e_ins)}")
                        finally: 
                            conn.close()