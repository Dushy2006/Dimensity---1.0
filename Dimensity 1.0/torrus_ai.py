import os
from google import genai
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import sys

"""*****************************************************************************************************************************"""
API_KEY=os.getenv("API_KEY")
if not API_KEY:
    # simple friendly popup and exit so the user knows why the app won't run
    import tkinter.messagebox as mb
    mb.showerror("Missing API Key", "Environment variable GEN_AI_API_KEY not set. Set it and restart.")
    sys.exit(1) 


client = genai.Client(api_key=API_KEY)
model = "gemini-2.0-flash-exp"


BASE_PATH = r"C:\Users\Chethan S\OneDrive\Desktop\Dimensity 1.0\Dimensity---1.0\Dimensity 1.0"
"""****************************************************************************************************************************"""
#                                           BASE APP
root=tk.Tk()
root.title("TAURUS AI")
root.geometry("1980x1080")
root.configure(bg="#000000")
root.attributes("-fullscreen", True)

HEADER_BG= "#070708"
HEADER_TEXT= "#EDEDED"

header=tk.Frame(root,bg=HEADER_BG,height=50)
header.pack(fill=tk.X, side=tk.TOP)

title_label=tk.Label(header,text="TAURUS AI",bg=HEADER_BG,fg=HEADER_TEXT,font=("Cascadia Code",16,"bold"))
title_label.pack(side=tk.LEFT, padx=18)

subtitle_label=tk.Label(header, text="Personal AI Assistant",bg=HEADER_BG, fg="#3B07F8", font=("Cascadia Code", 16 , "bold"))
subtitle_label.pack(side=tk.LEFT, padx=(6,0))

back_btn_settings= tk.Frame(root, bg="black")
back_btn_settings.pack(fill="x", padx=12, pady=8)
tk.Button(back_btn_settings, text="Close", font=("Helvetica Neue", 14, "bold"),
              bg="#222222", fg="black", activebackground="#333333",
              command=root.destroy,cursor="hand2").pack(side="right")

"""****************************************************************************************************************************"""
#                                            COLOURS
BG = "#0C0A0B"
TEXT = "#FFFFFF"
ENTRY_BG = "#1A1A1A"
BTN_BG = "#262626"
BTN_HOVER = "#3A3A3A"
CLEAR_BTN_BG = "#2A2A2A"
CLEAR_BTN_HOVER = "#3B3B3B"
"""****************************************************************************************************************************"""
#                                            HELPERS FOR EXTRA FUNCTIONS
def now_ts():
    return datetime.now().strftime("%I:%M %p")

def clear_chat():
    chat_box.config(state="normal")
    chat_box.delete(8.0, tk.END)
    chat_box.config(state="disabled")
    chat_box.see(tk.END)

def clear_enter(e):
    clear_btn["bg"] = CLEAR_BTN_HOVER
def clear_leave(e):
    clear_btn["bg"] = CLEAR_BTN_BG

clear_btn = tk.Button(header, text="Clear Chat", bg=CLEAR_BTN_BG, fg=HEADER_TEXT,
                      relief="flat", padx=12, pady=6, command=clear_chat , cursor="hand2")
clear_btn.pack(side=tk.RIGHT, padx=12)

def show_typing():
    chat_box.config(state="normal")
    chat_box.insert(tk.END, "Bot is thinking...\n", "typing")
    chat_box.tag_config("typing", foreground="#888888", font=("Segoe UI", 10, "italic"))
    chat_box.config(state="disabled")
    chat_box.see(tk.END)


def remove_typing():
    chat_box.config(state="normal")
                                                  # remove any text that has the "typing" tag
    ranges = chat_box.tag_ranges("typing")
    if ranges:
        chat_box.delete(ranges[0], ranges[1])
    chat_box.config(state="disabled")



"""****************************************************************************************************************************"""

#                CHAT WINDOW AND ENTRY OF THE TEXT AND SEND BUTTON WITH SOME DESIGNS AND BGCOLOUR AND TEXT COLOUR

chat_box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    state="disabled",
    bg=BG,
    fg=TEXT,
    font=("Cascadia Code", 11),
    insertbackground="white",
    borderwidth=0,
    )
chat_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

"""**************************************************************************************************************************"""
# ------------------                                           Message bubble + avatar setup         ------------------
#                                                  (paste immediately after chat_box.pack(...))

# Tag styles for bubble look
chat_box.tag_config(
    "bot_bubble",
    background="#111318",      # bubble background
    foreground="#E6E6E6",        # bubble text
    lmargin1=10, lmargin2=12,    # left margin (first line, other lines)
    rmargin=80,                 # right margin (keeps bubble narrow)
    spacing3=6,                    # space after paragraph
    font=("Cascadia Code", 11),
    justify="left"
)

chat_box.tag_config(
    "user_bubble",
    background="#1C1C1C",    
    foreground="#FB9405",
    lmargin1=80, lmargin2=80,   # push bubble to the right
    rmargin=10,
    spacing3=6,
    font=("Cascadia Code", 11),
    justify="right"
)

#                             Avatars (emoji text) - keeps simple, no external images
chat_box.tag_config("bot_avatar", font=("Segoe UI Emoji", 12), foreground="#9AA0A6")
chat_box.tag_config("user_avatar", font=("Segoe UI Emoji", 12), foreground="#FFFFFF")
"""**************************************************************************************************************************"""
#                      Helper functions to insert messages — use these instead of direct chat_box.insert

def insert_bot_message(text, ts=None):
    """Insert a left-aligned bubble with bot avatar."""
    if ts:
        msg = f"[{ts}] "
        send_btn.config(state="normal")
    else:
        msg = ""
        send_btn.config(state="normal")
    
    
    chat_box.config(state="normal")
    # avatar + bubble text
    chat_box.insert(tk.END, "🤖 ", "bot_avatar")
    chat_box.insert(tk.END, msg + text + "\n\n", "bot_bubble")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)
    

def insert_user_message(text, ts=None):
    """Insert a right-aligned bubble with user avatar."""
    if ts:
        msg = f"[{ts}] "
    else:
        msg = ""
    chat_box.config(state="normal")
    # avatar followed by a right-justified bubble
    chat_box.insert(tk.END, "🙂", "user_avatar")
    chat_box.insert(tk.END, msg + text + "\n\n", "user_bubble")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)

#                                                End of bubble setup

"""*****************************************************************************************************************************"""
entry = tk.Entry(
    root,
    bg=ENTRY_BG,
    fg=TEXT,
    font=("Cascadia Code", 12),
    insertbackground="white",
    relief="flat",
    borderwidth=2,
)
entry.pack(fill=tk.X, padx=10, pady=(0, 10))


send_btn = tk.Button(
    root,
    text="Send",
    bg=BTN_BG,
    fg=TEXT,
    font=("Segoe UI", 12),
    relief="flat",
    activebackground=BTN_HOVER,
    cursor="hand2",
)
send_btn.pack(pady=(0, 10))

"""***************************************************************************************************************************"""
"""***************************************************************************************************************************"""
#                SENDING THE REQUEST TO GENAI API TO GET THE ANSWER AND SHOW BOT TYPING WHILE SENDING


def send_message():
    user_text = entry.get().strip()
    send_btn.config(state="disabled")
    if not user_text:
        return
    entry.delete(0, tk.END)
    
    # configure once
    chat_box.tag_config("user_bubble", lmargin1=10, lmargin2=60, rmargin=10, spacing3=6, font=("Cascadia Code",11,"bold"))
    chat_box.tag_config("bot_bubble", lmargin1=60, lmargin2=10, rmargin=10, spacing3=6, font=("Cascadia Code",11))

#                                          insert user bubble (example)
    insert_user_message(user_text, ts=now_ts())
    
    #                                      show typing indicator BEFORE sending
    show_typing()

    root.update()  #                       update UI immediately

    try:
        response = client.models.generate_content(
            model=model,
            contents=user_text
        )
        bot_text = response.text
    except Exception as e:
        msg = str(e).lower()
        if "quota" in msg or "exhausted" in msg:
            bot_text = "Free-tier API quota reached. Please try again later."
        else:
            bot_text = "Error communicating with AI."
    finally:
        remove_typing()

    insert_bot_message(bot_text, ts=now_ts())
    send_btn.config(state="normal") 

    


"""***************************************************************************************************************************"""


clear_btn.bind("<Enter>", clear_enter)
clear_btn.bind("<Leave>", clear_leave)
send_btn.bind("<Enter>", lambda e: send_btn.config(bg=BTN_HOVER))
send_btn.bind("<Leave>", lambda e: send_btn.config(bg=BTN_BG))
# CLICK  F11 FOR FULLSCREEN
root.bind("<F11>", lambda e: root.attributes("-fullscreen",
                                             not root.attributes("-fullscreen")))
#                                  Exit fullscreen (but keep window open) with ESC BUTTON
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
# Enter key sends messages
entry.bind("<Return>", lambda e: send_message())



"""****************************************************************************************************************************"""
"""****************************************************************************************************************************"""
"""****************************************************************************************************************************"""
"""****************************************************************************************************************************"""
#                       THIS SECTION FOR TELLING THE OPEN APP_NAME SENTENCE SHOULD NOT GO TO THE API AS A REQUEST
#                         RATHER IT SHOULD SEE THE APP IS PRESENT IN THE FOLDER SPECIFIED WHICH MENTIONED 
#                                                    IN ALLOWED APPS
import subprocess, threading, re, os

ALLOWED_APPS = {
    "calci":    ("subprocess", os.path.join(BASE_PATH,"CALCI.py")),
    "brick_game": ("subprocess", os.path.join(BASE_PATH,"collision.py")),
    "asphalt" : ("subprocess", os.path.join(BASE_PATH,"asphalt.py")),
    "hangman" : ("subprocess", os.path.join(BASE_PATH,"hangman.py")),
    "pong"   :  ("subprocess", os.path.join(BASE_PATH,"pong.py")),
    "ecalendar" : ("subprocess", os.path.join(BASE_PATH,"ecalendar.py")), 
    "listapps":  ("apps",None)
    }


"""***************************************************************************************************************************"""

def _launch_subprocess(path):                         
    if not os.path.exists(path):                     #THIS IS TO LAUNCH THE PYTHON PROGRAMS IN THE SPECIFID FOLDER
        raise FileNotFoundError(path)                      
    # run in separate process
    subprocess.Popen([sys.executable, path])

# def _launch_startfile(path):
#      if not os.path.exists(path):
#          raise FileNotFoundError(path)               #THIS IS TO LAUNCH ANY EXE FILE IN THE SPECIFIED FOLDER
#      os.startfile(path)   # windows only


"""***************************************************************************************************************************"""

def safe_launch(key):
    """Launch whitelisted app in background. Returns (ok:bool, msg:str)."""
    ent = ALLOWED_APPS.get(key.lower())
    if not ent:
        return False, f"App '{key}' is not in our OS."
    typ, target = ent
    try:
        if typ == "subprocess":
            threading.Thread(target=_launch_subprocess, args=(target,), daemon=True).start()
            return True, f"Opening {key}..."
        if typ == "apps":
          return True, f"The apps in the OS are: {list(ALLOWED_APPS.keys())}"

        # if typ == "startfile":
        #      threading.Thread(target=_launch_startfile, args=(target,), daemon=True).start()
        #      return True, f"Opening {key}..."
        return False, "Unknown launch type."
    except Exception as e:
        return False, f"Failed to open {key}: {e}"


"""***************************************************************************************************************************"""

# Keep original send_message accessible      
_orig_send_message = send_message

def _send_wrapper(event=None):
    txt = entry.get().strip()
    if not txt:
        return
    # check "open appname" (single token name)
    m = re.match(r"^\s*open\s+([A-Za-z0-9_.-]+)\s*$", txt, re.I)
    if m:
        app = m.group(1).lower()
        ok, msg = safe_launch(app)
        # show user message (same UI behavior as original)
        entry.delete(0, tk.END)
        chat_box.config(state="normal")
        chat_box.insert(tk.END, f"You: {txt}\n", "user")
        chat_box.insert(tk.END, f"Bot: {msg}\n\n", "bot")
        chat_box.config(state="disabled")
        chat_box.see(tk.END)
        return
    # otherwise call original function (API path)
    return _orig_send_message()



"""***************************************************************************************************************************"""


entry.bind("<Return>", lambda e: send_message())
# Re-bind Enter key and Send button to wrapper
# (this replaces the existing binding so you don't need to modify original send_message)
entry.bind("<Return>", _send_wrapper)
send_btn.config(command=_send_wrapper)


"""***************************************************************************************************************************"""
"""***************************************************************************************************************************"""
"""***************************************************************************************************************************"""
"""***************************************************************************************************************************"""


welcome_text = (
    "Welcome to TORUS AI — your personal assistant.\n\n"
    "• Ask questions, get answers, and explore ideas.\n"
    "• Type commands like `open listapps` to launch allowed apps.\n\n"
    "Tip: Press F11 to toggle fullscreen, Esc to exit fullscreen."
)
insert_bot_message(welcome_text)




"""***************************************************************************************************************************"""
"""***************************************************************************************************************************"""
"""***************************************************************************************************************************"""
"""***************************************************************************************************************************"""


root.mainloop()
