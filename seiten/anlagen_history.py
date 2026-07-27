import streamlit as st
import pandas as pd

def zeige_anlagen_history():
    st.markdown("""
        <style>
        input, select, textarea, div[data-baseweb="select"] span, label {
            font-size: 0.82rem !important;
        }
        
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        
        div.stSelectbox {
            max-width: 50% !important;
        }
        
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
            background-color: var(--secondary-background-color) !important;
        }
        
        div[data-baseweb="popover"] ul li, 
        ul[data-baseweb="menu"] li,
        li[role="option"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            font-size: 0.85rem !important;
        }
        
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    lang = st.session_state.get("language", "de")
    
    txt = {
        "de": {
            "titel": "🔄 360° Anlagen-Ansicht",
            "untertitel": "Chronologische Ansicht: Alle Stammdaten, Verträge, Historien und Prüfberichte im Überblick.",
            "label_dropdown": "Anlage auswählen (Alphabetisch):",
            "tab1": "📋 Stammdaten",
            "tab2": "📄 Verträge",
            "tab3": "⏱️ Historie",
            "tab4": "🔍 Prüfberichte",
            "info_text": "Bitte wähle oben eine Anlage aus, um die vollständige 360°-Chronik anzuzeigen.",
            "geladen": "Ausgewählte Anlage geladen: **{anlage}**"
        },
        "en": {
            "titel": "🔄 360° Asset View",
            "untertitel": "Chronological view: All master data, contracts, histories, and inspection reports at a glance.",
            "label_dropdown": "Select Asset (Alphabetical):",
            "tab1": "📋 Master Data",
            "tab2": "📄 Contracts",
            "tab3": "⏱️ History",
            "tab4": "🔍 Inspection Reports",
            "info_text": "Please select an asset above to display the complete 360° chronicle.",
            "geladen": "Selected asset loaded: **{anlage}**"
        }
    }[lang]

    st.subheader(txt["titel"])
    st.markdown(
        f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 20px;'>{txt['untertitel']}</div>", 
        unsafe_allow_html=True
    )

    df_history_anlagen = pd.DataFrame({
        "id": [17501, 17502, 17503, 17504],
        "bezeichnung": [
            "Personenaufzug Hauptgebäude - Fördertechnik", 
            "Raumluftanlage Labor 3 - RLT", 
            "Hauptverteiler Elektrik - Trafo 1", 
            "Heizungsanlage Keller - Wärme"
        ],
        "standort": ["NP", "FG", "NP", "FG"],
        "zustand": ["Betriebsbereit", "Wartung überfällig", "Betriebsbereit", "Prüfung anstehend"]
    })

    anlagen_optionen = [""] + [f"{row['id']} - {row['bezeichnung']}" for _, row in df_history_anlagen.iterrows()]
    
    ausgewaehlte_anlage = st.selectbox(
        txt["label_dropdown"],
        options=anlagen_optionen,
        key="hist_anl_dropdown"
    )

    if ausgewaehlte_anlage:
        st.markdown("---")
        st.success(txt["geladen"].format(anlage=ausgewaehlte_anlage))
        
        t_stammdaten, t_vertraege, t_historie, t_pruefungen = st.tabs([
            txt["tab1"], txt["tab2"], txt["tab3"], txt["tab4"]
        ])
        
        with t_stammdaten:
            st.write("Hier stehen alle technischen und kaufmännischen Stammdaten der Anlage im Detail." if lang == "de" else "Detailed technical and commercial master data of the asset.")
        with t_vertraege:
            st.write("Zugeordnete Wartungs- und Serviceverträge." if lang == "de" else "Assigned maintenance and service contracts.")
        with t_historie:
            st.write("Chronologischer Verlauf aller vergangenen Einsätze und Reparaturen." if lang == "de" else "Chronological history of all past operations and repairs.")
        with t_pruefungen:
            st.write("Prüfprotokolle, Mängellisten und Fristen." if lang == "de" else "Inspection protocols, defect lists, and deadlines.")
            
    else:
        st.info(txt["info_text"])
