# reminder_app.py
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
import platform
import os

# System tray
try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_PYSTRAY = True
except Exception:
    HAS_PYSTRAY = False

# -----------------------------------------------
# GLOBAL VARIABLES
# -----------------------------------------------
reminders = {}
running = False
tray_icon = None

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
            # For Mac/Linux, simpler beep
            print('\a')
    except:
        print("⚠ Sound alert unavailable.")

# -----------------------------------------------
# CUSTOM NON-BLOCKING ALERT WINDOW
# -----------------------------------------------
def show_alert_window(med, t, parent=None):
    # parent: pass the reminder window (optional) so alert is on top
    alert = tk.Toplevel(parent) if parent else tk.Toplevel()
    alert.title("Reminder alert")
    alert.geometry("400x200")
    alert.attributes("-topmost", True)
    tk.Label(alert, text=f"Time to take:\n{med}",
             font=("Arial", 18, "bold"), pady=12).pack()
    tk.Label(alert, text=f"Scheduled: {t}",
             font=("Arial", 12)).pack()

    tk.Button(alert, text="Dismiss", command=alert.destroy, width=12, bg="#ffcccc").pack(pady=20)
    alert.lift()
    alert.focus_force()

# -----------------------------------------------
# REMINDER THREAD
# -----------------------------------------------
def reminder_loop(parent_window=None):
    global running
    already_alerted = set()

    while running:
        now_hm = datetime.now().strftime("%H:%M")

        for med, times in list(reminders.items()):
            for t in times:
                key = (med, t)
                if now_hm == t and key not in already_alerted:
                    # schedule GUI update on main thread
                    try:
                        if parent_window:
                            parent_window.after(0, lambda m=med, time=t: show_alert_window(m, time, parent=parent_window))
                        else:
                            # get default root if no parent
                            root = tk._get_default_root()
                            if root:
                                root.after(0, lambda m=med, time=t: show_alert_window(m, time))
                    except Exception:
                        # fallback
                        try:
                            show_alert_window(med, t)
                        except:
                            pass

                    # Play sound
                    threading.Thread(target=play_alert_sound, daemon=True).start()
                    already_alerted.add(key)

        # clean-up logic to allow next-day alarms to re-trigger
        time.sleep(2)

# -----------------------------------------------
# SYSTEM TRAY FUNCTIONS
# -----------------------------------------------
def create_image():
    # simple square icon
    width = 64
    height = 64
    color1 = "white"
    color2 = "blue"
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill=color2)
    return image

def quit_app(icon, item):
    global running
    running = False
    try:
        icon.stop()
    except:
        pass
    # close all tk windows
    try:
        root = tk._get_default_root()
        if root:
            root.after(0, root.destroy)
    except:
        pass

def show_window(icon, item):
    try:
        icon.stop()
    except:
        pass
    try:
        root = tk._get_default_root()
        if root:
            root.after(0, root.deiconify)
    except:
        pass

def run_tray_icon():
    global tray_icon
    if not HAS_PYSTRAY:
        return
    try:
        image = create_image()
        menu = (pystray.MenuItem('Show', show_window), pystray.MenuItem('Quit', quit_app))
        tray_icon = pystray.Icon("reminder", image, "Med Reminder", menu)
        tray_icon.run()
    except Exception as e:
        print("Tray icon failed:", e)

# -----------------------------------------------
# GUI: create reminder window factory (standalone)
# -----------------------------------------------
def create_reminder_window():
    global root, running

    root = tk.Tk()
    root.title("General Reminder")
    # position window near center
    root.geometry("550x450")

    def on_closing():
        # hide to tray if running
        if running and HAS_PYSTRAY:
            messagebox.showinfo("Minimized", "App is running in the background.\nCheck the system tray (near clock) to open or quit.")
            root.withdraw()
            threading.Thread(target=run_tray_icon, daemon=True).start()
        else:
            try:
                root.destroy()
            except:
                pass

    root.protocol("WM_DELETE_WINDOW", on_closing)

    tk.Label(root, text="General Reminder System", font=("Segoe UI", 16, "bold")).pack(pady=10)

    lbl_status = tk.Label(root, text="Status: STOPPED", fg="red", font=("Segoe UI", 10))
    lbl_status.pack()

    columns = ("Task", "Times")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
    tree.heading("Task", text="Task")
    tree.heading("Times", text="Times")
    tree.column("Task", width=200)
    tree.column("Times", width=300)
    tree.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    def add_medicine():
        name = simpledialog.askstring("Task Name", "Enter Task name:", parent=root)
        if not name:
            return

        times = []
        while True:
            t = simpledialog.askstring("Add Time", "Enter time (HH:MM) or Cancel to stop:", parent=root)
            if not t:
                break
            try:
                time.strptime(t, "%H:%M")
                times.append(t)
            except:
                messagebox.showerror("Error", "Invalid time format!", parent=root)
                continue

        if times:
            reminders[name] = times
            update_tree()

            if not running:
                start_reminder()

    def update_tree():
        for row in tree.get_children():
            tree.delete(row)
        for med, times in reminders.items():
            tree.insert("", "end", values=(med, ", ".join(times)))

    def start_reminder():
        nonlocal lbl_status
        global running
        if running:
            return
        running = True
        threading.Thread(target=reminder_loop, args=(root,), daemon=True).start()
        lbl_status.config(text="Status: RUNNING", fg="green")

    def stop_reminder():
        nonlocal lbl_status
        global running
        running = False
        lbl_status.config(text="Status: STOPPED", fg="red")

    tk.Button(frame, text="Add Tasks", width=15, command=add_medicine, bg="#e1e1e1").grid(row=0, column=0, padx=5)
    tk.Button(frame, text="Stop/Reset", width=15, command=stop_reminder, bg="#ffcccc").grid(row=0, column=1, padx=5)

    tk.Label(root, text="Note: Closing this window minimizes it to the System Tray.", font=("Arial", 8, "italic"), fg="gray").pack(pady=10, side="bottom")

    # Start window event loop
    root.mainloop()

# -----------------------------------------------
# Run reminder app if this script executed directly
# -----------------------------------------------
if __name__ == "__main__":
    create_reminder_window()
