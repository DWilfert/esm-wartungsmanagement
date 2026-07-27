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

    st.subheader("📂 Zentrales Vertragsarchiv" if st.session_state.language == "de" else "📂 Central Contract Archive")
    
    config_pfad = st.session_state.get("admin_doc_path_config", "C:/esm_dokumente")
    
    # Automatische Erkennung: Wenn der Pfad lokal nicht existiert, sind wir in der Cloud-Onlineversion
    is_cloud_mode = not os.path.exists(config_pfad)
    doc_pfad = config_pfad if not is_cloud_mode else "demo_archiv_simuliert"
    win_path = os.path.normpath(config_pfad)

    if is_cloud_mode:
        st.markdown(
            f"<div style='font-size: 11.5px; color: #38bdf8; background: rgba(56, 189, 248, 0.1); padding: 10px 14px; border-radius: 6px; margin-bottom: 15px; border: 1px solid rgba(56, 189, 248, 0.3);'>"
            f"ℹ️ <b>Hinweis zur Online-Version (Cloud):</b> Aus rechtlichen und sicherheitstechnischen Gründen (Browser-Richtlinien in der Cloud) "
            f"ist die direkte PDF-Vorschau im Formular hier deaktiviert. Sobald die Anwendung auf dem lokalen Schulserver (Intranet) "
            f"unter <code>{config_pfad}</code> läuft, öffnet sich die echte Dokumenten-Vorschau hier wieder vollautomatisch wie auf deinem lokalen PC."
            f"</div>",
            unsafe_allow_html=True
        )

    btn_ordner_lbl = "📂 Vertragsordner im System-Explorer öffnen" if st.session_state.language == "de" else "📂 Open Contract Folder in System Explorer"
    col_btn, _ = st.columns([4.0, 6.0])
    with col_btn:
        if st.button(btn_ordner_lbl, key="btn_open_dynamic_explorer_v18", use_container_width=True):
            if not is_cloud_mode:
                try:
                    subprocess.Popen(f'powershell -command "Start-Process explorer -ArgumentList \'{win_path}\'"')
                    st.success("Ordner geöffnet!" if st.session_state.language == "de" else "Folder opened!")
                except Exception as e_explorer:
                    st.error(f"Fehler beim Öffnen: {str(e_explorer)}" if st.session_state.language == "de" else f"Error opening: {str(e_explorer)}")
            else:
                st.info("📂 Im späteren Intranet-Betrieb öffnet dieser Button den echten Netzlaufwerk-Ordner.")

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
        st.info("Keine PDF-Dateien gefunden.")
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
        lbl_select = "💡 Tipp: Klicke links auf das kleine Quadrat einer Zeile, um das Dokument auszuwählen."
    else:
        lbl_file, lbl_contract, lbl_id = "File Name (PDF)", "Assigned Maintenance Contract", "Contract ID"
        lbl_select = "💡 Tip: Click the small checkbox on the left of any row to select the document."
        
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
        
        st.write("")
        preview_title = f"##### 👁️ Dokumenten-Ansicht: {gewaehlte_datei}" if st.session_state.language == "de" else f"##### 👁️ Document View: {gewaehlte_datei}"
        st.markdown(preview_title)
        
        vollständiger_pfad = os.path.join(doc_pfad, gewaehlte_datei) if not is_cloud_mode else None
        
        # WENN AUF DEM SCHULSERVER (Intranet-Modus): Echte Formular-Vorschau per IFrame laden
        if not is_cloud_mode and os.path.exists(vollständiger_pfad):
            try:
                with open(vollständiger_pfad, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="650px" type="application/pdf" style="border-radius: 8px; border: 1px solid rgba(128,128,128,0.3);"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            except Exception as e_pdf:
                st.error(f"Fehler beim Laden: {str(e_pdf)}")
        
        # WENN IN DER ONLINE-VERSION (Cloud-Modus): Rechtlicher/Sicherheits-Hinweis statt blockiertem IFrame
        else:
            st.markdown(f"""
                <div class="doc-preview-card">
                    <div style="font-size: 13px; font-weight: bold; color: var(--primary-color); margin-bottom: 8px;">
                        📄 Ausgewähltes Dokument: {gewaehlte_datei}
                    </div>
                    <div style="font-size: 12px; line-height: 1.6; opacity: 0.85;">
                        Die direkte Einbettung von lokalen PDFs im Browser ist in der öffentlichen Online-Version aus Sicherheits- und Datenschutzgründen gesperrt.<br>
                        <b>Sobald die App auf den internen Schulserver umzieht, wird das PDF hier direkt im Formular angezeigt.</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)
