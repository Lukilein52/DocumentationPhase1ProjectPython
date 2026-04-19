class Studium:
    def __init__(self, bezeichnung: str, startjahr: int, abschlusstitel: str):
        self.__bezeichnung = bezeichnung
        self.__startjahr = startjahr
        self.__abschlusstitel = abschlusstitel
        self.__semester = []  # Komposition

    def add_semester(self, semester):
        self.__semester.append(semester)

    def get_semester(self) -> list:
        return self.__semester

    def get_info(self) -> str:
        return f"{self.__abschlusstitel} in {self.__bezeichnung} (ab {self.__startjahr})"

    def __str__(self) -> str:
        return self.get_info()