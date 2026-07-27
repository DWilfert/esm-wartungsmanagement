import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

def zeige_anlagen_history():
    # Enterprise Premium CSS für saubere Container, Karten und Typografie
    st.markdown("""
        <style>
        input, select, textarea, div[data-baseweb="select"] span, label, .stRadio div {
            font-size: 0.82rem !important;
        }
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        div[data-testid="stDataFrame"] {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }
        .enterprise-card {
            background-color: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 0.5rem;
            padding: 15px;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.language == "de":
        TXT_AH = {
            "title": "🔄 360° Anlagen-Historie & Logbuch",
            "desc": "Chronologische Enterprise-Ansicht: Alle Stammdaten, Verträge, Historien und Prüfberichte im Überblick.",
            "select_lbl": "Anlage auswählen (Alphabetisch):",
            "sec_stammdaten": "📋 Stammdaten & Standort-Profil",
            "sec_vertraege": "📑 Zuständige Verträge & Firmen",
            "sec_historie": "🛠️ Anlagen-Historie (Wartungen & Einsätze seit Installation)",
            "sec_auffaelligkeiten": "⚠️ Mängel & Auffälligkeiten",
            "btn_pdf": "📄 Offiziellen 360° Anlagen-Report als PDF erstellen",
            "no_selection": "👈 Bitte wählen Sie oben in der Auswahlliste eine Anlage aus, um das 360° Dashboard zu laden."
        }
    else:
        TXT_AH = {
            "title": "🔄 360° Asset History & Logbook",
            "desc": "Chronological Enterprise view: All master data, contracts, histories, and inspection reports at a glance.",
            "select_lbl": "Select Asset (Alphabetical):",
            "sec_stammdaten": "📋 Master Data & Location Profile",
            "sec_vertraege": "📑 Assigned Contracts & Companies",
            "sec_historie": "🛠️ Asset History (Maintenance & Service since installation)",
            "sec_auffaelligkeiten": "⚠️ Defects & Discrepancies",
            "btn_pdf": "📄 Generate Official 360° Asset Report as PDF",
            "no_selection": "👈 Please select an asset from the list above to load the 360° dashboard."
        }

    st.subheader(TXT_AH["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 15px;'>{TXT_AH['desc']}</div>", unsafe_allow_html=True)

    # Sofortige lokale Demo-Anlagen bereitstellen
    df_anlagen = pd.DataFrame({
        "id": [17501 + i for i in range(10)],
        "bezeichnung": [f"Personenaufzug Objekt {i+1}" if i % 2 == 0 else f"Lüftungsanlage Gebäude {i+1}" for i in range(10)],
        "standort": ["NP" if i % 2 == 0 else "FG" for i in range(10)],
        "anlagentyp": ["Fördertechnik" if i % 2 == 0 else "Raumlufttechnik" for i in range(10)],
        "hersteller": ["Otis GmbH", "Schindler AG", "Stulz GmbH", "Siemens AG", "Viessmann Werke"] * 2,
        "baujahr": [2018 + (i % 5) for i in range(10)],
        "raum": [f"R-{100+i}" for i in range(10)],
        "din276": ["460 - Förderanlagen" if i % 2 == 0 else "430 - Raumlufttechnische Anlagen" for i in range(10)],
        "zustand": ["Betriebsbereit", "Wartung überfällig", "Prüfung anstehend", "Betriebsbereit", "Betriebsbereit"] * 2
    })

    anlagen_optionen = [f"[ID: {row['id']}] {row['bezeichnung']} ({row['standort']})" for _, row in df_anlagen.iterrows()]
    
    col_sel, _ = st.columns([6.0, 4.0])
    with col_sel:
        auswahl = st.selectbox(TXT_AH["select_lbl"], [""] + anlagen_optionen, key="history_anlagen_select")

    st.markdown("---")

    if not auswahl:
        st.info(TXT_AH["no_selection"])
        return

    try:
        anl_id_str = auswahl.split("[ID:")[1].split("]")[0].strip()
        wa_anlagen_id = int(anl_id_str)
    except:
        return

    # Details aus Demo-Daten filtern
    matched_row = df_anlagen[df_anlagen["id"] == wa_anlagen_id]
    if matched_row.empty:
        st.warning("Keine Details zur Anlage gefunden.")
        return

    stammdaten = matched_row.iloc[0].to_dict()

    # Status-Ampel Logik
    zustand_text = str(stammdaten.get('zustand', '')).lower()
    if "überfällig" in zustand_text:
        ampel = "🔴 Fällig / Überfällig"
    elif "anstehend" in zustand_text or "prüfung" in zustand_text:
        ampel = "🟡 Warnung / Anstehend"
    else:
        ampel = "🟢 In Ordnung / Betriebsbereit"

    # --- 1. STAATSDATEN IM ENTERPRISE-CONTAINER ---
    st.markdown(f"##### {TXT_AH['sec_stammdaten']}")
    with st.container():
        st.markdown(f"""
        <div class="enterprise-card">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 0.85rem;">
                <div><b>Status-Ampel:</b><br>{ampel}</div>
                <div><b>Anlagen-ID:</b><br>{stammdaten.get('id')}</div>
                <div><b>Standort:</b><br>{stammdaten.get('standort')}</div>
                <div><b>Typ:</b><br>{stammdaten.get('anlagentyp', '-')}</div>
                <div><b>Zustand:</b><br>{stammdaten.get('zustand', '-')}</div>
                <div><b>Hersteller:</b><br>{stammdaten.get('hersteller', '-')}</div>
                <div><b>Baujahr:</b><br>{stammdaten.get('baujahr', '-')}</div>
                <div><b>Raum / DIN 276:</b><br>{stammdaten.get('raum', '-')} ({stammdaten.get('din276', '-')})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- 2. VERTRÄGE & FIRMEN ---
    st.markdown(f"##### {TXT_AH['sec_vertraege']}")
    df_v_clean = pd.DataFrame({
        'Vertrag / Leistung': [f"Vollwartungsvertrag für {stammdaten.get('bezeichnung')}"],
        'Ausführende Firma': [stammdaten.get('hersteller')],
        'Intervall': ["12 Monate"],
        'Nächste Wartung': [(datetime.now().date() + timedelta(days=15 if wa_anlagen_id % 2 == 0 else -10)).strftime('%d.%m.%Y')]
    })
    st.dataframe(df_v_clean, use_container_width=True, hide_index=True)

    # --- 3. HISTORIE / SERVICEEINSÄTZE ---
    st.markdown(f"##### {TXT_AH['sec_historie']}")
    df_s_clean = pd.DataFrame({
        'Maßnahme / Beschreibung': ["Jahreswartung & Filterwechsel", "Sicherheitsprüfung nach DIN"],
        'Rechtsgrundlage / Vorgabe': ["Herstellervorgabe / BetrSichV", "Prüfverordnung Bayern"],
        'Erforderliche Qualifikation': ["Servicetechniker HVAC", "Sachkundiger Prüfer"]
    })
    st.dataframe(df_s_clean, use_container_width=True, hide_index=True)

    # --- 4. MÄNGEL & AUFFÄLLIGKEITEN ---
    st.markdown(f"##### {TXT_AH['sec_auffaelligkeiten']}")
    if "überfällig" in zustand_text:
        df_a_clean = pd.DataFrame({
            'Mangel / Vorfall': ["Wartungsfrist überschritten"],
            'Details & Historie': ["Termin wurde vom Dienstleister mehrfach verschoben."],
            'Gemeldet durch Firma': [stammdaten.get('hersteller')],
            'Protokoll-Nr.': ["PR-2026-99"]
        })
        st.dataframe(df_a_clean, use_container_width=True, hide_index=True)
    else:
        st.success("Keine Mängel oder Auffälligkeiten für diese Anlage bekannt.")

    st.markdown("---")

    if st.button(TXT_AH["btn_pdf"]):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(30, 136, 229)
            pdf.cell(0, 10, "Europäische Schule München - 360 Grad Anlagenbericht" if st.session_state.language == "de" else "European School Munich - 360 Degree Asset Report", ln=True)
            pdf.line(10, 20, 200, 20)
            pdf.ln(10)

            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(40, 40, 40)
            pdf.cell(0, 8, f"Anlage: {stammdaten.get('bezeichnung')} (ID: {stammdaten.get('id')})", ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, f"Standort: {stammdaten.get('standort')} | Typ: {stammdaten.get('anlagentyp')} | Zustand: {stammdaten.get('zustand')}", ln=True)
            pdf.cell(0, 6, f"Hersteller: {stammdaten.get('hersteller', '-')} | Baujahr: {stammdaten.get('baujahr', '-')} | Raum: {stammdaten.get('raum', '-')}", ln=True)
            pdf.ln(6)

            pdf_output = pdf.output(dest='S')
            pdf_bytes = bytes(pdf_output) if isinstance(pdf_output, bytearray) else pdf_output

            st.download_button(
                label="📥 PDF Herunterladen (Klicken zum Speichern)",
                data=pdf_bytes,
                file_name=f"ESM_360_Anlage_{stammdaten.get('id')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Fehler bei der PDF-Erstellung: {str(e)}")
