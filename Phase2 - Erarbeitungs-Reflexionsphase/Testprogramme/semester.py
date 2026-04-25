from datetime import timedelta

class Semester:
    def __init__(self, name: str, dauer_tage: int, module=None):
        self.name = name
        self.dauer = timedelta(days=dauer_tage)
        self.module = module or []

    def semester_ects(self) -> int:
        return sum(m.ects_kurs for m in self.module if m.abgabe_bestanden())
