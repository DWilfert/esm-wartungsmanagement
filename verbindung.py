import mysql.connector
import streamlit as st
import pandas as pd

def hole_datenbank_verbindung():
    try:
        return mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=int(st.secrets["mysql"]["port"])
        )
    except Exception:
        return None

def initialisiere_beispieldaten():
    pass

def hole_anlagen_daten():
    conn = hole_datenbank_verbindung()
    if conn is not None:
        try:
            return pd.read_sql("SELECT * FROM anlagen", conn)
        except Exception:
            pass
    return pd.DataFrame({
        "id": [17501 + i for i in range(20)],
        "standort": ["NP" if i % 2 == 0 else "FG" for i in range(20)],
        "anlagentyp": ["Fördertechnik", "Raumlufttechnik", "Elektrotechnik", "Wärmeversorgung", "Brandschutz"] * 4,
        "bezeichnung": [f"Test-Anlage Beschreibung Nummer {i+1}" for i in range(20)],
        "zustand": ["Betriebsbereit", "Wartung überfällig", "Prüfung anstehend", "Betriebsbereit", "Betriebsbereit"] * 4
    })

def hole_wartungsvertraege_daten():
    conn = hole_datenbank_verbindung()
    if conn is not None:
        try:
            return pd.read_sql("SELECT * FROM wartungsvertraege", conn)
        except Exception:
            pass
    return pd.DataFrame({
        "id": [i+1 for i in range(20)],
        "anlagenid": [17501 + i for i in range(20)],
        "bezeichnung": [f"Vollwartungsvertrag Objekt {i+1}" for i in range(20)],
        "firma": ["Otis GmbH", "Schindler AG", "Stulz GmbH", "Siemens AG", "Viessmann Werke"] * 4,
        "standort": ["NP" if i % 2 == 0 else "FG" for i in range(20)],
        "zyklusmonate": [12, 6, 12, 24, 12] * 4,
        "letztewartung": ["2025-05-10"] * 20,
        "naechstewartung": ["2026-05-10"] * 20,
        "weiterwartung": ["2027-05-10"] * 20
    })
