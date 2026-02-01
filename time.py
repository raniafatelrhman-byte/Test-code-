import tkinter as tk
from datetime import datetime


class PinkDigitalClock:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Pink Digital Clock")
        self.root.geometry("380x220")
        self.root.resizable(False, False)

        # إزالة شريط العنوان الافتراضي لستايل أنيق
        self.root.overrideredirect(True)

        # =====================
        # Pink Theme
        # =====================
        self.BG     = "#fff0f6"   # خلفية عامة
        self.CARD   = "#ffe4ef"   # بطاقة الساعة
        self.TEXT   = "#3a0f2e"   # نص أساسي
        self.MUTED  = "#8b3a62"   # نص ثانوي
        self.ACCENT = "#ff5fa2"   # وردي قوي
        self.BORDER = "#ff9cc7"   # حدود
        self.BTN    = "#ff7eb6"   # زر

        self.root.configure(bg=self.BG)

        # للسحب
        self._dx = 0
        self._dy = 0

        self._build_ui()
        self._tick()

    # =====================
    # واجهة المستخدم
    # =====================
    def _build_ui(self):
        self.card = tk.Frame(
            self.root,
            bg=self.CARD,
            highlightthickness=2,
            highlightbackground=self.BORDER
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=350, height=180)

        # Top bar
        topbar = tk.Frame(self.card, bg=self.CARD)
        topbar.pack(fill="x", padx=12, pady=(10, 0))

        title = tk.Label(
            topbar,
            text="Pink Clock",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 11, "bold")
        )
        title.pack(side="left")

        close_btn = tk.Label(
            topbar,
            text="✕",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 13, "bold"),
            cursor="hand2"
        )
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", lambda e: self.root.destroy())

        # الوقت
        self.time_lbl = tk.Label(
            self.card,
            text="00:00:00",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI", 38, "bold")
        )
        self.time_lbl.pack(pady=(18, 0))

        # التاريخ
        self.date_lbl = tk.Label(
            self.card,
            text="Mon, 01 Jan 2000",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 12)
        )
        self.date_lbl.pack(pady=(4, 0))

        # ربط السحب
        for w in (self.card, topbar, title, self.time_lbl, self.date_lbl):
            w.bind("<Button-1>", self._start_drag)
            w.bind("<B1-Motion>", self._on_drag)

        # Hover للزر
        close_btn.bind("<Enter>", lambda e: close_btn.configure(fg="#ff2f7a"))
        close_btn.bind("<Leave>", lambda e: close_btn.configure(fg=self.MUTED))

    # =====================
    # تحديث الوقت
    # =====================
    def _tick(self):
        now = datetime.now()
        self.time_lbl.config(text=now.strftime("%H:%M:%S"))
        self.date_lbl.config(text=now.strftime("%a, %d %b %Y"))
        self.root.after(200, self._tick)

    # =====================
    # السحب
    # =====================
    def _start_drag(self, event):
        self._dx = event.x_root - self.root.winfo_x()
        self._dy = event.y_root - self.root.winfo_y()

    def _on_drag(self, event):
        x = event.x_root - self._dx
        y = event.y_root - self._dy
        self.root.geometry(f"+{x}+{y}")


# =====================
# تشغيل الساعة
# =====================
if __name__ == "__main__":
    root = tk.Tk()
    PinkDigitalClock(root)
    root.mainloop()
