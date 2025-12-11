import tkinter as tk
from tkinter import messagebox, filedialog, Listbox, Scrollbar, END
from tkinter import scrolledtext
from PIL import Image, ImageTk
import os
import subprocess
import sys
import pickle
import csv
import sys
import time

BASE_PATH = r"C:\Users\Chethan S\OneDrive\Desktop\Dimensity 1.0\Dimensity---1.0\Dimensity 1.0"


sys.path.append(BASE_PATH)


# ---------------- Root / Base UI ----------------
root = tk.Tk()
root.title("Dimensity 1.0")

# Fullscreen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="black")
root.attributes("-fullscreen",True)


# --- Wallpaper (keep your original path) ---
wallpaper_path = os.path.join(BASE_PATH, "assets", "wallpaper.png")

try:
    image = Image.open(wallpaper_path)
    image = image.resize((screen_width, screen_height))
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception:
    bg_label = tk.Label(root, bg="black")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --- Title ---
title_label = tk.Label(
    bg_label,
    text="DIMENSITY 1.0",
    font=("Helvetica Neue", 85, "bold"),
    fg="white",
    bg=None,
    bd=0
)
title_label.place(relx=0.5, rely=0.4, anchor="center")

# --- Subtitle ---
subtitle_frame = tk.Frame(bg_label, bg=None)
subtitle_frame.place(relx=0.5, rely=0.48, anchor="center")

powered_label = tk.Label(subtitle_frame, text="powered by ",
                         font=("Helvetica Neue", 25, "italic"),
                         fg="white", bg=None)
powered_label.pack(side="left")

prism_label = tk.Label(subtitle_frame, text="PRISM",
                       font=("Helvetica Neue", 30, "italic"),
                       fg="cyan", bg=None)
prism_label.pack(side="left")

#settings------------------
def open_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("About — Dimensity")
    settings_win.geometry("900x700")
    settings_win.configure(bg="black")
    settings_win.attributes("-fullscreen",True)

    # Attach to main window (nice on macOS)
    try:
        settings_win.transient(root)
        settings_win.focus_force()
    except Exception:
        pass

    # Header
    header = tk.Frame(settings_win, bg="black")
    header.pack(fill="x", padx=12, pady=(12, 6))
    tk.Label(header, text="Dimensity 1.0", font=("Helvetica Neue", 28, "bold"),
             fg="cyan", bg="black").pack(side="left", anchor="w")
    tk.Label(header, text="Version 1.0 (alpha)", font=("Helvetica Neue", 12),
             fg="white", bg="black").pack(side="right", anchor="e")

    # About paragraph (readable label inside a frame)
    about_frame = tk.Frame(settings_win, bg="black")
    about_frame.pack(fill="both", padx=12, pady=(6, 12))
    about_text = (
        "Dimensity is more than just a program — it is a fully simulated user interface "
        "ecosystem created by Prism Operating Systems Limited and powered by Prism technology. "
        "Designed to behave like a lightweight, self-contained operating system, it brings "
        "multiple applications together into one seamless environment. With an integrated "
        "calculator, intelligent clock, and an evolving file manager system, Dimensity allows "
        "users to interact as if they were navigating a desktop OS. It includes a dynamic "
        "calendar, a built-in game library, and upcoming features such as a weather system for "
        "real-time experience personalization. The system is also preparing to incorporate "
        "encryption tools for security and privacy. Most notably, Dimensity is built to host its "
        "own AI assistant powered by the Gemini API, making it capable of smart responses and "
        "adaptive automation. Every component is designed to feel intuitive, polished, and "
        "immersive. Dimensity is not just a project — it is an ambitious step toward a fully "
        "modular, programmable digital environment."
    )
    tk.Label(about_frame, text=about_text, font=("Helvetica Neue", 13),
             fg="white", bg="black", wraplength=860, justify="left").pack()

    # Authors header
    tk.Label(settings_win, text="Authors & Contributions",
             font=("Helvetica Neue", 20, "bold"),
             fg="white", bg="black").pack(padx=12, pady=(8, 6), anchor="w")

    # Authors data (replace values in code if needed)
    authors_data = [
        ["Dushyanth R", "Developed the Pong game, E-Files and the E-Calci"],
        ["Jivesh", "Built the E-Calendar and Asphalt Game"],
        ["Author 3", "Created the Clock System and Integrated AI Framework "],
        ["Author 4", "Developed Brick Breaker, Hangman, and the To-Do List Application"]
    ]

    # Authors table (high-contrast labels — not disabled)
    authors_frame = tk.Frame(settings_win, bg="black")
    authors_frame.pack(fill="x", padx=12, pady=(0, 12))
    # headers
    tk.Label(authors_frame, text="Name", font=("Helvetica Neue", 14, "bold"),
             fg="cyan", bg="black", width=36, anchor="w").grid(row=0, column=0, padx=2, pady=2)
    tk.Label(authors_frame, text="Role / Contribution", font=("Helvetica Neue", 14, "bold"),
             fg="cyan", bg="black", width=60, anchor="w").grid(row=0, column=1, padx=2, pady=2)
    # rows
    for r, (name, role) in enumerate(authors_data, start=1):
        tk.Label(authors_frame, text=name, font=("Helvetica Neue", 13),
                 fg="white", bg="black", width=36, anchor="w").grid(row=r, column=0, padx=2, pady=2, sticky="w")
        tk.Label(authors_frame, text=role, font=("Helvetica Neue", 13),
                 fg="white", bg="black", width=60, anchor="w", justify="left", wraplength=700).grid(row=r, column=1, padx=2, pady=2, sticky="w")

    # What's Next / Roadmap (read-only display)
    tk.Label(settings_win, text="What's Next?", font=("Helvetica Neue", 18, "bold"),
             fg="cyan", bg="black").pack(padx=12, pady=(8, 4), anchor="w")

    roadmap_text = (
        "Roadmap — Dimensity -> Diamond City 2.0\n\n"
        "- Login system with user profiles and sessions\n"
        "- Weather app (third-party API integration)\n"
        "- Encryption / Decryption utility (in-app)\n"
        "- Integrated custom AI assistant (Gemini / LLM integration)\n"
        "- Improved UI toolkit, polish and bugfixes\n"
        "- Expandable app store: more contributors and modules\n\n"
        "Status: Active development — more features and bugfixes planned."
    )
    tk.Label(settings_win, text=roadmap_text, font=("Helvetica Neue", 13),
             fg="white", bg="black", wraplength=860, justify="left").pack(padx=12, pady=(0, 12), anchor="w")

    # Footer Close button (clear visible colors)
    back_btn_settinngs= tk.Frame(settings_win, bg="black")
    back_btn_settinngs.pack(fill="x", padx=12, pady=8)
    tk.Button(back_btn_settinngs, text="Close", font=("Helvetica Neue", 14, "bold"),
              bg="#222222", fg="black", activebackground="#333333",
              command=settings_win.destroy).pack(side="right")

# --- Settings Button (kept but inert) ---
settings_btn = tk.Button(bg_label, text="⚙️",
                         font=("Helvetica Neue", 20, "bold"),
                         bg="#000000", fg="white",
                         activebackground="#111111",
                         activeforeground="cyan", bd=0,command=open_settings)
settings_btn.place(x=20, y=20)

# ---------------- E-Files directories ----------------
BASE_DIR = os.path.join(BASE_PATH,"E-files")
TEXT_DIR = os.path.join(BASE_DIR, "text")
BINARY_DIR = os.path.join(BASE_DIR, "binary")
CSV_DIR = os.path.join(BASE_DIR, "csv")

for d in (BASE_DIR, TEXT_DIR, BINARY_DIR, CSV_DIR):
    if not os.path.exists(d):
        os.makedirs(d)

# ---------------- Helper ----------------
def make_button(parent, text, cmd, **kwargs):
    """Bold cyber button (visible)."""
    cfg = {
        "font": ("Helvetica Neue", 18, "bold"),
        "bg": "#131313",   # dark panel
        "fg": "black",
        "bd": 2,
        "relief": "raised",
        "activebackground": "#222222",
        "activeforeground": "white",
        "padx": 22,
        "pady": 12
    }
    cfg.update(kwargs)
    return tk.Button(parent, text=text, command=cmd, **cfg)

def big_back_button(parent, cmd):
    return tk.Button(parent, text="◀ Back", command=cmd,
                      font=("Helvetica Neue", 16, "bold"),
                      bg="#222222", fg="black", bd=2, relief="raised",
                      activebackground="#333333", padx=18, pady=10)

# ---------------- E-Files (dynamic single-window panels) ----------------
def open_efiles():
    dock_height = 90
    app_h = screen_height - dock_height
    ewin = tk.Toplevel(root)
    ewin.title("E-Files")
    ewin.geometry(f"{screen_width}x{app_h}+0+0")
    ewin.configure(bg="black")
    ewin.transient(root)
    ewin.grab_set()
    ewin.attributes("-fullscreen",True)

    content = tk.Frame(ewin, bg="black")
    content.pack(fill="both", expand=True, padx=40, pady=8)

    home_panel = tk.Frame(content, bg="black")
    type_panel = tk.Frame(content, bg="black")
    action_panel = tk.Frame(content, bg="black")
    for p in (home_panel, type_panel, action_panel):
        p.place(relx=0, rely=0, relwidth=1, relheight=1)

    state = {"mode": None, "file_type": None}

    def raise_panel(panel):
        panel.lift()

    # ---------------- Editor (must be defined before buttons call it) ----------------
    def start_editor(file_type, mode="new"):
        for w in action_panel.winfo_children():
            w.destroy()

        tk.Label(action_panel, text=f"{mode.upper()} — {file_type.upper()}",
                 font=("Helvetica Neue", 24), fg="cyan", bg="black").pack(pady=8)
        tk.Label(action_panel, text="Filename (without extension):", fg="white", bg="black",
                 font=("Helvetica Neue", 13)).pack(pady=(8, 4))
        fname_entry = tk.Entry(action_panel, width=40, font=("Helvetica Neue", 14))
        fname_entry.pack(pady=(0, 8))

        # Editor area
        editor_area = scrolledtext.ScrolledText(action_panel, width=100, height=18,
                                                font=("Helvetica Neue", 12),
                                                bg="#0b0b0b", fg="cyan", insertbackground="white")
        editor_area.pack(pady=8)

        def perform_save():
            name = fname_entry.get().strip()
            if not name:
                messagebox.showerror("Filename", "Please provide a filename.")
                return
            ext_map = {"text": ".txt", "binary": ".bin", "csv": ".csv"}
            dir_map = {"text": TEXT_DIR, "binary": BINARY_DIR, "csv": CSV_DIR}
            final_path = os.path.join(dir_map[file_type], name + ext_map[file_type])
            content_data = editor_area.get("1.0", END)

            try:
                if file_type == "text":
                    mode_flag = "a" if mode == "append" else "w"
                    with open(final_path, mode_flag, encoding="utf-8") as f:
                        f.write(content_data)
                elif file_type == "binary":
                    lines = content_data.strip().split("\n") if content_data.strip() else []
                    if mode == "append" and os.path.exists(final_path):
                        with open(final_path, "rb") as f:
                            try:
                                existing = pickle.load(f)
                                if not isinstance(existing, list):
                                    existing = [existing]
                            except:
                                existing = []
                        lines = existing + lines
                    with open(final_path, "wb") as f:
                        pickle.dump(lines, f)
                elif file_type == "csv":
                    mode_flag = "a" if mode == "append" else "w"
                    lines = [ln for ln in content_data.split("\n") if ln.strip() != ""]
                    with open(final_path, mode_flag, newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        for ln in lines:
                            writer.writerow([cell.strip() for cell in ln.split(",")])
                messagebox.showinfo("Saved", f"File saved: {final_path}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        btns_frame = tk.Frame(action_panel, bg="black")
        btns_frame.pack(pady=8)
        make_button(btns_frame, "SAVE", perform_save).pack(side="left", padx=8)
        make_button(btns_frame, "CLEAR", lambda: editor_area.delete("1.0", END)).pack(side="left", padx=8)
        big_back_button(action_panel, lambda: select_type(file_type)).pack(side="bottom", pady=8)
        raise_panel(action_panel)



    # ---------------- Home Panel ----------------
    tk.Label(home_panel, text="Choose Mode", font=("Helvetica Neue", 28), fg="white", bg="black").pack(pady=20)
    btns = tk.Frame(home_panel, bg="black")
    btns.pack(pady=40)

    def go_to_type(selected_mode):
        state["mode"] = selected_mode
        for w in type_panel.winfo_children():
            w.destroy()
        tk.Label(type_panel, text=f"{selected_mode.upper()} - Choose File Type",
                 font=("Helvetica Neue", 26), fg="cyan", bg="black").pack(pady=16)
        tf = tk.Frame(type_panel, bg="black")
        tf.pack(pady=20)
        make_button(tf, "TEXT", lambda: select_type("text")).pack(side="left", padx=20)
        make_button(tf, "BINARY", lambda: select_type("binary")).pack(side="left", padx=20)
        make_button(tf, "CSV", lambda: select_type("csv")).pack(side="left", padx=20)
        big_back_button(type_panel, lambda: raise_panel(home_panel)).pack(side="bottom", pady=12)
        raise_panel(type_panel)

    make_button(btns, "READ", lambda: go_to_type("read")).pack(side="left", padx=30)
    make_button(btns, "WRITE", lambda: go_to_type("write")).pack(side="left", padx=30)
    
    back_btn_files= tk.Frame(ewin, bg="black")
    back_btn_files.pack(fill="x", padx=12, pady=8)
    tk.Button(back_btn_files, text="Close", font=("Helvetica Neue", 14, "bold"),
              bg="#222222", fg="black", activebackground="#333333",
              command=ewin.destroy).pack(side="right")


    # ---------------- Type / Action Panel ----------------
    def select_type(ftype):
        state["file_type"] = ftype
        for w in action_panel.winfo_children():
            w.destroy()
        tk.Label(action_panel, text=f"{state['mode'].upper()} — {ftype.upper()}",
                 font=("Helvetica Neue", 24), fg="cyan", bg="black").pack(pady=10)

        if state["mode"] == "read":
            dir_map = {"text": TEXT_DIR, "binary": BINARY_DIR, "csv": CSV_DIR}
            folder = dir_map[ftype]
            files = os.listdir(folder)
            if not files:
                tk.Label(action_panel, text="No files available.", fg="white", bg="black",
                         font=("Helvetica Neue", 14)).pack(pady=20)
            else:
                lb = Listbox(action_panel, bg="black", fg="cyan", width=50, font=("Helvetica Neue", 14))
                lb.pack(pady=10)
                for f in files:
                    lb.insert(END, f)
                st = scrolledtext.ScrolledText(action_panel, width=100, height=15, bg="#111", fg="cyan",
                                               font=("Helvetica Neue", 12))
                st.pack(pady=10)
                def open_file():
                    try:
                        sel = lb.get(lb.curselection())
                    except:
                        messagebox.showwarning("Select", "Select a file first!")
                        return
                    path = os.path.join(folder, sel)
                    try:
                        if ftype == "text":
                            with open(path, "r", encoding="utf-8") as f:
                                st.delete("1.0", END)
                                st.insert("1.0", f.read())
                        elif ftype == "csv":
                            st.delete("1.0", END)
                            with open(path, encoding="utf-8") as f:
                                reader = csv.reader(f)
                                for r in reader:
                                    st.insert(END, ", ".join(r) + "\n")
                        elif ftype == "binary":
                            with open(path, "rb") as f:
                                data = pickle.load(f)
                                st.delete("1.0", END)
                                st.insert("1.0", str(data))
                    except Exception as e:
                        messagebox.showerror("Error", f"Cannot read file:\n{e}")
                make_button(action_panel, "OPEN", open_file).pack(pady=6)

        else:
            make_button(action_panel, "Create New File", lambda: start_editor(ftype, mode="new")).pack(pady=15)
            make_button(action_panel, "Append to Existing", lambda: start_editor(ftype, mode="append")).pack(pady=15)

        big_back_button(action_panel, lambda: go_to_type(state["mode"])).pack(side="bottom", pady=10)
        raise_panel(action_panel)

    raise_panel(home_panel)
    ewin.lift()
    ewin.focus_force()

# ---------------- E-Chat_bot ----------------
def open_chatbot():
    """Launch the chatbot program in a separate window."""
    try:
        subprocess.Popen([sys.executable,r"C:\Users\Chethan S\OneDrive\Desktop\Dimensity 1.0 Redesigned\Dimensity---1.0\Dimensity 1.0\torrus_ai.py"])
    except Exception as e:
        messagebox.showerror("Chatbot Error",
                             f"Could not open Chatbot:\n{e}")


# ---------------- E-Play (existing logic) ----------------
def open_eplay():
    eplay_window = tk.Toplevel(root)
    eplay_window.title("E-Play")
    eplay_window.geometry(f"{screen_width}x{screen_height}")
    eplay_window.configure(bg="black")
    eplay_window.attributes("-fullscreen",True)

    tk.Label(eplay_window, text="E-PLAY",
             font=("Helvetica Neue", 60, "bold"),
             fg="black", bg="black").pack(pady=50)

    games_frame = tk.Frame(eplay_window, bg="black")
    games_frame.pack(pady=20)

    back_btn_eplay= tk.Frame(eplay_window, bg="black")
    back_btn_eplay.pack(fill="x", padx=12, pady=8)
    tk.Button(back_btn_eplay, text="Close", font=("Helvetica Neue", 14, "bold"),
              bg="#222222", fg="black", activebackground="#333333",
              command=eplay_window.destroy).pack(side="right")

    # Pong game icon
    pong_icon_path = os.path.join(BASE_PATH, "pong-logo.jpg")
    

    try:
        pong_image = Image.open(pong_icon_path)
        pong_image = pong_image.resize((250, 150))
        pong_photo = ImageTk.PhotoImage(pong_image)
        def launch_pong():
            subprocess.Popen([sys.executable, os.path.join(BASE_PATH, "pong.py")])
        pong_btn = tk.Button(games_frame, image=pong_photo, text="PONG", compound="top",
                             font=("Helvetica Neue", 16, "bold"),
                             bg="#1e1e1e", fg="black", bd=0, command=launch_pong)
        pong_btn.image = pong_photo
        pong_btn.pack(side="left", padx=30, pady=30)
    except Exception:
        # fallback simple label
        tk.Label(games_frame, text="PONG (missing asset)", fg="cyan", bg="black", font=("Helvetica Neue", 18)).pack()
    #brick_shooter
    brick_icon_path =  os.path.join(BASE_PATH, "brick breaker.jpg")

    try:
        brick_image = Image.open(brick_icon_path)
        brick_image = brick_image.resize((250, 150))
        brick_photo = ImageTk.PhotoImage(brick_image)
        def launch_brick():
            subprocess.Popen([sys.executable,os.path.join(BASE_PATH, "collision.py")])
        brick_btn = tk.Button(games_frame, image=brick_photo, text="BRICK BREAKER", compound="top",
                             font=("Helvetica Neue", 16, "bold"),
                             bg="#1e1e1e", fg="black", bd=0, command=launch_brick)
        brick_btn.image = brick_photo
        brick_btn.pack(side="left", padx=30, pady=30)
    except Exception:
        # fallback simple label
        tk.Label(games_frame, text="BRICK (missing asset)", fg="cyan", bg="black", font=("Helvetica Neue", 18)).pack()
    #hang_man
    
    hang_icon_path = os.path.join(BASE_PATH, "hang.jpg")

    try:
        hang_image = Image.open(hang_icon_path)
        hang_image = hang_image.resize((250, 150))
        hang_photo = ImageTk.PhotoImage(hang_image)

        def launch_hang():
            import hangman   # file must be named hangman.py
            hangman.run_hangman(parent_window=eplay_window)   # root = your main Dimensity window


        hang_btn = tk.Button(
            games_frame,
            image=hang_photo,
            text="HANG MAN",
            compound="top",
            font=("Helvetica Neue", 16, "bold"),
            bg="#1e1e1e",
            fg="black",
            bd=0,
            command=launch_hang
        )
        hang_btn.image = hang_photo
        hang_btn.pack(side="left", padx=30, pady=30)

    except Exception:
        tk.Label(
            games_frame,
            text="HANG (missing asset)",
            fg="cyan",
            bg="black",
            font=("Helvetica Neue", 18)
        ).pack()
    # asphalt game icon
    asphalt_icon_path = os.path.join(BASE_PATH, "asphalt.jpg")
    

    try:
        asphalt_image = Image.open(asphalt_icon_path)
        asphalt_image = asphalt_image.resize((250, 150))
        asphalt_photo = ImageTk.PhotoImage(asphalt_image)
        def launch_asphalt():
           subprocess.Popen([sys.executable, os.path.join(BASE_PATH, "asphalt.py")])
        asphalt_btn = tk.Button(games_frame, image=asphalt_photo, text="ASPHALT", compound="top",
                             font=("Helvetica Neue", 16, "bold"),
                             bg="#1e1e1e", fg="black", bd=0, command=launch_asphalt)
        asphalt_btn.image = asphalt_photo
        asphalt_btn.pack(side="left", padx=30, pady=30)
    except Exception:
        # fallback simple label
        tk.Label(games_frame, text="ASPHALT (missing asset)", fg="cyan", bg="black", font=("Helvetica Neue", 18)).pack()


import importlib.util
import sys
import os
import tkinter as _tk_mod
from tkinter import messagebox

def launch_ecalc_embedded(parent_window, ecalc_filepath):
    """
    Embed an existing calculator .py (that does `root = tk.Tk(); root.mainloop()`)
    into parent_window as a Toplevel, without editing the calculator file.
    - parent_window: the tkinter window (root or a Toplevel) to attach to.
    - ecalc_filepath: full path to your CALCI.py file.
    Returns the created Toplevel or None on error.
    """
    # sanity
    if not os.path.isfile(ecalc_filepath):
        messagebox.showerror("E-Calc Error", f"Calculator file not found:\n{ecalc_filepath}")
        return None

    # create the Toplevel that will act as the calculator's "root"
    win = _tk_mod.Toplevel(parent_window)
    win.title("E-Calc")
    try:
        win.geometry("900x700")
        win.attributes("-fullscreen",True)
    except Exception:
        pass
    
    back_btn_calci= tk.Frame(win, bg="black")
    back_btn_calci.pack(fill="x", padx=12, pady=8)
    tk.Button(back_btn_calci, text="Close", font=("Helvetica Neue", 14, "bold"),
              bg="#222222", fg="black", activebackground="#333333",
              command=win.destroy).pack(side="right")
    # attach to parent so macOS groups window with the main app
    try:
        win.transient(parent_window)
        win.focus_force()
    except Exception:
        pass

    # safe close handler
    def _on_close_ecalc():
        try:
            win.destroy()
        except Exception:
            pass
        try:
            parent_window.focus_force()
            parent_window.lift()
        except Exception:
            pass

    win.protocol("WM_DELETE_WINDOW", _on_close_ecalc)

    # ---------- Monkeypatch tkinter.Tk so the calculator's `tk.Tk()` returns our Toplevel ----------
    original_Tk = _tk_mod.Tk
    original_mainloop = getattr(_tk_mod.Tk, "mainloop", None)

    try:
        # Make tk.Tk() return our Toplevel
        _tk_mod.Tk = lambda *a, **k: win

        # Make win.mainloop a no-op for the duration of the import (so import doesn't block)
        try:
            # store original if exists and replace with noop
            if hasattr(win, "mainloop"):
                win.__orig_mainloop = win.mainloop
            win.mainloop = lambda *a, **k: None
        except Exception:
            pass

        # Import the calculator file under a unique module name
        module_name = f"ecalc_embedded_{abs(hash(ecalc_filepath))}"
        if module_name in sys.modules:
            try:
                del sys.modules[module_name]
            except Exception:
                pass

        spec = importlib.util.spec_from_file_location(module_name, ecalc_filepath)
        if spec is None:
            raise ImportError(f"Cannot load spec from: {ecalc_filepath}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            # show error and cleanup
            messagebox.showerror("E-Calc Import Error", f"Failed to load E-Calc:\n{e}")
            try:
                del sys.modules[module_name]
            except Exception:
                pass
            try:
                win.destroy()
            except Exception:
                pass
            return None

    finally:
        # restore tkinter.Tk and win.mainloop
        try:
            _tk_mod.Tk = original_Tk
        except Exception:
            pass
        try:
            if hasattr(win, "__orig_mainloop"):
                win.mainloop = win.__orig_mainloop
                del win.__orig_mainloop
        except Exception:
            pass

    # bring to front
    try:
        win.lift()
        win.focus_force()
    except Exception:
        pass

    return win
ecalc_path = os.path.join(BASE_PATH, "CALCI.py")
#ecalendar_______________________________________________________________
# ---------------- E-Calendar Button ----------------
def open_calendar():
    """
    Opens the Life Organizer calendar as a standalone window.
    """
    try:
        # Import the refactored calendar file
        from ecalendar import UltimateCalendar  # make sure your file is NOT named calendar.py
        app = UltimateCalendar()
        app.mainloop()  # launches the calendar window
    except Exception as e:
        messagebox.showerror("Calendar Error", f"Could not open calendar:\n{e}")
#clock______________________________________________________________________________________________________
# ---------------- E-Clock Widget ----------------
class ClockWidget:
    def __init__(self, parent, x=0.85, y=0.05):
        """
        parent : parent frame (bg_label)
        x, y   : relative position (0.0-1.0)
        """
        self.frame = tk.Frame(parent, bg="black", bd=0)
        self.frame.place(relx=x, rely=y, anchor="ne")  # top-right corner

        # TIME label
        self.label_time = tk.Label(self.frame, font=("Segoe UI", 80), fg="teal", bg="black")
        self.label_time.pack(anchor="e")
        # DAY label
        self.label_day = tk.Label(self.frame, font=("Segoe UI", 30), fg="white", bg="black")
        self.label_day.pack(anchor="e")
        # DATE label
        self.label_date = tk.Label(self.frame, font=("Segoe UI", 20), fg="white", bg="black")
        self.label_date.pack(anchor="e")

        # Start updates
        self.update_clock()

    def update_clock(self):
        try:
            if self.frame.winfo_exists():
                now = time.localtime()
                self.label_time.config(text=time.strftime("%I:%M %p", now))
                self.label_day.config(text=time.strftime("%A", now))
                self.label_date.config(text=time.strftime("%d %B %Y", now))
                self.frame.after(1000, self.update_clock)
        except tk.TclError:
            pass
# After bg_label and title/subtitle setup
clock_widget = ClockWidget(bg_label)




# ---------------- Dock (always visible) ----------------
bottom_frame = tk.Frame(bg_label, bg=None)
bottom_frame.place(relx=0.5, rely=0.95, anchor="s")

btn_style = {
    "font": ("Helvetica Neue", 16, "bold"),
    "bg": "#1e1e1e",
    "fg": "black",
    "activebackground": "#333",
    "activeforeground": "cyan",
    "bd": 0,
    "padx": 20,
    "pady": 10
}


tk.Button(bottom_frame, text="🧠 Chatbot",
          command=open_chatbot, **btn_style)\
  .pack(side="left", padx=20, pady=10)


tk.Button(bottom_frame, text="🎮 E-Play", command=open_eplay, **btn_style).pack(side="left", padx=20, pady=10)
tk.Button(bottom_frame, text="🧮 E-Calci",command=lambda:launch_ecalc_embedded(root,ecalc_path) ,**btn_style).pack(side="left", padx=20, pady=10)
tk.Button(bottom_frame, text="📁 E-Files", command=open_efiles, **btn_style).pack(side="left", padx=20, pady=10)
tk.Button(bottom_frame, text="📅 E-Calendar", command=open_calendar,**btn_style).pack(side="left", padx=20, pady=10)

#Added fullscreen toggle button for the whole of dimensity


root.bind("<F11>", lambda e: root.attributes("-fullscreen",
                                             not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

root.mainloop()
