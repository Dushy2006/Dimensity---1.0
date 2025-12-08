import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, ttk
import platform


# -----------------------------------------------
# SOUND ALERT
# -----------------------------------------------
def play_alert_sound():
    system = platform.system()
    try:
        if system == "Windows":
            import winsound
            for i in range(3):
                winsound.Beep(2000, 500)
                time.sleep(0.2)
        else:
            from playsound import playsound
            playsound("alert.mp3")
    except:
        print("⚠ Sound alert unavailable.")


# -----------------------------------------------
# CUSTOM NON-BLOCKING ALERT WINDOW
# -----------------------------------------------
def show_alert_window(med, t):
    alert = tk.Toplevel()
    alert.title("Reminder alert")
    alert.geometry("1200x800")
    alert.resizable(False, False)

    tk.Label(alert, text=f"Time to take:\n{med} ({t})",
             font=("Arial", 60), pady=85).pack()

    tk.Button(alert, text="OK", command=alert.destroy, width=10).pack(pady=10)

    alert.attributes("-topmost", True)
    alert.lift()


# -----------------------------------------------
# REMINDER THREAD — non-blocking popup + sound
# -----------------------------------------------
def reminder_loop():
    global running

    already_alerted = set()

    while running:
        now = datetime.now().strftime("%H:%M")

        for med, times in reminders.items():
            for t in times:
                key = (med, t)

                if now == t and key not in already_alerted:

                    # SHOW POPUP (NOT BLOCKING)
                    root.after(0, show_alert_window, med, t)

                    # PLAY SOUND IN BACKGROUND THREAD
                    threading.Thread(target=play_alert_sound, daemon=True).start()

                    already_alerted.add(key)

        time.sleep(10)


# -----------------------------------------------
# ADD MEDICINE
# -----------------------------------------------
def add_medicine():
    name = simpledialog.askstring("Task Name", "Enter Task name:")
    if not name:
        return

    times = []

    while True:
        t = simpledialog.askstring("Add Time", "Enter time (HH:MM) or Cancel to stop:")
        if not t:
            break

        try:
            time.strptime(t, "%H:%M")
            times.append(t)
        except:
            tk.messagebox.showerror("Error", "Invalid time format!")
            continue

    if times:
        reminders[name] = times
        update_tree()


# -----------------------------------------------
# UPDATE TREE
# -----------------------------------------------
def update_tree():
    for row in tree.get_children():
        tree.delete(row)

    for med, times in reminders.items():
        tree.insert("", "end", values=(med, ", ".join(times)))


# -----------------------------------------------
# START REMINDER
# -----------------------------------------------
def start_reminder():
    global running

    if running:
        tk.messagebox.showinfo("Running", "Reminder already running!")
        return

    running = True

    thread = threading.Thread(target=reminder_loop, daemon=True)
    thread.start()

    tk.messagebox.showinfo("Started", "Reminder started!")


# -----------------------------------------------
# STOP REMINDER
# -----------------------------------------------
def stop_reminder():
    global running
    running = False
    tk.messagebox.showinfo("Stopped", "Reminder stopped.")


# -----------------------------------------------
# GUI SETUP
# -----------------------------------------------
root = tk.Tk()
root.title("Medicine Reminder (Tkinter)")
root.geometry("520x380")
root.resizable(False, False)

reminders = {}
running = False
tk.Label(root, text="Medicine Reminder System",
         font=("Arial", 16, "bold")).pack(pady=10)

columns = ("Medicine", "Times")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
tree.heading("Medicine", text="Medicine")
tree.heading("Times", text="Reminder Times")
tree.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Add Medicine", width=15, command=add_medicine).grid(row=0, column=0, padx=10)
tk.Button(frame, text="Start Reminder", width=15, command=start_reminder).grid(row=0, column=1, padx=10)
tk.Button(frame, text="Stop Reminder", width=15, command=stop_reminder).grid(row=0, column=2, padx=10)

root.mainloop()
