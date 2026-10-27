"""
CodSoft Task 2: Simple Calculator (GUI Edition)
A modern, sleek desktop calculator with arithmetic, powers, roots, history log, and keyboard support.
"""

import math
import tkinter as tk
from tkinter import ttk

# Palette - Slate & Deep Charcoal
THEME = {
    "bg": "#12141a",
    "surface": "#1a1d26",
    "screen_bg": "#101217",
    "text": "#ffffff",
    "text_muted": "#8b949e",
    "btn_num": "#212631",
    "btn_num_hover": "#2d3342",
    "btn_num_text": "#f0f6fc",
    "btn_op": "#2d3342",
    "btn_op_hover": "#3a4254",
    "btn_op_text": "#79c0ff",
    "btn_special": "#30363d",
    "btn_special_hover": "#3d444d",
    "btn_special_text": "#ffa657",
    "btn_equal": "#238636",
    "btn_equal_hover": "#2ea043",
    "btn_equal_text": "#ffffff",
    "btn_clear": "#da3633",
    "btn_clear_hover": "#f85149",
    "border": "#30363d"
}


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator • CodSoft Task 2")
        self.root.geometry("420x620")
        self.root.minsize(360, 520)
        self.root.configure(bg=THEME["bg"])

        # Calculation state
        self.current_input = "0"
        self.stored_val = None
        self.pending_op = None
        self.reset_on_next_digit = False
        self.expression_str = ""
        self.history = []

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # 1. Top Header with title and History toggle
        top_bar = tk.Frame(self.root, bg=THEME["surface"], padx=14, pady=10)
        top_bar.pack(fill="x")

        title_lbl = tk.Label(
            top_bar, text="🧮 Calculator", font=("Segoe UI", 12, "bold"),
            bg=THEME["surface"], fg=THEME["text"]
        )
        title_lbl.pack(side="left")

        self.history_toggle_btn = tk.Button(
            top_bar, text="🕒 History", font=("Segoe UI", 9, "bold"),
            bg=THEME["btn_op"], fg=THEME["btn_op_text"],
            relief="flat", padx=10, pady=3, cursor="hand2",
            activebackground=THEME["btn_op_hover"],
            activeforeground=THEME["btn_op_text"],
            command=self.toggle_history
        )
        self.history_toggle_btn.pack(side="right")

        # Main horizontal container (Calculator + Collapsible History)
        self.main_container = tk.Frame(self.root, bg=THEME["bg"])
        self.main_container.pack(fill="both", expand=True)

        self.calc_frame = tk.Frame(self.main_container, bg=THEME["bg"], padx=14, pady=10)
        self.calc_frame.pack(side="left", fill="both", expand=True)

        # 2. Display screen
        screen_frame = tk.Frame(
            self.calc_frame, bg=THEME["screen_bg"],
            highlightbackground=THEME["border"], highlightthickness=1,
            padx=16, pady=14
        )
        screen_frame.pack(fill="x", pady=(0, 10))

        # Expression history label (smaller)
        self.expr_lbl = tk.Label(
            screen_frame, text="", font=("Consolas", 11),
            bg=THEME["screen_bg"], fg=THEME["text_muted"], anchor="e"
        )
        self.expr_lbl.pack(fill="x")

        # Main numeric display label
        self.display_lbl = tk.Label(
            screen_frame, text="0", font=("Consolas", 28, "bold"),
            bg=THEME["screen_bg"], fg=THEME["text"], anchor="e"
        )
        self.display_lbl.pack(fill="x", pady=(4, 0))

        # 3. Keypad Grid
        self.keypad = tk.Frame(self.calc_frame, bg=THEME["bg"])
        self.keypad.pack(fill="both", expand=True)

        # Configure 6 rows x 4 columns grid weights
        for r in range(6):
            self.keypad.rowconfigure(r, weight=1)
        for c in range(4):
            self.keypad.columnconfigure(c, weight=1)

        # Button layout definition: (label, row, col, type, command)
        buttons = [
            # Row 0: Scientific / Advanced
            ("xʸ", 0, 0, "special", lambda: self.set_operator("**")),
            ("x²", 0, 1, "special", self.square),
            ("√", 0, 2, "special", self.square_root),
            ("%", 0, 3, "special", lambda: self.set_operator("%")),

            # Row 1: Clear & Core Ops
            ("C", 1, 0, "clear", self.clear_all),
            ("CE", 1, 1, "special", self.clear_entry),
            ("⌫", 1, 2, "special", self.backspace),
            ("÷", 1, 3, "op", lambda: self.set_operator("/")),

            # Row 2: 7, 8, 9, ×
            ("7", 2, 0, "num", lambda: self.press_digit("7")),
            ("8", 2, 1, "num", lambda: self.press_digit("8")),
            ("9", 2, 2, "num", lambda: self.press_digit("9")),
            ("×", 2, 3, "op", lambda: self.set_operator("*")),

            # Row 3: 4, 5, 6, -
            ("4", 3, 0, "num", lambda: self.press_digit("4")),
            ("5", 3, 1, "num", lambda: self.press_digit("5")),
            ("6", 3, 2, "num", lambda: self.press_digit("6")),
            ("-", 3, 3, "op", lambda: self.set_operator("-")),

            # Row 4: 1, 2, 3, +
            ("1", 4, 0, "num", lambda: self.press_digit("1")),
            ("2", 4, 1, "num", lambda: self.press_digit("2")),
            ("3", 4, 2, "num", lambda: self.press_digit("3")),
            ("+", 4, 3, "op", lambda: self.set_operator("+")),

            # Row 5: ±, 0, ., =
            ("±", 5, 0, "num", self.negate),
            ("0", 5, 1, "num", lambda: self.press_digit("0")),
            (".", 5, 2, "num", self.press_decimal),
            ("=", 5, 3, "equal", self.calculate_result),
        ]

        for label, row, col, btype, cmd in buttons:
            btn = self._create_button(self.keypad, label, btype, cmd)
            btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

        # 4. History Side Panel (Initially hidden)
        self.history_frame = tk.Frame(
            self.main_container, bg=THEME["surface"], width=200,
            highlightbackground=THEME["border"], highlightthickness=1
        )
        self.history_visible = False

        hist_header = tk.Frame(self.history_frame, bg=THEME["surface"], padx=8, pady=8)
        hist_header.pack(fill="x")
        tk.Label(
            hist_header, text="Calculation History",
            font=("Segoe UI", 10, "bold"), bg=THEME["surface"], fg=THEME["text"]
        ).pack(side="left")

        clear_hist_btn = tk.Button(
            hist_header, text="🗑️", font=("Segoe UI", 9),
            bg=THEME["surface"], fg=THEME["btn_clear"], relief="flat",
            cursor="hand2", command=self.clear_history
        )
        clear_hist_btn.pack(side="right")

        self.hist_listbox = tk.Listbox(
            self.history_frame, bg=THEME["screen_bg"], fg=THEME["text"],
            font=("Consolas", 10), relief="flat", highlightthickness=0,
            selectbackground=THEME["btn_op"], selectforeground=THEME["text"]
        )
        self.hist_listbox.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.hist_listbox.bind("<Double-Button-1>", self._recall_history_item)

    def _create_button(self, parent, text, btype, command):
        if btype == "num":
            bg = THEME["btn_num"]
            fg = THEME["btn_num_text"]
            active_bg = THEME["btn_num_hover"]
            font_spec = ("Segoe UI", 14, "bold")
        elif btype == "op":
            bg = THEME["btn_op"]
            fg = THEME["btn_op_text"]
            active_bg = THEME["btn_op_hover"]
            font_spec = ("Segoe UI", 15, "bold")
        elif btype == "equal":
            bg = THEME["btn_equal"]
            fg = THEME["btn_equal_text"]
            active_bg = THEME["btn_equal_hover"]
            font_spec = ("Segoe UI", 16, "bold")
        elif btype == "clear":
            bg = THEME["btn_clear"]
            fg = "#ffffff"
            active_bg = THEME["btn_clear_hover"]
            font_spec = ("Segoe UI", 13, "bold")
        else:  # special
            bg = THEME["btn_special"]
            fg = THEME["btn_special_text"]
            active_bg = THEME["btn_special_hover"]
            font_spec = ("Segoe UI", 12, "bold")

        btn = tk.Button(
            parent, text=text, font=font_spec,
            bg=bg, fg=fg, activebackground=active_bg, activeforeground=fg,
            relief="flat", cursor="hand2", command=command
        )
        return btn

    def _bind_keys(self):
        self.root.bind("<Key>", self._handle_key)

    def _handle_key(self, event):
        ch = event.char
        keysym = event.keysym

        if ch in "0123456789":
            self.press_digit(ch)
        elif ch == ".":
            self.press_decimal()
        elif ch in "+-":
            self.set_operator(ch)
        elif ch == "*":
            self.set_operator("*")
        elif ch == "/":
            self.set_operator("/")
        elif ch == "%":
            self.set_operator("%")
        elif ch == "^":
            self.set_operator("**")
        elif keysym in ("Return", "equal"):
            self.calculate_result()
        elif keysym == "BackSpace":
            self.backspace()
        elif keysym == "Escape":
            self.clear_all()

    # ---------------- Calculator Actions ----------------
    def press_digit(self, digit):
        if self.reset_on_next_digit or self.current_input == "0":
            self.current_input = str(digit)
            self.reset_on_next_digit = False
        else:
            if len(self.current_input) < 18:
                self.current_input += str(digit)
        self._update_display()

    def press_decimal(self):
        if self.reset_on_next_digit:
            self.current_input = "0."
            self.reset_on_next_digit = False
        elif "." not in self.current_input:
            self.current_input += "."
        self._update_display()

    def negate(self):
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self._update_display()

    def backspace(self):
        if self.reset_on_next_digit:
            return
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
            if self.current_input == "-":
                self.current_input = "0"
        else:
            self.current_input = "0"
        self._update_display()

    def clear_entry(self):
        self.current_input = "0"
        self._update_display()

    def clear_all(self):
        self.current_input = "0"
        self.stored_val = None
        self.pending_op = None
        self.reset_on_next_digit = False
        self.expression_str = ""
        self.expr_lbl.configure(text="")
        self._update_display()

    def set_operator(self, op):
        try:
            val = float(self.current_input)
        except ValueError:
            return

        op_symbols = {"+": "+", "-": "-", "*": "×", "/": "÷", "%": "%", "**": "^"}
        sym = op_symbols.get(op, op)

        if self.pending_op and not self.reset_on_next_digit:
            self.calculate_result(chaining=True)
            val = float(self.current_input)

        self.stored_val = val
        self.pending_op = op
        self.reset_on_next_digit = True
        self.expression_str = f"{self._format_num(val)} {sym}"
        self.expr_lbl.configure(text=self.expression_str)

    def calculate_result(self, chaining=False):
        if self.pending_op is None or self.stored_val is None:
            return

        try:
            b = float(self.current_input)
            a = self.stored_val
            op = self.pending_op

            if op == "+":
                res = a + b
            elif op == "-":
                res = a - b
            elif op == "*":
                res = a * b
            elif op == "/":
                if b == 0:
                    self.show_error("Cannot divide by 0")
                    return
                res = a / b
            elif op == "%":
                if b == 0:
                    self.show_error("Cannot divide by 0")
                    return
                res = a % b
            elif op == "**":
                try:
                    res = a ** b
                except OverflowError:
                    self.show_error("Overflow Error")
                    return
            else:
                return

            op_symbols = {"+": "+", "-": "-", "*": "×", "/": "÷", "%": "%", "**": "^"}
            sym = op_symbols.get(op, op)
            full_expr = f"{self._format_num(a)} {sym} {self._format_num(b)} ="
            formatted_res = self._format_num(res)

            self.expr_lbl.configure(text=full_expr)
            self.current_input = formatted_res

            # Log to history
            hist_item = f"{self._format_num(a)} {sym} {self._format_num(b)} = {formatted_res}"
            self.history.append(hist_item)
            self.hist_listbox.insert(tk.END, hist_item)
            self.hist_listbox.see(tk.END)

            if not chaining:
                self.pending_op = None
                self.stored_val = None
                self.reset_on_next_digit = True

            self._update_display()

        except Exception as e:
            self.show_error("Calculation Error")

    def square(self):
        try:
            val = float(self.current_input)
            res = val ** 2
            formatted_res = self._format_num(res)
            self.expr_lbl.configure(text=f"sqr({self._format_num(val)}) =")
            self.current_input = formatted_res
            self.reset_on_next_digit = True
            self._update_display()
        except Exception:
            self.show_error("Error")

    def square_root(self):
        try:
            val = float(self.current_input)
            if val < 0:
                self.show_error("Invalid Input (√ of negative)")
                return
            res = math.sqrt(val)
            formatted_res = self._format_num(res)
            self.expr_lbl.configure(text=f"√({self._format_num(val)}) =")
            self.current_input = formatted_res
            self.reset_on_next_digit = True
            self._update_display()
        except Exception:
            self.show_error("Error")

    def show_error(self, message):
        self.current_input = "0"
        self.stored_val = None
        self.pending_op = None
        self.reset_on_next_digit = True
        self.expr_lbl.configure(text="Error")
        self.display_lbl.configure(text=message, font=("Consolas", 16, "bold"), fg=THEME["btn_clear"])

    def _format_num(self, num):
        if isinstance(num, (int, float)):
            if math.isinf(num) or math.isnan(num):
                return str(num)
            # Check if whole number
            if float(num).is_integer():
                return str(int(num))
            # Format float nicely, stripping trailing zeroes
            formatted = f"{num:.10f}".rstrip("0").rstrip(".")
            return formatted
        return str(num)

    def _update_display(self):
        text = self.current_input
        # Adjust font size dynamically if number is long
        if len(text) > 14:
            font_size = 18
        elif len(text) > 10:
            font_size = 22
        else:
            font_size = 28

        self.display_lbl.configure(
            text=text, font=("Consolas", font_size, "bold"), fg=THEME["text"]
        )

    # ---------------- History Panel ----------------
    def toggle_history(self):
        if self.history_visible:
            self.history_frame.pack_forget()
            self.history_visible = False
            self.history_toggle_btn.configure(bg=THEME["btn_op"])
            self.root.geometry("420x620")
        else:
            self.history_frame.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)
            self.history_visible = True
            self.history_toggle_btn.configure(bg=THEME["btn_special"])
            self.root.geometry("640x620")

    def clear_history(self):
        self.history.clear()
        self.hist_listbox.delete(0, tk.END)

    def _recall_history_item(self, event):
        sel = self.hist_listbox.curselection()
        if sel:
            item = self.hist_listbox.get(sel[0])
            if "=" in item:
                result_part = item.split("=")[-1].strip()
                self.current_input = result_part
                self.reset_on_next_digit = True
                self._update_display()


def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
