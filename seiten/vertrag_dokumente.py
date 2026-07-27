import streamlit as st
import pandas as pd
import os
import subprocess
import base64
from datenbank.befehle import hole_datenbank_verbindung

def zeige_vertragsdokumente():
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
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }

        .doc-preview-card {
            background-color: var(--secondary-background-color);
            border: 1px solid var(--primary-color);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            color: var(--text-color);
        }
        </style>
    """, unsafe_allow_html=True)

    if 'language' not in st.session_state:
        st.session_state.language = "de"

    if st.session_state.language == "de":
        TXT_VD = {
            "title": "📂 Zentrales Vertragsarchiv",
            "cloud_hint": "ℹ️ <b>Hinweis zur Online-Version (Cloud):</b> Aus rechtlichen und sicherheitstechnischen Gründen (Browser-Richtlinien in der Cloud) ist die direkte PDF-Vorschau im Formular hier deaktiviert. Sobald die Anwendung auf dem lokalen Schulserver (Intranet) unter <code>{path}</code> läuft, öffnet sich die echte Dokumenten-Vorschau hier wieder vollautomatisch wie auf deinem lokalen PC.",
            "btn_explorer": "📂 Vertragsordner im System-Explorer öffnen",
            "explorer_success": "Ordner geöffnet!",
            "explorer_err": "Fehler beim Öffnen:",
            "cloud_explorer_info": "📂 Im späteren Intranet-Betrieb öffnet dieser Button den echten Netzlaufwerk-Ordner.",
            "no_files": "Keine PDF-Dateien gefunden.",
            "dir_content": "##### 📋 Verzeichnis-Inhalt ({count} PDFs):",
            "col_file": "Dateiname (PDF)",
            "col_contract": "Zugeordneter Wartungsvertrag",
            "col_id": "Vertrag ID",
            "tip": "💡 Tipp: Klicke links auf das kleine Quadrat einer Zeile, um das Dokument auszuwählen.",
            "preview": "##### 👁️ Dokumenten-Ansicht: {file}",
            "cloud_preview_title": "📄 Ausgewähltes Dokument: {file}",
            "cloud_preview_text": "Die direkte Einbettung von lokalen PDFs im Browser ist in der öffentlichen Online-Version aus Sicherheits- und Datenschutzgründen gesperrt.<br><b>Sobald die App auf den internen Schulserver umzieht, wird das PDF hier direkt im Formular angezeigt.</b>"
        }
    else:
        TXT_VD = {
            "title": "📂 Central Contract Archive",
            "cloud_hint": "ℹ️ <b>Cloud Version Note:</b> Due to legal and security guidelines (browser policies in the cloud), direct PDF preview in the form is disabled here. As soon as the application runs on the local school server (intranet) under <code>{path}</code>, the real document preview will open automatically just like on your local PC.",
            "btn_explorer": "📂 Open Contract Folder in System Explorer",
            "explorer_success": "Folder opened!",
            "explorer_err": "Error opening:",
            "cloud_explorer_info": "📂 During intranet operation, this button opens the actual network drive folder.",
            "no_files": "No PDF files found.",
            "dir_content": "##### 📋 Directory Content ({count} PDFs):",
            "col_file": "File Name (PDF)",
            "col_contract": "Assigned Maintenance Contract",
            "col_id": "Contract ID",
            "tip": "💡 Tip: Click the small checkbox on the left of any row to select the document.",
            "preview": "##### 👁️ Document View: {file}",
            "cloud_preview_title": "📄 Selected Document: {file}",
            "cloud_preview_text": "Direct embedding of local PDFs in the browser is disabled in the public online version for security and privacy reasons.<br><b>As soon as the app moves to the internal school server, the PDF will be displayed directly in the form here.</b>"
        }

    st.subheader(TXT_VD["title"])
    
    config_pfad = st.session_state.get("admin_doc_path_config", "C:/esm_dokumente")
    
    is_cloud_mode = not os.path.exists(config_pfad)
    doc_pfad = config_pfad if not is_cloud_mode else "demo_archiv_simuliert"
    win_path = os.path.normpath(config_pfad)

    if is_cloud_mode:
        st.markdown(
            f"<div style='font-size: 11.5px; color: #38bdf8; background: rgba(56, 189, 248, 0.1); padding: 10px 14px; border-radius: 6px; margin-bottom: 15px; border: 1px solid rgba(56, 189, 248, 0.3);'>"
            f"{TXT_VD['cloud_hint'].format(path=config_pfad)}"
            f"</div>",
            unsafe_allow_html=True
        )

    col_btn, _ = st.columns([4.0, 6.0])
    with col_btn:
        if st.button(TXT_VD["btn_explorer"], key="btn_open_dynamic_explorer_v18", use_container_width=True):
            if not is_cloud_mode:
                try:
                    subprocess.Popen(f'powershell -command "Start-Process explorer -ArgumentList \'{win_path}\'"')
                    st.success(TXT_VD["explorer_success"])
                except Exception as e_explorer:
                    st.error(f"{TXT_VD['explorer_err']} {str(e_explorer)}")
            else:
                st.info(TXT_VD["cloud_explorer_info"])

    st.write("---")
    vertrag_dict = {}
    
    conn = None
    try:
        conn = hole_datenbank_verbindung()
        if conn is not None:
            df_v = pd.read_sql("SELECT id, bezeichnung FROM `wartungsvertraege`", conn)
            vertrag_dict = dict(zip(df_v["id"], df_v["bezeichnung"]))
    except Exception:
        pass
    finally:
        try:
            if conn is not None and hasattr(conn, "close"):
                conn.close()
        except Exception:
            pass
        
    if not is_cloud_mode:
        try:
            alle_dateien = os.listdir(doc_pfad)
            pdf_dateien = [f for f in alle_dateien if f.lower().endswith('.pdf')]
        except Exception:
            pdf_dateien = []
    else:
        pdf_dateien = [
            "Wartungsvertrag_ID17501_Personenaufzug_A.pdf",
            "Servicevertrag_ID17502_RLT_Anlage.pdf",
            "Wartungsvertrag_ID17503_Heizung_Viessmann.pdf",
            "Pruefvertrag_ID17504_Brandmeldeanlage.pdf",
            "Vollwartung_ID17506_Rollstuhlhebebuehne.pdf"
        ]
    
    if not pdf_dateien:
        st.info(TXT_VD["no_files"])
        return

    st.markdown(TXT_VD["dir_content"].format(count=len(pdf_dateien)))
    
    tabelle_daten = []
    for pdf in pdf_dateien:
        id_extrakt = "".join(filter(str.isdigit, pdf))
        v_id = int(id_extrakt) if id_extrakt else None
        
        if st.session_state.language == "de":
            v_klarname = vertrag_dict.get(v_id, "Unbekannter Vertrag / Unassigned") if v_id else "Keine ID im Dateinamen / No ID"
        else:
            v_klarname = vertrag_dict.get(v_id, "Unknown Contract / Unassigned") if v_id else "No ID in file name / No ID"
        
        tabelle_daten.append({
            TXT_VD["col_file"]: pdf,
            TXT_VD["col_contract"]: v_klarname,
            TXT_VD["col_id"]: v_id if v_id else "-"
        })
        
    df_docs = pd.DataFrame(tabelle_daten)

    st.caption(TXT_VD["tip"])
    auswahl_tabelle = st.dataframe(
        df_docs,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            TXT_VD["col_id"]: st.column_config.TextColumn(TXT_VD["col_id"], alignment="left")
        }
    )
    
    if auswahl_tabelle and auswahl_tabelle.selection and "rows" in auswahl_tabelle.selection and auswahl_tabelle.selection["rows"]:
        reiner_index = auswahl_tabelle.selection["rows"][0]
        gewaehlte_datei = pdf_dateien[reiner_index]
        
        st.write("")
        st.markdown(TXT_VD["preview"].format(file=gewaehlte_datei))
        
        vollständiger_pfad = os.path.join(doc_pfad, gewaehlte_datei) if not is_cloud_mode else None
        
        if not is_cloud_mode and os.path.exists(vollständiger_pfad):
            try:
                with open(vollständiger_pfad, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="650px" type="application/pdf" style="border-radius: 8px; border: 1px solid rgba(128,128,128,0.3);"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            except Exception as e_pdf:
                st.error(f"Fehler beim Laden: {str(e_pdf)}")
        else:
            st.markdown(f"""
                <div class="doc-preview-card">
                    <div style="font-size: 13px; font-weight: bold; color: var(--primary-color); margin-bottom: 8px;">
                        {TXT_VD['cloud_preview_title'].format(file=gewaehlte_datei)}
                    </div>
                    <div style="font-size: 12px; line-height: 1.6; opacity: 0.85;">
                        {TXT_VD['cloud_preview_text']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
