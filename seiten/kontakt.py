import streamlit as st

def zeige_kontaktformular():
    st.markdown("""
        <style>
        input, select, textarea, label {
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
            background-color: rgba(128, 128, 128, 0.25) !important;
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
        </style>
    """, unsafe_allow_html=True)

    if 'language' not in st.session_state:
        st.session_state.language = "de"

    if st.session_state.language == "de":
        TXT_K = {
            "title": "✉️ Support & Kontakt",
            "desc": "Haben Sie Fragen, Fehlerberichte oder Verbesserungsvorschläge? Senden Sie mir diese direkt – ich werde mich schnellstmöglich darum kümmern.",
            "card_form": "📝 Nachricht an mich",
            "lbl_name": "Ihr Name:",
            "lbl_email": "Ihre E-Mail-Adresse:",
            "lbl_prio": "Priorität:",
            "lbl_nachricht": "Ihre Nachricht / Beschreibung:",
            "ph_nachricht": "Beschreiben Sie Ihr Anliegen oder Ihren Fehler...",
            "prio_normal": "Normal",
            "prio_hoch": "Hoch (Dringend)",
            "btn_send": "Nachricht senden",
            "success": "Vielen Dank! Ihre Nachricht wurde erfolgreich übermittelt.",
            "warning": "Bitte füllen Sie alle Pflichtfelder (Name, E-Mail, Nachricht) aus.",
            "card_info": "ℹ️ Support-Informationen",
            "info_text": "**Direkter Support & Verwaltung**\n\n- **Ansprechpartner:** D. Wilfert\n- **Standort:** Europäische Schule München (ESM)\n- **Hinweis:** Bei Server- / Netzwerkfehlern bitte die interne IT-Abteilung einschalten.\n- **System-Version:** Enterprise V1.3.1.0"
        }
    else:
        TXT_K = {
            "title": "✉️ Support & Contact",
            "desc": "Do you have questions, bug reports, or feature requests? Send them directly to me – I will take care of it as soon as possible.",
            "card_form": "📝 Message to Me",
            "lbl_name": "Your Name:",
            "lbl_email": "Your Email Address:",
            "lbl_prio": "Priority:",
            "lbl_nachricht": "Your Message / Description:",
            "ph_nachricht": "Describe your request or issue...",
            "prio_normal": "Normal",
            "prio_hoch": "High (Urgent)",
            "btn_send": "Send Message",
            "success": "Thank you! Your message has been successfully sent.",
            "warning": "Please fill out all required fields (Name, Email, Message).",
            "card_info": "ℹ️ Support Information",
            "info_text": "**Direct Support & Management**\n\n- **Contact Person:** D. Wilfert\n- **Location:** European School Munich (ESM)\n- **Note:** For server/network errors, please contact the internal IT department.\n- **System Version:** Enterprise V1.3.1.0"
        }

    st.subheader(TXT_K["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 25px;'>{TXT_K['desc']}</div>", unsafe_allow_html=True)

    col_k1, col_k2 = st.columns([6.0, 4.0], gap="medium")

    with col_k1:
        with st.container(border=True):
            st.markdown(f"##### {TXT_K['card_form']}")
            st.write("")
            
            with st.form("support_kontakt_formular", clear_on_submit=True):
                name = st.text_input(TXT_K["lbl_name"], placeholder="Max Mustermann")
                email = st.text_input(TXT_K["lbl_email"], placeholder="max@esm-intern.de")
                prioritaet = st.selectbox(TXT_K["lbl_prio"], [TXT_K["prio_normal"], TXT_K["prio_hoch"]])
                nachricht = st.text_area(TXT_K["lbl_nachricht"], placeholder=TXT_K["ph_nachricht"], height=120)
                
                st.write("")
                submitted = st.form_submit_button(TXT_K["btn_send"], type="primary")
                
                if submitted:
                    if name and email and nachricht:
                        st.success(TXT_K["success"])
                    else:
                        st.warning(TXT_K["warning"])

    with col_k2:
        with st.container(border=True):
            st.markdown(f"##### {TXT_K['card_info']}")
            st.write("")
            st.markdown(TXT_K["info_text"])
