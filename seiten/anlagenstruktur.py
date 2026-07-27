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
        
        # Sicherer Zugriff auf Spalten mit Fallback
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
        st.markdown("#### 📋 Neue Anlage erfassen" if st.session_state.language == "de" else "#### 📋 Register New Asset")
        with st.form("anl_form_n_einmalig", clear_on_submit=True):
            
            st.markdown("##### 1. Basisdaten & Kennzeichnung" if st.session_state.language == "de" else "##### 1. Basic Data & Identification")
            c1, c2, c3, c4, c5, c6 = st.columns([0.8, 1.5, 1.5, 2.0, 1.5, 4.0])
            with c1: anl_standort = st.selectbox("Standort *" if st.session_state.language == "de" else "Location *", ["", "FG", "NP"], key="anl_ins_std_v16")
            with c2: 
                anl_id_raw = st.text_input("Anlagen-ID *" if st.session_state.language == "de" else "Asset ID *", max_chars=6, placeholder="z. B. 17501" if st.session_state.language == "de" else "e.g. 17501", key="anl_ins_id_v16")
            with c3: anl_bauteilid = st.text_input("Bauteil-ID" if st.session_state.language == "de" else "Component ID", placeholder="z. B. 123" if st.session_state.language == "de" else "e.g. 123", key="anl_ins_btid_v16")
            with c4: anl_anlagentyp = st.text_input("Anlagentyp" if st.session_state.language == "de" else "Asset Type", placeholder="z. B. Aufzug" if st.session_state.language == "de" else "e.g. Elevator", key="anl_ins_altyp_v16")
            with c5: anl_untergewerk = st.text_input("Untergewerk" if st.session_state.language == "de" else "Sub-Trade", placeholder="z. B. 1" if st.session_state.language == "de" else "e.g. 1", key="anl_ins_ugew_v16")
            with c6: anl_bez = st.text_input("Bezeichnung der Anlage *" if st.session_state.language == "de" else "Asset Designation *", placeholder="z. B. Personenaufzug A" if st.session_state.language == "de" else "e.g. Passenger Elevator A", key="anl_ins_bez_v16")

            c7, c8 = st.columns([3, 3])
            with c7: anl_aks = st.text_input("AKS-Bezeichnung" if st.session_state.language == "de" else "AKS Designation", placeholder="z. B. AK-10" if st.session_state.language == "de" else "e.g. AK-10", key="anl_ins_aks_v16")
            
            din_276_optionen = [
                "",
                "100 - Grundstück" if st.session_state.language == "de" else "100 - Site",
                "200 - Vorbereitende Maßnahmen" if st.session_state.language == "de" else "200 - Preparatory Measures",
                "300 - Bauwerk - Baukonstruktion" if st.session_state.language == "de" else "300 - Building - Construction",
                "400 - Bauwerk - Technische Anlagen" if st.session_state.language == "de" else "400 - Building - Technical Installations",
                "500 - Außenanlagen und Freiflächen" if st.session_state.language == "de" else "500 - Outdoor Facilities and Open Spaces"
            ]
            with c8: anl_din = st.selectbox("Kostengruppe DIN 276" if st.session_state.language == "de" else "Cost Group DIN 276", din_276_optionen, key="anl_ins_din_v16")

            st.write("")
            if st.form_submit_button("Anlage im System speichern" if st.session_state.language == "de" else "Save Asset in System"):
                st.success("✅ Anlage erfolgreich in der Demo-Umgebung registriert!" if st.session_state.language == "de" else "✅ Asset successfully registered in demo mode!")
                st.rerun()
