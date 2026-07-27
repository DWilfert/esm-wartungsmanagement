import streamlit as st
import pandas as pd

def zeige_anlagen_history():
    # CSS für kompakte Schriftgröße, Dropdown-Fix und 40% verkleinertes Dropdown-Feld
    st.markdown("""
        <style>
        input, select, textarea, div[data-baseweb="select"] span, label {
            font-size: 0.82rem !important;
        }
        
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        
        /* Dropdown-Feld um 40% verkleinern (Breite auf 60% gesetzt) */
        div[data-baseweb="select"] {
            max-width: 60% !important;
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

    # Titel und angepasster Text
    st.subheader("🔄 360° Anlagen-Ansicht" if st.session_state.language == "de" else "🔄 360° Asset View")
    st.markdown(
        "<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 20px;'>"
        "Chronologische Ansicht: Alle Stammdaten, Verträge, Historien und Prüfberichte im Überblick."
        "</div>", 
        unsafe_allow_html=True
    )

    # Beispieldaten für die 360°-Ansicht
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

    # Dropdown zur Auswahl der Anlage (jetzt 40% schmaler)
    anlagen_optionen = [""] + [f"{row['id']} - {row['bezeichnung']}" for _, row in df_history_anlagen.iterrows()]
    
    ausgewaehlte_anlage = st.selectbox(
        "Anlage auswählen (Alphabetisch):" if st.session_state.language == "de" else "Select Asset (Alphabetical):",
        options=anlagen_optionen,
        key="hist_anl_dropdown"
    )

    if ausgewaehlte_anlage:
        st.markdown("---")
        st.success(f"Ausgewählte Anlage geladen: **{ausgewaehlte_anlage}**")
        
        # Tabs für die 360-Grad-Ansicht
        t_stammdaten, t_vertraege, t_historie, t_pruefungen = st.tabs([
            "📋 Stammdaten", "📄 Verträge", "⏱️ Historie", "🔍 Prüfberichte"
        ])
        
        with t_stammdaten:
            st.write("Hier stehen alle technischen und kaufmännischen Stammdaten der Anlage im Detail.")
        with t_vertraege:
            st.write("zugeordnete Wartungs- und Serviceverträge.")
        with t_historie:
            st.write("Chronologischer Verlauf aller vergangenen Einsätze und Reparaturen.")
        with t_pruefungen:
            st.write("Prüfprotokolle, Mängellisten und Fristen.")
            
    else:
        st.info("Bitte wähle oben eine Anlage aus, um die vollständige 360°-Chronik anzuzeigen.")
