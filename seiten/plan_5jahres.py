import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fpdf import FPDF

def zeige_5jahresplan():
    # Einheitlicher Design-Fix für Tooltips, Dropdowns, Toolbars und kompakteres Gitternetz
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

        /* Kompaktere Zeilendichte und Matrix-Gitternetz für st.dataframe */
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

    # --- DYNAMISCHE FARBEN FÜR PLOTLY & HTML ---
    theme = st.session_state.get("app_theme", "Premium Dark")
    
    if theme == "Premium Light":
        chart_text = "#0f172a"
        chart_grid = "rgba(0, 0, 0, 0.15)"
        text_muted = "#64748b"
        chart_bg = "#ffffff"
    elif theme == "Premium Cashmere":
        chart_text = "#433422"
        chart_grid = "rgba(139, 115, 85, 0.25)"
        text_muted = "#8b7355"
        chart_bg = "#fdfbf7"
    elif theme == "Premium Business":
        chart_text = "#f8fafc"
        chart_grid = "rgba(30, 41, 59, 0.8)"
        text_muted = "#94a3b8"
        chart_bg = "#0f172a"
    elif theme == "Premium Slate":
        chart_text = "#f4f4f5"
        chart_grid = "rgba(161, 161, 170, 0.25)"
        text_muted = "#a1a1aa"
        chart_bg = "#18181b"
    else:
        chart_text = "#e2e8f0"
        chart_grid = "rgba(30, 41, 59, 0.9)"
        text_muted = "#94a3b8"
        chart_bg = "#0e1117"

    # --- SAUBERE, DEZENTE TRANSPARENZ FÜR FILTER ---
    st.markdown("""
        <style>
            div[data-testid="stCheckbox"] label p, 
            div[data-testid="stRadio"] label p { 
                font-size: 11px !important; 
                color: var(--text-color) !important; 
            }
            div[data-testid="stCheckbox"] {
                margin-bottom: -10px !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.language == "de":
        TXT_PLAN = {
            "title": "Strategischer 5-Jahres-Wartungsplan",
            "desc": "Langfristige Instandhaltungprojektion inklusive interaktiver Matrix-Ampel-Analyse und automatisiertem PDF-Audit-Export.",
            "chart_title": "Strategische Fristen-Zeitachse (Matrix)"
        }
    else:
        TXT_PLAN = {
            "title": "Strategic 5-Year Maintenance Plan",
            "desc": "Long-term maintenance projection including interactive matrix traffic-light analysis and automated PDF audit export.",
            "chart_title": "Strategic Deadline Timeline (Matrix)"
        }

    st.subheader(TXT_PLAN["title"])
    st.markdown(f"<div style='font-size: 13px; color: {text_muted}; margin-bottom: 25px;'>{TXT_PLAN['desc']}</div>", unsafe_allow_html=True)
    
    # Sofortige Demo-Daten für den 5-Jahres-Plan bereitstellen
    heute = datetime.now()
    df_ueber = pd.DataFrame({
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "anlagenid": [17501, 17502, 17503, 17504, 17505, 17506, 17507, 17508, 17509, 17510],
        "bezeichnung": [
            "Personenaufzug Hauptgebäude", "Lüftungsanlage Bibliothek", "Heizungsanlage Zentrale", 
            "Brandmeldeanlage Ost", "Klimaanlage Serverraum", "Rollstuhlhebebühne", 
            "Rauchabzugsanlage", "Trafo-Station Hauptgebäude", "Notstromaggregat", "Sanitärpumpe Keller"
        ],
        "firma": ["Otis GmbH", "Stulz GmbH", "Viessmann Werke", "Siemens AG", "Stulz GmbH", "Schindler AG", "Siemens AG", "Siemens AG", "Viessmann Werke", "Stulz GmbH"],
        "standort": ["NP", "FG", "NP", "FG", "NP", "FG", "NP", "FG", "NP", "FG"],
        "zyklusmonate": [12, 6, 12, 24, 6, 12, 12, 24, 12, 12],
        "letztewartung": [
            (heute - timedelta(days=400)).strftime('%Y-%m-%d'),
            (heute - timedelta(days=200)).strftime('%Y-%m-%d'),
            (heute - timedelta(days=100)).strftime('%Y-%m-%d'),
            (heute - timedelta(days=500)).strftime('%Y-%m-%d'),
            (heute - timedelta(days=30)).strftime('%Y-%m-%d'),
            (heute - timedelta(days=450)).strftime('%Y-%m-%d'),
            (heute - timedelta(days=150)).strftime('%Y-%m-%d'),
            (heute - timedelta(days=800)).strftime('%Y-%m-%d'),
            (heute - timedelta(days=90)).strftime('%Y-%m-%d'),
            (heute - timedelta(days=20)).strftime('%Y-%m-%d')
        ],
        "naechstewartung": [
            (heute - timedelta(days=35)).strftime('%Y-%m-%d'),  # Überfällig (Rot)
            (heute + timedelta(days=20)).strftime('%Y-%m-%d'),  # Anstehend (Gelb)
            (heute + timedelta(days=200)).strftime('%Y-%m-%d'), # Später
            (heute - timedelta(days=10)).strftime('%Y-%m-%d'),  # Überfällig (Rot)
            (heute + timedelta(days=15)).strftime('%Y-%m-%d'),  # Anstehend (Gelb)
            (heute - timedelta(days=60)).strftime('%Y-%m-%d'),  # Überfällig (Rot)
            (heute + timedelta(days=45)).strftime('%Y-%m-%d'),  # Anstehend (Gelb)
            (heute - timedelta(days=5)).strftime('%Y-%m-%d'),   # Überfällig (Rot)
            (heute + timedelta(days=70)).strftime('%Y-%m-%d'),  # Anstehend (Gelb)
            (heute + timedelta(days=180)).strftime('%Y-%m-%d')  # Später
        ]
    })

    if not df_ueber.empty:
        col_links, col_rechts = st.columns([8.6, 1.4])
        
        with col_rechts:
            proj_lbl = "Projektion" if st.session_state.language == "de" else "Projection"
            st.markdown(f"<p style='font-size: 12px; font-weight: 600; color: {text_muted}; margin-bottom: 5px;'>{proj_lbl}</p>", unsafe_allow_html=True)
            show_np = st.checkbox("NP (Neuperlach)", value=True, key="chk_np_v12_final")
            show_fg = st.checkbox("FG (Fasangarten)", value=True, key="chk_fg_v12_final")
            std_filter = []
            if show_np: std_filter.append("NP")
            if show_fg: std_filter.append("FG")
            
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
            
            aktuelles_jahr = datetime.now().year
            jahre_optionen = [aktuelles_jahr + i for i in range(5)]
            wahl_jahr = st.radio("Jahre" if st.session_state.language == "de" else "Years", options=jahre_optionen, index=0, label_visibility="collapsed", key="rad_year_v12_final")
            
            st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
            show_rot = st.checkbox("🔴 Fällig" if st.session_state.language == "de" else "🔴 Due", value=True, key="chk_rot_v12_final")
            show_gelb = st.checkbox("🟡 Warnung" if st.session_state.language == "de" else "🟡 Warning", value=True, key="chk_gelb_v12_final")
            status_filter = []
            if show_rot: status_filter.append("🔴 Überfällig" if st.session_state.language == "de" else "🔴 Overdue")
            if show_gelb: status_filter.append("🟡 Anstehend" if st.session_state.language == "de" else "🟡 Pending")
            
        with col_links:
            heute_dt = pd.to_datetime(datetime.now().date())
            timeline_punkte = []
            df_u_fil = df_ueber[df_ueber["standort"].isin(std_filter)].copy() if std_filter else df_ueber.copy()
            for _, r in df_u_fil.iterrows():
                n_w_val = r["naechstewartung"]
                if not n_w_val: continue
                n_w_dt = pd.to_datetime(n_w_val, errors='coerce')
                if pd.isnull(n_w_dt): continue
                intervall_monate = int(r["zyklusmonate"]) if r["zyklusmonate"] else 12
                
                for j in range(5):
                    verschiebung_tage = j * (intervall_monate * 30.44)
                    projizierter_termin = n_w_dt + timedelta(days=verschiebung_tage)
                    proj_jahr = projizierter_termin.year
                    
                    if j == 0 and n_w_dt.date() < heute_dt.date():
                        p_status = "🔴 Überfällig" if st.session_state.language == "de" else "🔴 Overdue"
                        p_color = "#ef4444"
                    elif heute_dt.date() <= projizierter_termin.date() <= (heute_dt.date() + timedelta(days=90)):
                        p_status = "🟡 Anstehend" if st.session_state.language == "de" else "🟡 Pending"
                        p_color = "#f59e0b"
                    else: 
                        continue
                        
                    timeline_punkte.append({
                        "id": r["id"], "anlagenid": r["anlagenid"], "bezeichnung": r["bezeichnung"],
                        "firma": r["firma"], "standort": r["standort"], "Datum": projizierter_termin,
                        "Jahr": proj_jahr, "Status": p_status, "Farbe": p_color
                    })
                    
            if timeline_punkte:
                df_chart = pd.DataFrame(timeline_punkte)
                if wahl_jahr: df_chart = df_chart[df_chart["Jahr"] == wahl_jahr]
                if status_filter: df_chart = df_chart[df_chart["Status"].isin(status_filter)]
            else: 
                df_chart = pd.DataFrame()
                
            if not df_chart.empty:
                if st.session_state.language == "de":
                    monats_namen = ["Jan", "Feb", "März", "Apr", "Mai", "Juni", "Juli", "Aug", "Sept", "Okt", "Nov", "Dez"]
                else:
                    monats_namen = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                df_chart["Monat_Name"] = df_chart["Datum"].dt.month.apply(lambda m: monats_namen[m-1])
                
                anzahl_eintraege = df_chart["bezeichnung"].nunique()
                dynamische_hoehe = max(400, anzahl_eintraege * 24)
                
                fig = go.Figure()
                for status_name, gruppe in df_chart.groupby("Status"):
                    farbe_auswahl = gruppe["Farbe"].iloc[0] if not gruppe["Farbe"].empty else "#ef4444"
                    if st.session_state.language == "de":
                        hover_texts = [f"<b>{row['bezeichnung']}</b><br>📍 {row['standort']} | 🏢 {row['firma']}<br>🗓️ Datum: {row['Datum'].strftime('%d.%m.%Y')}<br>⚠️ Status: {row['Status']}" for _, row in gruppe.iterrows()]
                    else:
                        hover_texts = [f"<b>{row['bezeichnung']}</b><br>📍 {row['standort']} | 🏢 {row['firma']}<br>🗓️ Date: {row['Datum'].strftime('%m/%d/%Y')}<br>⚠️ Status: {row['Status']}" for _, row in gruppe.iterrows()]
                    
                    # KLEINERE AMPEL-PUNKTE MIT GLOW-EFFEKT & VOLLSTÄNDIGER MATRIX
                    fig.add_trace(go.Scatter(
                        x=gruppe["Monat_Name"], y=gruppe["bezeichnung"], mode="markers", name=status_name,
                        marker=dict(
                            size=8, 
                            color=farbe_auswahl, 
                            opacity=0.9,
                            line=dict(width=1.5, color=farbe_auswahl)
                        ),
                        text=hover_texts,
                        hoverinfo="text"
                    ))
                    
                fig.update_layout(
                    title=TXT_PLAN["chart_title"],
                    font=dict(color=chart_text),
                    xaxis=dict(
                        title=None, 
                        type="category", 
                        categoryorder="array", 
                        categoryarray=monats_namen, 
                        range=[-0.5, 11.5], 
                        showgrid=True,
                        gridcolor=chart_grid, 
                        gridwidth=1,
                        zeroline=False, 
                        tickfont=dict(color=chart_text)
                    ),
                    yaxis=dict(
                        title=None, 
                        showticklabels=True, 
                        showgrid=True,
                        gridcolor=chart_grid, 
                        gridwidth=1,
                        zeroline=False, 
                        tickfont=dict(color=chart_text),
                        automargin=True
                    ),
                    showlegend=True, hovermode="closest", 
                    paper_bgcolor=chart_bg, 
                    plot_bgcolor=chart_bg, 
                    height=dynamische_hoehe, 
                    margin=dict(l=10, r=10, t=40, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                no_term_msg = "ℹ️ Keine fälligen oder anstehenden Termine im gewählten Filter." if st.session_state.language == "de" else "ℹ️ No due or upcoming appointments in the selected filter."
                st.info(no_term_msg)

        st.markdown("---")
        if not df_chart.empty:
            # Hier greifen wir nun auf alle im Chart sichtbaren (fälligen & anstehenden) Termine zu
            df_roote_vertraege = df_chart.drop_duplicates(subset=["id"])
            if not df_roote_vertraege.empty:
                if st.session_state.language == "de":
                    fristen_subtext = "Fristen-Feinsteuerung (Wochenweise) für fällige & anstehende Termine"
                else:
                    fristen_subtext = "Deadline Fine-Tuning (Weekly) for Due & Pending Appointments"

                st.markdown(f"<p style='font-size: 11px; font-weight: bold; color: #4a90e2; letter-spacing: 1px;'>FRISTEN MANAGER &nbsp;|&nbsp; <span style='font-size: 10px; font-weight: normal; font-style: italic; opacity: 0.8;'>{fristen_subtext}</span></p>", unsafe_allow_html=True)
                liste_roote_labels = [f"[ID: {r['id']}] {r['bezeichnung']} ({r['Status']}) - {r['Datum'].strftime('%d.%m.%Y')}" if st.session_state.language == "de" else f"[ID: {r['id']}] {r['bezeichnung']} ({r['Status']}) - {r['Datum'].strftime('%m/%d/%Y')}" for _, r in df_roote_vertraege.iterrows()]
                
                col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns([4.0, 1.5, 1.5, 1.5, 1.5])
                with col_m1:
                    sel_lbl = "Anlage wählen:" if st.session_state.language == "de" else "Select Asset:"
                    v_schieb_auswahl = st.selectbox(sel_lbl, [""] + liste_roote_labels, label_visibility="collapsed", key="v_schieb_select_v12_unique_clean")
                
                if v_schieb_auswahl:
                    v_id_bereinigt = v_schieb_auswahl.replace("[ID:", "").strip()
                    v_schieb_id = int(v_id_bereinigt.split("]")[0].strip())
                    
                    row_target = df_roote_vertraege[df_roote_vertraege["id"] == v_schieb_id]
                    if not row_target.empty:
                        basis_datum = pd.to_datetime(row_target["Datum"].values[0])

                        if not pd.isnull(basis_datum):
                            with col_m2:
                                if st.button("⏪ -2W", use_container_width=True, key=f"btn_m2w_{v_schieb_id}"):
                                    st.success("Termin 2 Wochen vorverlegt!" if st.session_state.language == "de" else "Advanced by 2 weeks!")
                                    st.rerun()
                            with col_m3:
                                if st.button("◀️ -1W", use_container_width=True, key=f"btn_m1w_{v_schieb_id}"):
                                    st.success("Termin 1 Woche vorverlegt!" if st.session_state.language == "de" else "Advanced by 1 week!")
                                    st.rerun()
                            with col_m4:
                                if st.button("▶️ +1W", use_container_width=True, key=f"btn_p1w_{v_schieb_id}"):
                                    st.success("Termin 1 Woche verschoben!" if st.session_state.language == "de" else "Postponed by 1 week!")
                                    st.rerun()
                            with col_m5:
                                if st.button("⏩ +2W", use_container_width=True, key=f"btn_p2w_{v_schieb_id}"):
                                    st.success("Termin 2 Wochen verschoben!" if st.session_state.language == "de" else "Postponed by 2 weeks!")
                                    st.rerun()
            st.write("")
            if st.session_state.language == "de":
                spalten_u = {
                    "id": "Vertrag-ID", "anlagenid": "Anlagen-ID", "bezeichnung": "Vertragsbezeichnung",
                    "firma": "Wartungsfirma", "standort": "Standort", "zyklusmonate": "Intervall",
                    "letztewartung": "Letzte Wartung", "naechstewartung": "Nächste Wartung"
                }
            else:
                spalten_u = {
                    "id": "Contract ID", "anlagenid": "Asset ID", "bezeichnung": "Contract Designation",
                    "firma": "Maintenance Company", "standort": "Location", "zyklusmonate": "Interval",
                    "letztewartung": "Last Maintenance", "naechstewartung": "Next Maintenance"
                }

            df_u_fil_schick = df_u_fil.copy()
            df_u_fil_schick.rename(columns=spalten_u, inplace=True)
            
            col_next_exam = "Nächste Prüfung" if st.session_state.language == "de" else "Next Inspection"
            col_year_1 = "Jahr 1" if st.session_state.language == "de" else "Year 1"
            next_maint_key = "Nächste Wartung" if st.session_state.language == "de" else "Next Maintenance"

            df_u_fil_schick[col_next_exam] = pd.to_datetime(df_u_fil_schick[next_maint_key], errors="coerce").dt.date + timedelta(days=365)
            df_u_fil_schick[col_year_1] = df_u_fil_schick[next_maint_key]
            
            c_id_col = "Vertrag-ID" if st.session_state.language == "de" else "Contract ID"
            a_id_col = "Anlagen-ID" if st.session_state.language == "de" else "Asset ID"
            c_des_col = "Vertragsbezeichnung" if st.session_state.language == "de" else "Contract Designation"
            m_comp_col = "Wartungsfirma" if st.session_state.language == "de" else "Maintenance Company"
            loc_col = "Standort" if st.session_state.language == "de" else "Location"
            int_col = "Intervall" if st.session_state.language == "de" else "Interval"
            last_m_col = "Letzte Wartung" if st.session_state.language == "de" else "Last Maintenance"

            st.dataframe(
                df_u_fil_schick[[c_id_col, a_id_col, c_des_col, m_comp_col, loc_col, int_col, last_m_col, next_maint_key, col_next_exam, col_year_1]], 
                use_container_width=True, hide_index=True
            )
            st.write("")
            
            class ESM_PDF(FPDF):
                def header(self):
                    self.set_font("Helvetica", "B", 12)
                    self.set_text_color(30, 136, 229)
                    title_pdf = "Europäische Schule München - Wartungsmanagement" if st.session_state.language == "de" else "European School Munich - Maintenance Management"
                    self.cell(0, 10, title_pdf, ln=True, align="L")
                    self.line(10, 18, 200, 18)
                    self.ln(5)
                def footer(self):
                    self.set_y(-15)
                    self.set_font("Helvetica", "I", 8)
                    self.set_text_color(100, 116, 139)
                    lbl_page = "Seite" if st.session_state.language == "de" else "Page"
                    gen_lbl = "Generiert am" if st.session_state.language == "de" else "Generated on"
                    self.cell(0, 10, f"{gen_lbl} {datetime.now().strftime('%d.%m.%Y %H:%M')} | {lbl_page} {self.page_no()}", align="C")

            pdf = ESM_PDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 14)
            doc_title = "Strategischer Wartungsplan (Audit-Bericht)" if st.session_state.language == "de" else "Strategic Maintenance Plan (Audit Report)"
            pdf.cell(0, 10, doc_title, ln=True)
            pdf.ln(5)
            pdf.set_font("Helvetica", "", 10)
            
            for idx, row in df_u_fil_schick.head(35).iterrows():
                bez_val = str(row.get(c_des_col, ""))
                std_val = str(row.get(loc_col, ""))
                frm_val = str(row.get(m_comp_col, ""))
                nxt_val = str(row.get(next_maint_key, ""))
                
                if st.session_state.language == "de":
                    text_line = f"Anlage: {bez_val} ({std_val}) | Firma: {frm_val} | Nächste Wartung: {nxt_val}"
                else:
                    text_line = f"Asset: {bez_val} ({std_val}) | Company: {frm_val} | Next Maintenance: {nxt_val}"
                    
                text_line = text_line.replace("Ä", "Ae").replace("ä", "ae").replace("Ö", "Oe").replace("ö", "oe").replace("Ü", "Ue").replace("ü", "ue")
                pdf.cell(0, 7, text_line.encode('latin-1', 'ignore').decode('latin-1'), ln=True)
            
            pdf_raw = pdf.output(dest='S')
            pdf_bytes = bytes(pdf_raw) if isinstance(pdf_raw, bytearray) else pdf_raw
            btn_dl_lbl = "📄 Strategischen 5-Jahresplan als PDF exportieren" if st.session_state.language == "de" else "📄 Export Strategic 5-Year Plan as PDF"
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(label=btn_dl_lbl, data=pdf_bytes, file_name=f"ESM_Maintenance_Plan_{datetime.now().strftime('%Y%m%d')}.pdf", mime="application/pdf", key="download_btn_5y_plan_pdf")
