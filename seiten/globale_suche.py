import streamlit as st
import pandas as pd
from datetime import datetime
from datenbank.befehle import hole_anlagen_daten, hole_wartungsvertraege_daten

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

    if st.session_state.get("language", "de") == "de":
        TXT_GS = {
            "title": "🔍 Globale 360° Volltextsuche",
            "desc": "Durchsuchen Sie das gesamte ESM Wartungsmanagement in Echtzeit (Anlagen, Verträge, Serviceeinsätze, Firmen & Mängel).",
            "placeholder": "Suchbegriff eingeben (z.B. Aufzug, Otis, Heizung, Lüftung)...",
            "res_anlagen": "🏫 Treffer bei Anlagen & Gebäuden",
            "res_vertraege": "📑 Treffer bei Verträgen & Firmen",
            "no_results": "Keine Treffer im System gefunden für:",
            "prompt_start": "👆 Bitte geben Sie einen Suchbegriff ein, um das System zu durchforsten."
        }
    else:
        TXT_GS = {
            "title": "🔍 Global 360° Full-Text Search",
            "desc": "Search across the entire ESM maintenance management system in real-time (assets, contracts, service history, companies & defects).",
            "placeholder": "Enter search term (e.g. elevator, Otis, heating)...",
            "res_anlagen": "🏫 Matching Assets & Buildings",
            "res_vertraege": "📑 Matching Contracts & Companies",
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

    term = suchbegriff.strip().lower()

    # Demodaten direkt aus den Befehlen laden
    df_anlagen = hole_anlagen_daten()
    df_vertraege = hole_wartungsvertraege_daten()

    # Suche in den Anlagen-Demodaten über alle Spalten
    res_anlagen = []
    if not df_anlagen.empty:
        mask_a = df_anlagen.astype(str).apply(lambda col: col.str.lower().str.contains(term, na=False)).any(axis=1)
        res_anlagen = df_anlagen[mask_a].to_dict(orient="records")

    # Suche in den Vertrags-Demodaten über alle Spalten
    res_vertraege = []
    if not df_vertraege.empty:
        mask_v = df_vertraege.astype(str).apply(lambda col: col.str.lower().str.contains(term, na=False)).any(axis=1)
        res_vertraege = df_vertraege[mask_v].to_dict(orient="records")

    res_service = []
    res_auffaelligkeiten = []

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
        }, errors='ignore')
        st.dataframe(df_a, use_container_width=True, hide_index=True)

    if res_vertraege:
        st.markdown(f"##### {TXT_GS['res_vertraege']} ({len(res_vertraege)})")
        df_v = pd.DataFrame(res_vertraege)
        if 'naechstewartung' in df_v.columns:
            df_v['naechstewartung'] = df_v['naechstewartung'].apply(formatiere_datum)
            
        df_v = df_v.rename(columns={
            'id': 'ID', 'bezeichnung': 'Vertrag', 'firma': 'Firma', 
            'naechstewartung': 'Nächste Wartung', 'kostenpa': 'Kosten (€)'
        }, errors='ignore')
        st.dataframe(df_v, use_container_width=True, hide_index=True)
