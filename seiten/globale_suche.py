import streamlit as st
import pandas as pd

def zeige_globale_suche():
    st.markdown("""
        <style>
        input, select, textarea, div[data-baseweb="select"] span, label, .stRadio div {
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
        
        div[data-testid="stDataFrame"] {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 2px;
            background-image: linear-gradient(to right, rgba(128, 128, 128, 0.08) 1px, transparent 1px),
                              linear-gradient(to bottom, rgba(128, 128, 128, 0.08) 1px, transparent 1px);
            background-size: 15px 15px;
        }
        
        div[data-testid="stDataFrame"] td {
            padding-top: 2px !important;
            padding-bottom: 2px !important;
            font-size: 0.78rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'language' not in st.session_state:
        st.session_state.language = "de"

    if st.session_state.language == "de":
        TXT_GS = {
            "title": "🔍 Globale 360° Volltextsuche",
            "desc": "Durchsuche den gesamten Datenbestand (Anlagen, Verträge, Standorte und Komponenten) in Echtzeit.",
            "placeholder": "Suchbegriff eingeben...",
            "info_leer": "Bitte geben Sie einen Suchbegriff ein.",
            "treffer": "🎉 {count} Treffer gefunden für '{term}'",
            "keine_treffer": "Keine Treffer für: '{term}'",
            "sec_anlagen": "Treffer bei Anlagen",
            "sec_vertraege": "Treffer bei Verträgen"
        }
    else:
        TXT_GS = {
            "title": "🔍 Global 360° Full-Text Search",
            "desc": "Search the entire database (assets, contracts, locations, and components) in real-time.",
            "placeholder": "Enter search term...",
            "info_leer": "Please enter a search term.",
            "treffer": "🎉 {count} matches found for '{term}'",
            "keine_treffer": "No matches found for: '{term}'",
            "sec_anlagen": "Matches in Assets",
            "sec_vertraege": "Matches in Contracts"
        }

    st.subheader(TXT_GS["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 20px;'>{TXT_GS['desc']}</div>", unsafe_allow_html=True)
    
    suchbegriff = st.text_input(TXT_GS["placeholder"], key="globaler_such_input")
    
    if not suchbegriff.strip():
        st.info(TXT_GS["info_leer"])
        return

    term = suchbegriff.strip().lower()

    df_anlagen = pd.DataFrame({
        "id": [17501, 17502, 17503, 17504, 17505, 17506, 17507],
        "standort": ["Fasangarten", "Neuperlach", "Fasangarten", "Neuperlach", "Fasangarten", "Neuperlach", "Fasangarten"],
        "anlagentyp": ["Fördertechnik", "Raumlufttechnik", "Elektrotechnik", "Wärmeversorgung", "Brandschutz", "Sanitär", "Kältetechnik"],
        "bezeichnung": [
            "Hauptaufzug Gebäude A", 
            "Lüftungsanlage Zentral", 
            "Hauptverteiler Elektrik", 
            "Heizung / Heizkessel Anlage 2", 
            "Rauchmeldezentrale Ost",
            "Hauptwasserleitung & Sanitär",
            "Klimaanlage Serverraum"
        ],
        "zustand": ["Betriebsbereit", "Wartung überfällig", "Prüfung anstehend", "Betriebsbereit", "Betriebsbereit", "Wartung fällig", "Störung"],
        "hersteller": ["Otis", "Stulz", "Siemens", "Viessmann", "Hilti", "Grohe", "Daikin"],
        "raum": ["U01", "Dachboden", "E05", "Keller", "Foyer", "U02", "Serverraum 3"]
    })

    df_vertraege = pd.DataFrame({
        "id": [1, 2, 3, 4, 5, 6, 7],
        "bezeichnung": [
            "Vollwartungsvertrag Aufzugsanlagen", 
            "Wartung Lüftungstechnik", 
            "Jahresinspektion Elektrik", 
            "Wärmeversorgung & Heizung Service", 
            "Brandschutzprüfung",
            "Sanitär Instandhaltung",
            "Klimaanlagen Vollservice"
        ],
        "firma": ["Otis GmbH", "Stulz GmbH", "Siemens AG", "Viessmann Werke", "Hilti Service", "Sanitär Profi GmbH", "Daikin Service"]
    })

    mask_a = df_anlagen.astype(str).apply(lambda col: col.str.lower().str.contains(term, na=False)).any(axis=1)
    res_anlagen = df_anlagen[mask_a].to_dict(orient="records")

    mask_v = df_vertraege.astype(str).apply(lambda col: col.str.lower().str.contains(term, na=False)).any(axis=1)
    res_vertraege = df_vertraege[mask_v].to_dict(orient="records")

    gesamt = len(res_anlagen) + len(res_vertraege)

    if gesamt == 0:
        st.warning(TXT_GS["keine_treffer"].format(term=suchbegriff))
        return

    st.success(TXT_GS["treffer"].format(count=gesamt, term=suchbegriff))
    st.write("")
    
    if res_anlagen:
        st.markdown(f"##### {TXT_GS['sec_anlagen']}")
        st.dataframe(pd.DataFrame(res_anlagen), use_container_width=True, hide_index=True)
        st.write("")
        
    if res_vertraege:
        st.markdown(f"##### {TXT_GS['sec_vertraege']}")
        st.dataframe(pd.DataFrame(res_vertraege), use_container_width=True, hide_index=True)
