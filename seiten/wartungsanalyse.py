import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

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

    # Lokale Demo-Daten erzwingen, damit sofort etwas da ist
    df_card = pd.DataFrame({
        "id": [i+1 for i in range(20)],
        "anlagenid": [17501 + i for i in range(20)],
        "bezeichnung": [f"Vollwartungsvertrag Objekt {i+1}" for i in range(20)],
        "firma": ["Otis GmbH", "Schindler AG", "Stulz GmbH", "Siemens AG", "Viessmann Werke"] * 4,
        "standort": ["NP" if i % 2 == 0 else "FG" for i in range(20)],
        "zyklusmonate": [12, 6, 12, 24, 12] * 4,
        "letztewartung": ["2025-05-10"] * 20,
        "naechstewartung": ["2026-05-10", "2026-03-15", "2027-01-10", "2026-06-01", "2028-02-20"] * 4,
        "weiterwartung": ["2027-05-10"] * 20,
        "status": ["In Ordnung", "Überfällig", "Anstehend", "In Ordnung", "In Ordnung"] * 4,
        "kostenpa": [1500.0] * 20,
        "anzahl": [2] * 20,
        "benchmarkep": [750.0] * 20,
        "benchmarkpa": [1500.0] * 20,
        "protokollvorhanden": ["Ja"] * 20,
        "grundlage": ["Wartungsvertrag nach DIN"] * 20,
        "hinweise": ["Keine"] * 20,
        "bemerkung": ["Demo-Eintrag"] * 20,
        "din276": ["400"] * 20
    })

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
    else:
        no_contracts_msg = "ℹ️ Keine Verträge vorhanden, die den gewählten Filtereinstellungen entsprechen." if st.session_state.language == "de" else "ℹ️ No contracts available matching the selected filter settings."
        st.info(no_contracts_msg)
