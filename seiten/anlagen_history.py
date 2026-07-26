import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from datenbank.befehle import hole_datenbank_verbindung

def zeige_anlagen_history():
    # Kompaktes Design und gezielte Begrenzung der Dropdown-Breite auf ca. 60%
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
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.language == "de":
        TXT_AH = {
            "title": "🔄 360° Anlagen-Historie & Logbuch",
            "desc": "Chronologische Historie: Wer hat wann, wo und was an dieser Anlage gearbeitet.",
            "select_lbl": "Anlage auswählen (Alphabetisch):",
            "sec_stammdaten": "📋 Stammdaten & Standort",
            "sec_vertraege": "📑 Zuständige Verträge & Firmen",
            "sec_historie": "🛠️ Anlagen-Historie (Wartungen & Einsätze seit Installation)",
            "sec_auffaelligkeiten": "⚠️ Mängel & Auffälligkeiten",
            "btn_pdf": "📄 Offiziellen 360° Anlagen-Report als PDF erstellen",
            "no_selection": "👈 Bitte wählen Sie oben in der Auswahlliste eine Anlage aus, um die Historie einzusehen."
        }
    else:
        TXT_AH = {
            "title": "🔄 360° Asset History & Logbook",
            "desc": "Chronological history: Who worked on this asset, when, where, and what was done.",
            "select_lbl": "Select Asset (Alphabetical):",
            "sec_stammdaten": "📋 Master Data & Location",
            "sec_vertraege": "📑 Assigned Contracts & Companies",
            "sec_historie": "🛠️ Asset History (Maintenance & Service since installation)",
            "sec_auffaelligkeiten": "⚠️ Defects & Discrepancies",
            "btn_pdf": "📄 Generate Official 360° Asset Report as PDF",
            "no_selection": "👈 Please select an asset from the list above to view its history."
        }

    st.subheader(TXT_AH["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 15px;'>{TXT_AH['desc']}</div>", unsafe_allow_html=True)

    conn = hole_datenbank_verbindung()
    if conn is None:
        st.error("Datenbankfehler!")
        return

    try:
        df_anlagen = pd.read_sql("SELECT id, bezeichnung, standort, anlagentyp FROM `anlagen` ORDER BY bezeichnung ASC", conn)
    except Exception as e:
        st.error(f"Fehler beim Laden: {str(e)}")
        conn.close()
        return
    finally:
        conn.close()

    if df_anlagen.empty:
        st.info("Keine Anlagen in der Datenbank gefunden.")
        return

    anlagen_optionen = [f"[ID: {row['id']}] {row['bezeichnung']} ({row['standort']})" for _, row in df_anlagen.iterrows()]
    
    # Hier wird das Auswahlfeld auf ca. 60% Breite (40% schmaler) skaliert
    col_sel, col_empty = st.columns([6.0, 4.0])
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

    # Details aus der Datenbank holen
    conn = hole_datenbank_verbindung()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM `anlagen` WHERE id = %s", (wa_anlagen_id,))
            stammdaten = cursor.fetchone()
            
            cursor.execute("SELECT * FROM `wartungsvertraege` WHERE anlagenid = %s", (wa_anlagen_id,))
            vertraege = cursor.fetchall()
            
            cursor.execute("SELECT * FROM `serviceeinsaetze` WHERE anlagenid = %s", (wa_anlagen_id,))
            service_einsaetze = cursor.fetchall()
            
            cursor.execute("SELECT * FROM `wartungsplanung` WHERE bezeichnung LIKE %s", (f"%{stammdaten.get('bezeichnung', '')}%",))
            auffaelligkeiten = cursor.fetchall()
            cursor.close()
        except Exception as e:
            st.error(f"Fehler beim Abrufen der Details: {str(e)}")
            stammdaten, vertraege, service_einsaetze, auffaelligkeiten = None, [], [], []
        finally:
            conn.close()

    if not stammdaten:
        st.warning("Keine Details zur Anlage gefunden.")
        return

    # 1. Stammdaten
    st.markdown(f"##### {TXT_AH['sec_stammdaten']}")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"**Anlagen-ID:** {stammdaten.get('id')}")
    with c2: st.markdown(f"**Standort:** {stammdaten.get('standort')}")
    with c3: st.markdown(f"**Typ:** {stammdaten.get('anlagentyp', '-')}")
    with c4: st.markdown(f"**Zustand:** {stammdaten.get('zustand', '-')}")

    c5, c6, c7, c8 = st.columns(4)
    with c5: st.markdown(f"**Hersteller:** {stammdaten.get('hersteller', '-')}")
    with c6: st.markdown(f"**Baujahr:** {stammdaten.get('baujahr', '-')}")
    with c7: st.markdown(f"**Raum:** {stammdaten.get('raum', '-')}")
    with c8: st.markdown(f"**DIN 276:** {stammdaten.get('din276', '-')}")

    st.write("")

    # 2. Verträge & Firmen (Wer ist zuständig?)
    st.markdown(f"##### {TXT_AH['sec_vertraege']}")
    if vertraege:
        df_v = pd.DataFrame(vertraege)
        # Nur sinnvolle Spalten anzeigen (keine kryptischen IDs oder Benchmarks)
        saubere_v_spalten = [c for c in ['bezeichnung', 'firma', 'intervall', 'naechstewartung'] if c in df_v.columns]
        df_v_clean = df_v[saubere_v_spalten].rename(columns={
            'bezeichnung': 'Vertrag / Leistung',
            'firma': 'Ausführende Firma',
            'intervall': 'Intervall',
            'naechstewartung': 'Nächste Wartung'
        })
        st.dataframe(df_v_clean, use_container_width=True, hide_index=True)
    else:
        st.info("Keine Verträge an diese Anlage gebunden.")

    # 3. Historie / Serviceeinsaetze (Wer, was, wann, wo passiert ist)
    st.markdown(f"##### {TXT_AH['sec_historie']}")
    if service_einsaetze:
        df_s = pd.DataFrame(service_einsaetze)
        saubere_s_spalten = [c for c in ['kurz', 'gesetzliche_grundlage', 'qualifikation'] if c in df_s.columns]
        df_s_clean = df_s[saubere_s_spalten].rename(columns={
            'kurz': 'Maßnahme / Beschreibung',
            'gesetzliche_grundlage': 'Rechtsgrundlage / Vorgabe',
            'qualifikation': 'Erforderliche Qualifikation'
        })
        st.dataframe(df_s_clean, use_container_width=True, hide_index=True)
    else:
        st.info("Keine historischen Serviceeinsätze hinterlegt.")

    # 4. Mängel & Auffälligkeiten
    st.markdown(f"##### {TXT_AH['sec_auffaelligkeiten']}")
    if auffaelligkeiten:
        df_a = pd.DataFrame(auffaelligkeiten)
        saubere_a_spalten = [c for c in ['bezeichnung', 'bemerkung', 'firma', 'protokoll'] if c in df_a.columns]
        df_a_clean = df_a[saubere_a_spalten].rename(columns={
            'bezeichnung': 'Mangel / Vorfall',
            'bemerkung': 'Details & Historie',
            'firma': 'Gemeldet durch Firma',
            'protokoll': 'Protokoll-Nr.'
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