import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta
from datenbank.befehle import hole_datenbank_verbindung

def zeige_wartungsanalyse():
    if st.session_state.language == "de":
        TXT_VA = {
            "title": "Wartungsverträge & Risikoanalyse",
            "desc": "Live-Zustandsüberwachung aller Fristen inklusive automatisiertem Eskalationsmanagement bei Wartungsverzug.",
            "mode_card": "📊 Übersicht & Live-Alarme",
            "mode_edit": "⚙️ Vertrag bearbeiten / löschen",
            "v_bez": "Vertragsbezeichnung / Gewerk:", "v_firma": "Wartungsfirma / Dienstleister:", "din276": "DIN 276 Klasse:",
            "kosten": "Kosten pro Jahr (€):", "standort": "Standort:", "anzahl": "Anzahl Einheiten:", "bench_ep": "Benchmark Einzelpreis (€):",
            "protokoll": "Protokoll-Status:", "v_grund": "Gesetzliche Grundlage / Wartungsumfang:", "v_hinw": "Besondere Hinweise / Auflagen:",
            "btn_update": "Änderungen dauerhaft speichern", "btn_edit_mode": "Bearbeitungsmodus aktivieren",
            "btn_del": "Diesen Vertrag unwiderruflich löschen", 
            "chk_del_confirm": "⚠️ Ja, ich bin mir absolut sicher, dass dieser Vertrag gelöscht werden soll.",
            "success_update": "Vertragsdaten erfolgreich aktualisiert!",
            "success_del": "Vertrag wurde erfolgreich gelöscht.",
            "filter_all": "Alle",
            "filter_all_status": "Alle",
            "lbl_status_filter": "Status Filter"
        }
    else:
        TXT_VA = {
            "title": "Maintenance Contracts & Risk Analysis",
            "desc": "Live condition monitoring of all deadlines including automated escalation management in case of maintenance delay.",
            "mode_card": "📊 Overview & Live Alarms",
            "mode_edit": "⚙️ Edit / Delete Contract",
            "v_bez": "Contract Designation / Trade:", "v_firma": "Maintenance Company / Provider:", "din276": "DIN 276 Class:",
            "kosten": "Cost p.a. (€):", "location": "Location:", "anzahl": "Number of Units:", "bench_ep": "Benchmark Unit Price (€):",
            "protokoll": "Protocol Status:", "v_grund": "Legal Basis / Maintenance Scope:", "v_hinw": "Special Notes / Requirements:",
            "btn_update": "Save Changes Permanently", "btn_edit_mode": "Activate Edit Mode",
            "btn_del": "Irrevocably Delete This Contract", 
            "chk_del_confirm": "⚠️ Yes, I am absolutely sure that this contract should be deleted.",
            "success_update": "Contract data successfully updated!",
            "success_del": "Contract successfully deleted.",
            "filter_all": "All",
            "filter_all_status": "All",
            "lbl_status_filter": "Status Filter"
        }

    st.subheader(TXT_VA["title"])
    st.markdown(f"<div style='font-size: 13px; color: #64748b; margin-bottom: 15px;'>{TXT_VA['desc']}</div>", unsafe_allow_html=True)

    if "va_active_mode" not in st.session_state:
        st.session_state.va_active_mode = "card"

    col_m1, _ = st.columns([4.0, 6.0])
    with col_m1:
        if st.session_state.va_active_mode == "card":
            if st.button(TXT_VA["mode_edit"], use_container_width=True):
                st.session_state.va_active_mode = "edit"
                st.rerun()
        else:
            if st.button(TXT_VA["mode_card"], use_container_width=True):
                st.session_state.va_active_mode = "card"
                st.rerun()

    st.write("")

    if st.session_state.va_active_mode == "edit":
        conn = hole_datenbank_verbindung()
        if conn is not None:
            try:
                df_va_edit = pd.read_sql("SELECT id, bezeichnung FROM `wartungsvertraege`", conn)
                if not df_va_edit.empty:
                    anzeige_liste = [f"[ID: {row['id']}] {row['bezeichnung']}" for _, row in df_va_edit.iterrows()]
                    col_sel, _ = st.columns([4.0, 6.0])
                    select_contract_lbl = "Vertrag wählen:" if st.session_state.language == "de" else "Select Contract:"
                    with col_sel: v_auswahl = st.selectbox(select_contract_lbl, [""] + anzeige_liste, key="va_select_edit_contract")
                    if v_auswahl:
                        v_id_bereinigt = v_auswahl.replace("[ID:", "").strip()
                        vertrag_id = int(v_id_bereinigt.split("]")[0].strip())
                        
                        cursor_get = conn.cursor(dictionary=True)
                        cursor_get.execute("SELECT * FROM `wartungsvertraege` WHERE id = %s", (vertrag_id,))
                        v_det = cursor_get.fetchone()
                        cursor_get.close()
                        if v_det:
                            if "edit_vertrag_mode" not in st.session_state: st.session_state.edit_vertrag_mode = False
                            
                            col_vbtn1, col_vbtn2, _ = st.columns([2.5, 2.5, 5.0])
                            with col_vbtn1:
                                if st.button(TXT_VA["btn_edit_mode"], key="va_edit_mode_toggle_btn"): 
                                    st.session_state.edit_vertrag_mode = not st.session_state.edit_vertrag_mode
                                    st.rerun()
                            
                            with col_vbtn2:
                                if "show_del_confirm" not in st.session_state:
                                    st.session_state.show_del_confirm = False
                                
                                if not st.session_state.show_del_confirm:
                                    if st.button(TXT_VA["btn_del"], key="va_delete_contract_btn_init"):
                                        st.session_state.show_del_confirm = True
                                        st.rerun()
                                else:
                                    warn_del_msg = "⚠️ Achtung: Dieser Schritt kann nicht rückgängig gemacht werden!" if st.session_state.language == "de" else "⚠️ Warning: This step cannot be undone!"
                                    st.error(warn_del_msg)
                                    del_confirmed = st.checkbox(TXT_VA["chk_del_confirm"], key=f"chk_del_{vertrag_id}")
                                    
                                    c_del_yes, c_del_no = st.columns(2)
                                    with c_del_yes:
                                        btn_yes_lbl = "🔴 Ja, endgültig löschen" if st.session_state.language == "de" else "🔴 Yes, delete permanently"
                                        if st.button(btn_yes_lbl, key="va_confirm_del_exec", use_container_width=True):
                                            if del_confirmed:
                                                cursor_del = conn.cursor()
                                                cursor_del.execute("DELETE FROM `wartungsvertraege` WHERE id = %s", (vertrag_id,))
                                                conn.commit()
                                                cursor_del.close()
                                                st.session_state.show_del_confirm = False
                                                st.success(TXT_VA["success_del"])
                                                st.rerun()
                                            else:
                                                chk_warn_msg = "Bitte aktiviere zuerst das Bestätigungshäkchen." if st.session_state.language == "de" else "Please activate the confirmation checkbox first."
                                                st.warning(chk_warn_msg)
                                    with c_del_no:
                                        btn_cancel_lbl = "Abbrechen" if st.session_state.language == "de" else "Cancel"
                                        if st.button(btn_cancel_lbl, key="va_cancel_del", use_container_width=True):
                                            st.session_state.show_del_confirm = False
                                            st.rerun()

                            if st.session_state.edit_vertrag_mode:
                                with st.form("form_edit_vertrag_daten"):
                                    if st.session_state.language == "de":
                                        din276_optionen = [
                                            "", "100 - Grundstück", "110 - Grundstückswert", "120 - Grundstücksnebenkosten", "130 - Rechte Dritter",
                                            "200 - Vorbereitende Maßnahmen", "210 - Herrichten", "220 - Öffentliche Erschließung", "230 - Nichtöffentliche Erschließung", "240 - Ausgleichsmaßnahmen und -abgaben", "250 - Übergangsmaßnahmen",
                                            "300 - Bauwerk - Baukonstruktion", "310 - Baugrube / Erdbau", "320 - Gründung, Unterbau", "330 - Außenwände / Vertikale Baukonstruktionen, außen", "340 - Innenwände / Vertikale Baukonstruktionen, innen", "350 - Decken / Horizontale Baukonstruktionen", "360 - Dächer", "370 - Infrastrukturanlagen", "380 - Baukonstruktive Einbauten", "390 - Sonstige Maßnahmen für Baukonstruktionen",
                                            "400 - Bauwerk - Technische Anlagen", "410 - Abwasser-, Wasser-, Gasanlagen", "420 - Wärmeversorgungsanlage", "430 - Raumlufttechnische Anlagen", "440 - Elektrische Anlagen", "450 - Kommunikations-, sicherheits- und informationstechnische Anlagen", "460 - Förderanlagen", "470 - Nutzungsspezifische und verfahrenstechnische Anlagen", "480 - Gebäude- und Anlagenautomation", "490 - Sonstige Maßnahmen für technische Anlagen",
                                            "500 - Außenanlagen und Freiflächen", "510 - Erdbau", "520 - Gründung, Unterbau", "530 - Oberbau, Deckschichten", "540 - Baukonstruktionen", "550 - Technische Anlagen", "560 - Einbauten in Außenanlagen und Freiflächen", "570 - Vegetationsflächen", "580 - Wasserflächen", "590 - Sonstige Maßnahmen für Außenanlagen und Freiflächen",
                                            "600 - Ausstattung und Kunstwerke", "610 - Allgemeine Ausstattung", "620 - Besondere Ausstattung", "630 - Informationstechnische Ausstattung", "640 - Künstlerische Ausstattung", "690 - Sonstige Ausstattung",
                                            "700 - Baunebenkosten", "710 - Bauherrenaufgaben", "720 - Vorbereitung der Objektplanung", "730 - Objektplanung", "740 - Fachplanung", "750 - Künstlerische Leistungen", "760 - Allgemeine Baunebenkosten", "790 - Sonstige Baunebenkosten",
                                            "800 - Finanzierung", "810 - Finanzierungsnebenkosten", "820 - Fremdkapitalzinsen", "830 - Eigenkapitalzinsen", "840 - Bürgschaften", "890 - Sonstige Finanzierungskosten"
                                        ]
                                    else:
                                        din276_optionen = [
                                            "", "100 - Site", "110 - Site Value", "120 - Incidental Site Costs", "130 - Rights of Third Parties",
                                            "200 - Preparatory Measures", "210 - Site Preparation", "220 - Public Utility Connections", "230 - Private Utility Connections", "240 - Mitigation Measures and Fees", "250 - Transitional Measures",
                                            "300 - Building - Construction", "310 - Excavation / Earthworks", "320 - Foundation, Substructure", "330 - Exterior Walls / Vertical Structures, Exterior", "340 - Interior Walls / Vertical Structures, Interior", "350 - Ceilings / Horizontal Structures", "360 - Roofs", "370 - Infrastructure Facilities", "380 - Structural Fixtures", "390 - Other Measures for Structures",
                                            "400 - Building - Technical Installations", "410 - Drainage, Water, Gas Systems", "420 - Heat Supply Systems", "430 - HVAC Systems", "440 - Electrical Installations", "450 - Communication, Safety and IT Systems", "460 - Conveying Systems", "470 - Use-Specific and Process Systems", "480 - Building and Plant Automation", "490 - Other Measures for Technical Installations",
                                            "500 - Outdoor Facilities and Open Spaces", "510 - Earthworks", "520 - Foundation, Substructure", "530 - Superstructure, Surfacing", "540 - Structural Elements", "550 - Technical Installations", "560 - Fixtures in Outdoor Facilities", "570 - Vegetation Areas", "580 - Water Areas", "590 - Other Measures for Outdoor Facilities",
                                            "600 - Equipment and Artworks", "610 - General Equipment", "620 - Special Equipment", "630 - IT Equipment", "640 - Artistic Equipment", "690 - Other Equipment",
                                            "700 - Non-Construction Costs", "710 - Client Tasks", "720 - Preparation of Design", "730 - General Planning", "740 - Specialized Planning", "750 - Artistic Services", "760 - General Non-Construction Costs", "790 - Other Non-Construction Costs",
                                            "800 - Financing", "810 - Incidental Financing Costs", "820 - Debt Capital Interest", "830 - Equity Capital Interest", "840 - Guarantees", "890 - Other Financing Costs"
                                        ]
                                    
                                    c_main1, c_main2, c_main3 = st.columns([4.0, 4.0, 2.0])
                                    with c_main1: u_v_bez = st.text_input(TXT_VA["v_bez"], value=str(v_det['bezeichnung']), key="u_v_bez_f")
                                    with c_main2: u_v_firma = st.text_input(TXT_VA["v_firma"], value=str(v_det['firma']), key="u_v_firma_f")
                                    with c_main3:
                                        db_din_wert = str(v_det['din276']).strip()
                                        default_din_idx = 0
                                        for idx, opt in enumerate(din276_optionen):
                                            if db_din_wert in opt or opt.startswith(db_din_wert):
                                                default_din_idx = idx
                                                break
                                        din_lbl = "Kostengruppe DIN 276" if st.session_state.language == "de" else "Cost Group DIN 276"
                                        u_v_din = st.selectbox(din_lbl, options=din276_optionen, index=default_din_idx, key="u_v_din_f")

                                    st.write("")
                                    c_short1, c_main_std, c_short2, c_short3, c_short4, c_short5 = st.columns([1.5, 1.2, 1.2, 1.5, 1.2, 1.4])
                                    with c_short1: u_v_kosten = st.number_input(TXT_VA["kosten"], min_value=0.0, value=float(v_det['kostenpa']), key="u_v_kosten_f")
                                    with c_main_std: u_v_std = st.selectbox(TXT_VA["standort"], ["NP", "FG"], index=0 if v_det['standort'] == "NP" else 1, key="u_v_std_f")
                                    with c_short2: u_v_anz = st.number_input(TXT_VA["anzahl"], min_value=1, value=int(v_det['anzahl']), key="u_v_anz_f")
                                    with c_short3: u_v_bep = st.number_input(TXT_VA["bench_ep"], min_value=0.0, value=float(v_det['benchmarkep']), key="u_v_bep_f")
                                    with c_short4: 
                                        intervall_lbl = "Intervall" if st.session_state.language == "de" else "Interval"
                                        u_v_zmon = st.number_input(intervall_lbl, min_value=1, value=int(v_det['zyklusmonate'] if v_det['zyklusmonate'] else 12), key="u_v_zmon_f")
                                    with c_short5: 
                                        if st.session_state.language == "de":
                                            prot_opt_edit = ["", "Ja", "Nein", "Prüfung"]
                                        else:
                                            prot_opt_edit = ["", "Yes", "No", "Inspection"]
                                        u_v_prot = st.selectbox(TXT_VA["protokoll"], prot_opt_edit, index=0, key="u_v_prot_f")

                                    st.write("")
                                    lbl_l = "Letzte Wartung" if st.session_state.language == "de" else "Last Maintenance"
                                    lbl_nw = "Nächste Wartung" if st.session_state.language == "de" else "Next Maintenance"
                                    lbl_np = "Nächste Prüfung" if st.session_state.language == "de" else "Next Inspection"
                                    val_lw = pd.to_datetime(v_det['letztewartung']).date() if v_det['letztewartung'] else None
                                    val_nw = pd.to_datetime(v_det['naechstewartung']).date() if v_det['naechstewartung'] else None
                                    val_wp = pd.to_datetime(v_det['weiterewartung']).date() if v_det['weiterewartung'] else None

                                    c_date1, c_date2, c_date3, c_date4, _ = st.columns([2.0, 2.0, 2.0, 1.0, 3.0])
                                    with c_date1: u_v_last_w = st.date_input(lbl_l, value=val_lw, format="DD.MM.YYYY", key="u_v_lw_f")
                                    with c_date2: u_v_next_w = st.date_input(lbl_nw, value=val_nw, format="DD.MM.YYYY", key="u_v_nw_f")
                                    with c_date3: u_v_next_p = st.date_input(lbl_np, value=val_wp, format="DD.MM.YYYY", key="u_v_np_f")
                                    with c_date4: u_v_cluster = st.text_input("Cluster", value=str(v_det.get('gewaehrleistung', 'A')), key="u_v_cl_f")

                                    st.write("")
                                    c_text1, c_text2 = st.columns(2)
                                    with c_text1: u_v_grund = st.text_area(TXT_VA["v_grund"], value=str(v_det['grundlage']), height=110, key="u_v_grund_f")
                                    with c_text2: u_v_hinw = st.text_area(TXT_VA["v_hinw"], value=str(v_det['hinweise']), height=110, key="u_v_hinw_f")
                                    u_v_bem = st.text_area("Anmerkung" if st.session_state.language == "de" else "Notes", value=str(v_det['bemerkung']), height=110, key="u_v_bem_f")
                                        
                                    if st.form_submit_button(TXT_VA["btn_update"]):
                                        cursor_up = conn.cursor()
                                        u_v_bpa = int(u_v_anz) * float(u_v_bep)
                                        db_lw = u_v_last_w.strftime('%Y-%m-%d') if u_v_last_w else None
                                        db_nw = u_v_next_w.strftime('%Y-%m-%d') if u_v_next_w else None
                                        db_np = u_v_next_p.strftime('%Y-%m-%d') if u_v_next_p else None
                                        db_din_zahl = u_v_din.split(" - ")[0].strip() if u_v_din else ""
                                        
                                        sql_up = "UPDATE `wartungsvertraege` SET bezeichnung=%s, firma=%s, standort=%s, kostenpa=%s, anzahl=%s, benchmarkep=%s, benchmarkpa=%s, protokollvorhanden=%s, zyklusmonate=%s, din276=%s, grundlage=%s, hinweise=%s, bemerkung=%s, letztewartung=%s, naechstewartung=%s, weiterewartung=%s WHERE id=%s"
                                        cursor_up.execute(sql_up, (u_v_bez, u_v_firma, u_v_std, u_v_kosten, u_v_anz, u_v_bep, u_v_bpa, u_v_prot, u_v_zmon, db_din_zahl, u_v_grund, u_v_hinw, u_v_bem, db_lw, db_nw, db_np, vertrag_id))
                                        conn.commit()
                                        cursor_up.close()
                                        st.session_state.edit_vertrag_mode = False
                                        st.success(TXT_VA["success_update"])
                                        st.rerun()
            except Exception as e: 
                err_prefix = "Fehler:" if st.session_state.language == "de" else "Error:"
                st.error(f"{err_prefix} {str(e)}")
            finally: 
                conn.close()

    else:
        conn = hole_datenbank_verbindung()
        if conn is not None:
            try:
                df_card = pd.read_sql("SELECT * FROM `wartungsvertraege`", conn)
                if not df_card.empty:
                    heute_dt = pd.to_datetime(datetime.now().date())
                    status_liste = []
                    for _, r in df_card.iterrows():
                        nw_val = r["naechstewartung"]
                        if not nw_val:
                            status_liste.append("🟢 Erledigt" if st.session_state.language == "de" else "🟢 Completed")
                            continue
                        nw_dt = pd.to_datetime(nw_val, errors='coerce')
                        if pd.isnull(nw_dt):
                            status_liste.append("🟢 Erledigt" if st.session_state.language == "de" else "🟢 Completed")
                            continue
                        if nw_dt.date() < heute_dt.date():
                            status_liste.append("🔴 Fällig" if st.session_state.language == "de" else "🔴 Due")
                        elif heute_dt.date() <= nw_dt.date() <= (heute_dt.date() + timedelta(days=90)):
                            status_liste.append("🟡 Warnung" if st.session_state.language == "de" else "🟡 Warning")
                        else:
                            status_liste.append("🟢 Erledigt" if st.session_state.language == "de" else "🟢 Completed")
                    df_card["Live_Status"] = status_liste
                    
                    ueberfaellig_str = "🔴 Fällig" if st.session_state.language == "de" else "🔴 Due"
                    warnung_str = "🟡 Warnung" if st.session_state.language == "de" else "🟡 Warning"

                    anz_rot = len(df_card[df_card["Live_Status"] == ueberfaellig_str])
                    anz_gelb = len(df_card[df_card["Live_Status"] == warnung_str])
                    
                    c_zaehler, c_fil_std, c_fil_stat = st.columns([2.5, 3.0, 4.5])
                    with c_zaehler:
                        if st.session_state.language == "de":
                            alarm_lbl = f"<div style='font-size:12px; font-weight:600; color:#94a3b8; margin-top:5px;'>🚨 Alarme aktiv: <span style='color:#ef4444;'>{anz_rot} Fällig</span> | <span style='color:#f59e0b;'>{anz_gelb} Warnung</span></div>"
                        else:
                            alarm_lbl = f"<div style='font-size:12px; font-weight:600; color:#94a3b8; margin-top:5px;'>🚨 Active Alarms: <span style='color:#ef4444;'>{anz_rot} Due</span> | <span style='color:#f59e0b;'>{anz_gelb} Warning</span></div>"
                        st.markdown(alarm_lbl, unsafe_allow_html=True)
                    
                    with c_fil_std:
                        standort_optionen = [TXT_VA["filter_all"], "NP", "FG"]
                        std_label = "Standort" if st.session_state.language == "de" else "Location"
                        fil_std = st.radio(std_label, options=standort_optionen, horizontal=True, key="va_fil_std_radio_v1")

                    with c_fil_stat:
                        erledigt_str = "🟢 Erledigt" if st.session_state.language == "de" else "🟢 Completed"
                        status_optionen = [TXT_VA["filter_all_status"], ueberfaellig_str, warnung_str, erledigt_str]
                        fil_stat = st.radio(TXT_VA["lbl_status_filter"], options=status_optionen, horizontal=True, key="va_fil_stat_radio_v1")
                    
                    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
                    df_filtered = df_card.copy()
                    
                    if fil_std != TXT_VA["filter_all"]:
                        df_filtered = df_filtered[df_filtered["standort"] == fil_std]
                        
                    if fil_stat != TXT_VA["filter_all_status"]:
                        df_filtered = df_filtered[df_filtered["Live_Status"] == fil_stat]

                    if not df_filtered.empty:
                        for _, row in df_filtered.iterrows():
                            v_id = row["id"]
                            v_bez = row["bezeichnung"]
                            v_firma = row["firma"]
                            v_std = row["standort"]
                            v_next_val = str(row["naechstewartung"]).strip()
                            v_next = pd.to_datetime(row["naechstewartung"]).strftime('%d.%m.%Y') if v_next_val and v_next_val != "None" and v_next_val != "nan" and v_next_val != "-" else "-"
                            v_status = row["Live_Status"]
                            
                            next_lbl = "Nächste" if st.session_state.language == "de" else "Next"
                            expander_titel = f"{v_status} | {v_bez} ({v_firma}) | 📍 {v_std} | 📅 {next_lbl}: {v_next}"
                            with st.expander(expander_titel, expanded=False):
                                details_header = f"##### 📋 Vertrags-Details (ID: {v_id})" if st.session_state.language == "de" else f"##### 📋 Contract Details (ID: {v_id})"
                                st.markdown(details_header)
                                c_det1, c_date_info = st.columns([6.0, 4.0])
                                with c_det1:
                                    dl_lbl = "Dienstleister / Firma" if st.session_state.language == "de" else "Service Provider / Company"
                                    basis_lbl = "Grundlage / Umfang" if st.session_state.language == "de" else "Basis / Scope"
                                    notes_lbl = "Hinweise / Auflagen" if st.session_state.language == "de" else "Notes / Requirements"
                                    remark_lbl = "Anmerkung" if st.session_state.language == "de" else "Remark"

                                    st.markdown(f"**{dl_lbl}:** {v_firma if str(v_firma) != 'nan' else '-'}")
                                    st.markdown(f"**{basis_lbl}:** {row['grundlage'] if str(row['grundlage']) != 'nan' and row['grundlage'] else '-'}")
                                    st.markdown(f"**{notes_lbl}:** {row['hinweise'] if str(row['hinweise']) != 'nan' and row['hinweise'] else '-'}")
                                    st.markdown(f"**{remark_lbl}:** {row['bemerkung'] if str(row['bemerkung']) != 'nan' and row['bemerkung'] else '-'}")
                                with c_date_info:
                                    costs_lbl = "Kosten p.a." if st.session_state.language == "de" else "Cost p.a."
                                    interval_lbl = "Intervall" if st.session_state.language == "de" else "Interval"
                                    months_lbl = "Monate" if st.session_state.language == "de" else "Months"
                                    proto_lbl = "Protokoll vorhanden" if st.session_state.language == "de" else "Protocol available"
                                    last_m_lbl = "Letzte Wartung" if st.session_state.language == "de" else "Last Maintenance"

                                    st.markdown(f"🪙 **{costs_lbl}:** {row['kostenpa'] if str(row['kostenpa']) != 'nan' else '0.0'} €")
                                    st.markdown(f"🔄 **{interval_lbl}:** {row['zyklusmonate'] if str(row['zyklusmonate']) != 'nan' else '12'} {months_lbl}")
                                    
                                    prot_val = str(row['protokollvorhanden']).strip()
                                    if not prot_val or prot_val == "-" or prot_val == "nan" or prot_val == "None" or prot_val.lower() == "nein":
                                        prot_display = "Keines" if st.session_state.language == "de" else "None"
                                    elif prot_val.lower() == "ja":
                                        prot_display = "Ja" if st.session_state.language == "de" else "Yes"
                                    else:
                                        prot_display = prot_val
                                    st.markdown(f"📜 **{proto_lbl}:** {prot_display}")
                                    
                                    v_last_val = str(row["letztewartung"]).strip()
                                    v_last = pd.to_datetime(row["letztewartung"]).strftime('%d.%m.%Y') if v_last_val and v_last_val != "None" and v_last_val != "nan" and v_last_val != "-" else "-"
                                    st.markdown(f"📅 **{last_m_lbl}:** {v_last}")
                                if v_status in ("🔴 Fällig", "🔴 Due"):
                                    st.markdown("<div style='border-top: 1px solid #334155; margin: 15px 0 10px 0;'></div>", unsafe_allow_html=True)
                                    esk_header = "ESKALATIONS-STUFEN FÜR DIESEN VERTRAG:" if st.session_state.language == "de" else "ESCALATION STAGES FOR THIS CONTRACT:"
                                    st.markdown(f"<p style='font-size: 11px; font-weight: bold; color: #4a90e2; letter-spacing: 0.5px; margin-bottom: 8px;'>🚨 {esk_header}</p>", unsafe_allow_html=True)
                                    
                                    key_active_stufe = f"esk_active_{v_id}"
                                    if key_active_stufe not in st.session_state:
                                        st.session_state[key_active_stufe] = None
                                        
                                    col_e1, col_e2, col_e3, col_e4 = st.columns(4)
                                    with col_e1:
                                        btn_s1 = "⚠️ Stufe 1: Erinnerung" if st.session_state.language == "de" else "⚠️ Stage 1: Reminder"
                                        if st.button(btn_s1, key=f"btn_esk1_{v_id}", use_container_width=True):
                                            st.session_state[key_active_stufe] = 1
                                            st.rerun()
                                    with col_e2:
                                        btn_s2 = "🚨 Stufe 2: Mahnung 1" if st.session_state.language == "de" else "🚨 Stage 2: Warning 1"
                                        if st.button(btn_s2, key=f"btn_esk2_{v_id}", use_container_width=True):
                                            st.session_state[key_active_stufe] = 2
                                            st.rerun()
                                    with col_e3:
                                        btn_s3 = "🔥 Stufe 3: Chef-Eskalation" if st.session_state.language == "de" else "🔥 Stage 3: Management Escalation"
                                        if st.button(btn_s3, key=f"btn_esk3_{v_id}", use_container_width=True):
                                            st.session_state[key_active_stufe] = 3
                                            st.rerun()
                                    with col_e4:
                                        btn_s4 = "🚫 Stufe 4: Rechtsschritt" if st.session_state.language == "de" else "🚫 Stage 4: Legal Action"
                                        if st.button(btn_s4, key=f"btn_esk4_{v_id}", use_container_width=True):
                                            st.session_state[key_active_stufe] = 4
                                            st.rerun()

                                    if st.session_state[key_active_stufe] is not None:
                                        aktuelle_stufe = st.session_state[key_active_stufe]
                                        
                                        if st.session_state.language == "de":
                                            if aktuelle_stufe == 1:
                                                betreff_default = f"Erinnerung: Fällige Wartung für Vertrag-ID {v_id} ({v_bez}) - ESM"
                                                text_default = f"Sehr geehrte Damen und Herren,\n\nlaut unseren Systemunterlagen ist die vertraglich vereinbarte Wartung für den Vertrag '{v_bez}' (Vertrags-ID: {v_id}, Standort: {v_std}) seit dem {v_next} überfällig.\n\nBitte teilen Sie uns kurzfristig einen verbindlichen Ausführungstermin mit.\n\nMit freundlichen Grüßen,\nEuropäische Schule München\nWartungsmanagement"
                                            elif aktuelle_stufe == 2:
                                                betreff_default = f"1. FÖRMLICHE MAHNUNG: Wartungsverzug zu Vertrag-ID {v_id} ({v_bez}) - ESM"
                                                text_default = f"Sehr geehrte Damen und Herren,\n\ntrotz unserer vorherigen Erinnerung liegt uns für die fällige Wartung des Gewerks '{v_bez}' (Vertrags-ID: {v_id}, Standort: {v_std}) noch kein Ausführungstermin vor. Die Frist für diese vertragliche Leistung lief am {v_next} ab.\n\nWir fordern Sie hiermit förmlich auf, die Arbeiten innerhalb von 7 Werktagen nachzuholen, um den Versicherungsschutz der betroffenen Anlagen nicht zu gefährden.\n\nMit freundlichen Grüßen,\nEuropäische Schule München\nGebäudemanagement"
                                            elif aktuelle_stufe == 3:
                                                betreff_default = f"INTERNER ALARMBERICHT: Kritischer Wartungsverzug bei Vertrag-ID {v_id} ({v_bez})"
                                                text_default = f"Meldung an die Schulleitung / Sicherheitsbeauftragte der ESM:\n\nHiermit wird gemeldet, dass der beauftragte Dienstleister '{v_firma}' für das sicherheitsrelevante Gewerk '{v_bez}' (Vertrags-ID: {v_id}) trotz mehrfacher Mahnung massiv im Verzug ist.\n\nUrsprüngliches Fälligkeitsdatum: {v_next}\nBetroffener Standort: {v_std}\n\nEs wird dringend empfohlen, eine letztmalige Fristsetzung mit Kündigungsandrohung wegen Nichterfüllung vorzubereiten."
                                            else:
                                                betreff_default = f"Übergabe Akte an Rechtsabteilung: Vertragsbruch durch {v_firma} (Vertrag-ID {v_id})"
                                                text_default = f"Sehr geehrte Damen und Herren,\n\nhiermit übergeben wir die Rechtsakte zur Vertrag-ID {v_id} ({v_bez}). Der Dienstleister '{v_firma}' verweigert die vertraglich geschuldete Wartung für diesen Vertrag seit dem Fälligkeitsdatum {v_next}.\n\nSämtliche außergerichtlichen Mahnstufen wurden ergebnislos durchlaufen. Bitte leiten Sie unverzüglich die notwendigen rechtlichen Schritte ein."
                                        else:
                                            if aktuelle_stufe == 1:
                                                betreff_default = f"Reminder: Due Maintenance for Contract ID {v_id} ({v_bez}) - ESM"
                                                text_default = f"Dear Ladies and Gentlemen,\n\naccording to our system records, the contractually agreed maintenance for contract '{v_bez}' (Contract ID: {v_id}, Location: {v_std}) has been overdue since {v_next}.\n\nPlease provide a binding execution date shortly.\n\nKind regards,\nEuropean School Munich\nMaintenance Management"
                                            elif aktuelle_stufe == 2:
                                                betreff_default = f"1st FORMAL WARNING: Maintenance Delay for Contract ID {v_id} ({v_bez}) - ESM"
                                                text_default = f"Dear Ladies and Gentlemen,\n\ndespite our previous reminder, we have not yet received an execution date for the due maintenance of trade '{v_bez}' (Contract ID: {v_id}, Location: {v_std}). The deadline expired on {v_next}.\n\nWe hereby formally request you to catch up on the work within 7 business days so as not to jeopardize the insurance coverage of the affected assets.\n\nKind regards,\nEuropean School Munich\nFacility Management"
                                            elif aktuelle_stufe == 3:
                                                betreff_default = f"INTERNAL ALARM REPORT: Critical Maintenance Delay for Contract ID {v_id} ({v_bez})"
                                                text_default = f"Report to School Management / Safety Officers of ESM:\n\nThis is to report that the commissioned service provider '{v_firma}' for the safety-relevant trade '{v_bez}' (Contract ID: {v_id}) is massively delayed despite multiple warnings.\n\nOriginal Due Date: {v_next}\nAffected Location: {v_std}\n\nIt is strongly recommended to prepare a final deadline with threat of termination for non-performance."
                                            else:
                                                betreff_default = f"Handover of File to Legal Department: Breach of Contract by {v_firma} (Contract ID {v_id})"
                                                text_default = f"Dear Ladies and Gentlemen,\n\nwe hereby hand over the legal file for Contract ID {v_id} ({v_bez}). The service provider '{v_firma}' has refused the contractually owed maintenance for this contract since the due date {v_next}.\n\nAll out-of-court warning stages have been exhausted without result. Please initiate the necessary legal steps immediately."

                                        edit_letter_lbl = f"**{'Bearbeite Anschreiben' if st.session_state.language == 'de' else 'Edit Letter'}: {'Stufe' if st.session_state.language == 'de' else 'Stage'} {aktuelle_stufe}**"
                                        st.markdown(edit_letter_lbl)
                                        subj_lbl = "Betreffzeile:" if st.session_state.language == "de" else "Subject Line:"
                                        body_lbl = "Inhalt des Schreibens (frei anpassbar):" if st.session_state.language == "de" else "Content of the Letter (fully customizable):"
                                        u_betreff = st.text_input(subj_lbl, value=betreff_default, key=f"txt_betreff_{v_id}_{aktuelle_stufe}")
                                        u_text = st.text_area(body_lbl, value=text_default, height=180, key=f"txt_area_{v_id}_{aktuelle_stufe}")

                                        c_action1, c_action2 = st.columns([5.0, 5.0])
                                        with c_action1:
                                            if aktuelle_stufe in (1, 2):
                                                mail_enc_subject = urllib.parse.quote(u_betreff)
                                                mail_enc_body = urllib.parse.quote(u_text)
                                                outlook_btn_lbl = "📧 E-Mail Entwurf in Outlook öffnen" if st.session_state.language == "de" else "📧 Open Email Draft in Outlook"
                                                st.markdown(f'<a href="mailto:info@{v_firma.lower().replace(" ", "")}.de?subject={mail_enc_subject}&body={mail_enc_body}"><button style="background-color:#1e3a8a;color:#cbd5e1;border:1px solid #3b82f6;padding:8px 16px;border-radius:6px;cursor:pointer;font-weight:600;width:100%;">{outlook_btn_lbl}</button></a>', unsafe_allow_html=True)
                                            else:
                                                from fpdf import FPDF
                                                pdf_esk = FPDF()
                                                pdf_esk.add_page()
                                                pdf_esk.set_font("Helvetica", "B", 14)
                                                pdf_esk.set_text_color(30, 136, 229)
                                                pdf_esk.cell(0, 10, "Europäische Schule München - Eskalationsbericht" if st.session_state.language == "de" else "European School Munich - Escalation Report", ln=True)
                                                pdf_esk.line(10, 20, 200, 20)
                                                pdf_esk.ln(10)
                                                pdf_esk.set_font("Helvetica", "B", 11)
                                                pdf_esk.set_text_color(244, 63, 94)
                                                pdf_esk.cell(0, 8, f"BETREFF: {u_betreff}".encode('latin-1', 'ignore').decode('latin-1'), ln=True)
                                                pdf_esk.ln(4)
                                                pdf_esk.set_font("Helvetica", "", 10)
                                                pdf_esk.set_text_color(226, 232, 240)
                                                
                                                for zeile in u_text.split('\n'):
                                                    zeile_sauber = zeile.replace("Ä", "Ae").replace("ä", "ae").replace("Ö", "Oe").replace("ö", "oe").replace("Ü", "Ue").replace("ü", "ue")
                                                    pdf_esk.cell(0, 6, zeile_sauber.encode('latin-1', 'ignore').decode('latin-1'), ln=True)
                                                
                                                pdf_raw_esk = pdf_esk.output(dest='S')
                                                pdf_bytes_esk = bytes(pdf_raw_esk) if isinstance(pdf_raw_esk, bytearray) else pdf_raw_esk
                                                btn_lbl_pdf = "📄 PDF-Bericht herunterladen" if st.session_state.language == "de" else "📄 Download PDF Report"
                                                st.download_button(label=btn_lbl_pdf, data=pdf_bytes_esk, file_name=f"ESM_Eskalation_Stufe_{aktuelle_stufe}_{v_id}.pdf", mime="application/pdf", key=f"dl_btn_esk_pdf_{v_id}")

                                        with c_action2:
                                            close_lbl = "❌ Schließen" if st.session_state.language == "de" else "❌ Close"
                                            if st.button(close_lbl, key=f"btn_close_esk_{v_id}", use_container_width=True):
                                                st.session_state[key_active_stufe] = None
                                                st.rerun()
                                                
                                st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        no_contracts_msg = "ℹ️ Keine Verträge vorhanden, die den gewählten Filtereinstellungen entsprechen." if st.session_state.language == "de" else "ℹ️ No contracts available matching the selected filter settings."
                        st.info(no_contracts_msg)
            except Exception as e: 
                err_msg = "Fehler:" if st.session_state.language == "de" else "Error:"
                st.error(f"{err_msg} {str(e)}")
            finally: 
                conn.close()