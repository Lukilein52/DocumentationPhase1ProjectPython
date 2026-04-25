from datetime import date, timedelta

class Studium:
    def __init__(self, name: str, moegliche_ects: int,
                 startdatum: date, enddatum: date, semester=None):
        self.name = name
        self.moegliche_ects = moegliche_ects
        self.startdatum = startdatum
        self.enddatum = enddatum
        self.semester = semester or []

    def gesamt_ects(self) -> int:
        return sum(s.semester_ects() for s in self.semester)

    def verbleibende_zeit(self) -> timedelta:
        return max(timedelta(0), self.enddatum - date.today())

    def tage_studiert(self) -> int:
        return max(0, (date.today() - self.startdatum).days)

    def fortschritt_prozent(self) -> float:
        if self.moegliche_ects == 0:
            return 0.0
        return min(100.0, self.gesamt_ects() / self.moegliche_ects * 100)

    def ects_pro_monat(self) -> dict:
        monate_order = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
                        "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
        result = {m: 0 for m in monate_order}
        for sem in self.semester:
            for modul in sem.module:
                if modul.abgabe_bestanden() and modul.monat in result:
                    result[modul.monat] += modul.ects_kurs
        return result
