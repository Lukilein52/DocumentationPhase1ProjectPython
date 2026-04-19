class Semester:
    def __init__(self, nummer: int, bezeichnung: str):
        self.__nummer = nummer
        self.__bezeichnung = bezeichnung  # z.B. "Wintersemester 2024"
        self.__kurse = []  # Aggregation

    def add_kurs(self, kurs):
        self.__kurse.append(kurs)

    def get_kurse(self) -> list:
        return self.__kurse

    def get_ects(self) -> int:
        return sum(kurs.get_credits() for kurs in self.__kurse)

    def __str__(self) -> str:
        return f"Semester {self.__nummer}: {self.__bezeichnung}"