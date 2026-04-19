import tkinter as tk
from tkinter import ttk, messagebox

from modul import Modul
from pruefungsleistung import Pruefungsleistung
from semester import Semester
from speichern import Speichern
from studium import Studium


class Dashboard:
    def __init__(self, studium: Studium):
        self.__studium = studium
        self.__speichern = Speichern("studium.json")

        # Hauptfenster
        self.__fenster = tk.Tk()
        self.__fenster.title("Studium Dashboard")
        self.__fenster.geometry("600x500")
        self.__gui_aufbauen()

    def __gui_aufbauen(self):
        # Titel
        titel_label = tk.Label(
            self.__fenster,
            text=self.__studium.get_info(),
            font=("Arial", 16, "bold")
        )
        titel_label.pack(pady=10)

        # Treeview für Semester, Kurse, Prüfungsleistungen
        self.__baum = ttk.Treeview(self.__fenster)
        self.__baum.heading("#0", text="Studium", anchor="w")
        self.__baum.pack(fill="both", expand=True, padx=10, pady=10)

        self.__baum_befuellen()

        # Buttons
        button_frame = tk.Frame(self.__fenster)
        button_frame.pack(pady=10)

        speichern_btn = tk.Button(
            button_frame,
            text="Speichern",
            command=self.auf_speichern_klicken,
            width=15
        )
        speichern_btn.grid(row=0, column=0, padx=5)

        laden_btn = tk.Button(
            button_frame,
            text="Laden",
            command=self.auf_laden_klicken,
            width=15
        )
        laden_btn.grid(row=0, column=1, padx=5)

        aktualisieren_btn = tk.Button(
            button_frame,
            text="Aktualisieren",
            command=self.aktualisieren,
            width=15
        )
        aktualisieren_btn.grid(row=0, column=2, padx=5)

    def __baum_befuellen(self):
        # Baum leeren
        for item in self.__baum.get_children():
            self.__baum.delete(item)

        # Semester einfügen
        for semester in self.__studium.get_semester():
            sem_id = self.__baum.insert(
                "", "end",
                text=str(semester),
                open=True
            )

            # Kurse einfügen
            for modul in semester.get_kurse():
                status = "✓" if modul.bestanden() else "✗"
                kurs_id = self.__baum.insert(
                    sem_id, "end",
                    text=f"[{status}] {modul}",
                    open=True
                )

                # Prüfungsleistungen einfügen
                for pl in modul.get_pruefungsleistung():
                    self.__baum.insert(
                        kurs_id, "end",
                        text=str(pl)
                    )

    def aktualisieren(self) -> None:
        self.__baum_befuellen()

    def auf_speichern_klicken(self) -> None:
        self.__speichern.speichern(self.__studium)
        messagebox.showinfo("Erfolg", "Daten wurden gespeichert!")

    def auf_laden_klicken(self) -> None:
        self.__studium = self.__speichern.laden()
        self.__baum_befuellen()
        messagebox.showinfo("Erfolg", "Daten wurden geladen!")

    def starten(self) -> None:
        self.__fenster.mainloop()


if __name__ == "__main__":
    from datetime import date

    # Daten erstellen
    studium = Studium("Informatik", 2023, "Bachelor")
    semester1 = Semester(1, "Wintersemester 2023")
    modul1 = Modul("Mathematik 1", 5)
    pl1 = Pruefungsleistung("Klausur", date(2024, 1, 15), 2.0, 5)

    modul1.add_pruefungsleistung(pl1)
    semester1.add_kurs(modul1)
    studium.add_semester(semester1)

    # Dashboard starten
    dashboard = Dashboard(studium)
    dashboard.starten()