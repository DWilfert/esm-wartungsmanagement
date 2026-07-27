import streamlit as st
import pandas as pd
import os
import subprocess
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
        </style>
    """, unsafe_allow_html=True)

    st.subheader("📂 Zentrales Vertragsarchiv" if st.session_state.language == "de" else "📂 Central Contract Archive")
    
    config_pfad = st.session_state.get("admin_doc_path_config", "C:/esm_dokumente")
    
    is_cloud_mode = not os.path.exists(config_pfad)
    doc_pfad = config_pfad if not is_cloud_mode else "demo_archiv_simuliert"
    win_path = os.path.normpath(config_pfad)

    if is_cloud_mode:
        st.markdown(
            f"<div style='font-size: 11.5px; color: #38bdf8; background: rgba(56, 189, 248, 0.1); padding: 8px 12px; border-radius: 6px; margin-bottom: 12px; border: 1px solid rgba(56, 189, 248, 0.3);'>"
            f"ℹ️ <em>Cloud-Modus aktiv:</em> Netzlaufwerk-Pfad ('{config_pfad}') wird für die Demo sicher simuliert. Echte lokale Beispieldokumente stehen bereit."
            f"</div>" if st.session_state.language == "de" else
            f"<div style='font-size: 11.5px; color: #38bdf8; background: rgba(56, 189, 248, 0.1); padding: 8px 12px; border-radius: 6px; margin-bottom: 12px; border: 1px solid rgba(56, 189, 248, 0.3);'>"
            f"ℹ️ <em>Cloud Mode Active:</em> Network path ('{config_pfad}') is safely simulated for the demo. Local sample documents are ready."
            f"</div>",
            unsafe_allow_html=True
        )

    btn_ordner_lbl = "📂 Vertragsordner im System-Explorer öffnen" if st.session_state.language == "de" else "📂 Open Contract Folder in System Explorer"
    col_btn, _ = st.columns([4.0, 6.0])
    with col_btn:
        if st.button(btn_ordner_lbl, key="btn_open_dynamic_explorer_v17", use_container_width=True):
            if not is_cloud_mode:
                try:
                    subprocess.Popen(f'powershell -command "Start-Process explorer -ArgumentList \'{win_path}\'"')
                    st.success("Ordner geöffnet!" if st.session_state.language == "de" else "Folder opened!")
                except Exception as e_explorer:
                    st.error(f"Fehler beim Öffnen: {str(e_explorer)}" if st.session_state.language == "de" else f"Error opening: {str(e_explorer)}")
            else:
                st.info("📂 Simulierter Netzlaufwerk-Ordner aktiv." if st.session_state.language == "de" else "📂 Simulated network folder active.")

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
        except Exception as e_dir:
            pdf_dateien = []
            st.error(f"Fehler: {str(e_dir)}" if st.session_state.language == "de" else f"Error: {str(e_dir)}")
    else:
        pdf_dateien = [
            "Wartungsvertrag_ID17501_Personenaufzug_A.pdf",
            "Servicevertrag_ID17502_RLT_Anlage.pdf",
            "Wartungsvertrag_ID17503_Heizung_Viessmann.pdf",
            "Pruefvertrag_ID17504_Brandmeldeanlage.pdf",
            "Vollwartung_ID17506_Rollstuhlhebebuehne.pdf"
        ]
    
    if not pdf_dateien:
        no_pdf_msg = (
            f"ℹ️ Der Dokumenten-Pfad '{doc_pfad}' enthält aktuell keine PDF-Dateien." 
            if st.session_state.language == "de" 
            else f"ℹ️ The document path '{doc_pfad}' currently contains no PDF files."
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
        lbl_select = "💡 Tipp: Klicke links auf das kleine Quadrat einer Zeile, um das PDF direkt hier in der App zu betrachten!"
    else:
        lbl_file, lbl_contract, lbl_id = "File Name (PDF)", "Assigned Maintenance Contract", "Contract ID"
        lbl_select = "💡 Tip: Click the small checkbox on the left of any row to view the PDF directly here in the app!"
        
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
    
    if aus_wahl_check := (auswahl_tabelle and auswahl_tabelle.selection and "rows" in auswahl_tabelle.selection and auswahl_tabelle.selection["rows"]):
        reiner_index = auswahl_tabelle.selection["rows"][0]
        gewaehlte_datei = pdf_dateien[reiner_index]
        
        try:
            if not is_cloud_mode:
                vollstaendiger_pfad = os.path.join(doc_pfad, gewaehlte_datei)
                with open(vollstaendiger_pfad, "rb") as f:
                    pdf_bytes = f.read()
            else:
                pdf_bytes = b'%PDF-1.4 1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 595 842]/Parent 2 0 R/Resources<<>>/Contents 4 0 R>>endobj 4 0 obj<</Length 55>>stream\nBT /F1 18 Tf 50 750 Td (ESM Wartungsmanagement - DEMO VERTRAGSDOKUMENT) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000228 00000 n \ntrailer<</Size 5/Root 1 0 R>>\nstartstart\nstartxref\n338\n%%EOF'

            st.write("")
            preview_title = f"##### 👁️ Dokumenten-Vorschau: {gewaehlte_datei}" if st.session_state.language == "de" else f"##### 👁️ Document Preview: {gewaehlte_datei}"
            st.markdown(preview_title)
            
            # Verwendung der offiziellen, blockierungsfreien Streamlit-Komponente zur Anzeige von Dokumenten im Layout
            st.code(f"Dokumenten-Pfad: {os.path.abspath(os.path.join(doc_pfad, gewaehlte_datei)) if not is_cloud_mode else 'Virtuelles Netzlaufwerk (Cloud-Demo)'}", language="text")
            
            # Direkte Übergabe der Binärdaten an den nativen Streamlit-PDF-Viewer (ohne externe Fenster, ohne Download-Zwang)
            st.pdf(pdf_bytes, height=700)
            
        except Exception as e_view:
            err_view_msg = f"Fehler beim Laden der Vorschau: {str(e_view)}" if st.session_state.language == "de" else f"Error loading preview: {str(e_view)}"
            st.error(err_view_msg)
