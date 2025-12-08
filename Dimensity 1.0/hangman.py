import tkinter as tk
from tkinter import messagebox
import random

# ---------------------------------------
# WORD CATEGORIES WITH LEVELS
# ---------------------------------------
WORDS = {
    "Animals": {
        "Easy": ["cat", "dog", "cow", "lion"],
        "Medium": ["elephant", "giraffe", "dolphin"],
        "Hard": ["chameleon", "hippopotamus", "orangutan"]
    },
    "Countries": {
        "Easy": ["india", "china", "egypt"],
        "Medium": ["brazil", "australia", "germany"],
        "Hard": ["kazakhstan", "uzbekistan", "switzerland"]
    },
    "Food": {
        "Easy": ["rice", "milk", "bread"],
        "Medium": ["noodles", "dosa", "biryani"],
        "Hard": ["guacamole", "lasagna", "tiramisu"]
    },
    "Technology": {
        "Easy": ["mouse", "robot", "phone"],
        "Medium": ["python", "laptop", "android"],
        "Hard": ["microprocessor", "neuralnetwork", "encryption"]
    },
    "Space": {
        "Easy": ["sun", "moon", "star"],
        "Medium": ["planet", "galaxy", "nebula"],
        "Hard": ["supernova", "andromeda", "exoplanet"]
    }
}

# Hangman pictures (unchanged)
HANGMAN_PICS = [
    """
    +---+
        |
        |
        |
       ===
    """,
    """
    +---+
    O   |
        |
        |
       ===
    """,
    """
    +---+
    O   |
    |   |
        |
       ===
    """,
    """
    +---+
    O   |
   /|   |
        |
       ===
    """,
    """
    +---+
    O   |
   /|\\  |
        |
       ===
    """,
    """
    +---+
    O   |
   /|\\  |
   /    |
       ===
    """,
    """
    +---+
    O   |
   /|\\  |
   / \\  |
       ===
    """
]


# ---------------------------------------
# MAIN GAME CLASS (unchanged internals)
# ---------------------------------------
class HangmanGUI:
    def __init__(self, root):   # FIXED CONSTRUCTOR
        self.root = root
        self.root.title("🎮 Hangman Game - GUI Version")
        # set a sensible default size if none provided
        try:
            self.root.geometry("600x500")
        except Exception:
            pass

        self.category = tk.StringVar(value="Animals")
        self.level = tk.StringVar(value="Easy")

        self.create_settings_ui()

    # ---------------------------------------
    # SETTINGS SCREEN
    # ---------------------------------------
    def create_settings_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="🎮 Hangman Game", font=("Arial", 24, "bold")).pack(pady=20)

        tk.Label(self.root, text="Choose Category:", font=("Arial", 14)).pack()
        tk.OptionMenu(self.root, self.category, *WORDS.keys()).pack(pady=5)

        tk.Label(self.root, text="Choose Difficulty:", font=("Arial", 14)).pack()
        tk.OptionMenu(self.root, self.level, "Easy", "Medium", "Hard").pack(pady=5)

        tk.Button(self.root, text="Start Game", font=("Arial", 14, "bold"),
                  command=self.start_game, bg="green", fg="black").pack(pady=20)

    # ---------------------------------------
    # START GAME
    # ---------------------------------------
    def start_game(self):
        self.word = random.choice(WORDS[self.category.get()][self.level.get()])
        self.guessed = ["_"] * len(self.word)
        self.used = []
        self.wrong = 0

        # Hints
        if self.level.get() == "Easy":
            self.guessed[0] = self.word[0]
            self.guessed[-1] = self.word[-1]
        elif self.level.get() == "Medium":
            if len(self.word) > 0:
                idx = random.randint(0, len(self.word) - 1)
                self.guessed[idx] = self.word[idx]

        self.build_game_ui()

    # ---------------------------------------
    # GAME UI
    # ---------------------------------------
    def build_game_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.hangman_label = tk.Label(self.root, text=HANGMAN_PICS[self.wrong],
                                      font=("Courier", 14), justify="left")
        self.hangman_label.pack()

        self.word_label = tk.Label(self.root, text=" ".join(self.guessed),
                                   font=("Arial", 24))
        self.word_label.pack(pady=10)

        self.used_label = tk.Label(self.root, text="Used: ", font=("Arial", 14))
        self.used_label.pack(pady=5)

        self.entry = tk.Entry(self.root, font=("Arial", 16))
        self.entry.pack()
        self.entry.focus()

        tk.Button(self.root, text="Guess", font=("Arial", 14),
                  command=self.check_guess, bg="blue", fg="black").pack(pady=10)

        tk.Button(self.root, text="Get Hint", font=("Arial", 12),
                  command=self.hint).pack(pady=5)

        tk.Button(self.root, text="Back to Menu", command=self.create_settings_ui).pack(pady=10)

    # ---------------------------------------
    # CHECK GUESS
    # ---------------------------------------
    def check_guess(self):
        letter = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if not letter.isalpha() or len(letter) != 1:
            messagebox.showwarning("Invalid", "Enter a single letter!")
            return

        if letter in self.used:
            messagebox.showwarning("Used", "You already used that letter!")
            return

        self.used.append(letter)

        if letter in self.word:
            for i, ch in enumerate(self.word):
                if ch == letter:
                    self.guessed[i] = letter
        else:
            self.wrong += 1

        self.update_ui()

    # ---------------------------------------
    # HINT SYSTEM
    # ---------------------------------------
    def hint(self):
        unopened = [i for i, ch in enumerate(self.guessed) if ch == "_"]
        if unopened:
            idx = random.choice(unopened)
            self.guessed[idx] = self.word[idx]
            self.update_ui()

    # ---------------------------------------
    # UPDATE UI
    # ---------------------------------------
    def update_ui(self):
        # clamp wrong to available pics
        idx = min(self.wrong, len(HANGMAN_PICS) - 1)
        self.hangman_label.config(text=HANGMAN_PICS[idx])
        self.word_label.config(text=" ".join(self.guessed))
        self.used_label.config(text="Used: " + ", ".join(self.used))

        if "_" not in self.guessed:
            messagebox.showinfo("WIN 🎉", f"You guessed the word: {self.word}")
            self.create_settings_ui()

        elif self.wrong >= len(HANGMAN_PICS) - 1:
            messagebox.showerror("GAME OVER 💀", f"The word was: {self.word}")
            self.create_settings_ui()


# ---------------------------------------
# RUN THE GAME (safe wrapper)
# ---------------------------------------
def run_hangman(parent_window=None):
    """
    parent_window: if provided -> embed in a Toplevel attached to parent_window
                   if None -> run in standalone Tk() (useful for subprocess)
    """
    if parent_window is None:
        # Standalone mode: create independent root and run mainloop
        root = tk.Tk()
        HangmanGUI(root)
        root.mainloop()
        return None
    else:
        # Embedded mode: create a Toplevel attached to the parent window
        try:
            win = tk.Toplevel(parent_window)
        except Exception:
            # fallback: if something went wrong with Toplevel, create independent Tk
            root = tk.Tk()
            HangmanGUI(root)
            root.mainloop()
            return None

        # Make the toplevel behave well with the parent (no aggressive grab)
        win.transient(parent_window)
        try:
            win.focus_force()
        except Exception:
            pass

        # install safe close handler that does minimal cleanup
        def _on_close():
            try:
                # if current grab belongs to this window, release it safely
                if win.grab_current() is not None:
                    try:
                        win.grab_release()
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                win.destroy()
            except Exception:
                pass
            try:
                parent_window.focus_force()
            except Exception:
                pass

        win.protocol("WM_DELETE_WINDOW", _on_close)

        # build UI and return immediately (non-blocking)
        HangmanGUI(win)
        return win


# Allow running hangman.py directly
if __name__ == "__main__":
    run_hangman(parent_window=None)
