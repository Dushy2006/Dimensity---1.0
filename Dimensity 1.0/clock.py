# # clock_widget.py
# import tkinter as tk
# import time
# import subprocess
# import sys
# import os

# class SimpleClockApp:
#     def __init__(self, x=200, y=200):
#         # create window
#         self.root = tk.Tk()
#         self.root.geometry(f"500x140+{x}+{y}")
#         # remove window decorations (frameless)
#         self.root.overrideredirect(True)
#         # make black treated as transparent (works on Windows)
#         try:
#             self.root.wm_attributes("-transparentcolor", "black")
#         except Exception:
#             # attribute may not exist on some platforms; ignore
#             pass
#         self.root.configure(bg="black")

#         # TIME label
#         self.label_time = tk.Label(self.root, font=("Segoe UI", 60), fg="teal", bg="black")
#         self.label_time.pack()

#         # DAY label
#         self.label_day = tk.Label(self.root, font=("Segoe UI", 20), fg="white", bg="black")
#         self.label_day.pack()

#         # DATE label
#         self.label_date = tk.Label(self.root, font=("Segoe UI", 18), fg="white", bg="black")
#         self.label_date.pack()

#         # bind drag to the whole window
#         self.root.bind("<Button-1>", self.start_move)
#         self.root.bind("<B1-Motion>", self.do_move)

#         # optional exit bindings
#         self.root.bind("<Escape>", lambda e: self.root.destroy())
#         self.root.bind("<Button-3>", lambda e: self.root.destroy())

#     def start_move(self, event):
#         # record where the mouse was clicked
#         self.root.x = event.x
#         self.root.y = event.y

#     def do_move(self, event):
#         # compute new top-left coordinates for the window
#         x = event.x_root - self.root.x
#         y = event.y_root - self.root.y
#         self.root.geometry(f"+{x}+{y}")

#     def update_clock(self):
#         now = time.localtime()
#         hour = time.strftime("%I", now)
#         minute = time.strftime("%M", now)
#         ampm = time.strftime("%p", now)
#         time_text = f"{hour}:{minute} {ampm}"
#         self.label_time.config(text=time_text)

#         # day and date
#         self.label_day.config(text=time.strftime("%A", now))
#         self.label_date.config(text=time.strftime("%d %B %Y", now))

#         # schedule next update
#         self.root.after(1000, self.update_clock)

#     def run(self):
#         # start the periodic update and run main loop
#         self.update_clock()
#         self.root.mainloop()

# if __name__ == "__main__":
#     app = SimpleClockApp(x=200, y=200)  # change x,y initial position if you want
#     app.run()
