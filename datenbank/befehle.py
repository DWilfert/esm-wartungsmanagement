import streamlit as st
import pandas as pd

def hole_datenbank_verbindung():
    # Gibt None zurück, damit keine störende Demo-Meldung auf dem Bildschirm erscheint, aber die App stabil bleibt
    return None

def initialisiere_beispieldaten():
    pass

def hole_anlagen_daten():
    return pd.DataFrame({
        "id": [17501 + i for i in range(20)],
        "standort": ["NP" if i % 2 == 0 else "FG" for i in range(20)],
        "anlagentyp": ["Fördertechnik", "Raumlufttechnik", "Elektrotechnik", "Wärmeversorgung", "Brandschutz"] * 4,
        "bezeichnung": [f"Test-Anlage Beschreibung Nummer {i+1}" for i in range(20)],
        "zustand": ["Betriebsbereit", "Wartung überfällig", "Prüfung anstehend", "Betriebsbereit", "Betriebsbereit"] * 4
    })

def hole_wartungsvertraege_daten():
    return pd.DataFrame({
        "id": [i+1 for i in range(20)],
        "anlagenid": [17501 + i for i in range(20)],
        "bezeichnung": [f"Vollwartungsvertrag Objekt {i+1}" for i in range(20)],
        "firma": ["Otis GmbH", "Schindler AG", "Stulz GmbH", "Siemens AG", "Viessmann Werke"] * 4,
        "standort": ["NP" if i % 2 == 0 else "FG" for i in range(20)],
        "zyklusmonate": [12, 6, 12, 24, 12] * 4,
        "letztewartung": ["2025-05-10"] * 20,
        "naechstewartung": ["2026-05-10", "2026-03-15", "2027-01-10", "2026-06-01", "2028-02-20"] * 4,
        "weiterwartung": ["2027-05-10"] * 20,
        "status": ["In Ordnung", "Überfällig", "Anstehend", "In Ordnung", "In Ordnung"] * 4
    })
