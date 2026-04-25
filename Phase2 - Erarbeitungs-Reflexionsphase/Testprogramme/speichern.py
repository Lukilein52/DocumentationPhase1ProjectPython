import os
import json

from datetime import date
from modul import Modul
from pruefungsleistung import Pruefungsleistung
from semester import Semester
from studium import Studium

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "studium_data.json")

class Speichern:

    def load_data(self) -> Studium:
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, encoding="utf-8") as f:
                    d = json.load(f)
                semester_list = []
                for sem in d.get("semester", []):
                    module = [
                        Modul(m["name"], m["ects_kurs"], m.get("bestanden", False),
                              Pruefungsleistung(m["note"]) if m.get("note") is not None else None,
                              m.get("monat", "Jan"))
                        for m in sem.get("module", [])
                    ]
                    semester_list.append(Semester(sem["name"], sem["dauer_tage"], module))
                return Studium(d["name"], d["moegliche_ects"],
                               date.fromisoformat(d["startdatum"]),
                               date.fromisoformat(d["enddatum"]),
                               semester_list)
            except Exception as e:
                print(f"Ladefehler: {e}")

        # Demo-Daten
        module_s1 = [
            Modul("Mathematik I", 8, pruefung=Pruefungsleistung(2), monat="Jan"),
            Modul("Programmierung", 6, pruefung=Pruefungsleistung(1), monat="Feb"),
            Modul("BWL Grundlagen", 5, pruefung=Pruefungsleistung(3), monat="Feb"),
        ]
        module_s2 = [
            Modul("Mathematik II", 8, pruefung=Pruefungsleistung(3), monat="Mär"),
            Modul("Datenbanken", 6, pruefung=Pruefungsleistung(2), monat="Apr"),
            Modul("Statistik", 5, pruefung=Pruefungsleistung(4), monat="Apr"),
            Modul("Algorithmen", 6, bestanden=False, monat="Mai"),
        ]
        module_s3 = [
            Modul("Softwareentwicklung", 7, bestanden=False, monat="Mai"),
            Modul("Netzwerke", 5, bestanden=False, monat="Jun"),
        ]
        return Studium("Informatik B.Sc.", 180,
                       date(2023, 10, 1), date(2026, 9, 30),
                       [Semester("Semester 1", 180, module_s1),
                        Semester("Semester 2", 180, module_s2),
                        Semester("Semester 3", 180, module_s3)])

    def save_data(studium: Studium):
        d = {
            "name": studium.name,
            "moegliche_ects": studium.moegliche_ects,
            "startdatum": studium.startdatum.isoformat(),
            "enddatum": studium.enddatum.isoformat(),
            "semester": [
                {"name": s.name, "dauer_tage": s.dauer.days,
                 "module": [{"name": m.name, "ects_kurs": m.ects_kurs,
                             "bestanden": m.bestanden,
                             "note": m.pruefung.note if m.pruefung else None,
                             "monat": m.monat} for m in s.module]}
                for s in studium.semester
            ]
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
