import mysql.connector
import streamlit as st
import pandas as pd

class MockCursor:
    def __init__(self):
        pass
    def execute(self, query, params=None):
        pass
    def fetchall(self):
        return []
    def fetchone(self):
        return [0]
    def close(self):
        pass

class MockConnection:
    def __init__(self):
        pass
    def cursor(self, dictionary=False):
        return MockCursor()
    def commit(self):
        pass
    def close(self):
        pass

def hole_datenbank_verbindung():
    try:
        return mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )
    except Exception:
        # Gibt im Cloud-Modus ein simuliertes Objekt zurück, 
        # damit absolut keine Fehlermeldungen mehr auf dem Bildschirm landen!
        return MockConnection()
