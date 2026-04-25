class Pruefungsleistung:
    def __init__(self, note: int):
        self.note = note

    def ist_bestanden(self) -> bool:
        return self.note <= 4

# Getter und Setter

    def get_note(self) -> int:
        return self.note

    def set_note(self, note: int):
        self.note = note