import streamlit as st
import pandas as pd

def zeige_globale_suche():
    st.subheader("🔍 Globale 360° Volltextsuche")
    
    suchbegriff = st.text_input("Suchbegriff eingeben...", key="globaler_such_input")
    
    if not suchbegriff.strip():
        st.info("Bitte geben Sie einen Suchbegriff ein.")
        return

    term = suchbegriff.strip().lower()

    # Lokale Demodaten direkt auf der Seite definieren (identisch zu den anderen Ansichten)
    df_anlagen = pd.DataFrame({
        "id": [17501, 17502, 17503, 17504, 17505],
        "standort": ["Fasangarten", "Neuperlach", "Fasangarten", "Neuperlach", "Fasangarten"],
        "anlagentyp": ["Fördertechnik", "Raumlufttechnik", "Elektrotechnik", "Wärmeversorgung", "Brandschutz"],
        "bezeichnung": [
            "Hauptaufzug Gebäude A", 
            "Lüftungsanlage Zentral", 
            "Hauptverteiler Elektrik", 
            "Heizkessel Anlage 2", 
            "Rauchmeldezentrale Ost"
        ],
        "zustand": ["Betriebsbereit", "Wartung überfällig", "Prüfung anstehend", "Betriebsbereit", "Betriebsbereit"],
        "hersteller": ["Otis", "Stulz", "Siemens", "Viessmann", "Hilti"],
        "raum": ["U01", "Dachboden", "E05", "Keller", "Foyer"]
    })

    df_vertraege = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "bezeichnung": [
            "Vollwartungsvertrag Aufzugsanlagen", 
            "Wartung Lüftungstechnik", 
            "Jahresinspektion Elektrik", 
            "Wärmeversorgung Service", 
            "Brandschutzprüfung"
        ],
        "firma": ["Otis GmbH", "Stulz GmbH", "Siemens AG", "Viessmann Werke", "Hilti Service"]
    })

    # Suche durchführen
    mask_a = df_anlagen.astype(str).apply(lambda col: col.str.lower().str.contains(term, na=False)).any(axis=1)
    res_anlagen = df_anlagen[mask_a].to_dict(orient="records")

    mask_v = df_vertraege.astype(str).apply(lambda col: col.str.lower().str.contains(term, na=False)).any(axis=1)
    res_vertraege = df_vertraege[mask_v].to_dict(orient="records")

    gesamt = len(res_anlagen) + len(res_vertraege)

    if gesamt == 0:
        st.warning(f"Keine Treffer für: '{suchbegriff}'")
        return

    st.success(f"🎉 {gesamt} Treffer gefunden!")
    
    if res_anlagen:
        st.markdown("##### Treffer bei Anlagen")
        st.dataframe(pd.DataFrame(res_anlagen), use_container_width=True, hide_index=True)
        
    if res_vertraege:
        st.markdown("##### Treffer bei Verträgen")
        st.dataframe(pd.DataFrame(res_vertraege), use_container_width=True, hide_index=True)
