"""
CodSoft Task 3: Password Generator (GUI Edition)
A modern, secure password generator with strength estimation, entropy meter, history, and clipboard support.
"""

import math
import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox

# Palette - Deep Charcoal & Emerald / Cyan
THEME = {
    "bg": "#11141c",
    "surface": "#181d28",
    "surface_alt": "#222938",
    "surface_hover": "#2c3447",
    "border": "#2d3748",
    "text": "#f1f5f9",
    "text_muted": "#94a3b8",
    "accent_cyan": "#38bdf8",
    "accent_green": "#10b981",
    "accent_yellow": "#f59e0b",
    "accent_orange": "#f97316",
    "accent_red": "#ef4444",
    "card_bg": "#151923"
}


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator • CodSoft Task 3")
        self.root.geometry("560x730")
        self.root.minsize(480, 640)
        self.root.configure(bg=THEME["bg"])

        # Options state
        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.no_ambiguous_var = tk.BooleanVar(value=False)
        self.show_password_var = tk.BooleanVar(value=True)

        self.current_password = ""
        self.history = []

        self._setup_styles()
        self._build_ui()
        self.generate()

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Progress bar (Strength meter)
        style.configure(
            "Strength.Horizontal.TProgressbar",
            troughcolor=THEME["surface_alt"],
            bordercolor=THEME["surface"],
            thickness=8
        )

        # Scale slider
        style.configure(
            "Horizontal.TScale",
            troughcolor=THEME["surface_alt"],
            background=THEME["accent_cyan"]
        )

    def _build_ui(self):
        # 1. Header Frame
        header = tk.Frame(self.root, bg=THEME["surface"], padx=20, pady=16)
        header.pack(fill="x")

        title_row = tk.Frame(header, bg=THEME["surface"])
        title_row.pack(fill="x")

        icon_lbl = tk.Label(
            title_row, text="🔐", font=("Segoe UI", 20),
            bg=THEME["surface"], fg=THEME["accent_cyan"]
        )
        icon_lbl.pack(side="left", padx=(0, 10))

        title_lbl = tk.Label(
            title_row, text="Password Generator", font=("Segoe UI", 18, "bold"),
            bg=THEME["surface"], fg=THEME["text"]
        )
        title_lbl.pack(side="left")

        desc_lbl = tk.Label(
            header, text="Generate cryptographically secure passwords with custom security parameters",
            font=("Segoe UI", 9), bg=THEME["surface"], fg=THEME["text_muted"]
        )
        desc_lbl.pack(anchor="w", pady=(4, 0))

        # Main scrollable body
        main_body = tk.Frame(self.root, bg=THEME["bg"], padx=20, pady=16)
        main_body.pack(fill="both", expand=True)

        # 2. Password Display Box (Card)
        disp_card = tk.Frame(
            main_body, bg=THEME["surface"],
            highlightbackground=THEME["border"], highlightthickness=1,
            padx=16, pady=16
        )
        disp_card.pack(fill="x", pady=(0, 14))

        # Password output entry & controls
        pw_row = tk.Frame(disp_card, bg=THEME["surface"])
        pw_row.pack(fill="x")

        self.password_entry = tk.Entry(
            pw_row, font=("Consolas", 15, "bold"),
            bg=THEME["surface_alt"], fg=THEME["text"],
            insertbackground=THEME["text"], relief="flat",
            highlightbackground=THEME["border"], highlightthickness=1
        )
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))

        # Show / Hide Toggle
        self.toggle_show_btn = tk.Button(
            pw_row, text="👁️", font=("Segoe UI", 12),
            bg=THEME["surface_alt"], fg=THEME["text"],
            activebackground=THEME["surface_hover"], relief="flat",
            padx=10, pady=6, cursor="hand2", command=self.toggle_visibility
        )
        self.toggle_show_btn.pack(side="left", padx=(0, 6))

        # Regenerate button
        refresh_btn = tk.Button(
            pw_row, text="🔄", font=("Segoe UI", 12, "bold"),
            bg=THEME["surface_alt"], fg=THEME["accent_cyan"],
            activebackground=THEME["surface_hover"], relief="flat",
            padx=10, pady=6, cursor="hand2", command=self.generate
        )
        refresh_btn.pack(side="left", padx=(0, 6))

        # Copy button
        self.copy_btn = tk.Button(
            pw_row, text="📋 Copy", font=("Segoe UI", 10, "bold"),
            bg=THEME["accent_cyan"], fg="#0b1120",
            activebackground="#7dd3fc", relief="flat",
            padx=14, pady=8, cursor="hand2", command=self.copy_to_clipboard
        )
        self.copy_btn.pack(side="left")

        # Strength Meter row
        strength_frame = tk.Frame(disp_card, bg=THEME["surface"])
        strength_frame.pack(fill="x", pady=(12, 0))

        meter_labels = tk.Frame(strength_frame, bg=THEME["surface"])
        meter_labels.pack(fill="x")

        tk.Label(
            meter_labels, text="Strength:", font=("Segoe UI", 9),
            bg=THEME["surface"], fg=THEME["text_muted"]
        ).pack(side="left")

        self.strength_badge = tk.Label(
            meter_labels, text="Strong", font=("Segoe UI", 9, "bold"),
            bg=THEME["surface"], fg=THEME["accent_green"]
        )
        self.strength_badge.pack(side="left", padx=(6, 0))

        self.entropy_lbl = tk.Label(
            meter_labels, text="85 bits entropy", font=("Segoe UI", 9),
            bg=THEME["surface"], fg=THEME["text_muted"]
        )
        self.entropy_lbl.pack(side="right")

        # Custom canvas strength bar for colored segments
        self.strength_canvas = tk.Canvas(
            strength_frame, height=6, bg=THEME["surface_alt"], highlightthickness=0
        )
        self.strength_canvas.pack(fill="x", pady=(6, 0))

        # 3. Customization Controls Card
        opts_card = tk.Frame(
            main_body, bg=THEME["surface"],
            highlightbackground=THEME["border"], highlightthickness=1,
            padx=16, pady=16
        )
        opts_card.pack(fill="x", pady=(0, 14))

        tk.Label(
            opts_card, text="Password Parameters", font=("Segoe UI", 11, "bold"),
            bg=THEME["surface"], fg=THEME["text"]
        ).pack(anchor="w")

        # Length section
        len_frame = tk.Frame(opts_card, bg=THEME["surface"])
        len_frame.pack(fill="x", pady=(10, 8))

        len_top = tk.Frame(len_frame, bg=THEME["surface"])
        len_top.pack(fill="x")

        tk.Label(
            len_top, text="Password Length:", font=("Segoe UI", 10),
            bg=THEME["surface"], fg=THEME["text"]
        ).pack(side="left")

        self.len_display = tk.Label(
            len_top, text=str(self.length_var.get()),
            font=("Segoe UI", 11, "bold"), bg=THEME["surface"], fg=THEME["accent_cyan"]
        )
        self.len_display.pack(side="right")

        # Slider
        self.slider = ttk.Scale(
            len_frame, from_=4, to=64, orient="horizontal",
            variable=self.length_var, command=self._on_slider_change,
            style="Horizontal.TScale"
        )
        self.slider.pack(fill="x", pady=(6, 4))

        # Quick length presets
        preset_frame = tk.Frame(len_frame, bg=THEME["surface"])
        preset_frame.pack(fill="x", pady=(4, 8))
        tk.Label(
            preset_frame, text="Presets: ", font=("Segoe UI", 8),
            bg=THEME["surface"], fg=THEME["text_muted"]
        ).pack(side="left")

        for p_len in [8, 12, 16, 24, 32]:
            btn = tk.Button(
                preset_frame, text=f"{p_len}", font=("Segoe UI", 8),
                bg=THEME["surface_alt"], fg=THEME["text"],
                relief="flat", padx=8, pady=2, cursor="hand2",
                command=lambda l=p_len: self.set_preset_length(l)
            )
            btn.pack(side="left", padx=2)

        # Character Pools Checklist
        tk.Label(
            opts_card, text="Character Types Included:", font=("Segoe UI", 10, "bold"),
            bg=THEME["surface"], fg=THEME["text"]
        ).pack(anchor="w", pady=(8, 4))

        pools = [
            (self.upper_var, "Uppercase Letters (A-Z)", "ABC..."),
            (self.lower_var, "Lowercase Letters (a-z)", "abc..."),
            (self.digits_var, "Digits (0-9)", "123..."),
            (self.symbols_var, "Special Symbols (!@#$%...)", "#$%..."),
            (self.no_ambiguous_var, "Avoid Ambiguous Characters (0, O, l, 1, I)", "Clear"),
        ]

        for var, title, sample in pools:
            row = tk.Frame(opts_card, bg=THEME["surface"])
            row.pack(fill="x", pady=3)

            cb = tk.Checkbutton(
                row, text=title, variable=var,
                font=("Segoe UI", 9), bg=THEME["surface"], fg=THEME["text"],
                selectcolor=THEME["surface_alt"], activebackground=THEME["surface"],
                activeforeground=THEME["text"], cursor="hand2",
                command=self.generate
            )
            cb.pack(side="left")

            tk.Label(
                row, text=sample, font=("Consolas", 8),
                bg=THEME["surface"], fg=THEME["text_muted"]
            ).pack(side="right")

        # 4. Generate Big Button
        gen_btn = tk.Button(
            main_body, text="⚡ Generate Secure Password", font=("Segoe UI", 11, "bold"),
            bg=THEME["accent_green"], fg="#072718",
            activebackground="#34d399", relief="flat",
            padx=16, pady=10, cursor="hand2", command=self.generate
        )
        gen_btn.pack(fill="x", pady=(0, 14))

        # 5. History Box
        hist_frame = tk.Frame(
            main_body, bg=THEME["surface"],
            highlightbackground=THEME["border"], highlightthickness=1,
            padx=12, pady=10
        )
        hist_frame.pack(fill="both", expand=True)

        hist_header = tk.Frame(hist_frame, bg=THEME["surface"])
        hist_header.pack(fill="x", pady=(0, 6))

        tk.Label(
            hist_header, text="Session History", font=("Segoe UI", 9, "bold"),
            bg=THEME["surface"], fg=THEME["text"]
        ).pack(side="left")

        clear_hist_btn = tk.Button(
            hist_header, text="Clear", font=("Segoe UI", 8),
            bg=THEME["surface_alt"], fg=THEME["text_muted"], relief="flat",
            cursor="hand2", command=self.clear_history
        )
        clear_hist_btn.pack(side="right")

        self.hist_listbox = tk.Listbox(
            hist_frame, bg=THEME["surface_alt"], fg=THEME["text"],
            font=("Consolas", 9), relief="flat", highlightthickness=0, height=4,
            selectbackground=THEME["surface_hover"]
        )
        self.hist_listbox.pack(fill="both", expand=True)
        self.hist_listbox.bind("<Double-Button-1>", self._recall_history)

        # Bottom status
        self.status_var = tk.StringVar(value="Ready")
        status_lbl = tk.Label(
            self.root, textvariable=self.status_var, font=("Segoe UI", 8),
            bg=THEME["bg"], fg=THEME["text_muted"], pady=6
        )
        status_lbl.pack(side="bottom")

    # ---------------- Generator Logic ----------------
    def _on_slider_change(self, val):
        length = int(float(val))
        self.len_display.configure(text=str(length))
        self.generate()

    def set_preset_length(self, length):
        self.length_var.set(length)
        self.len_display.configure(text=str(length))
        self.generate()

    def generate(self):
        length = int(self.length_var.get())
        use_upper = self.upper_var.get()
        use_lower = self.lower_var.get()
        use_digits = self.digits_var.get()
        use_symbols = self.symbols_var.get()
        no_ambig = self.no_ambiguous_var.get()

        pools = []
        if use_lower:
            pool = string.ascii_lowercase
            if no_ambig:
                pool = pool.replace("l", "")
            if pool:
                pools.append(pool)

        if use_upper:
            pool = string.ascii_uppercase
            if no_ambig:
                pool = pool.replace("I", "").replace("O", "")
            if pool:
                pools.append(pool)

        if use_digits:
            pool = string.digits
            if no_ambig:
                pool = pool.replace("0", "").replace("1", "")
            if pool:
                pools.append(pool)

        if use_symbols:
            pool = "!@#$%^&*()-_=+[]{};:,.<>?"
            pools.append(pool)

        if not pools:
            # Fallback to avoid empty
            pools.append(string.ascii_lowercase)
            self.lower_var.set(True)

        # Minimum required characters
        if length < len(pools):
            length = len(pools)
            self.length_var.set(length)
            self.len_display.configure(text=str(length))

        # Guarantee at least one character from every chosen pool
        chars = [secrets.choice(p) for p in pools]
        all_chars = "".join(pools)
        chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]

        # Secure shuffle
        secrets.SystemRandom().shuffle(chars)
        password = "".join(chars)

        self.current_password = password
        self._update_password_display()
        self._evaluate_strength(password, len(all_chars))

        # Append to history
        if not self.history or self.history[-1] != password:
            self.history.append(password)
            self.hist_listbox.insert(tk.END, f"• {password}")
            self.hist_listbox.see(tk.END)

    def _update_password_display(self):
        self.password_entry.delete(0, tk.END)
        if self.show_password_var.get():
            self.password_entry.insert(0, self.current_password)
            self.password_entry.configure(show="")
        else:
            self.password_entry.insert(0, self.current_password)
            self.password_entry.configure(show="•")

    def toggle_visibility(self):
        current = self.show_password_var.get()
        self.show_password_var.set(not current)
        self.toggle_show_btn.configure(text="👁️" if not current else "🔒")
        self._update_password_display()

    def _evaluate_strength(self, password, pool_size):
        length = len(password)
        if pool_size <= 1:
            pool_size = 2
        # Shannon Entropy = L * log2(pool_size)
        entropy = round(length * math.log2(pool_size), 1)

        self.entropy_lbl.configure(text=f"{entropy} bits entropy")

        # Determine tier
        if entropy < 35 or length < 6:
            text = "Very Weak"
            fg = THEME["accent_red"]
            fill_pct = 0.2
        elif entropy < 55 or length < 9:
            text = "Weak"
            fg = THEME["accent_orange"]
            fill_pct = 0.45
        elif entropy < 75 or length < 13:
            text = "Good"
            fg = THEME["accent_yellow"]
            fill_pct = 0.75
        else:
            text = "Strong"
            fg = THEME["accent_green"]
            fill_pct = 1.0

        self.strength_badge.configure(text=text, fg=fg)

        # Draw custom canvas bar
        self.root.update_idletasks()
        w = self.strength_canvas.winfo_width()
        if w < 10:
            w = 300
        self.strength_canvas.delete("all")
        self.strength_canvas.create_rectangle(
            0, 0, w, 6, fill=THEME["surface_alt"], outline=""
        )
        self.strength_canvas.create_rectangle(
            0, 0, int(w * fill_pct), 6, fill=fg, outline=""
        )

    def copy_to_clipboard(self):
        if not self.current_password:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_password)
        self.status_var.set("Copied password to clipboard! ✓")

        # Temporary button badge animation
        self.copy_btn.configure(
            text="✓ Copied!", bg=THEME["accent_green"], fg="#072718"
        )
        self.root.after(1500, lambda: self.copy_btn.configure(
            text="📋 Copy", bg=THEME["accent_cyan"], fg="#0b1120"
        ))

    def clear_history(self):
        self.history.clear()
        self.hist_listbox.delete(0, tk.END)

    def _recall_history(self, event):
        sel = self.hist_listbox.curselection()
        if sel:
            item = self.hist_listbox.get(sel[0])
            pw = item.replace("• ", "").strip()
            self.current_password = pw
            self.length_var.set(len(pw))
            self.len_display.configure(text=str(len(pw)))
            self._update_password_display()
            self.copy_to_clipboard()


def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
