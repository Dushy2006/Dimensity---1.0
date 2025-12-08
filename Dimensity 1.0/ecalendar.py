import customtkinter as ctk
import calendar
import datetime
import ctypes

# --- Sharpness Fix for Windows ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# --- Configuration ---
ctk.set_appearance_mode("Dark")

# --- Colors ---
COLOR_BG = "#0f172a"       # Background
COLOR_PANEL = "#1e293b"    # Panels
COLOR_TODAY = "#22c55e"    # Green for today
COLOR_TASK = "#eab308"     # Gold/Yellow for tasks
COLOR_BDAY = "#d946ef"     # Fuchsia/Purple for birthdays
COLOR_DEFAULT = "#334155"  # Grey/Blue default

class UltimateCalendar(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Life Organizer")
        self.geometry("900x600")
        self.configure(fg_color=COLOR_BG)
        
        # --- Data ---
        self.today = datetime.date.today()
        self.year = self.today.year
        self.month = self.today.month
        self.selected_day = self.today.day
        
        self.events = {}  # {"2025-11-22": [{'text':'...', 'type':'task/bday','done':False}]}
        
        # --- Layout ---
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # === LEFT: Calendar Panel ===
        self.frame_cal = ctk.CTkFrame(self, fg_color=COLOR_PANEL, corner_radius=15)
        self.frame_cal.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # Navigation
        self.frame_nav = ctk.CTkFrame(self.frame_cal, fg_color="transparent")
        self.frame_nav.pack(fill="x", pady=15)

        self.btn_prev = ctk.CTkButton(self.frame_nav, text="<", width=40, command=self.prev_month, fg_color=COLOR_DEFAULT)
        self.btn_prev.pack(side="left", padx=10)
        
        self.lbl_header = ctk.CTkLabel(self.frame_nav, text="Month Year", font=("Arial", 22, "bold"))
        self.lbl_header.pack(side="left", expand=True)
        
        self.btn_next = ctk.CTkButton(self.frame_nav, text=">", width=40, command=self.next_month, fg_color=COLOR_DEFAULT)
        self.btn_next.pack(side="right", padx=10)

        self.btn_today = ctk.CTkButton(self.frame_cal, text="Jump to Today", fg_color=COLOR_DEFAULT, command=self.go_to_today)
        self.btn_today.pack(pady=5)

        # Grid for days
        self.frame_days = ctk.CTkFrame(self.frame_cal, fg_color="transparent")
        self.frame_days.pack(padx=10, pady=10)

        # === RIGHT: Event Panel ===
        self.frame_events = ctk.CTkFrame(self, fg_color=COLOR_PANEL, corner_radius=15)
        self.frame_events.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)

        self.lbl_event_header = ctk.CTkLabel(self.frame_events, text="Planner", font=("Arial", 20, "bold"))
        self.lbl_event_header.pack(pady=15)

        self.scroll_list = ctk.CTkScrollableFrame(self.frame_events, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True, padx=10)

        # Input for adding events
        self.frame_input = ctk.CTkFrame(self.frame_events, fg_color="transparent")
        self.frame_input.pack(fill="x", padx=10, pady=15)
        
        self.entry_text = ctk.CTkEntry(self.frame_input, placeholder_text="Enter details...", height=35)
        self.entry_text.pack(fill="x", pady=(0, 10))

        self.btn_add_task = ctk.CTkButton(
            self.frame_input, text="+ Task", 
            fg_color=COLOR_TASK, text_color="black",
            command=lambda: self.add_item("task")
        )
        self.btn_add_task.pack(side="left", fill="x", expand=True, padx=2)

        self.btn_add_bday = ctk.CTkButton(
            self.frame_input, text="🎂 Birthday", 
            fg_color=COLOR_BDAY, text_color="white",
            command=lambda: self.add_item("bday")
        )
        self.btn_add_bday.pack(side="right", fill="x", expand=True, padx=2)

        # Initial draw
        self.update_calendar()
        self.show_events()

    # ---------------- CALENDAR ----------------
    def update_calendar(self):
        self.lbl_header.configure(text=f"{calendar.month_name[self.month]} {self.year}")

        for widget in self.frame_days.winfo_children():
            widget.destroy()

        # Day names
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            ctk.CTkLabel(self.frame_days, text=day, width=50, text_color="gray").grid(row=0, column=i)

        # Dates
        month_matrix = calendar.monthcalendar(self.year, self.month)
        for r, week in enumerate(month_matrix):
            for c, day in enumerate(week):
                if day != 0:
                    key = f"{self.year}-{self.month}-{day}"
                    btn_color = COLOR_DEFAULT
                    has_bday = False
                    has_task = False
                    if key in self.events:
                        for item in self.events[key]:
                            if item['type'] == 'bday': has_bday = True
                            if item['type'] == 'task' and not item['done']: has_task = True
                    if has_bday: btn_color = COLOR_BDAY
                    elif has_task: btn_color = COLOR_TASK
                    if day == self.today.day and self.month == self.today.month and self.year == self.today.year:
                        btn_color = COLOR_TODAY
                    border = 2 if day == self.selected_day else 0
                    btn = ctk.CTkButton(
                        self.frame_days, text=str(day), width=50, height=50,
                        fg_color=btn_color, border_width=border, border_color="white",
                        font=("Arial", 14, "bold"),
                        command=lambda d=day: self.select_day(d)
                    )
                    btn.grid(row=r+1, column=c, padx=3, pady=3)

    def select_day(self, day):
        self.selected_day = day
        self.update_calendar()
        self.show_events()

    # ---------------- EVENTS ----------------
    def show_events(self):
        for w in self.scroll_list.winfo_children(): w.destroy()
        
        key = f"{self.year}-{self.month}-{self.selected_day}"
        self.lbl_event_header.configure(text=f"Plan: {key}")
        items = self.events.get(key, [])

        for index, item in enumerate(items):
            row = ctk.CTkFrame(self.scroll_list, fg_color="#2a3b55")
            row.pack(fill="x", pady=3)

            chk = ctk.CTkCheckBox(
                row, text="", width=20,
                command=lambda i=index: self.toggle_done(key, i)
            )
            chk.pack(side="left", padx=5)
            if item['done']:
                chk.select()

            display_text = item['text']
            text_col = "white"
            if item['type'] == 'bday':
                display_text = f"🎂 {display_text}"
                text_col = COLOR_BDAY
            if item['done']:
                text_col = "gray"

            lbl = ctk.CTkLabel(row, text=display_text, text_color=text_col, anchor="w")
            lbl.pack(side="left", padx=5, fill="x", expand=True)

            btn_del = ctk.CTkButton(
                row, text="×", width=30, height=30, 
                fg_color="#ef4444", hover_color="#b91c1c",
                command=lambda i=index: self.delete_item(key, i)
            )
            btn_del.pack(side="right", padx=5, pady=2)

    def add_item(self, type_name):
        text = self.entry_text.get()
        if not text: return
        key = f"{self.year}-{self.month}-{self.selected_day}"
        if key not in self.events:
            self.events[key] = []
        new_item = {"text": text, "type": type_name, "done": False}
        self.events[key].append(new_item)
        self.entry_text.delete(0, "end")
        self.show_events()
        self.update_calendar()

    def delete_item(self, key, index):
        if key in self.events:
            self.events[key].pop(index)
            if not self.events[key]:
                del self.events[key]
        self.show_events()
        self.update_calendar()

    def toggle_done(self, key, index):
        self.events[key][index]['done'] = not self.events[key][index]['done']
        self.show_events()
        self.update_calendar()

    # ---------------- NAVIGATION ----------------
    def go_to_today(self):
        self.year, self.month, self.selected_day = self.today.year, self.today.month, self.today.day
        self.update_calendar()
        self.show_events()

    def next_month(self):
        self.month += 1
        if self.month > 12: self.month, self.year = 1, self.year + 1
        self.selected_day = 1
        self.update_calendar()
        self.show_events()

    def prev_month(self):
        self.month -= 1
        if self.month < 1: self.month, self.year = 12, self.year - 1
        self.selected_day = 1
        self.update_calendar()
        self.show_events()


if __name__ == "__main__":
    app = UltimateCalendar()
    app.mainloop()
