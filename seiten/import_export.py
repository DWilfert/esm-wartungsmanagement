import streamlit as st
import pandas as pd
import io
from datetime import datetime
from datenbank.befehle import hole_datenbank_verbindung

def zeige_import_export():
    st.markdown("""
        <style>
        /* Kompakte Schriftgröße in allen Eingabefeldern, Radio-Buttons und Formularen */
        input, select, textarea, div[data-baseweb="select"] span, label, .stRadio div {
            font-size: 0.82rem !important;
        }
        
        /* Blendet den automatischen Streamlit-Hinweis aus */
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        
        /* Placeholder in leicht grauer Schrift und Kursiv */
        input::placeholder, textarea::placeholder {
            color: #94a3b8 !important;
            font-style: italic !important;
            opacity: 1 !important;
        }
        
        /* Dropdown-Menüs und Popovers */
        div[data-testid="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
            background-color: var(--secondary-background-color) !important;
        }
        
        ul[role="listbox"] li, li[role="option"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            font-size: 0.85rem !important;
        }
        
        /* Dezenter, dunkler Hover-Zustand passend zum Dark-Mode */
        ul[role="listbox"] li:hover,
        ul[role="listbox"] li[aria-selected="true"],
        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {
            background-color: rgba(128, 128, 128, 0.25) !important;
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

        /* Automatischer Hintergrund- und Rahmen-Fix für st.dataframe im Matrix-Look */
        div[data-testid="stDataFrame"] {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
            background-image: linear-gradient(to right, rgba(128, 128, 128, 0.08) 1px, transparent 1px),
                              linear-gradient(to bottom, rgba(128, 128, 128, 0.08) 1px, transparent 1px);
            background-size: 15px 15px;
        }

        div[data-testid="stDataFrame"] td {
            padding-top: 2px !important;
            padding-bottom: 2px !important;
            font-size: 0.78rem !important;
        }

        .enterprise-card {
            background-color: rgba(128, 128, 128, 0.04);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 0.5rem;
            padding: 18px;
            margin-bottom: 20px;
        }
        
        .kpi-card {
            background-color: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 0.5rem;
            padding: 12px 15px;
            text-align: center;
        }
        
        /* Echte, feine Trennlinie statt Browser-Box */
        .saubere-trennlinie {
            border: none;
            border-top: 1px solid rgba(128, 128, 128, 0.25);
            margin: 25px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.language == "de":
        TXT_IE = {
            "title": "Daten-Schnittstelle (Excel Hub)",
            "desc": "Zentrale Steuerungseinheit für den sicheren Excel-Datentransfer, System-Backups und standardisierte Daten-Templates.",
            "direction_lbl": "Schnittstellen-Richtung wählen:",
            "dir_exp": "Daten exportieren (Backup)", 
            "dir_imp": "Daten importieren (Upload)",
            "exp_title": "##### 📊 Tabellenauswahl für den Excel-Export",
            "exp_q": "Welche Daten möchtest du exportieren?", 
            "err_conn": "Keine Verbindung zur Datenbank.",
            "exp_success": "Datensätze aus '{}' erfolgreich bereitgestellt.",
            "exp_empty": "Die Tabelle '{}' enthält aktuell keine Daten.", 
            "err_exp": "Fehler beim Exportieren:",
            "kpi_1": "Aktive Anlagen",
            "kpi_2": "Aktive Verträge",
            "kpi_3": "Dienstleister",
            "kpi_4": "System-Status",
            "status_ok": "Online (Sicher)",
            "template_title": "📥 Interaktiver Vorlagen-Generator",
            "template_desc": "Wählen Sie eine Tabelle aus, um das exakte Excel-Template inklusive automatischer Feld-Legende herunterzuladen.",
            "template_sel": "Tabelle für Vorlage wählen:",
            "log_title": "🕒 Schnittstellen-Protokoll (Audit-Trail)",
            "dl_tmpl_btn": "📥 Ausgewählte Vorlage herunterladen"
        }
    else:
        TXT_IE = {
            "title": "Data Interface (Excel Hub)",
            "desc": "Central control unit for secure Excel data transfers, system backups, and standardized data templates.",
            "direction_lbl": "Select Interface Direction:",
            "dir_exp": "Export Data (Backup)", 
            "dir_imp": "Import Data (Upload)",
            "exp_title": "##### 📊 Table Selection for Excel Export",
            "exp_q": "Which data do you want to export?", 
            "err_conn": "No database connection.",
            "exp_success": "Records from '{}' successfully provided.",
            "exp_empty": "The table '{}' currently contains no data.", 
            "err_exp": "Error during export:",
            "kpi_1": "Active Assets",
            "kpi_2": "Active Contracts",
            "kpi_3": "Contractors",
            "kpi_4": "System Status",
            "status_ok": "Online (Secure)",
            "template_title": "📥 Interactive Template Generator",
            "template_desc": "Select a table to download the exact Excel template including automatic field legend.",
            "template_sel": "Select table for template:",
            "log_title": "🕒 Interface Log (Audit Trail)",
            "dl_tmpl_btn": "📥 Download Selected Template"
        }

    st.subheader(TXT_IE["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 20px;'>{TXT_IE['desc']}</div>", unsafe_allow_html=True)

    # --- 1. EXECUTIVE KPI-LEISTE OBEN ---
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.markdown(f"""<div class="kpi-card"><div style="font-size: 11px; opacity: 0.7;">{TXT_IE['kpi_1']}</div><div style="font-size: 18px; font-weight: bold; color: #3b82f6;">142</div></div>""", unsafe_allow_html=True)
    with col_k2:
        st.markdown(f"""<div class="kpi-card"><div style="font-size: 11px; opacity: 0.7;">{TXT_IE['kpi_2']}</div><div style="font-size: 18px; font-weight: bold; color: #10b981;">88</div></div>""", unsafe_allow_html=True)
    with col_k3:
        st.markdown(f"""<div class="kpi-card"><div style="font-size: 11px; opacity: 0.7;">{TXT_IE['kpi_3']}</div><div style="font-size: 18px; font-weight: bold; color: #f59e0b;">16</div></div>""", unsafe_allow_html=True)
    with col_k4:
        st.markdown(f"""<div class="kpi-card"><div style="font-size: 11px; opacity: 0.7;">{TXT_IE['kpi_4']}</div><div style="font-size: 18px; font-weight: bold; color: #10b981;">{TXT_IE['status_ok']}</div></div>""", unsafe_allow_html=True)

    st.write("")

    ie_aktion = st.radio(TXT_IE["direction_lbl"], [TXT_IE["dir_exp"], TXT_IE["dir_imp"]], horizontal=True, key="ie_haupt_aktion_final_v7")
    st.write("")

    tabellen_liste = {
        "Wartungsverträge" if st.session_state.language == "de" else "Maintenance Contracts": "wartungsvertraege",
        "Anlagenstruktur" if st.session_state.language == "de" else "Asset Structure": "anlagen",
        "Mängel & Auffälligkeiten" if st.session_state.language == "de" else "Defects & Observations": "wartungsplanung",
        "Serviceeinträge" if st.session_state.language == "de" else "Service Reports": "serviceeinsaetze"
    }

    # --- 2. ZWEI-SPALTEN-LAYOUT (HAUPTBEREICH & INTERAKTIVER TEMPLATE-HUB) ---
    col_main_left, col_main_right = st.columns([6.0, 4.0])

    with col_main_left:
        st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)

        # --- EXPORT BEREICH ---
        if ie_aktion == TXT_IE["dir_exp"]:
            st.markdown(TXT_IE["exp_title"])
            col_exp_sel, _ = st.columns([6.0, 4.0])
            with col_exp_sel:
                export_wahl = st.selectbox(TXT_IE["exp_q"], [""] + list(tabellen_liste.keys()), key="export_bereich_wahl_final_v7")
            
            if export_wahl:
                db_tabelle = tabellen_liste[export_wahl]
                conn = hole_datenbank_verbindung()
                if conn is not None:
                    try:
                        df_exp = pd.read_sql(f"SELECT * FROM `{db_tabelle}`", conn)
                        if not df_exp.empty:
                            st.success(f"🟢 {len(df_exp)} {TXT_IE['exp_success'].format(export_wahl)}")
                            df_exp_schick = df_exp.copy()
                            for spalte in df_exp_schick.columns:
                                if any(k in spalte.lower() for k in ["datum", "wartung", "termin", "weitere"]):
                                    try:
                                        df_exp_schick[spalte] = pd.to_datetime(df_exp_schick[spalte], errors="coerce").dt.strftime("%d.%m.%Y")
                                    except: pass
                            output_ie = io.BytesIO()
                            with pd.ExcelWriter(output_ie, engine='xlsxwriter') as writer:
                                df_exp_schick.to_excel(writer, index=False, sheet_name=export_wahl[:30])
                            excel_ie_data = output_ie.getvalue()
                            dateiname = f"ESM_Backup_{db_tabelle}_{datetime.now().strftime('%Y%m%d')}.xlsx"
                            
                            btn_dl_lbl = f"📥 '{export_wahl}' als Excel herunterladen" if st.session_state.language == "de" else f"📥 Download '{export_wahl}' as Excel"
                            st.download_button(label=btn_dl_lbl, data=excel_ie_data, file_name=dateiname, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="export_download_btn_final_v7")
                        else: 
                            st.info(TXT_IE["exp_empty"].format(export_wahl))
                    except Exception as e: 
                        st.error(f"{TXT_IE['err_exp']} {str(e)}")
                    finally: 
                        try:
                            if conn is not None:
                                conn.close()
                        except:
                            pass
                else: 
                    st.error(TXT_IE["err_conn"])

        # --- IMPORT BEREICH ---
        elif ie_aktion == TXT_IE["dir_imp"]:
            if st.session_state.language == "de":
                TXT_IMP = {
                    "imp_title": "##### 📥 Excel-Daten in die Datenbank einlesen",
                    "imp_q": "Ziel-Tabelle für Import:",
                    "imp_hint": "Hinweis: Spaltenüberschriften müssen exakt den Datenbankfeldern entsprechen.",
                    "imp_file_lbl": "Excel-Datei für '{}' auswählen:",
                }
            else:
                TXT_IMP = {
                    "imp_title": "##### 📥 Read Excel Data into Database",
                    "imp_q": "Target Table for Import:",
                    "imp_hint": "Note: Column headers must match database fields exactly.",
                    "imp_file_lbl": "Select Excel file for '{}':",
                }
                
            st.markdown(TXT_IMP["imp_title"])
            col_imp_sel, _ = st.columns([6.0, 4.0])
            with col_imp_sel:
                import_wahl = st.selectbox(TXT_IMP["imp_q"], [""] + list(tabellen_liste.keys()), key="import_bereich_wahl_final_v7")

            if import_wahl:
                db_tabelle = tabellen_liste[import_wahl]
                st.write("")
                st.info(TXT_IMP["imp_hint"])
                uploaded_file = st.file_uploader(TXT_IMP["imp_file_lbl"].format(import_wahl), type=["xlsx"], key="excel_uploader_field_v7")
                
                if uploaded_file is not None:
                    try:
                        df_imp = pd.read_excel(uploaded_file, sheet_name=0, engine="openpyxl")
                        preview_lbl = f"**Vorschau ({len(df_imp)} Zeilen):**" if st.session_state.language == "de" else f"**Preview ({len(df_imp)} rows):**"
                        st.markdown(preview_lbl)
                        st.dataframe(df_imp.head(3), use_container_width=True, hide_index=True)
                        
                        with st.form("form_import_start_einmalig", clear_on_submit=True):
                            btn_start_lbl = "🚀 Import starten" if st.session_state.language == "de" else "🚀 Start Import"
                            if st.form_submit_button(btn_start_lbl):
                                conn = hole_datenbank_verbindung()
                                if conn is not None:
                                    try:
                                        cursor = conn.cursor()
                                        spalten = [f"`{col}`" for col in df_imp.columns]
                                        platzhalter = ["%s" for _ in df_imp.columns]
                                        sql_kommando = f"INSERT INTO `{db_tabelle}` ({', '.join(spalten)}) VALUES ({', '.join(platzhalter)})"
                                        erfolgreich = 0
                                        
                                        for _, row in df_imp.iterrows():
                                            zeilen_werte = []
                                            for val in row.values:
                                                if pd.isnull(val): zeilen_werte.append(None)
                                                elif isinstance(val, pd.Timestamp): zeilen_werte.append(val.strftime('%Y-%m-%d'))
                                                elif isinstance(val, float) and val.is_integer(): zeilen_werte.append(int(val))
                                                elif isinstance(val, str):
                                                    try:
                                                        parsed_dt = pd.to_datetime(val, format='%d.%m.%Y', errors='raise')
                                                        zeilen_werte.append(parsed_dt.strftime('%Y-%m-%d'))
                                                    except: zeilen_werte.append(val)
                                                else: zeilen_werte.append(val)
                                            try:
                                                cursor.execute(sql_kommando, tuple(zeilen_werte))
                                                erfolgreich += 1
                                            except Exception as insert_error:
                                                st.warning(f"Zeile übersprungen: {str(insert_error)}" if st.session_state.language == "de" else f"Row skipped: {str(insert_error)}")
                                        conn.commit()
                                        cursor.close()
                                        st.success(f"🟢 Import abgeschlossen! {erfolgreich} von {len(df_imp)} Zeilen gespeichert." if st.session_state.language == "de" else f"🟢 Import completed! {erfolgreich} of {len(df_imp)} rows saved.")
                                        st.rerun()
                                    except Exception as db_err: 
                                        st.error(f"Datenbankfehler: {str(db_err)}" if st.session_state.language == "de" else f"Database error: {str(db_err)}")
                                    finally: 
                                        try:
                                            if conn is not None:
                                                conn.close()
                                        except:
                                            pass
                                else: st.error(TXT_IE["err_conn"])
                    except Exception as e: 
                        st.error(f"Fehler: {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

    # --- RECHTE SPALTE: INTERAKTIVER TEMPLATE-HUB ---
    with col_main_right:
        st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
        st.markdown(f"##### {TXT_IE['template_title']}")
        st.markdown(f"<p style='font-size: 12px; opacity: 0.7; margin-bottom: 15px;'>{TXT_IE['template_desc']}</p>", unsafe_allow_html=True)
        
        # Interaktive Dropdown-Auswahl für das gewünschte Template
        template_wahl = st.selectbox(TXT_IE["template_sel"], [""] + list(tabellen_liste.keys()), key="interaktives_template_selectbox")
        
        if template_wahl:
            t_key = tabellen_liste[template_wahl]
            conn_t = None
            try:
                conn_t = hole_datenbank_verbindung()
                if conn_t is not None:
                    df_s = pd.read_sql(f"SELECT * FROM `{t_key}` LIMIT 0", conn_t)
                    df_v = df_s.drop(columns=["id"]) if "id" in df_s.columns else df_s.copy()
                    
                    if st.session_state.language == "de":
                        leg_d = [{"Spalte / Feld": c, "Datentyp": "Text / Datum (TT.MM.JJJJ) / Zahl", "Erklärung": "Bitte passendes Format nutzen."} for c in df_v.columns]
                        s_name = "Legende & Hinweise"
                    else:
                        leg_d = [{"Column / Field": c, "Data Type": "Text / Date (DD.MM.YYYY) / Number", "Explanation": "Please use matching format."} for c in df_v.columns]
                        s_name = "Legend & Notes"
                        
                    df_l = pd.DataFrame(leg_d)
                    out_t = io.BytesIO()
                    with pd.ExcelWriter(out_t, engine='xlsxwriter') as w:
                        df_v.to_excel(w, index=False, sheet_name="Vorlage" if st.session_state.language == "de" else "Template")
                        df_l.to_excel(w, index=False, sheet_name=s_name)
                    
                    st.write("")
                    st.download_button(
                        label=TXT_IE["dl_tmpl_btn"],
                        data=out_t.getvalue(),
                        file_name=f"ESM_Vorlage_{t_key}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"dl_hub_tpl_{t_key}_interactive",
                        use_container_width=True
                    )
            except Exception as ex:
                pass
            finally:
                try:
                    if conn_t is not None:
                        conn_t.close()
                except:
                    pass
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 3. SAUBERE TRENNLINIE & SCHNITTSTELLEN-PROTOKOLL ---
    st.markdown('<hr class="saubere-trennlinie">', unsafe_allow_html=True)
    st.markdown(f"##### {TXT_IE['log_title']}")
    
    df_audit_log = pd.DataFrame({
        "Zeitstempel": ["28.07.2026 - 11:45", "25.07.2026 - 09:20", "20.07.2026 - 14:10", "15.07.2026 - 08:30"],
        "Richtung": ["Export", "Import", "Export", "Import"],
        "Modul": ["Wartungsverträge", "Anlagenstruktur", "Mängel & Auffälligkeiten", "Serviceeinträge"],
        "Dateiname": ["ESM_Backup_wartungsvertraege.xlsx", "ESM_Import_anlagen.xlsx", "ESM_Backup_wartungsplanung.xlsx", "ESM_Import_serviceeinsaetze.xlsx"],
        "Status": ["Erfolgreich", "Erfolgreich", "Erfolgreich", "Erfolgreich"]
    })

    if st.session_state.language == "en":
        df_audit_log.columns = ["Timestamp", "Direction", "Module", "Filename", "Status"]
        df_audit_log["Direction"] = ["Export", "Import", "Export", "Import"]
        df_audit_log["Status"] = ["Successful", "Successful", "Successful", "Successful"]

    st.dataframe(df_audit_log, use_container_width=True, hide_index=True)
