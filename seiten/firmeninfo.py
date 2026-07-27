import streamlit as st
import pandas as pd

def zeige_firmeninfo():
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
        TXT_FIRMA = {
            "title": "🏢 Firmen- & Dienstleisterverwaltung",
            "desc": "Zentrale Verwaltung der Wartungsfirmen, Kontaktdaten und Vertragszuordnungen.",
            "act_lbl": "Aktion wählen:",
            "act_list": "Firmenübersicht",
            "act_add": "Neue Firma anlegen",
            "sel_del": "Firma auswählen zum Bearbeiten / Löschen / Verträge anzeigen:",
            "btn_del": "Firma unwiderruflich löschen",
            "succ_del": "Firma erfolgreich gelöscht!",
            "btn_save": "Firma speichern",
            "succ_save": "Neue Firma erfolgreich angelegt!",
            "empty_db": "Keine Firmen in der Datenbank vorhanden.",
            "vertrag_title": "📑 Verknüpfte Verträge & Anlagen für",
            "no_contracts": "ℹ️ Keine aktiven Verträge für diese Firma hinterlegt."
        }
    else:
        TXT_FIRMA = {
            "title": "🏢 Company & Contractor Management",
            "desc": "Central management of maintenance contractors, contact details, and contract assignments.",
            "act_lbl": "Select action:",
            "act_list": "Company List",
            "act_add": "Add New Company",
            "sel_del": "Select company to edit / delete / view contracts:",
            "btn_del": "Permanently delete company",
            "succ_del": "Company deleted successfully!",
            "btn_save": "Save Company",
            "succ_save": "New company created successfully!",
            "empty_db": "No companies available in database.",
            "vertrag_title": "📑 Linked Contracts & Assets for",
            "no_contracts": "ℹ️ No active contracts found for this company."
        }

    st.subheader(TXT_FIRMA["title"])
    st.markdown(f"<div style='font-size: 13px; color: var(--text-color); opacity: 0.7; margin-bottom: 20px;'>{TXT_FIRMA['desc']}</div>", unsafe_allow_html=True)

    firma_aktion = st.radio(
        TXT_FIRMA["act_lbl"],
        [TXT_FIRMA["act_list"], TXT_FIRMA["act_add"]],
        horizontal=True,
        key="firmen_haupt_aktion_radio_v1"
    )
    st.write("")

    if firma_aktion == TXT_FIRMA["act_list"]:
        df_firmen = pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "firmenname": ["Otis GmbH", "Schindler AG", "Stulz GmbH", "Siemens AG", "Viessmann Werke"],
            "firmenart": ["Aufzugtechnik", "Fördertechnik", "Klimatechnik", "Gebäudeautomation", "Wärmeversorgung"],
            "firmenadresse": ["München", "Berlin", "Hamburg", "Frankfurt", "Stuttgart"],
            "firmen_telefon": ["+49 89 1111", "+49 30 2222", "+49 40 3333", "+49 69 4444", "+49 711 5555"],
            "firmen_fax": ["+49 89 1112", "+49 30 2223", "+49 40 3334", "+49 69 4445", "+49 711 5556"],
            "firmen_mail": ["info@otis.de", "kontakt@schindler.de", "service@stulz.de", "info@siemens.de", "kontakt@viessmann.de"],
            "firmen_website": ["www.otis.de", "www.schindler.de", "www.stulz.de", "www.siemens.de", "www.viessmann.de"],
            "firmen_ansprechpartner": ["Herr Müller", "Frau Schmidt", "Herr Weber", "Frau Wagner", "Herr Becker"],
            "technikername": ["Max Mustermann", "Erika Musterfrau", "Hans Meier", "Anna Fischer", "Karl Koch"],
            "techniker_telefon": ["0176-123456", "0175-654321", "0171-112233", "0172-445566", "0173-778899"],
            "techniker_mail": ["max@otis.de", "erika@schindler.de", "hans@stulz.de", "anna@siemens.de", "karl@viessmann.de"],
            "qualifikation": ["Sachkundiger Aufzug", "Zertifizierter Techniker", "Klima-Experte", "SPS-Spezialist", "Heizungsbaumeister"],
            "zugeweseneid": [101, 102, 103, 104, 105]
        })

        df_demo_vertraege = pd.DataFrame({
            "vertrag_id": [501, 502, 503, 504, 505, 506],
            "firmenname": ["Otis GmbH", "Otis GmbH", "Stulz GmbH", "Siemens AG", "Viessmann Werke", "Schindler AG"],
            "anlagen_bezeichnung": ["Personenaufzug Hauptgebäude", "Rollstuhlhebebühne", "Lüftungsanlage Bibliothek", "Brandmeldeanlage Ost", "Heizungsanlage Zentrale", "Fahrstuhl Nebeneingang"],
            "standort": ["NP", "FG", "FG", "FG", "NP", "NP"],
            "intervall": ["12 Monate", "12 Monate", "6 Monate", "24 Monate", "12 Monate", "12 Monate"]
        })

        if not df_firmen.empty:
            if st.session_state.language == "de":
                spalten_mapping = {
                    "id": "ID", "firmenname": "Firmenname", "firmenart": "Firmenart",
                    "firmenadresse": "Adresse", "firmen_telefon": "Telefon", "firmen_fax": "Fax",
                    "firmen_mail": "E-Mail", "firmen_website": "Website", "firmen_ansprechpartner": "Ansprechpartner",
                    "technikername": "Techniker Name", "techniker_telefon": "Techniker Telefon",
                    "techniker_mail": "Techniker E-Mail", "qualifikation": "Qualifikation", "zugeweseneid": "Zugewiesene ID"
                }
            else:
                spalten_mapping = {
                    "id": "ID", "firmenname": "Company Name", "firmenart": "Company Type",
                    "firmenadresse": "Address", "firmen_telefon": "Phone", "firmen_fax": "Fax",
                    "firmen_mail": "E-Mail", "firmen_website": "Website", "firmen_ansprechpartner": "Contact Person",
                    "technikername": "Technician Name", "techniker_telefon": "Technician Phone",
                    "techniker_mail": "Technician E-Mail", "qualifikation": "Qualification", "zugeweseneid": "Assigned ID"
                }
            df_anzeige = df_firmen.rename(columns=spalten_mapping)
            st.dataframe(df_anzeige, use_container_width=True, hide_index=True)
            
            st.write("---")
            name_col = "firmenname" if "firmenname" in df_firmen.columns else df_firmen.columns[1]
            unbenannt_text = "Unbenannt" if st.session_state.language == "de" else "Unnamed"
            firmen_liste = [""] + [f"[ID: {row['id']}] {row.get(name_col, unbenannt_text)}" for _, row in df_firmen.iterrows()]
            
            col_sel, _ = st.columns([3.5, 6.5])
            with col_sel:
                ausgewaehlte_firma = st.selectbox(TXT_FIRMA["sel_del"], firmen_liste, key="firmen_del_selectbox_v1")

            if ausgewaehlte_firma:
                gefundener_firmenname = ausgewaehlte_firma.split("]")[1].strip()
                if " (" in gefundener_firmenname:
                    gefundener_firmenname = gefundener_firmenname.split(" (")[0].strip()

                st.markdown("<hr style='margin: 25px 0; border: none; border-top: 1px solid rgba(128, 128, 128, 0.3);'>", unsafe_allow_html=True)

                st.markdown(f"##### {TXT_FIRMA['vertrag_title']} **{gefundener_firmenname}**")
                df_v_filtered = df_demo_vertraege[df_demo_vertraege["firmenname"] == gefundener_firmenname]

                if not df_v_filtered.empty:
                    if st.session_state.language == "de":
                        v_map = {"vertrag_id": "Vertrags-ID", "anlagen_bezeichnung": "Anlagen-Bezeichnung", "standort": "Standort", "intervall": "Wartungs-Intervall"}
                    else:
                        v_map = {"vertrag_id": "Contract ID", "anlagen_bezeichnung": "Asset Description", "standort": "Location", "intervall": "Maintenance Interval"}
                    
                    df_v_anzeige = df_v_filtered[["vertrag_id", "anlagen_bezeichnung", "standort", "intervall"]].rename(columns=v_map)
                    
                    st.dataframe(df_v_anzeige, use_container_width=True, hide_index=True)
                else:
                    st.info(TXT_FIRMA["no_contracts"])

                st.write("")
                bestaetigt_del = st.checkbox(
                    "Sicherheitsabfrage: Wirklich löschen?" if st.session_state.language == "de" else "Security check: Really delete?",
                    key="firmen_del_checkbox_confirm"
                )
                if bestaetigt_del:
                    if st.button(TXT_FIRMA["btn_del"], key="firmen_del_action_btn"):
                        st.success(TXT_FIRMA["succ_del"])
                        st.rerun()
        else:
            st.info(TXT_FIRMA["empty_db"])

    elif firma_aktion == TXT_FIRMA["act_add"]:
        with st.form("firma_anlegen_form", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                f_name = st.text_input("Firmenname *" if st.session_state.language == "de" else "Company Name *", placeholder="z.B. Lift Service GmbH" if st.session_state.language == "de" else "e.g. Lift Service Ltd.", key="f_name_inp")
                f_art = st.text_input("Firmenart" if st.session_state.language == "de" else "Company Type", placeholder="z.B. Wartungsdienstleister" if st.session_state.language == "de" else "e.g. Maintenance Provider", key="f_art_inp")
                f_adresse = st.text_input("Firmenadresse" if st.session_state.language == "de" else "Company Address", placeholder="z.B. Hauptstraße 12, München" if st.session_state.language == "de" else "e.g. Main Street 12, Munich", key="f_adr_inp")
                f_telefon = st.text_input("Telefonnummer" if st.session_state.language == "de" else "Phone Number", placeholder="z.B. +49 89 1234567" if st.session_state.language == "de" else "e.g. +49 89 1234567", key="f_tel_inp")
            with col_f2:
                f_fax = st.text_input("Fax" if st.session_state.language == "de" else "Fax", placeholder="z.B. +49 89 1234568" if st.session_state.language == "de" else "e.g. +49 89 1234568", key="f_fax_inp")
                f_mail = st.text_input("E-Mail Adresse" if st.session_state.language == "de" else "E-Mail Address", placeholder="z.B. info@liftservice.de" if st.session_state.language == "de" else "e.g. info@liftservice.com", key="f_email_inp")
                f_website = st.text_input("Website" if st.session_state.language == "de" else "Website", placeholder="z.B. www.liftservice.de" if st.session_state.language == "de" else "e.g. www.liftservice.com", key="f_web_inp")
                f_ansprechpartner = st.text_input("Ansprechpartner" if st.session_state.language == "de" else "Contact Person", placeholder="z.B. Max Mustermann" if st.session_state.language == "de" else "e.g. John Doe", key="f_ap_inp")

            if st.form_submit_button(TXT_FIRMA["btn_save"]):
                if not f_name:
                    st.error("Bitte mindestens den Firmennamen angeben!" if st.session_state.language == "de" else "Please specify at least the company name!")
                else:
                    st.success(TXT_FIRMA["succ_save"])
                    st.rerun()
