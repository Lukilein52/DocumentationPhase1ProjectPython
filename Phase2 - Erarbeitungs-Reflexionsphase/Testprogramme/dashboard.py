import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import speichern
from constants import *
import matplotlib
from modul import Modul
from pruefungsleistung import Pruefungsleistung
matplotlib.use("TkAgg")
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import studium as studium


class Dashboard:
    def __init__(self, root: tk.Tk, studium: studium.Studium):
        self.root = root
        self.studium = studium
        self.root.title("Studium Dashboard")
        self.root.configure(bg=BG)
        self.root.geometry("1920x1080")
        self.root.minsize(900, 580)
        self.root.state("zoomed")
        self._build_ui()
        self.anzeigen()

    # ── Layout ──────────────────────────────

    def _card(self, parent, title: str) -> tk.Frame:
        outer = tk.Frame(parent, bg=BORD)
        tk.Label(outer, text=title, font=(FONT, 8, "bold"),
                 fg=MUTED, bg=BORD).pack(anchor="w", padx=8, pady=(5, 0))
        inner = tk.Frame(outer, bg=CARD)
        inner.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        return inner

    def _build_ui(self):
        # ── Header ──
        hdr = tk.Frame(self.root, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(16, 0))

        self.lbl_title = tk.Label(hdr, text="", font=(FONT, 16, "bold"),
                                   fg=WHITE, bg=BG)
        self.lbl_title.pack(side="left")

        for txt, cmd, color in [
            ("💾 SPEICHERN", self._speichern, BLUE),
            ("＋ HINZUFÜGEN", self._dialog_modul, RED),
            ("⚙️ STUDIUM BEARBEITEN",self._daten_bearbeiten, ORANGE)
        ]:
            tk.Button(hdr, text=txt, command=cmd,
                      bg=CARD, fg=color, relief="flat",
                      font=(FONT, 9, "bold"),
                      activebackground=BORD, activeforeground=color,
                      highlightbackground=BORD, highlightthickness=1,
                      padx=10, pady=5).pack(side="right", padx=(0, 6))

        # ── Grid ──
        g = tk.Frame(self.root, bg=BG)
        g.pack(fill="both", expand=True, padx=20, pady=14)
        g.columnconfigure(0, weight=1)
        g.columnconfigure(1, weight=2)
        g.rowconfigure(0, weight=1)
        g.rowconfigure(1, weight=1)

        self.f_donut    = self._card(g, "ECTS")
        self.f_bar      = self._card(g, "ECTS / Monat")
        self.f_progress = self._card(g, "Studienzeit & Fortschritt")
        self.f_module   = self._card(g, "Module")

        self.f_donut.master.grid(   row=0, column=0, sticky="nsew", padx=(0, 6), pady=(0, 6))
        self.f_bar.master.grid(     row=0, column=1, sticky="nsew", padx=(6, 0), pady=(0, 6))
        self.f_progress.master.grid(row=1, column=0, sticky="nsew", padx=(0, 6), pady=(6, 0))
        self.f_module.master.grid(  row=1, column=1, sticky="nsew", padx=(6, 0), pady=(6, 0))

    # ── Anzeigen ────────────────────────────

    def anzeigen(self):
        s = self.studium
        self.lbl_title.config(
            text=f"Hallo {s.studierender}, Du studierst {s.name} seit {s.tage_studiert()} Tagen!")
        self.plot_donut()
        self.plot_ects_monat()
        self.plot_fortschritt()
        self._render_module()

    # ── Donut-Chart (ECTS) ──────────────────

    def plot_donut(self):
        for w in self.f_donut.winfo_children():
            w.destroy()

        s = self.studium
        ects  = s.gesamt_ects()
        maxe  = s.moegliche_ects
        frac  = min(ects / maxe, 1.0) if maxe else 0

        fig = Figure(figsize=(2.5, 2.5), facecolor=CARD)
        ax  = fig.add_axes([0.05, 0.05, 0.90, 0.90])
        ax.set_facecolor(CARD)
        ax.set_aspect("equal")
        ax.axis("off")

        # Hintergrund-Ring
        ax.add_patch(mpatches.Wedge((0, 0), 1.0, 0, 360, width=0.24,
                                     facecolor=BORD, zorder=1))
        # Fortschritts-Arc
        if frac > 0:
            ax.add_patch(mpatches.Wedge((0, 0), 1.0,
                                         90 - frac * 360, 90,
                                         width=0.24, facecolor=RED, zorder=2))
        # Innenkreis
        ax.add_patch(plt.Circle((0, 0), 0.76, color=CARD, zorder=3))

        ax.text(0,  0.12, str(ects), ha="center", va="center",
                fontsize=24, fontweight="bold", color=WHITE,
                fontfamily=FONT, zorder=4)
        ax.text(0, -0.20, f"/ {maxe}", ha="center", va="center",
                fontsize=12, color=MUTED, fontfamily=FONT, zorder=4)
        ax.text(0, -0.52, "ECTS", ha="center", va="center",
                fontsize=8,  color=MUTED, fontfamily=FONT, zorder=4)
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        c = FigureCanvasTkAgg(fig, master=self.f_donut)
        c.draw()
        c.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    # ── Balkendiagramm ECTS/Monat ───────────

    def plot_ects_monat(self):
        for w in self.f_bar.winfo_children():
            w.destroy()

        epm   = self.studium.ects_pro_monat()
        alle  = list(epm.keys())
        werte = list(epm.values())

        # Nur sinnvolle Monate zeigen
        aktive = [i for i, v in enumerate(werte) if v > 0]
        if aktive:
            end_idx = min(max(aktive) + 2, len(alle) - 1)
            idxs = list(range(0, end_idx + 1))
        else:
            idxs = list(range(6))

        labels = [alle[i]  for i in idxs]
        vals   = [werte[i] for i in idxs]
        colors = [RED if v > 0 else BORD for v in vals]

        fig = Figure(figsize=(5.0, 2.5), facecolor=CARD)
        ax  = fig.add_subplot(111)
        fig.patch.set_facecolor(CARD)
        style_ax(ax)

        bars = ax.bar(labels, vals, color=colors, width=0.6, zorder=2)
        ax.yaxis.grid(True, color=BORD, linewidth=0.5, zorder=0)
        ax.set_axisbelow(True)
        ax.set_ylabel("ECTS", color=MUTED, fontsize=8, fontfamily=FONT)

        for bar, v in zip(bars, vals):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.15, str(v),
                        ha="center", va="bottom",
                        color=WHITE, fontsize=7, fontfamily=FONT)

        fig.tight_layout(pad=1.0)
        c = FigureCanvasTkAgg(fig, master=self.f_bar)
        c.draw()
        c.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    # ── Fortschritts-Balken ─────────────────

    def plot_fortschritt(self):
        for w in self.f_progress.winfo_children():
            w.destroy()

        s = self.studium
        gesamt_tage = max((s.enddatum - s.startdatum).days, 1)
        vergangen   = s.tage_studiert()
        verbleibend = s.verbleibende_zeit().days
        fort_pct    = s.fortschritt_prozent()
        zeit_frac   = min(vergangen / gesamt_tage, 1.0)

        fig = Figure(figsize=(2.5, 2.5), facecolor=CARD)
        ax  = fig.add_subplot(111)
        fig.patch.set_facecolor(CARD)
        ax.set_facecolor(CARD)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        def draw_bar(y, label, frac, color, val_text):
            # Hintergrund
            ax.barh(y, 1.0, height=0.11, color=BORD,   left=0, align="center", zorder=1)
            # Füllung
            ax.barh(y, frac, height=0.11, color=color, left=0, align="center", zorder=2)
            ax.text(0.01, y + 0.10, label, color=WHITE,
                    fontsize=8, fontfamily=FONT, ha="left", va="bottom")
            ax.text(frac + 0.02, y, val_text, color=color,
                    fontsize=7, fontfamily=FONT, ha="left", va="center",
                    clip_on=True)

        draw_bar(0.68, "Studienzeit",
                 zeit_frac, BLUE,
                 f"{vergangen} / {gesamt_tage} Tage")

        draw_bar(0.38, "ECTS-Fortschritt",
                 fort_pct / 100, RED,
                 f"{fort_pct:.1f}%")

        ax.text(0.5, 0.08,
                f"Noch {verbleibend} Tage bis zum Studienende",
                ha="center", color=MUTED, fontsize=7, fontfamily=FONT)

        ax.text(0.5, 0.92,
                f"{s.gesamt_ects()} von {s.moegliche_ects} ECTS erreicht",
                ha="center", color=WHITE, fontsize=9,
                fontfamily=FONT, fontweight="bold")

        fig.tight_layout(pad=1.2)
        c = FigureCanvasTkAgg(fig, master=self.f_progress)
        c.draw()
        c.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    # ── Modulliste ──────────────────────────

    def _render_module(self):
        for w in self.f_module.winfo_children():
            w.destroy()

        canvas = tk.Canvas(self.f_module, bg=CARD, highlightthickness=0)
        sb = tk.Scrollbar(self.f_module, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=CARD)
        sf.bind("<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        for sem in self.studium.semester:
            tk.Label(sf, text=f"▸ {sem.name}  ({sem.semester_ects()} ECTS)",
                     font=(FONT, 9, "bold"), fg=BLUE, bg=CARD,
                     anchor="w").pack(fill="x", padx=10, pady=(8, 2))

            for m in sem.module:
                ok    = m.abgabe_bestanden()
                col   = GREEN if ok else MUTED
                sym   = "✓" if ok else "○"
                note  = f"  {m.pruefung.note}" if m.pruefung else ""

                row = tk.Frame(sf, bg=CARD)
                row.pack(fill="x", padx=10, pady=1)
                tk.Label(row, text=sym,    fg=col,   bg=CARD,
                         font=(FONT, 10)).pack(side="left", padx=(0, 5))
                tk.Label(row, text=m.name, fg=WHITE, bg=CARD,
                         font=(FONT, 9), anchor="w").pack(side="left", fill="x", expand=True)
                tk.Label(row, text=f"{m.ects_kurs} ECTS{note}", fg=col, bg=CARD,
                         font=(FONT, 8)).pack(side="right")

    # ── Dialog: Modul hinzufügen ────────────

    def _dialog_modul(self):
        if not self.studium.semester:
            messagebox.showwarning("Warnung", "Kein Semester vorhanden.")
            return

        MONATE = ["Jan","Feb","Mär","Apr","Mai","Jun",
                  "Jul","Aug","Sep","Okt","Nov","Dez"]

        dlg = tk.Toplevel(self.root)
        dlg.title("Modul hinzufügen")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.grab_set()

        def row(label, widget_fn):
            tk.Label(dlg, text=label, fg=MUTED, bg=BG,
                     font=(FONT, 8), anchor="w").pack(fill="x", padx=16, pady=(8, 0))
            w = widget_fn()
            w.pack(fill="x", padx=16)
            return w

        def mk_entry():
            return tk.Entry(dlg, bg=CARD, fg=WHITE, insertbackground=WHITE,
                            font=(FONT, 10), relief="flat",
                            highlightbackground=BORD, highlightthickness=1)

        sem_var = tk.StringVar(value=self.studium.semester[0].name)
        row("Semester", lambda: ttk.Combobox(
            dlg, textvariable=sem_var,
            values=[s.name for s in self.studium.semester],
            state="readonly", font=(FONT, 9)))

        e_name = row("Modulname", mk_entry)
        e_ects = row("ECTS",      mk_entry); e_ects.insert(0, "5")
        e_note = row("Note (leer = nicht bestanden)", mk_entry)

        mon_var = tk.StringVar(value="Jan")
        row("Monat", lambda: ttk.Combobox(
            dlg, textvariable=mon_var, values=MONATE,
            state="readonly", font=(FONT, 9)))

        def ok():
            name = e_name.get().strip()
            if not name:
                messagebox.showerror("Fehler", "Bitte Modulname eingeben.", parent=dlg)
                return
            try:
                ects = int(e_ects.get().strip())
            except ValueError:
                messagebox.showerror("Fehler", "ECTS muss eine Zahl sein.", parent=dlg)
                return
            note_str = e_note.get().strip()
            pruefung = None
            if note_str:
                try:
                    pruefung = Pruefungsleistung(int(note_str))
                except ValueError:
                    messagebox.showerror("Fehler", "Note muss eine Zahl sein.", parent=dlg)
                    return
            modul = Modul(name, ects, False, pruefung, mon_var.get())
            for sem in self.studium.semester:
                if sem.name == sem_var.get():
                    sem.module.append(modul)
                    break
            dlg.destroy()
            self.anzeigen()

        tk.Button(dlg, text="SPEICHERN", command=ok,
                  bg=RED, fg=WHITE, font=(FONT, 10, "bold"),
                  relief="flat", pady=8).pack(fill="x", padx=16, pady=16)


    # ── Daten bearbeiten ───────────────────────────

    def _daten_bearbeiten(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Studium bearbeiten")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.grab_set()

        def mk_entry(prefill: str) -> tk.Entry:
            e = tk.Entry(dlg, bg=CARD, fg=WHITE, insertbackground=WHITE, font=(FONT, 10), relief="flat", highlightbackground=BORD, highlightthickness=1)
            e.insert(0, prefill)
            e.pack(fill="x", padx=16)
            return e

        def lbl(text: str):
            tk.Label(dlg, text=text, fg=MUTED, bg=BG, font=(FONT, 8), anchor="w").pack(fill="x", padx=16, pady=(8, 0))

        def mk_calendar(prefill: date) -> DateEntry:
            cal = DateEntry(
                dlg,
                year=prefill.year,
                month=prefill.month,
                day=prefill.day,
                date_pattern="yyyy-mm-dd",
                background=RED,
                foreground=WHITE,
                bordercolor=BORD,
                headersbackground=CARD,
                headersforeground=WHITE,
                selectbackground=RED,
                selectforeground=WHITE,
                normalbackground=CARD,
                normalforeground=WHITE,
                weekendbackground=CARD,
                weekendforeground=MUTED,
                othermonthbackground=BG,
                otermonthforeground=MUTED,
                font=(FONT, 9),
                relief="flat",
            )
            cal.pack(fill="x", padx=16)
            return cal

        lbl("Name")
        e_studierender: tk.Entry = mk_entry(self.studium.studierender)

        lbl("Studiengang Name")
        e_name: tk.Entry = mk_entry(self.studium.name)

        lbl("Startdatum")
        cal_start: DateEntry = mk_calendar(self.studium.startdatum)

        lbl("Enddatum")
        cal_end: DateEntry = mk_calendar(self.studium.enddatum)

        lbl("Mögliche ECTS")
        e_ects: tk.Entry = mk_entry(str(self.studium.moegliche_ects))

        def ok():
            studierender = e_studierender.get().strip()
            name: str = e_name.get().strip()
            if not name:
                messagebox.showerror("Fehler", "Bitte einen Namen eingeben.", parent=dlg)
                return

            startdatum: date = cal_start.get_date()  # returns a date object directly
            enddatum: date = cal_end.get_date()

            if enddatum <= startdatum:
                messagebox.showerror("Fehler", "Enddatum muss nach dem Startdatum liegen.", parent=dlg)
                return

            try:
                moegliche_ects: int = int(e_ects.get().strip())
            except ValueError:
                messagebox.showerror("Fehler", "ECTS muss eine Zahl sein.", parent=dlg)
                return
            self.studium.studierender = studierender
            self.studium.name = name
            self.studium.startdatum = startdatum
            self.studium.enddatum = enddatum
            self.studium.moegliche_ects = moegliche_ects

            dlg.destroy()
            self.anzeigen()

        tk.Button(dlg, text="SPEICHERN", command=ok,
                  bg=RED, fg=WHITE, font=(FONT, 10, "bold"),
                  relief="flat", pady=8).pack(fill="x", padx=16, pady=16)


    # ── Speichern ───────────────────────────
    def _speichern(self):
        speichern.Speichern().save_data(self.studium)
        messagebox.showinfo("Gespeichert", "Daten wurden erfolgreich gespeichert.")


def main():
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox",
                    fieldbackground=CARD, background=CARD,
                    foreground=WHITE, selectbackground=BORD,
                    selectforeground=WHITE)
    studium = speichern.Speichern().load_data()
    Dashboard(root, studium)
    root.mainloop()


if __name__ == "__main__":
    main()
