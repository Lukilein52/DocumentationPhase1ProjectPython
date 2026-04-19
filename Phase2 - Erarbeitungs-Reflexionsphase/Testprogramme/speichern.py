import json
from datetime import date

from modul import Modul
from pruefungsleistung import Pruefungsleistung
from semester import Semester
from studium import Studium


class Speichern:
    def __init__(self, dateipfad: str):
        self.__dateipfad = dateipfad

    def speichern(self, studium) -> None:
        daten = self.__zu_json(studium)
        with open(self.__dateipfad, 'w', encoding='utf-8') as f:
            json.dump(daten, f, ensure_ascii=False, indent=2)

    def laden(self):
        with open(self.__dateipfad, 'r', encoding='utf-8') as f:
            daten = json.load(f)
        return self.__von_json(daten)

    def __zu_json(self, studium) -> dict:
        return {
            "bezeichnung": studium._Studium__bezeichnung,
            "startjahr": studium._Studium__startjahr,
            "abschlusstitel": studium._Studium__abschlusstitel,
            "semester": [
                {
                    "nummer": s._Semester__nummer,
                    "bezeichnung": s._Semester__bezeichnung,
                    "module": [
                        {
                            "name": k._Kurs__name,
                            "modul_id": k._Kurs__kurs_id,
                            "credits": k._Kurs__credits,
                            "pruefungsleistungen": [
                                {
                                    "titel": pl._Pruefungsleistung__titel,
                                    "typ": pl._Pruefungsleistung__typ,
                                    "datum": str(pl._Pruefungsleistung__datum),
                                    "note": pl._Pruefungsleistung__note,
                                    "gewichtung": pl._Pruefungsleistung__gewichtung
                                }
                                for pl in k.get_pruefungsleistungen()
                            ]
                        }
                        for k in s.get_kurse()
                    ]
                }
                for s in studium.get_semester()
            ]
        }

    def __von_json(self, daten: dict):
        from datetime import date
        studium = Studium(
            daten["bezeichnung"],
            daten["startjahr"],
            daten["abschlusstitel"]
        )
        for s_daten in daten["semester"]:
            semester = Semester(s_daten["nummer"], s_daten["bezeichnung"])
            for k_daten in s_daten["Module"]:
                modul = Modul(k_daten["name"], k_daten["modul_id"], k_daten["credits"])
                for pl_daten in k_daten["pruefungsleistungen"]:
                    datum = date.fromisoformat(pl_daten["datum"])
                    pl = Pruefungsleistung(
                        pl_daten["titel"],
                        pl_daten["typ"],
                        datum,
                        pl_daten["note"],
                        pl_daten["gewichtung"]
                    )
                    modul.add_pruefungsleistung(pl)
                semester.add_modul(modul)
            studium.add_semester(semester)
        return studium