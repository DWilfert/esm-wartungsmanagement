import streamlit as st
import pandas as pd

def zeige_anlagenstruktur():
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

    lang = st.session_state.get("language", "de")
    
    txt = {
        "de": {
            "titel": "🏫 Anlagenstruktur",
            "btn_toggle": "🔄 Endlosliste & Neuerfassung umschalten",
            "filter_std": "Standort filtern:",
            "beide": "Beide",
            "suche": "🔍 Echtzeit-Suche:",
            "sel_anlage": "Anlage wählen für Details:",
            "zustandampel": "Zustandsampel:",
            "tabs": ["📋 Basis", "🔧 Technik", "📍 Ort", "⏱️ Historie", "📝 Bearbeiten"],
            "basis": {"art": "Anlagenart", "bauteil": "Bauteil-ID", "untergewerk": "Untergewerk", "aks": "AKS-Bezeichnung", "din": "DIN 276", "beschr": "Beschreibung"},
            "technik": {"herst": "Hersteller", "typ": "Modell / Typ", "sn": "Seriennummer", "bj": "Baujahr", "ld": "Lebensdauer / -ende"},
            "ort": {"gteil": "Gebäudeteil", "etage": "Etage", "raum": "Raum / -bez."},
            "hist_cols": ["id", "klassebez", "kurz", "intervall", "hinweis"],
            "edit_bez": "Bezeichnung",
            "edit_zustand": "Zustand",
            "btn_save": "Änderungen speichern",
            "success_upd": "Aktualisiert!",
            "info_extra": "🏢 **Zugeordnete Wartungsfirma:** Otis GmbH\n\n👤 **Zuständiger Service-Techniker:** Max Mustermann (0176 / 12345678)\n\n🛠️ **Erforderliches Spezialwerkzeug / Equipment:** Vierkant-Schlüssel erforderlich",
            "btn_back": "📊 Zurück zur kaufmännischen Vertragsanalyse",
            "new_titel": "📋 Neue Anlage erfassen (Vollständige Felder)",
            "sec1": "1. Basisdaten & Kennzeichnung",
            "lbl_std": "Standort *",
            "lbl_aid": "Anlagen-ID *",
            "lbl_atyp": "Anlagentyp",
            "lbl_bauteil": "Bauteil der Anlage",
            "lbl_aname": "Anlagenname *",
            "lbl_ugew": "Untergewerk",
            "lbl_aks": "AKS-Bezeichnung",
            "lbl_din": "Kostengruppe (DIN 276)",
            "lbl_dingr": "Kostengruppenbezeichnung",
            "sec2": "2. Interne Kennzeichnungen (1 - 5)",
            "sec3": "3. Technische Daten & Beschreibung",
            "lbl_beschr_neu": "Beschreibung der Anlage",
            "lbl_bj": "Baujahr",
            "lbl_anz": "Anzahl",
            "lbl_bep": "Bezugsmenge EP",
            "lbl_herst": "Hersteller",
            "lbl_typ": "Typ / Modell",
            "lbl_sn": "Seriennummer",
            "lbl_ldauer": "Lebensdauer (rechnerisch)",
            "lbl_lende": "Lebensende",
            "sec4": "4. Gebäude- und Standortzuordnung",
            "sec5": "5. Zusätzliche Merkmale (Merkmal A bis K)",
            "btn_reg": "💾 Vollständige Anlage im System speichern",
            "success_reg": "✅ Anlage mit allen Feldern und Merkmalen A–K erfolgreich in der Demo-Umgebung registriert!"
        },
        "en": {
            "titel": "🏫 Asset Structure",
            "btn_toggle": "🔄 Toggle List & Registration",
            "filter_std": "Filter Location:",
            "beide": "Both",
            "suche": "🔍 Real-time Search:",
            "sel_anlage": "Select Asset for Details:",
            "zustandampel": "Condition Traffic Light:",
            "tabs": ["📋 Basic", "🔧 Tech", "📍 Location", "⏱️ History", "📝 Edit"],
            "basis": {"art": "Asset Type", "bauteil": "Component ID", "untergewerk": "Sub-Trade", "aks": "AKS Designation", "din": "DIN 276", "beschr": "Description"},
            "technik": {"herst": "Manufacturer", "typ": "Model / Type", "sn": "Serial Number", "bj": "Year of Construction", "ld": "Lifespan / End"},
            "ort": {"gteil": "Building Section", "etage": "Floor", "raum": "Room / Descr."},
            "hist_cols": ["id", "klassebez", "kurz", "intervall", "hinweis"],
            "edit_bez": "Designation",
            "edit_zustand": "Condition",
            "btn_save": "Save Changes",
            "success_upd": "Updated!",
            "info_extra": "🏢 **Assigned Maintenance Company:** Otis GmbH\n\n👤 **Responsible Service Technician:** Max Mustermann (0176 / 12345678)\n\n🛠️ **Required Special Tool / Equipment:** Square key required",
            "btn_back": "📊 Back to Commercial Contract Analysis",
            "new_titel": "📋 Register New Asset (Complete Fields)",
            "sec1": "1. Basic Data & Identification",
            "lbl_std": "Location *",
            "lbl_aid": "Asset ID *",
            "lbl_atyp": "Asset Type",
            "lbl_bauteil": "Component",
            "lbl_aname": "Asset Name *",
            "lbl_ugew": "Sub-Trade",
            "lbl_aks": "AKS Designation",
            "lbl_din": "Cost Group (DIN 276)",
            "lbl_dingr": "Cost Group Description",
            "sec2": "2. Internal Designations (1 - 5)",
            "sec3": "3. Technical Data & Description",
            "lbl_beschr_neu": "Asset Description",
            "lbl_bj": "Year of Construction",
            "lbl_anz": "Quantity",
            "lbl_bep": "Unit Quantity EP",
            "lbl_herst": "Manufacturer",
            "lbl_typ": "Model / Type",
            "lbl_sn": "Serial Number",
            "lbl_ldauer": "Lifespan (calculated)",
            "lbl_lende": "End of Life",
            "sec4": "4. Building & Location Assignment",
            "sec5": "5. Additional Attributes (Attribute A to K)",
            "btn_reg": "💾 Save Complete Asset in System",
            "success_reg": "✅ Asset with all fields and attributes A–K successfully registered in demo mode!"
        }
    }[lang]

    st.subheader(txt["titel"])
    
    if "ziel_vertrags_id" in st.session_state and st.session_state.ziel_vertrags_id is not None:
        st.session_state.showendlos = True

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
        
    if st.button(txt["btn_toggle"], key="anl_toggle_btn_main"):
        st.session_state.showendlos = not st.session_state.showendlos
        if "ziel_vertrags_id" in st.session_state:
            st.session_state.ziel_vertrags_id = None
        st.rerun()

    if st.session_state.showendlos and not df_anlagen.empty:
        col_filt, col_src = st.columns([4.0, 6.0])
        with col_filt: 
            anl_filter = st.radio(txt["filter_std"], [txt["beide"], "NP", "FG"], horizontal=True, key="anl_std_filter_v7")
        with col_src: 
            anl_suche = st.text_input(txt["suche"], autocomplete="off", key="anl_src_input_v7")

        df_endlos = df_anlagen.copy()
        if_anl_filter = anl_filter != txt["beide"]
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
            txt["sel_anlage"], 
            options=id_liste, 
            index=vorauswahl_index, 
            key="anl_sel_id_dropdown_v7"
        )
        if sel_id_raw:
            sel_id = int(sel_id_raw)
            df_target = df_endlos[df_endlos["id"] == sel_id]
            if not df_target.empty:
                row_det = df_target.iloc[0].to_dict()
                st.markdown(f"**{txt['zustandampel']}** {'🟡' if 'betriebsbereit' in str(row_det.get('zustand', '')).lower() else '🔴'}")
                
                t1, t2, t3, t4, t5 = st.tabs(txt["tabs"])
                with t1:
                    st.write(f"**{txt['basis']['art']}:** {row_det.get('anlagentyp', '-')}")
                    st.write(f"**{txt['basis']['bauteil']}:** {row_det.get('bauteilid', '-')}")
                    st.write(f"**{txt['basis']['untergewerk']}:** {row_det.get('untergewerk', '-')}")
                    st.write(f"**{txt['basis']['aks']}:** {row_det.get('aksbez', '-')}")
                    st.write(f"**DIN 276:** {row_det.get('din276', '-')}")
                    st.write(f"**{txt['basis']['beschr']}:** {row_det.get('beschreibung', '-')}")
                with t2:
                    st.write(f"**{txt['technik']['herst']}:** {row_det.get('hersteller', '-')}")
                    st.write(f"**{txt['technik']['typ']}:** {row_det.get('typ', '-')}")
                    st.write(f"**{txt['technik']['sn']}:** {row_det.get('seriennummer', '-')}")
                    st.write(f"**{txt['technik']['bj']}:** {row_det.get('baujahr', '-')}")
                    st.write(f"**{txt['technik']['ld']}:** {row_det.get('lebensdauer', '-')} / {row_det.get('lebensende', '-')}")
                with t3:
                    st.write(f"**{txt['ort']['gteil']}:** {row_det.get('gebaudeteil', '-')}")
                    st.write(f"**{txt['ort']['etage']}:** {row_det.get('etage', '-')}")
                    st.write(f"**{txt['ort']['raum']}:** {row_det.get('raum', '-')} ({row_det.get('raumbezeichnung', '-')})")
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
                        u_bez = st.text_input(txt["edit_bez"], value=str(row_det.get('bezeichnung', '')), key=f"u_bez_anl_{sel_id}")
                        u_st = st.text_input(txt["edit_zustand"], value=str(row_det.get('zustand', '')), key=f"u_st_anl_{sel_id}")
                        if st.form_submit_button(txt["btn_save"]):
                            st.success(txt["success_upd"])
                            st.rerun()

                st.markdown("---")
                st.markdown(txt["info_extra"])
                
                st.write("")
                col_back, _ = st.columns([4.0, 6.0])
                with col_back:
                    if st.button(txt["btn_back"], key="anl_btn_back_to_va", use_container_width=True):
                        st.session_state.app_ziel_seite = "📊 Vertragsanalyse" if lang == "de" else "📊 Contract Analysis"
                        st.session_state.app_seite_wechseln = True
                        st.rerun()
                st.write("---")
                
        if "ziel_vertrags_id" in st.session_state and st.session_state.ziel_vertrags_id is not None:
            st.session_state.ziel_vertrags_id = None

    else:
        st.markdown(f"#### {txt['new_titel']}")
        with st.form("anl_form_n_vollstaendig", clear_on_submit=True):
            
            st.markdown(f"##### {txt['sec1']}")
            c1, c2, c3, c4, c5 = st.columns([1.0, 1.8, 1.8, 2.4, 3.0])
            with c1: anl_standort = st.selectbox(txt["lbl_std"], ["", "FG", "NP"], key="f_std")
            with c2: anl_id = st.text_input(txt["lbl_aid"], placeholder="z. B. 17501", key="f_aid")
            with c3: anl_typ_kat = st.text_input(txt["lbl_atyp"], placeholder="z. B. Fördertechnik", key="f_atyp")
            with c4: anl_bauteil = st.text_input(txt["lbl_bauteil"], placeholder="z. B. Antrieb", key="f_bauteil")
            with c5: anl_bez_name = st.text_input(txt["lbl_aname"], placeholder="z. B. Personenaufzug A", key="f_aname")

            c6, c7, c8, c9 = st.columns([1.5, 2.0, 3.0, 3.5])
            with c6: anl_untergewerk = st.text_input(txt["lbl_ugew"], placeholder="z. B. 1", key="f_ugew")
            with c7: anl_aks = st.text_input(txt["lbl_aks"], placeholder="z. B. AK-10", key="f_aks")
            
            din_276_optionen = [
                "",
                "100 - Grundstück", "110 - Grundstückswert", "120 - Grundstücksnebenkosten", "130 - Rechte Dritter",
                "200 - Vorbereitende Maßnahmen", "210 - Herrichten", "220 - Öffentliche Erschließung", "230 - Nichtöffentliche Erschließung", "240 - Ausgleichsmaßnahmen und -abgaben", "250 - Übergangsmaßnahmen",
                "300 - Bauwerk - Baukonstruktion", "310 - Baugrube / Erdbau", "320 - Gründung, Unterbau", "330 - Außenwände / Vertikale Baukonstruktionen, außen", "340 - Innenwände / Vertikale Baukonstruktionen, innen", "350 - Decken / Horizontale Baukonstruktionen", "360 - Dächer", "370 - Infrastrukturanlagen", "380 - Baukonstruktive Einbauten", "390 - Sonstige Maßnahmen für Baukonstruktionen",
                "400 - Bauwerk - Technische Anlagen", "410 - Abwasser-, Wasser-, Gasanlagen", "420 - Wärmeversorgungsanlage", "430 - Raumlufttechnische Anlagen", "440 - Elektrische Anlagen", "450 - Kommunikations-, sicherheits- und Informationsanlagen", "460 - Förderanlagen", "470 - Nutzungsspezifische und verfahrenstechnische Anlagen", "480 - Gebäude- und Anlagenautomation", "490 - Sonstige Maßnahmen für technische Anlagen",
                "500 - Außenanlagen und Freiflächen", "510 - Erdbau", "520 - Gründung, Unterbau", "530 - Oberbau, Deckschichten", "540 - Baukonstruktionen", "550 - Technische Anlagen", "560 - Einbauten in Außenanlagen und Freiflächen", "570 - Vegetationsflächen", "580 - Wasserflächen", "590 - Sonstige Maßnahmen für Außenanlagen und Freiflächen",
                "600 - Ausstattung und Kunstwerke", "610 - Allgemeine Ausstattung", "620 - Besondere Ausstattung", "630 - Informationstechnische Ausstattung", "640 - Künstlerische Ausstattung", "690 - Sonstige Ausstattung",
                "700 - Baunebenkosten", "710 - Bauherrenaufgaben", "720 - Vorbereitung der Objektplanung", "730 - Objektplanung", "740 - Fachplanung", "750 - Künstlerische Leistungen", "760 - Allgemeine Baunebenkosten", "790 - Sonstige Baunebenkosten",
                "800 - Finanzierung", "810 - Finanzierungsnebenkosten", "820 - Fremdkapitalzinsen", "830 - Eigenkapitalzinsen", "840 - Bürgschaften", "890 - Sonstige Finanzierungskosten"
            ]
            with c8: anl_din = st.selectbox(txt["lbl_din"], din_276_optionen, key="f_din")
            with c9: anl_dingruppe_bez = st.text_input(txt["lbl_dingr"], placeholder="z. B. Förderanlagen", key="f_dingr_bez")

            st.markdown("---")
            
            st.markdown(f"##### {txt['sec2']}")
            k_cols = st.columns(5)
            k1 = k_cols[0].text_input("Kennzeichnung 1", key="f_k1")
            k2 = k_cols[1].text_input("Kennzeichnung 2", key="f_k2")
            k3 = k_cols[2].text_input("Kennzeichnung 3", key="f_k3")
            k4 = k_cols[3].text_input("Kennzeichnung 4", key="f_k4")
            k5 = k_cols[4].text_input("Kennzeichnung 5", key="f_k5")

            st.markdown("---")

            st.markdown(f"##### {txt['sec3']}")
            st.text_area(txt["lbl_beschr_neu"], placeholder="Detaillierte Funktionsbeschreibung...", height=70, key="f_beschr")

            t_cols1 = st.columns(4)
            with t_cols1[0]: st.text_input(txt["lbl_bj"], placeholder="z. B. 2020", key="f_bj")
            with t_cols1[1]: st.text_input(txt["lbl_anz"], placeholder="1", key="f_anz")
            with t_cols1[2]: st.text_input(txt["lbl_bep"], placeholder="z. B. Stk", key="f_bep")
            with t_cols1[3]: st.text_input(txt["lbl_herst"], placeholder="z. B. Otis GmbH", key="f_herst")

            t_cols2 = st.columns(4)
            with t_cols2[0]: st.text_input(txt["lbl_typ"], placeholder="z. B. Gen2", key="f_typ")
            with t_cols2[1]: st.text_input(txt["lbl_sn"], placeholder="SN-12345", key="f_sn")
            with t_cols2[2]: st.text_input(txt["lbl_ldauer"], placeholder="z. B. 20J", key="f_ldauer")
            with t_cols2[3]: st.text_input(txt["lbl_lende"], placeholder="z. B. 2040", key="f_lende")

            st.markdown("---")

            st.markdown(f"##### {txt['sec4']}")
            o_cols = st.columns(6)
            with o_cols[0]: st.text_input("Gebäudeteil", placeholder="Hauptgebäude", key="f_gteil")
            with o_cols[1]: st.text_input("Etage", placeholder="OG 1", key="f_etage")
            with o_cols[2]: st.text_input("Raum", placeholder="R-101", key="f_raum")
            with o_cols[3]: st.text_input("Raumbezeichnung", placeholder="Büro", key="f_rbez")
            with o_cols[4]: st.text_input("Zustand", placeholder="Betriebsbereit", key="f_zustand")

            st.markdown("---")

            st.markdown(f"##### {txt['sec5']}")
            
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
            if st.form_submit_button(txt["btn_reg"]):
                st.success(txt["success_reg"])
                st.rerun()
