import tkinter as tk
from tkinter import ttk, messagebox
import itertools
import hashlib
import time
import threading

# ---------- big brain behind code ----------

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def brute_force(target_hash, charset, max_len, update_callback, stop_flag):
    attempts = 0
    start = time.time()

    for length in range(1, max_len + 1):
        for combo in itertools.product(charset, repeat=length):
            if stop_flag["stop"]:
                return None, attempts, time.time() - start

            attempts += 1
            guess = ''.join(combo)

            if attempts % 500 == 0:
                update_callback(guess, attempts, time.time() - start)

            if hash_password(guess) == target_hash:
                return guess, attempts, time.time() - start

    return None, attempts, time.time() - start
# ---------- user interface ----------
class PasswordCrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ethical Password Cracker Simulator 🔐")
        self.root.geometry("500x420")

        self.stop_flag = {"stop": False}

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Password (simulation only):").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(self.root, text="Character Set:").pack()
        self.charset_var = tk.StringVar(value="abc")

        ttk.Radiobutton(self.root, text="Lowercase (a–z)", variable=self.charset_var, value="abcdefghijklmnopqrstuvwxyz").pack()
        ttk.Radiobutton(self.root, text="Letters + Numbers", variable=self.charset_var,
                        value="abcdefghijklmnopqrstuvwxyz0123456789").pack()
        ttk.Radiobutton(self.root, text="Letters + Numbers + Symbols", variable=self.charset_var,
                        value="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*").pack()

        tk.Label(self.root, text="Max Password Length:").pack(pady=(10, 0))
        self.max_len = tk.IntVar(value=4)
        ttk.Spinbox(self.root, from_=1, to=6, textvariable=self.max_len, width=5).pack()

        self.start_btn = ttk.Button(self.root, text="Start Simulation", command=self.start)
        self.start_btn.pack(pady=10)

        self.stop_btn = ttk.Button(self.root, text="Stop", command=self.stop)
        self.stop_btn.pack()

        self.status = tk.Label(self.root, text="Status: Waiting", wraplength=480)
        self.status.pack(pady=10)

        self.stats = tk.Label(self.root, text="", wraplength=480)
        self.stats.pack()

    def update_status(self, guess, attempts, elapsed):
        self.status.config(text=f"Trying: {guess}")
        self.stats.config(
            text=f"Attempts: {attempts}\nTime: {elapsed:.2f}s\nAttempts/sec: {attempts / max(elapsed, 0.001):.0f}"
        )

    def start(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Enter a password first.")
            return

        self.stop_flag["stop"] = False
        self.start_btn.config(state="disabled")

        target_hash = hash_password(password)
        charset = self.charset_var.get()
        max_len = self.max_len.get()

        threading.Thread(
            target=self.run_cracker,
            args=(target_hash, charset, max_len),
            daemon=True
        ).start()

    def run_cracker(self, target_hash, charset, max_len):
        guess, attempts, duration = brute_force(
            target_hash,
            charset,
            max_len,
            self.update_status,
            self.stop_flag
        )

        self.start_btn.config(state="normal")

        if guess:
            messagebox.showinfo(
                "Password Cracked",
                f"Password: {guess}\nAttempts: {attempts}\nTime: {duration:.2f}s"
            )
        else:
            messagebox.showwarning(
                "Not Found",
                f"Password not cracked.\nAttempts: {attempts}\nTime: {duration:.2f}s"
            )

    def stop(self):
        self.stop_flag["stop"] = True
        self.start_btn.config(state="normal")
        self.status.config(text="Status: Stopped")
# ---------- Run ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCrackerApp(root)
    root.mainloop()
