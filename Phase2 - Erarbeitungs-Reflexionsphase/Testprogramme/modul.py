class Modul:
    def __init__(self, name: str, ects_kurs: int, bestanden: bool = False,
                 pruefung=None, monat: str = "Jan"):
        self.name = name
        self.bestanden = bestanden
        self.ects_kurs = ects_kurs
        self.pruefung = pruefung
        self.monat = monat

    def abgabe_bestanden(self) -> bool:
        if self.pruefung:
            return self.pruefung.ist_bestanden()
        return self.bestanden
