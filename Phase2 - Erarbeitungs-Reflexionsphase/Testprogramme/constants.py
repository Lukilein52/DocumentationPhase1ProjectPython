# constants.py – Design-Konstanten für das Studium Dashboard

BG    = "#0d0d0d"
CARD  = "#141414"
BORD  = "#252525"
RED   = "#e63946"
BLUE  = "#4361ee"
WHITE = "#f0f0f0"
MUTED = "#666666"
GREEN = "#2dc653"
ORANGE = "#e74c3c"
FONT  = "Courier New"

def style_ax(ax, fig_color=None):
    bg = fig_color or CARD
    ax.set_facecolor(bg)
    ax.tick_params(colors=MUTED, labelsize=8)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_color(BORD)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_color(MUTED)
        lbl.set_fontfamily(FONT)
