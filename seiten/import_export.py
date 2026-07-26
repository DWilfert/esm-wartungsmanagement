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
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
            background-color: var(--secondary-background-color) !important;
        }
        
        ul[role="listbox"] li, li[role="option"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            font-size: 0.85rem !important;
        }
        
        /* Dezenter, dunkler Hover-Zustand passend zum Dark-Mode (verhindert den weißen Balken) */
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

        /* Automatischer Hintergrund- und Rahmen-Fix für st.dataframe */
        div[data-testid="stDataFrame"] {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.language == "de":
        TXT_IE = {
            "title": "Daten-Schnittstelle (Excel)",
            "direction_lbl": "Schnittstellen-Richtung wählen:",
            "dir_exp": "Daten exportieren (Backup)", "dir_imp": "Daten importieren (Upload)",
            "exp_title": "##### 📊 Tabellenauswahl für den Excel-Export",
            "exp_q": "Welche Daten möchtest du exportieren?", "err_conn": "Keine Verbindung zur Datenbank.",
            "exp_success": "Datensätze aus '{}' erfolgreich bereitgestellt.",
            "exp_empty": "Die Tabelle '{}' enthält aktuell keine Daten.", "err_exp": "Fehler beim Exportieren:"
        }
    else:
        TXT_IE = {
            "title": "Data Interface (Excel)",
            "direction_lbl": "Select Interface Direction:",
            "dir_exp": "Export Data (Backup)", "dir_imp": "Import Data (Upload)",
            "exp_title": "##### 📊 Table Selection for Excel Export",
            "exp_q": "Which data do you want to export?", "err_conn": "No database connection.",
            "exp_success": "Records from '{}' successfully provided.",
            "exp_empty": "The table '{}' currently contains no data.", "err_exp": "Error during export:"
        }

    st.subheader(TXT_IE["title"])
    ie_aktion = st.radio(TXT_IE["direction_lbl"], [TXT_IE["dir_exp"], TXT_IE["dir_imp"]], horizontal=True, key="ie_haupt_aktion_final_v7")
    
    tabellen_liste = {
        "Wartungsverträge" if st.session_state.language == "de" else "Maintenance Contracts": "wartungsvertraege",
        "Anlagenstruktur" if st.session_state.language == "de" else "Asset Structure": "anlagen",
        "Mängel & Auffälligkeiten" if st.session_state.language == "de" else "Defects & Observations": "wartungsplanung",
        "Serviceeinträge" if st.session_state.language == "de" else "Service Reports": "serviceeinsaetze"
    }

    # --- EXPORT BEREICH ---
    if ie_aktion == TXT_IE["dir_exp"]:
        st.markdown(TXT_IE["exp_title"])
        col_exp_sel, _ = st.columns([4.0, 6.0])
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
                        
                        btn_dl_lbl = f"📥 '{export_wahl}' als Excel-Datei herunterladen" if st.session_state.language == "de" else f"📥 Download '{export_wahl}' as Excel File"
                        st.download_button(label=btn_dl_lbl, data=excel_ie_data, file_name=dateiname, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="export_download_btn_final_v7")
                    else: 
                        st.info(TXT_IE["exp_empty"].format(export_wahl))
                except Exception as e: 
                    st.error(f"{TXT_IE['err_exp']} {str(e)}")
                finally: 
                    conn.close()
            else: 
                st.error(TXT_IE["err_conn"])

    # --- IMPORT BEREICH ---
    elif ie_aktion == TXT_IE["dir_imp"]:
        if st.session_state.language == "de":
            TXT_IMP = {
                "imp_title": "##### 📥 Excel-Daten in die Datenbank einlesen",
                "imp_q": "In welche Tabelle sollen die Daten importiert werden?",
                "imp_hint": "Hinweis: Die Spaltenüberschriften der Excel-Datei müssen exakt den Datenbankfeldern entsprechen. Nutze hierfür am besten die offizielle Vorlage.",
                "imp_file_lbl": "Excel-Datei für '{}' auswählen:",
                "btn_template": "📥 Leere Import-Vorlage mit Legende herunterladen"
            }
        else:
            TXT_IMP = {
                "imp_title": "##### 📥 Read Excel Data into Database",
                "imp_q": "Into which table should the data be imported?",
                "imp_hint": "Note: The column headers of the Excel file must exactly match the database fields. Use the official template for best results.",
                "imp_file_lbl": "Select Excel file for '{}':",
                "btn_template": "📥 Download Empty Import Template with Legend"
            }
            
        st.markdown(TXT_IMP["imp_title"])
        col_imp_sel, _ = st.columns([4.0, 6.0])
        with col_imp_sel:
            import_wahl = st.selectbox(TXT_IMP["imp_q"], [""] + list(tabellen_liste.keys()), key="import_bereich_wahl_final_v7")

        if import_wahl:
            db_tabelle = tabellen_liste[import_wahl]
            
            conn_v = hole_datenbank_verbindung()
            if conn_v is not None:
                try:
                    df_struktur = pd.read_sql(f"SELECT * FROM `{db_tabelle}` LIMIT 0", conn_v)
                    
                    if "id" in df_struktur.columns:
                        df_vorlage = df_struktur.drop(columns=["id"])
                    else:
                        df_vorlage = df_struktur.copy()
                        
                    if st.session_state.language == "de":
                        legenden_daten = [
                            {"Spalte / Feld": col, "Datentyp": "Text / Datum (TT.MM.JJJJ) / Zahl", "Erklärung & Erlaubte Werte": "Bitte entsprechendes Format eintragen. Pflichtfelder beachten."} 
                            for col in df_vorlage.columns
                        ]
                        sheet_name_legende = "Legende & Hinweise"
                    else:
                        legenden_daten = [
                            {"Column / Field": col, "Data Type": "Text / Date (DD.MM.YYYY) / Number", "Explanation & Allowed Values": "Please enter the appropriate format. Observe mandatory fields."} 
                            for col in df_vorlage.columns
                        ]
                        sheet_name_legende = "Legend & Notes"

                    df_legende = pd.DataFrame(legenden_daten)
                    
                    output_template = io.BytesIO()
                    with pd.ExcelWriter(output_template, engine='xlsxwriter') as writer:
                        df_vorlage.to_excel(writer, index=False, sheet_name="Import-Vorlage" if st.session_state.language == "de" else "Import Template")
                        df_legende.to_excel(writer, index=False, sheet_name=sheet_name_legende)
                        
                    template_data = output_template.getvalue()
                    template_filename = f"ESM_Import_Vorlage_{db_tabelle}.xlsx" if st.session_state.language == "de" else f"ESM_Import_Template_{db_tabelle}.xlsx"
                    
                    st.download_button(
                        label=TXT_IMP["btn_template"],
                        data=template_data,
                        file_name=template_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"dl_template_{db_tabelle}"
                    )
                except Exception as ex:
                    print(f"Template-Fehler: {ex}" if st.session_state.language == "de" else f"Template Error: {ex}")
                finally:
                    conn_v.close()

            st.write("")
            st.info(TXT_IMP["imp_hint"])
            uploaded_file = st.file_uploader(TXT_IMP["imp_file_lbl"].format(import_wahl), type=["xlsx"], key="excel_uploader_field_v7")
            
            if uploaded_file is not None:
                try:
                    df_imp = pd.read_excel(uploaded_file, sheet_name=0, engine="openpyxl")
                    
                    preview_lbl = f"**Vorschau der hochgeladenen Daten ({len(df_imp)} Zeilen):**" if st.session_state.language == "de" else f"**Preview of uploaded data ({len(df_imp)} rows):**"
                    st.markdown(preview_lbl)
                    st.dataframe(df_imp.head(3), use_container_width=True, hide_index=True)
                    
                    with st.form("form_import_start_einmalig", clear_on_submit=True):
                        btn_start_lbl = "🚀 Import in MySQL-Datenbank starten" if st.session_state.language == "de" else "🚀 Start Import into MySQL Database"
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
                                            warn_msg = f"Zeile übersprungen: {str(insert_error)}" if st.session_state.language == "de" else f"Row skipped: {str(insert_error)}"
                                            st.warning(warn_msg)
                                    conn.commit()
                                    cursor.close()
                                    success_msg = f"🟢 Import abgeschlossen! {erfolgreich} von {len(df_imp)} Zeilen erfolgreich gespeichert." if st.session_state.language == "de" else f"🟢 Import completed! {erfolgreich} of {len(df_imp)} rows successfully saved."
                                    st.success(success_msg)
                                    st.rerun()
                                except Exception as db_err: 
                                    err_msg = f"Datenbankfehler beim Import: {str(db_err)}" if st.session_state.language == "de" else f"Database error during import: {str(db_err)}"
                                    st.error(err_msg)
                                finally: conn.close()
                            else: st.error(TXT_IE["err_conn"])
                except Exception as e: 
                    err_proc = f"Fehler beim Verarbeiten der Excel-Datei: {str(e)}" if st.session_state.language == "de" else f"Error processing Excel file: {str(e)}"
                    st.error(err_proc)