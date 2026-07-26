import streamlit as st
import pandas as pd
import base64
import os
import subprocess
from datenbank.befehle import hole_datenbank_verbindung

def zeige_vertragsdokumente():
    # Einheitlicher Design- & Helligkeits-Fix (angepasst für Light- und Dark-Mode)
    st.markdown("""
        <style>
        /* Kompakte Schriftgröße in allen Eingabefeldern und Formularen */
        input, select, textarea, div[data-baseweb="select"] span, label {
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
        
        ul[role="listbox"] li:hover,
        ul[role="listbox"] li[aria-selected="true"],
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

        /* Automatischer Hintergrund- und Rahmen-Fix für st.dataframe (verhindert den weißen Kasten im Dark-Mode) */
        div[data-testid="stDataFrame"] {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("📂 Zentrales Vertragsarchiv" if st.session_state.language == "de" else "📂 Central Contract Archive")
    
    doc_pfad = st.session_state.get("admin_doc_path_config", "C:/esm_dokumente")
    win_path = os.path.normpath(doc_pfad)
    
    if not doc_pfad or not os.path.exists(doc_pfad):
        err_path_msg = (
            f"🔴 Der konfigurierte Archiv-Pfad '{doc_pfad}' ist aktuell nicht erreichbar. Bitte prüfe die Pfad-Einstellung im Adminbereich!" 
            if st.session_state.language == "de" 
            else f"🔴 The configured archive path '{doc_pfad}' is unreachable. Please check the path setting in the admin area!"
        )
        st.error(err_path_msg)
        return

    btn_ordner_lbl = "📂 Vertragsordner im System-Explorer öffnen" if st.session_state.language == "de" else "📂 Open Contract Folder in System Explorer"
    col_btn, _ = st.columns([4.0, 6.0])
    with col_btn:
        if st.button(btn_ordner_lbl, key="btn_open_dynamic_explorer_v17", use_container_width=True):
            try:
                # Öffnet den Explorer garantiert im Vordergrund und mit Fokus
                subprocess.Popen(f'powershell -command "Start-Process explorer -ArgumentList \'{win_path}\'"')
                success_open = "Ordner geöffnet!" if st.session_state.language == "de" else "Folder opened!"
                st.success(success_open)
            except Exception as e_explorer:
                err_open_msg = f"Fehler beim Öffnen: {str(e_explorer)}" if st.session_state.language == "de" else f"Error opening: {str(e_explorer)}"
                st.error(err_open_msg)

    st.write("---")
    vertrag_dict = {}
    conn = hole_datenbank_verbindung()
    if conn is not None:
        try:
            df_v = pd.read_sql("SELECT id, bezeichnung FROM `wartungsvertraege`", conn)
            vertrag_dict = dict(zip(df_v["id"], df_v["bezeichnung"]))
        except: 
            pass
        finally: 
            conn.close()
        
    try:
        alle_dateien = os.listdir(doc_pfad)
        pdf_dateien = [f for f in alle_dateien if f.lower().endswith('.pdf')]
    except Exception as e_dir:
        pdf_dateien = []
        err_dir_msg = f"Fehler: {str(e_dir)}" if st.session_state.language == "de" else f"Error: {str(e_dir)}"
        st.error(err_dir_msg)
    
    if not pdf_dateien:
        no_pdf_msg = (
            f"ℹ️ Der Dokumenten-Ordner '{doc_pfad}' enthält aktuell keine PDF-Dateien." 
            if st.session_state.language == "de" 
            else f"ℹ️ The document folder '{doc_pfad}' currently contains no PDF files."
        )
        st.info(no_pdf_msg)
        return

    dir_content_lbl = (
        f"##### 📋 Verzeichnis-Inhalt ({len(pdf_dateien)} PDFs):" 
        if st.session_state.language == "de" 
        else f"##### 📋 Directory Content ({len(pdf_dateien)} PDFs):"
    )
    st.markdown(dir_content_lbl)
    
    tabelle_daten = []
    for pdf in pdf_dateien:
        id_extrakt = "".join(filter(str.isdigit, pdf))
        v_id = int(id_extrakt) if id_extrakt else None
        
        if st.session_state.language == "de":
            v_klarname = vertrag_dict.get(v_id, "Unbekannter Vertrag / Unassigned") if v_id else "Keine ID im Dateinamen / No ID"
        else:
            v_klarname = vertrag_dict.get(v_id, "Unknown Contract / Unassigned") if v_id else "No ID in file name / No ID"
        
        tabelle_daten.append({
            "Dateiname": pdf,
            "Zugeordneter Vertrag": v_klarname,
            "Vertrag ID": v_id if v_id else "-"
        })
        
    df_docs = pd.DataFrame(tabelle_daten)
    
    if st.session_state.language == "de":
        lbl_file, lbl_contract, lbl_id = "Dateiname (PDF)", "Zugeordneter Wartungsvertrag", "Vertrag ID"
        lbl_select = "💡 Tipp: Klicke links auf das kleine Quadrat einer Zeile, um das PDF direkt hier anzuzeigen!"
    else:
        lbl_file, lbl_contract, lbl_id = "File Name (PDF)", "Assigned Maintenance Contract", "Contract ID"
        lbl_select = "💡 Tip: Click the small checkbox on the left of any row to view the PDF directly below!"
        
    df_docs.columns = [lbl_file, lbl_contract, lbl_id]

    st.caption(lbl_select)
    auswahl_tabelle = st.dataframe(
        df_docs,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            lbl_id: st.column_config.TextColumn(lbl_id, alignment="left")
        }
    )
    
    if auswahl_tabelle and auswahl_tabelle.selection and "rows" in auswahl_tabelle.selection and auswahl_tabelle.selection["rows"]:
        reiner_index = auswahl_tabelle.selection["rows"][0]
        gewaehlte_datei = pdf_dateien[reiner_index]
        vollstaendiger_pfad = os.path.join(doc_pfad, gewaehlte_datei)
        
        try:
            with open(vollstaendiger_pfad, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" style="border: 1px solid #232d42; border-radius: 8px;"></iframe>'
            st.write("")
            preview_title = f"##### 👁️ Dokumenten-Vorschau: {gewaehlte_datei}" if st.session_state.language == "de" else f"##### 👁️ Document Preview: {gewaehlte_datei}"
            st.markdown(preview_title)
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e_view:
            err_view_msg = f"Fehler beim Laden der Vorschau: {str(e_view)}" if st.session_state.language == "de" else f"Error loading preview: {str(e_view)}"
            st.error(err_view_msg)