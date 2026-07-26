import mysql.connector
import streamlit as st
import pandas as pd

def hole_datenbank_verbindung():
    try:
        return mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )
    except Exception as e:
        st.error(f"Datenbankverbindungsfehler: {str(e)}")
        return None

def initialisiere_beispieldaten():
    conn = hole_datenbank_verbindung()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM `anlagen`")
            if cursor.fetchone()[0] == 0:
                sql = "INSERT INTO `anlagen` (id, standort, anlagentyp, bezeichnung, zustand) VALUES (%s,%s,%s,%s,%s)"
                bsp = [
                    (17501, "NP", "Fördertechnik", "Personenaufzug Hauptgebäude", "Betriebsbereit"),
                    (17502, "FG", "Fördertechnik", "Personenaufzug Grundschule", "Betriebsbereit"),
                    (17503, "NP", "Raumlufttechnik", "RTL-Anlage Serverraum", "Betriebsbereit"),
                    (17504, "NP", "Elektrotechnik", "Netzersatzanlage Diesel", "Wartung überfällig"),
                    (17505, "FG", "Wärmeversorgung", "Heizkessel Turnhalle", "Prüfung anstehend"),
                    (17506, "NP", "Brandschutz", "Brandmeldezentrale BMZ", "Betriebsbereit"),
                    (17507, "FG", "Raumlufttechnik", "RLT-Anlage Mensaküche", "Betriebsbereit"),
                    (17508, "NP", "Wärmeversorgung", "Fernwärmestation Aula", "Betriebsbereit"),
                    (17509, "FG", "Elektrotechnik", "Hauptverteilung NSHV", "Prüfung anstehend"),
                    (17510, "NP", "Sanitärtechnik", "Hebeanlage Fäkalien", "Wartung überfällig")
                ]
                cursor.executemany(sql, bsp)
                
            cursor.execute("SELECT COUNT(*) FROM `wartungsvertraege`")
            if cursor.fetchone()[0] == 0:
                sql_v = "INSERT INTO `wartungsvertraege` (id, anlagenid, bezeichnung, firma, standort, zyklusmonate, letztewartung, naechstewartung, weiterewartung) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                bsp_v = [
                    (1, 17501, "Vollwartung Personenaufzug NP", "Otis GmbH", "NP", 12, "2025-05-10", "2026-05-10", "2027-05-10"),
                    (2, 17502, "Intervallwartung Lastenaufzug", "Schindler AG", "FG", 12, "2025-08-15", "2026-08-15", "2027-08-15"),
                    (3, 17503, "Systempflege Serverklima NP", "Stulz GmbH", "NP", 6, "2026-05-20", "2026-11-20", "2027-05-20"),
                    (4, 17504, "Leistungsprüfung NEA Diesel", "Caterpillar Service", "NP", 12, "2025-06-01", "2026-06-01", "2027-06-01"),
                    (5, 17505, "Kesselwartung Sportkomplex", "Viessmann Werke", "FG", 12, "2025-09-10", "2026-09-10", "2027-09-10"),
                    (6, 17506, "Wartung Brandmeldezentrale", "Siemens AG", "NP", 3, "2026-06-15", "2026-09-15", "2026-12-15"),
                    (7, 17507, "Küchenabluft-Inspektion FG", "Klimaservice Süd", "FG", 6, "2026-06-25", "2026-12-25", "2027-06-25"),
                    (8, 17508, "Check Kompaktstation Aula", "Danfoss Service", "NP", 12, "2025-09-01", "2026-09-01", "2027-09-01"),
                    (9, 17509, "Prüfung NSHV Schaltanlage", "ABB Service", "FG", 48, "2024-03-10", "2028-03-10", "2032-03-10"),
                    (10, 17510, "Fäkalienhebeanlage Wartung", "Jung Pumpen GmbH", "NP", 6, "2025-11-15", "2026-05-15", "2026-11-15")
                ]
                cursor.executemany(sql_v, bsp_v)
            conn.commit()
            cursor.close()
        except Exception as e:
            st.error(f"Fehler bei Beispieldaten: {str(e)}")
        finally:
            conn.close()
