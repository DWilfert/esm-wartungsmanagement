import streamlit as st
import urllib.parse

def zeige_kontaktformular():
    # Einheitliches Design-Styling für Premium-Look
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
        </style>
    """, unsafe_allow_html=True)

    # Zweisprachiges Wörterbuch
    if st.session_state.language == "de":
        TXT_MAIL = {
            "title": "✉️ Support & Entwickler-Kontakt",
            "desc": "Senden Sie Fehlerberichte, Fragen oder Verbesserungsvorschläge direkt per Outlook an den Systemadministrator.",
            "f_cat": "Kategorie:",
            "cat_options": ["Bug / Systemfehler", "Verbesserungsvorschlag", "Frage zur Bedienung", "Sonstiges"],
            "f_prio": "Priorität:",
            "prio_options": ["🟢 Niedrig (Info)", "🟡 Mittel (Stört den Ablauf)", "🔴 Hoch (Systemkritisch)"],
            "f_msg": "Ihre Nachricht (wird in Outlook übertragen):",
            "msg_ph": "Bitte beschreiben Sie Ihr Anliegen so genau wie möglich...",
            "btn_send": "📧 In MS Outlook öffnen & senden",
            "info_text": "💡 Wenn Sie auf den Button klicken, öffnet sich automatisch Ihr Outlook mit einem fertigen E-Mail-Entwurf. Sie können dort ggf. noch Screenshots anfügen, bevor Sie die Mail absenden."
        }
    else:
        TXT_MAIL = {
            "title": "✉️ Support & Developer Contact",
            "desc": "Send bug reports, questions, or suggestions for improvement directly via Outlook to the system administrator.",
            "f_cat": "Category:",
            "cat_options": ["Bug / System Error", "Improvement Suggestion", "Usage Question", "Other"],
            "f_prio": "Priority:",
            "prio_options": ["🟢 Low (Info)", "🟡 Medium (Workflow hindered)", "🔴 High (System Critical)"],
            "f_msg": "Your Message (will be transferred to Outlook):",
            "msg_ph": "Please describe your request as accurately as possible...",
            "btn_send": "📧 Open & Send in MS Outlook",
            "info_text": "💡 Clicking the button will automatically open Outlook with a ready-made email draft. You can easily attach screenshots there before hitting send."
        }

    st.subheader(TXT_MAIL["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 25px;'>{TXT_MAIL['desc']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        kategorie = st.selectbox(TXT_MAIL["f_cat"], TXT_MAIL["cat_options"])
    with col2:
        prioritaet = st.selectbox(TXT_MAIL["f_prio"], TXT_MAIL["prio_options"])

    nachricht = st.text_area(TXT_MAIL["f_msg"], placeholder=TXT_MAIL["msg_ph"], height=150)
    
    # KLEINERER, KURSIVER INFOTEXT
    st.markdown(f"<p style='font-size: 11.5px; font-style: italic; color: var(--text-color); opacity: 0.75; margin-top: 8px; margin-bottom: 15px;'>{TXT_MAIL['info_text']}</p>", unsafe_allow_html=True)

    # Daten für die E-Mail aufbereiten
    ziel_adresse = "davidwdavid@hotmail.de"
    prio_clean = prioritaet.split(" ")[1] if " " in prioritaet else prioritaet 
    
    betreff = f"[ESM App] {prio_clean}: {kategorie}"
    
    body = f"""ESM Wartungsmanagement - Support-Ticket

Kategorie: {kategorie}
Priorität: {prioritaet}

----------------------------------------
NACHRICHT:
{nachricht if nachricht.strip() else 'Hier bitte die Nachricht eintragen...'}
----------------------------------------

Automatisch generiert durch die ESM Enterprise App.
"""

    mail_enc_subject = urllib.parse.quote(betreff)
    mail_enc_body = urllib.parse.quote(body)
    
    mailto_link = f"mailto:{ziel_adresse}?subject={mail_enc_subject}&body={mail_enc_body}"

    # REALISTISCHER, KOMPAKTER BUTTON (Zentriert oder Links, auf max. 320px begrenzt)
    btn_html = f"""
    <div style="margin-top: 5px;">
        <a href="{mailto_link}" style="text-decoration: none;">
            <button style="
                background-color: #1e3a8a;
                color: #cbd5e1;
                border: 1px solid #3b82f6;
                padding: 8px 18px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                font-size: 13.5px;
                display: inline-block;
                transition: all 0.3s ease;">
                {TXT_MAIL["btn_send"]}
            </button>
        </a>
    </div>
    """
    
    st.markdown(btn_html, unsafe_allow_html=True)