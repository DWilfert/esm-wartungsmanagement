import streamlit as st
import pandas as pd
from datetime import datetime
from datenbank.befehle import hole_datenbank_verbindung

def formatiere_datum(wert):
    if pd.isna(wert) or not wert:
        return "-"
    try:
        s_val = str(wert).strip()
        if len(s_val) >= 10 and '-' in s_val[:10]:
            parts = s_val[:10].split('-')
            if len(parts) == 3:
                jahr, monat, tag = parts
                return f"{tag}.{monat}.{jahr}"
        if hasattr(wert, 'strftime'):
            return wert.strftime('%d.%m.%Y')
    except Exception:
        pass
    return str(wert)

def zeige_globale_suche():
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
        TXT_GS = {
            "title": "🔍 Globale 360° Volltextsuche",
            "desc": "Durchsuchen Sie das gesamte ESM Wartungsmanagement in Echtzeit (Anlagen, Verträge, Serviceeinsätze, Firmen & Mängel).",
            "placeholder": "Suchbegriff oder Anlagen-ID eingeben (z.B. 12, Aufzug, Siemens, Raum U05)...",
            "res_anlagen": "🏫 Treffer bei Anlagen & Gebäuden",
            "res_vertraege": "📑 Treffer bei Verträgen & Firmen",
            "res_service": "🛠️ Treffer bei Service-Historie",
            "res_auffaelligkeiten": "⚠️ Treffer bei Mängeln & Auffälligkeiten",
            "no_results": "Keine Treffer im System gefunden für:",
            "prompt_start": "👆 Bitte geben Sie einen Suchbegriff ein, um das System zu durchforsten."
        }
    else:
        TXT_GS = {
            "title": "🔍 Global 360° Full-Text Search",
            "desc": "Search across the entire ESM maintenance management system in real-time (assets, contracts, service history, companies & defects).",
            "placeholder": "Enter search term or asset ID (e.g. 12, elevator, Siemens, Room U05)...",
            "res_anlagen": "🏫 Matching Assets & Buildings",
            "res_vertraege": "📑 Matching Contracts & Companies",
            "res_service": "🛠️ Matching Service History",
            "res_auffaelligkeiten": "⚠️ Matching Defects & Discrepancies",
            "no_results": "No results found in the system for:",
            "prompt_start": "👆 Please enter a search term to scan the system."
        }

    st.subheader(TXT_GS["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 15px;'>{TXT_GS['desc']}</div>", unsafe_allow_html=True)

    col_suche, _ = st.columns([5.0, 5.0])
    with col_suche:
        suchbegriff = st.text_input("", placeholder=TXT_GS["placeholder"], label_visibility="collapsed", key="globaler_such_input")

    st.markdown("---")

    if not suchbegriff.strip():
        st.info(TXT_GS["prompt_start"])
        return

    such_pattern = f"%{suchbegriff.strip()}%"
    
    try:
        such_id = int(suchbegriff.strip())
    except ValueError:
        such_id = -1

    conn = hole_datenbank_verbindung()
    if conn is None:
        st.error("Datenbankverbindung fehlgeschlagen!")
        return

    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, bezeichnung, standort, anlagentyp, zustand, hersteller, raum 
            FROM anlagen 
            WHERE id = %s OR bezeichnung LIKE %s OR standort LIKE %s OR anlagentyp LIKE %s OR hersteller LIKE %s OR raum LIKE %s
        """, (such_id, such_pattern, such_pattern, such_pattern, such_pattern, such_pattern))
        res_anlagen = cursor.fetchall()

        cursor.execute("""
            SELECT id, bezeichnung, firma, naechstewartung, kostenpa 
            FROM wartungsvertraege 
            WHERE id = %s OR bezeichnung LIKE %s OR firma LIKE %s
        """, (such_id, such_pattern, such_pattern))
        res_vertraege = cursor.fetchall()

        try:
            cursor.execute("""
                SELECT id, kurz, gesetzliche_grundlage, qualifikation 
                FROM serviceeinsaetze 
                WHERE id = %s OR kurz LIKE %s OR gesetzliche_grundlage LIKE %s OR qualifikation LIKE %s
            """, (such_id, such_pattern, such_pattern, such_pattern))
            res_service = cursor.fetchall()
        except Exception:
            res_service = []

        try:
            cursor.execute("""
                SELECT id, bezeichnung, bemerkung, firma, protokoll 
                FROM wartungsplanung 
                WHERE id = %s OR bezeichnung LIKE %s OR bemerkung LIKE %s OR firma LIKE %s OR protokoll LIKE %s
            """, (such_id, such_pattern, such_pattern, such_pattern, such_pattern))
            res_auffaelligkeiten = cursor.fetchall()
        except Exception:
            res_auffaelligkeiten = []

        cursor.close()
    except Exception as e:
        st.error(f"Fehler bei der Suche: {str(e)}")
        res_anlagen, res_vertraege, res_service, res_auffaelligkeiten = [], [], [], []
    finally:
        conn.close()

    gesamt_treffer = len(res_anlagen) + len(res_vertraege) + len(res_service) + len(res_auffaelligkeiten)

    if gesamt_treffer == 0:
        st.warning(f"{TXT_GS['no_results']} **'{suchbegriff}'**")
        return

    st.success(f"🎉 **{gesamt_treffer} Treffer** für **'{suchbegriff}'** im System gefunden:")
    st.write("")

    if res_anlagen:
        st.markdown(f"##### {TXT_GS['res_anlagen']} ({len(res_anlagen)})")
        df_a = pd.DataFrame(res_anlagen).rename(columns={
            'id': 'ID', 'bezeichnung': 'Anlage', 'standort': 'Standort', 
            'anlagentyp': 'Typ', 'zustand': 'Zustand', 'hersteller': 'Hersteller', 'raum': 'Raum'
        })
        st.dataframe(df_a, use_container_width=True, hide_index=True)

    if res_vertraege:
        st.markdown(f"##### {TXT_GS['res_vertraege']} ({len(res_vertraege)})")
        df_v = pd.DataFrame(res_vertraege)
        if 'naechstewartung' in df_v.columns:
            df_v['naechstewartung'] = df_v['naechstewartung'].apply(formatiere_datum)
            
        df_v = df_v.rename(columns={
            'id': 'ID', 'bezeichnung': 'Vertrag', 'firma': 'Firma', 
            'naechstewartung': 'Nächste Wartung', 'kostenpa': 'Kosten (€)'
        })
        st.dataframe(df_v, use_container_width=True, hide_index=True)

    if res_service:
        st.markdown(f"##### {TXT_GS['res_service']} ({len(res_service)})")
        df_s = pd.DataFrame(res_service).rename(columns={
            'id': 'ID', 'kurz': 'Maßnahme', 
            'gesetzliche_grundlage': 'Rechtsgrundlage', 'qualifikation': 'Qualifikation'
        })
        st.dataframe(df_s, use_container_width=True, hide_index=True)

    if res_auffaelligkeiten:
        st.markdown(f"##### {TXT_GS['res_auffaelligkeiten']} ({len(res_auffaelligkeiten)})")
        df_af = pd.DataFrame(res_auffaelligkeiten).rename(columns={
            'id': 'ID', 'bezeichnung': 'Mangel / Vorfall', 'bemerkung': 'Bemerkung', 
            'firma': 'Firma', 'protokoll': 'Protokoll-Nr.'
        })
        st.dataframe(df_af, use_container_width=True, hide_index=True)
