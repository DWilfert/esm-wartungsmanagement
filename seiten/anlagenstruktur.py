import streamlit as st
import pandas as pd

def zeige_anlagenstruktur():
    # CSS für kompakte Schriftgröße, Dropdown-Fix und kursive, hellgraue Placeholder
    st.markdown("""
        <style>
        input, select, textarea, div[data-baseweb="select"] span, label {
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
        
        div[data-baseweb="popover"] ul li, 
        ul[data-baseweb="menu"] li,
        li[role="option"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            font-size: 0.85rem !important;
        }
        
        div[data-baseweb="popover"] ul li:hover,
        div[data-baseweb="popover"] ul li[aria-selected="true"],
        ul[data-baseweb="menu"] li:hover,
        ul[data-baseweb="menu"] li[aria-selected="true"],
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
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("🏫 Anlagenstruktur" if st.session_state.language == "de" else "🏫 Asset Structure")
    
    if "ziel_vertrags_id" in st.session_state and st.session_state.ziel_vertrags_id is not None:
        st.session_state.showendlos = True

    # Sofortige lokale Demo-Daten für Anlagen bereitstellen
    df_anlagen = pd.DataFrame({
        "id": [17501 + i for i in range(20)],
        "standort": ["NP" if i % 2 == 0 else "FG" for i in range(20)],
        "anlagentyp": ["Fördertechnik", "Raumlufttechnik", "Elektrotechnik", "Wärmeversorgung", "Brandschutz"] * 4,
        "bauteilid": [100 + i for i in range(20)],
        "untergewerk": [1] * 20,
        "aksbez": [f"AK-{10+i}" for i in range(20)],
        "din276": ["460 - Förderanlagen" if i % 5 == 0 else "430 - Raumlufttechnische Anlagen" for i in range(20)],
        "beschreibung": [f"Test-Anlage Beschreibung Nummer {i+1} mit vollem Funktionsumfang" for i in range(20)],
        "baujahr": [2018 + (i % 5) for i in range(20)],
        "anzahl": [1] * 20,
        "hersteller": ["Otis GmbH", "Schindler AG", "Stulz GmbH", "Siemens AG", "Viessmann Werke"] * 4,
        "typ": ["Gen2", "Transit", "CyberAir", "Desigo", "Vitodens"] * 4,
        "seriennummer": [f"SN-987{i:02d}" for i in range(20)],
        "gebaudeteil": ["Hauptgebäude" if i % 2 == 0 else "Neubau" for i in range(20)],
        "etage": ["OG 1", "EG", "OG 2", "KG", "OG 3"] * 4,
        "raum": [f"R-{100+i}" for i in range(20)],
        "raumbezeichnung": ["Büro Leitung", "Technikraum", "Klassenzimmer", "Labor", "Flur"] * 4,
        "lebensdauer": ["20J"] * 20,
        "lebensende": ["2038"] * 20,
        "zustand": ["Betriebsbereit", "Wartung überfällig", "Betriebsbereit", "Prüfung anstehend", "Betriebsbereit"] * 4,
        "merkc": ["Vierkant-Schlüssel erforderlich"] * 20
    })
            
    if "showendlos" not in st.session_state:
        st.session_state.showendlos = False
            
    btn_text = "🔄 Endlosliste & Neuerfassung umschalten" if st.session_state.language == "de" else "🔄 Toggle List & Registration"
    if st.button(btn_text, key="anl_toggle_btn_main"):
        st.session_state.showendlos = not st.session_state.showendlos
        if "ziel_vertrags_id" in st.session_state:
            st.session_state.ziel_vertrags_id = None
        st.rerun()

    if st.session_state.showendlos and not df_anlagen.empty:
        col_filt, col_src = st.columns([4.0, 6.0])
        with col_filt: 
            anl_filter = st.radio("Standort filtern:" if st.session_state.language == "de" else "Filter Location:", ["Beide" if st.session_state.language == "de" else "Both", "NP", "FG"], horizontal=True, key="anl_std_filter_v7")
        with col_src: 
            anl_suche = st.text_input("🔍 Echtzeit-Suche:" if st.session_state.language == "de" else "🔍 Real-time Search:", autocomplete="off", key="anl_src_input_v7")

        df_endlos = df_anlagen.copy()
        if_anl_filter = anl_filter != ("Beide" if st.session_state.language == "de" else "Both")
        if if_anl_filter: 
            df_endlos = df_endlos[df_endlos["standort"] == anl_filter]
        if anl_suche:
            s_l = anl_suche.lower()
            df_endlos = df_endlos[df_endlos["bezeichnung"].str.lower().str.contains(s_l, na=False)]
        
        verfuegbare_spalten = [col for col in ["id", "standort", "bezeichnung", "hersteller", "typ", "zustand"] if col in df_endlos.columns]
        st.dataframe(df_endlos[verfuegbare_spalten], use_container_width=True, hide_index=True)

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
                    df_hist = pd.DataFrame({
                        "id": [1, 2],
                        "klassebez": ["Wartung", "Prüfung"],
                        "kurz": ["Jahreswartung durchgeführt", "Sicherheitsprüfung bestanden"],
                        "intervall": ["12 Monate", "24 Monate"],
                        "hinweis": ["Keine Mängel", "Alles in Ordnung"]
                    })
                    st.dataframe(df_hist, use_container_width=True, hide_index=True)
                with t5:
                    with st.form(f"form_edit_anl_{sel_id}"):
                        u_bez = st.text_input("Bezeichnung" if st.session_state.language == "de" else "Designation", value=str(row_det.get('bezeichnung', '')), key=f"u_bez_anl_{sel_id}")
                        u_st = st.text_input("Zustand" if st.session_state.language == "de" else "Condition", value=str(row_det.get('zustand', '')), key=f"u_st_anl_{sel_id}")
                        if st.form_submit_button("Änderungen speichern" if st.session_state.language == "de" else "Save Changes"):
                            st.success("Aktualisiert!" if st.session_state.language == "de" else "Updated!")
                            st.rerun()

                st.markdown("---")
                st.info(f"🏢 **{'Zugeordnete Wartungsfirma' if st.session_state.language == 'de' else 'Assigned Maintenance Company'}:** Otis GmbH\n\n👤 **{'Zuständiger Service-Techniker' if st.session_state.language == 'de' else 'Responsible Service Technician'}:** Max Mustermann (0176 / 12345678)\n\n🛠️ **{'Erforderliches Spezialwerkzeug / Equipment' if st.session_state.language == 'de' else 'Required Special Tool / Equipment'}:** Vierkant-Schlüssel erforderlich")
                
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
        st.markdown("#### 📋 Neue Anlage erfassen (Vollständige Felder)" if st.session_state.language == "de" else "#### 📋 Register New Asset (Complete Fields)")
        with st.form("anl_form_n_vollstaendig", clear_on_submit=True):
            
            # Sektion 1: Basisdaten & Zuordnung
            st.markdown("##### 1. Basisdaten & Kennzeichnung" if st.session_state.language == "de" else "##### 1. Basic Data & Identification")
            c1, c2, c3, c4, c5 = st.columns([1.0, 1.8, 1.8, 2.4, 3.0])
            with c1: anl_standort = st.selectbox("Standort *" if st.session_state.language == "de" else "Location *", ["", "FG", "NP"], key="f_std")
            with c2: anl_id = st.text_input("Anlagen-ID *" if st.session_state.language == "de" else "Asset ID *", placeholder="z. B. 17501", key="f_aid")
            with c3: anl_typ_kat = st.text_input("Anlagentyp" if st.session_state.language == "de" else "Asset Type", placeholder="z. B. Fördertechnik", key="f_atyp")
            with c4: anl_bauteil = st.text_input("Bauteil der Anlage" if st.session_state.language == "de" else "Component", placeholder="z. B. Antrieb", key="f_bauteil")
            with c5: anl_bez_name = st.text_input("Anlagenname *" if st.session_state.language == "de" else "Asset Name *", placeholder="z. B. Personenaufzug A", key="f_aname")

            c6, c7, c8, c9 = st.columns([1.5, 2.0, 3.0, 3.5])
            with c6: anl_untergewerk = st.text_input("Untergewerk" if st.session_state.language == "de" else "Sub-Trade", placeholder="z. B. 1", key="f_ugew")
            with c7: anl_aks = st.text_input("AKS-Bezeichnung" if st.session_state.language == "de" else "AKS Designation", placeholder="z. B. AK-10", key="f_aks")
            
            din_276_optionen = [
                "",
                "100 - Grundstück",
                "200 - Vorbereitende Maßnahmen",
                "300 - Bauwerk - Baukonstruktion",
                "400 - Bauwerk - Technische Anlagen",
                "500 - Außenanlagen und Freiflächen"
            ]
            with c8: anl_din = st.selectbox("Kostengruppe (DIN 276)" if st.session_state.language == "de" else "Cost Group (DIN 276)", din_276_optionen, key="f_din")
            with c9: anl_dingruppe_bez = st.text_input("Kostengruppenbezeichnung" if st.session_state.language == "de" else "Cost Group Description", placeholder="z. B. Förderanlagen", key="f_dingr_bez")

            st.markdown("---")
            
            # Sektion 2: Kennzeichnungen 1 bis 5
            st.markdown("##### 2. Interne Kennzeichnungen (1 - 5)" if st.session_state.language == "de" else "##### 2. Internal Designations (1 - 5)")
            k_cols = st.columns(5)
            k1 = k_cols[0].text_input("Kennzeichnung 1", key="f_k1")
            k2 = k_cols[1].text_input("Kennzeichnung 2", key="f_k2")
            k3 = k_cols[2].text_input("Kennzeichnung 3", key="f_k3")
            k4 = k_cols[3].text_input("Kennzeichnung 4", key="f_k4")
            k5 = k_cols[4].text_input("Kennzeichnung 5", key="f_k5")

            st.markdown("---")

            # Sektion 3: Beschreibung, Technik & Hersteller
            st.markdown("##### 3. Technische Daten & Beschreibung" if st.session_state.language == "de" else "##### 3. Technical Data & Description")
            st.text_area("Beschreibung der Anlage" if st.session_state.language == "de" else "Asset Description", placeholder="Detaillierte Funktionsbeschreibung...", height=70, key="f_beschr")

            t_cols1 = st.columns(4)
            with t_cols1[0]: st.text_input("Baujahr", placeholder="z. B. 2020", key="f_bj")
            with t_cols1[1]: st.text_input("Anzahl", placeholder="1", key="f_anz")
            with t_cols1[2]: st.text_input("Bezugsmenge EP", placeholder="z. B. Stk", key="f_bep")
            with t_cols1[3]: st.text_input("Hersteller", placeholder="z. B. Otis GmbH", key="f_herst")

            t_cols2 = st.columns(4)
            with t_cols2[0]: st.text_input("Typ / Modell", placeholder="z. B. Gen2", key="f_typ")
            with t_cols2[1]: st.text_input("Seriennummer", placeholder="SN-12345", key="f_sn")
            with t_cols2[2]: st.text_input("Lebensdauer (rechnerisch)", placeholder="z. B. 20J", key="f_ldauer")
            with t_cols2[3]: st.text_input("Lebensende", placeholder="z. B. 2040", key="f_lende")

            st.markdown("---")

            # Sektion 4: Standort im Gebäude & Zustand
            st.markdown("##### 4. Gebäude- und Standortzuordnung" if st.session_state.language == "de" else "##### 4. Building & Location Assignment")
            o_cols = st.columns(6)
            with o_cols[0]: st.text_input("Gebäudeteil", placeholder="Hauptgebäude", key="f_gteil")
            with o_cols[1]: st.text_input("Etage", placeholder="OG 1", key="f_etage")
            with o_cols[2]: st.text_input("Raum", placeholder="R-101", key="f_raum")
            with o_cols[3]: st.text_input("Raumbezeichnung", placeholder="Büro", key="f_rbez")
            with o_cols[4]: st.text_input("Zustand", placeholder="Betriebsbereit", key="f_zustand")

            st.markdown("---")

            # Sektion 5: Merkmale A bis K (Alphabetisch)
            st.markdown("##### 5. Zusätzliche Merkmale (Merkmal A bis K)" if st.session_state.language == "de" else "##### 5. Additional Attributes (Attribute A to K)")
            
            # Wir verteilen die 11 Merkmale in 3 saubere Reihen (z.B. 4 + 4 + 3 Spalten)
            mk_row1 = st.columns(4)
            ma = mk_row1[0].text_input("Merkmal a", key="f_m_a")
            mb = mk_row1[1].text_input("Merkmal b", key="f_m_b")
            mc = mk_row1[2].text_input("Merkmal c", key="f_m_c")
            md = mk_row1[3].text_input("Merkmal d", key="f_m_d")

            mk_row2 = st.columns(4)
            me = mk_row2[0].text_input("Merkmal e", key="f_m_e")
            mf = mk_row2[1].text_input("Merkmal f", key="f_m_f")
            mg = mk_row2[2].text_input("Merkmal g", key="f_m_g")
            mh = mk_row2[3].text_input("Merkmal h", key="f_m_h")

            mk_row3 = st.columns(3)
            mi = mk_row3[0].text_input("Merkmal i", key="f_m_i")
            mj = mk_row3[1].text_input("Merkmal j", key="f_m_j")
            mk = mk_row3[2].text_input("Merkmal k", key="f_m_k")

            st.write("")
            st.write("")
            if st.form_submit_button("💾 Vollständige Anlage im System speichern" if st.session_state.language == "de" else "💾 Save Complete Asset in System"):
                st.success("✅ Anlage mit allen Feldern und Merkmalen A–K erfolgreich in der Demo-Umgebung registriert!" if st.session_state.language == "de" else "✅ Asset with all fields and attributes A–K successfully registered in demo mode!")
                st.rerun()
