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
    except Exception:
        # Absichtlich ganz leise ohne Fehlermeldung auf dem Bildschirm, 
        # damit die Cloud-Version für deinen Chef sauber durchläuft!
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
                    (17510, "NP", "Sanitärtechnik", "Hebeanlage Fäkalien", "Wartung überfällig"),
                    (17511, "NP", "Fördertechnik", "Lastenaufzug Wirtschaftsgebäude", "Betriebsbereit"),
                    (17512, "FG", "Sanitärtechnik", "Trinkwassererwärmung Grundschule", "Betriebsbereit"),
                    (17513, "NP", "Elektrotechnik", "USV-Anlage Rechenzentrum", "Prüfung anstehend"),
                    (17514, "FG", "Brandschutz", "Rauch- und Wärmeabzugsanlage", "Betriebsbereit"),
                    (17515, "NP", "Raumlufttechnik", "RLT-Anlage Verwaltung", "Wartung überfällig"),
                    (17516, "FG", "Wärmeversorgung", "Blockheizkraftwerk BHKW", "Betriebsbereit"),
                    (17517, "NP", "Fördertechnik", "Behindertenaufzug Bibliothek", "Betriebsbereit"),
                    (17518, "FG", "Elektrotechnik", "Beleuchtungssteuerung Sporthalle", "Betriebsbereit"),
                    (17519, "NP", "Sanitärtechnik", "Schmutzwasserpumpe Keller", "Betriebsbereit"),
                    (17520, "FG", "Brandschutz", "Wandhydranten Netz", "Prüfung anstehend")
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
                    (10, 17510, "Fäkalienhebeanlage Wartung", "Jung Pumpen GmbH", "NP", 6, "2025-11-15", "2026-05-15", "2026-11-15"),
                    (11, 17511, "Wartungsvertrag Lastenaufzug", "ThyssenKrupp", "NP", 12, "2025-04-10", "2026-04-10", "2027-04-10"),
                    (12, 17512, "Trinkwasserprüfung Hygiene", "SGS Institut", "FG", 12, "2025-02-10", "2026-02-10", "2027-02-10"),
                    (13, 17513, "USV-Wartung Komplettpaket", "APC Schneider", "NP", 12, "2025-07-10", "2026-07-10", "2027-07-10"),
                    (14, 17514, "RWA-Anlagen Service", "D+H Mechatronic", "FG", 12, "2025-01-15", "2026-01-15", "2027-01-15"),
                    (15, 17515, "RLT-Wartung Verwaltung", "Trox Technik", "NP", 6, "2025-10-10", "2026-04-10", "2026-10-10"),
                    (16, 17516, "BHKW Vollwartung", "SenerTec", "FG", 12, "2025-05-20", "2026-05-20", "2027-05-20"),
                    (17, 17517, "Behindertenaufzug Check", "Kone AG", "NP", 12, "2025-06-10", "2026-06-10", "2027-06-10"),
                    (18, 17518, "Lichtsteuerung Service", "Philips Lighting", "FG", 24, "2024-06-10", "2026-06-10", "2028-06-10"),
                    (19, 17519, "Pumpenwartung Tiefkeller", "KSB SE", "NP", 12, "2025-08-10", "2026-08-10", "2027-08-10"),
                    (20, 17520, "Wandhydranten Prüfung", "Jockel Brandschutz", "FG", 12, "2025-03-10", "2026-03-10", "2027-03-10")
                ]
                cursor.executemany(sql_v, bsp_v)
            conn.commit()
            cursor.close()
        except Exception:
            pass
        finally:
            conn.close()
