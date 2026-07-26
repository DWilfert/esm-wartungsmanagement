import streamlit as st
import pandas as pd
from datenbank.befehle import hole_datenbank_verbindung

def zeige_firmeninfo():
    # Einheitlicher Design-Fix für Tooltips, Dropdowns, Toolbars und Tabellen
    st.markdown("""
        <style>
        /* Kompakte Schriftgröße in allen Eingabefeldern, Radio-Buttons und Formularen */
        input, select, textarea, div[data-baseweb="select"] span, label, .stRadio div {
            font-size: 0.82rem !important;
        }
        
        /* Blendet den automatischen Streamlit-Hinweis aus */
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        
        /* Placeholder in leicht grauer Schrift und Kursiv */
        input::placeholder, textarea::placeholder {
            color: #94a3b8 !important;
            font-style: italic !important;
            opacity: 1 !important;
        }
        
        /* Dropdown-Menüs und Popovers */
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
        
        /* Tooltips & Toolbar-Buttons */
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

        /* Automatischer Hintergrund- und Rahmen-Fix für st.dataframe (verhindert den weißen Kasten im Dark-Mode) */
        div[data-testid="stDataFrame"] {
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-radius: 0.5rem;
            padding: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.language == "de":
        TXT_FIRMA = {
            "title": "🏢 Firmen- & Dienstleisterverwaltung",
            "desc": "Zentrale Verwaltung der Wartungsfirmen, Kontaktdaten und Vertragszuordnungen.",
            "act_lbl": "Aktion wählen:",
            "act_list": "Firmenübersicht",
            "act_add": "Neue Firma anlegen",
            "sel_del": "Firma auswählen zum Bearbeiten / Löschen:",
            "btn_del": "Firma unwiderruflich löschen",
            "succ_del": "Firma erfolgreich gelöscht!",
            "btn_save": "Firma speichern",
            "succ_save": "Neue Firma erfolgreich angelegt!",
            "empty_db": "Keine Firmen in der Datenbank vorhanden."
        }
    else:
        TXT_FIRMA = {
            "title": "🏢 Company & Contractor Management",
            "desc": "Central management of maintenance contractors, contact details, and contract assignments.",
            "act_lbl": "Select action:",
            "act_list": "Company List",
            "act_add": "Add New Company",
            "sel_del": "Select company to edit / delete:",
            "btn_del": "Permanently delete company",
            "succ_del": "Company deleted successfully!",
            "btn_save": "Save Company",
            "succ_save": "New company created successfully!",
            "empty_db": "No companies available in database."
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
        conn = hole_datenbank_verbindung()
        if conn is not None:
            try:
                df_firmen = pd.read_sql("SELECT * FROM `firmeninfo`", conn)
                if not df_firmen.empty:
                    # Schöne, lesbare Spaltenüberschriften für die Anzeige (abhängig von Sprache)
                    if st.session_state.language == "de":
                        spalten_mapping = {
                            "id": "ID",
                            "firmenname": "Firmenname",
                            "firmenart": "Firmenart",
                            "firmenadresse": "Adresse",
                            "firmen_telefon": "Telefon",
                            "firmen_fax": "Fax",
                            "firmen_mail": "E-Mail",
                            "firmen_website": "Website",
                            "firmen_ansprechpartner": "Ansprechpartner",
                            "technikername": "Techniker Name",
                            "techniker_telefon": "Techniker Telefon",
                            "techniker_mail": "Techniker E-Mail",
                            "qualifikation": "Qualifikation",
                            "zugeweseneid": "Zugewiesene ID"
                        }
                    else:
                        spalten_mapping = {
                            "id": "ID",
                            "firmenname": "Company Name",
                            "firmenart": "Company Type",
                            "firmenadresse": "Address",
                            "firmen_telefon": "Phone",
                            "firmen_fax": "Fax",
                            "firmen_mail": "E-Mail",
                            "firmen_website": "Website",
                            "firmen_ansprechpartner": "Contact Person",
                            "technikername": "Technician Name",
                            "techniker_telefon": "Technician Phone",
                            "techniker_mail": "Technician E-Mail",
                            "qualifikation": "Qualification",
                            "zugeweseneid": "Assigned ID"
                        }
                    df_anzeige = df_firmen.rename(columns=spalten_mapping)
                    st.dataframe(df_anzeige, use_container_width=True, hide_index=True)
                    
                    st.write("---")
                    name_col = "firmenname" if "firmenname" in df_firmen.columns else df_firmen.columns[1]
                    unbenannt_text = "Unbenannt" if st.session_state.language == "de" else "Unnamed"
                    firmen_liste = [""] + [f"[ID: {row['id']}] {row.get(name_col, unbenannt_text)}" for _, row in df_firmen.iterrows()]
                    ausgewaehlte_firma = st.selectbox(TXT_FIRMA["sel_del"], firmen_liste, key="firmen_del_selectbox_v1")

                    if ausgewaehlte_firma:
                        f_id = int(ausgewaehlte_firma.split("]")[0].replace("[ID:", "").strip())
                        
                        # Sicherheitsabfrage vor dem Löschen
                        bestaetigt_del = st.checkbox(
                            "Sicherheitsabfrage: Wirklich löschen?" if st.session_state.language == "de" else "Security check: Really delete?",
                            key="firmen_del_checkbox_confirm"
                        )
                        if bestaetigt_del:
                            if st.button(TXT_FIRMA["btn_del"], key="firmen_del_action_btn"):
                                cursor = conn.cursor()
                                cursor.execute("DELETE FROM `firmeninfo` WHERE id = %s", (f_id,))
                                conn.commit()
                                cursor.close()
                                st.success(TXT_FIRMA["succ_del"])
                                st.rerun()
                else:
                    st.info(TXT_FIRMA["empty_db"])
            except Exception as e:
                st.error(f"Fehler: {str(e)}" if st.session_state.language == "de" else f"Error: {str(e)}")
            finally:
                conn.close()

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
                    conn = hole_datenbank_verbindung()
                    if conn is not None:
                        try:
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT INTO `firmeninfo` (firmenname, firmenart, firmenadresse, firmen_telefon, firmen_fax, firmen_mail, firmen_website, firmen_ansprechpartner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                (f_name, f_art, f_adresse, f_telefon, f_fax, f_mail, f_website, f_ansprechpartner)
                            )
                            conn.commit()
                            cursor.close()
                            st.success(TXT_FIRMA["succ_save"])
                            st.rerun()
                        except Exception as e_ins:
                            st.error(f"Fehler beim Speichern: {str(e_ins)}" if st.session_state.language == "de" else f"Error while saving: {str(e_ins)}")
                        finally:
                            conn.close()