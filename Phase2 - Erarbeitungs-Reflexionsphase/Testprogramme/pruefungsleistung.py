from datetime import date, datetime


class Pruefungsleistung:
    def __init__(self, titel: str, datum: date, note: float, ects: int):
        self.titel = titel
        self.datum = datum
        self.note = note
        self.ects = ects

    # getter
    def get_titel(self) -> str:
        return self.titel

    def get_datum(self) -> date:
        return self.datum

    def get_note(self) -> str:
        return self.note

    def get_ects(self) -> int:
        return self.ects

    # Methoden
    def bestanden(self) -> bool:
        if self.note <= 4.0 and self.note >= 1.0:
            return True
        else:
            return False


def bestanden():
    return None