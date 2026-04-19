import pruefungsleistung
from pruefungsleistung import Pruefungsleistung


class Modul:
    def __init__(self, name: str, ects: int):
        self.name = name
        self.ects = ects
        self.pruefungsleistung = []

    def add_pruefungsleistung(self, pl: Pruefungsleistung):
        self.pruefungsleistung.append(pl)

    def get_pruefungsleistung(self):
        return self.pruefungsleistung

    def berstanden(self):
        return all(pruefungsleistung.bestanden() for pl in self.pruefungsleistung)