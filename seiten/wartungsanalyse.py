import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def zeige_wartungsanalyse():
    if 'language' not in st.session_state:
        st.session_state.language = "de"

    if st.session_state.language == "de":
        TXT_VA = {
            "title": "Wartungsverträge & Risikoanalyse",
            "desc": "Live-Zustandsüberwachung aller Fristen inklusive automatisiertem Eskalationsmanagement bei Wartungsverzug.",
            "select_contract": "Wählen Sie einen Vertrag zur Detailansicht:",
            "lbl_status_filter": "Status Filter",
            "filter_all": "Alle",
            "filter_all_status": "Alle"
        }
    else:
        TXT_VA = {
            "title": "Maintenance Contracts & Risk Analysis",
            "desc": "Live condition monitoring of all deadlines including automated escalation management in case of maintenance delay.",
            "select_contract": "Select a contract for detailed view:",
            "lbl_status_filter": "Status Filter",
            "filter_all": "All",
            "filter_all_status": "All"
        }

    st.subheader(TXT_VA["title"])
    st.markdown(f"<div style='font-size: 13px; opacity: 0.7; margin-bottom: 20px;'>{TXT_VA['desc']}</div>", unsafe_allow_html=True)

    # Lokale Demo-Daten erzwingen
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
    
    # KPI-Leiste oben
    if st.session_state.language == "de":
        st.markdown(f"<div style='font-size:13px; font-weight:600; margin-bottom:15px;'>🚨 Alarme aktiv: <span style='color:#ef4444;'>{anz_rot} Fällig</span> | <span style='color:#f59e0b;'>{anz_gelb} Warnung</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='font-size:13px; font-weight:600; margin-bottom:15px;'>🚨 Active Alarms: <span style='color:#ef4444;'>{anz_rot} Due</span> | <span style='color:#f59e0b;'>{anz_gelb} Warning</span></div>", unsafe_allow_html=True)

    # --- ENTERPRISE MASTER-DETAIL LAYOUT (Zwei Spalten) ---
    col_master, col_detail = st.columns([4.0, 6.0], gap="medium")

    with col_master:
        with st.container(border=True):
            st.markdown(f"##### 📑 {TXT_VA['select_contract']}")
            
            # Filteroptionen für die Auswahlliste
            standort_optionen = [TXT_VA["filter_all"], "NP", "FG"]
            fil_std = st.selectbox("Standort-Filter", options=standort_optionen, key="va_master_std")
            
            erledigt_str = "🟢 Erledigt" if st.session_state.language == "de" else "🟢 Completed"
            status_optionen = [TXT_VA["filter_all_status"], ueberfaellig_str, warnung_str, erledigt_str]
            fil_stat = st.selectbox(TXT_VA["lbl_status_filter"], options=status_optionen, key="va_master_stat")

            df_filtered = df_card.copy()
            if fil_std != TXT_VA["filter_all"]:
                df_filtered = df_filtered[df_filtered["standort"] == fil_std]
            if fil_stat != TXT_VA["filter_all_status"]:
                df_filtered = df_filtered[df_filtered["Live_Status"] == fil_stat]

            if not df_filtered.empty:
                vertrag_labels = []
                for _, r in df_filtered.iterrows():
                    next_val = pd.to_datetime(r["naechstewartung"]).strftime('%d.%m.%Y') if pd.notnull(r["naechstewartung"]) else "-"
                    label = f"{r['Live_Status']} | {r['bezeichnung']} ({r['firma']}) - 📍 {r['standort']}"
                    vertrag_labels.append((label, r["id"]))

                auswahl_label = st.selectbox(
                    "Vertragsauswahl", 
                    options=[item[0] for item in vertrag_labels],
                    label_visibility="collapsed",
                    key="va_master_selectbox"
                )
                
                # Finde die ID des ausgewählten Vertrags
                selected_id = next(item[1] for item in vertrag_labels if item[0] == auswahl_label)
                row = df_card[df_card["id"] == selected_id].iloc[0]
            else:
                st.warning("Keine Verträge für diese Filterkombination gefunden.")
                row = None

    with col_detail:
        if row is not None:
            with st.container(border=True):
                v_id = row["id"]
                v_bez = row["bezeichnung"]
                v_firma = row["firma"]
                v_status = row["Live_Status"]
                v_next = pd.to_datetime(row["naechstewartung"]).strftime('%d.%m.%Y') if pd.notnull(row["naechstewartung"]) else "-"
                
                st.markdown(f"##### 📋 {v_status} | {v_bez} (ID: {v_id})")
                st.markdown(f"<div style='font-size: 11px; opacity: 0.7; margin-bottom: 10px;'>Wartungsfirma: <b>{v_firma}</b> | Standort: <b>{row['standort']}</b> | Nächste Wartung: <b>{v_next}</b></div>", unsafe_allow_html=True)
                
                c_det_sub1, c_det_sub2 = st.columns(2)
                with c_det_sub1:
                    dl_lbl = "Dienstleister / Firma" if st.session_state.language == "de" else "Service Provider"
                    basis_lbl = "Grundlage / Umfang" if st.session_state.language == "de" else "Basis / Scope"
                    costs_lbl = "Kosten p.a." if st.session_state.language == "de" else "Cost p.a."
                    interval_lbl = "Intervall" if st.session_state.language == "de" else "Interval"
                    
                    st.markdown(f"**{dl_lbl}:** {v_firma}")
                    st.markdown(f"**{basis_lbl}:** {row['grundlage']}")
                    st.markdown(f"🪙 **{costs_lbl}:** {row['kostenpa']} €")
                    st.markdown(f"🔄 **{interval_lbl}:** {row['zyklusmonate']} Monate")

                with c_det_sub2:
                    notes_lbl = "Hinweise / Auflagen" if st.session_state.language == "de" else "Notes"
                    proto_lbl = "Protokoll vorhanden" if st.session_state.language == "de" else "Protocol available"
                    last_m_lbl = "Letzte Wartung" if st.session_state.language == "de" else "Last Maintenance"
                    
                    st.markdown(f"**{notes_lbl}:** {row['hinweise']}")
                    st.markdown(f"📜 **{proto_lbl}:** {row['protokollvorhanden']}")
                    v_last = pd.to_datetime(row["letztewartung"]).strftime('%d.%m.%Y') if pd.notnull(row["letztewartung"]) else "-"
                    st.markdown(f"📅 **{last_m_lbl}:** {v_last}")

                st.markdown("---")
                st.markdown("⚙️ **Direkt-Steuerung & Notizen**")
                
                status_change_lbl = "Status anpassen:" if st.session_state.language == "de" else "Update Status:"
                aktuelle_optionen = ["In Ordnung", "Überfällig", "Anstehend", "Erledigt"]
                neuer_status = st.selectbox(status_change_lbl, options=aktuelle_optionen, index=0, key=f"sel_status_{v_id}")
                
                notiz_lbl = "Schnellnotiz / Vermerk:" if st.session_state.language == "de" else "Quick Note:"
                aktuelle_bemerkung = str(row['bemerkung']) if str(row['bemerkung']) != 'nan' else ""
                neue_notiz = st.text_area(notiz_lbl, value=aktuelle_bemerkung, height=75, key=f"txt_notiz_{v_id}")
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    save_lbl = "💾 Speichern" if st.session_state.language == "de" else "💾 Save"
                    if st.button(save_lbl, key=f"btn_save_{v_id}", use_container_width=True):
                        success_msg = "Änderungen erfolgreich übernommen!" if st.session_state.language == "de" else "Changes applied successfully!"
                        st.success(success_msg)
                        
                with btn_col2:
                    doc_link_lbl = "📂 Dokument" if st.session_state.language == "de" else "📂 Document"
                    if st.button(doc_link_lbl, key=f"btn_doc_{v_id}", use_container_width=True):
                        doc_info = f"Navigiere zum Vertrag im Dokumentenarchiv (ID: {v_id})" if st.session_state.language == "de" else f"Navigating to contract (ID: {v_id})"
                        st.info(doc_info)
        else:
            st.info("Bitte wählen Sie links einen Vertrag aus.")
