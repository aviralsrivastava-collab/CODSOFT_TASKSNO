"""
CodSoft Task 1: To-Do List Application (GUI Edition)
A modern, feature-rich graphical task manager with persistent JSON storage.
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

FILE = "tasks.json"

# Theme colors (Catppuccin Mocha / Modern Dark palette)
THEME = {
    "bg": "#181825",            # Base background
    "surface": "#1e1e2e",       # Surface / Card background
    "surface_alt": "#313244",   # Elevated card
    "surface_hover": "#45475a", # Hover card
    "border": "#45475a",
    "text": "#cdd6f4",          # Main text
    "text_muted": "#a6adc8",    # Muted text
    "text_done": "#6c7086",     # Strikethrough/completed text
    "accent": "#89b4fa",        # Blue primary
    "accent_hover": "#b4befe",
    "accent_green": "#a6e3a1",  # Completed badge
    "accent_green_hover": "#94e2d5",
    "accent_red": "#f38ba8",    # Delete
    "accent_red_hover": "#eba0ac",
    "accent_yellow": "#f9e2af", # Warning / Edit
    "entry_bg": "#11111b",
    "entry_border": "#585b70"
}


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List • CodSoft Task 1")
        self.root.geometry("640x760")
        self.root.minsize(500, 600)
        self.root.configure(bg=THEME["bg"])

        # Data
        self.tasks = self.load_tasks()
        self.filter_mode = "all"  # 'all', 'active', 'completed'
        self.search_query = tk.StringVar()
        self.search_query.trace_add("write", lambda *_: self.render_tasks())

        self._setup_styles()
        self._build_ui()
        self.render_tasks()

    # ------------------ Persistence ------------------
    def load_tasks(self):
        if os.path.exists(FILE):
            try:
                with open(FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            except Exception:
                pass
        return []

    def save_tasks(self):
        try:
            with open(FILE, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=2)
            self.status_var.set(f"Saved {len(self.tasks)} tasks to {FILE}")
        except Exception as e:
            self.status_var.set(f"Error saving: {e}")

    # ------------------ UI Styling ------------------
    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Configure Scrollbar
        style.configure(
            "Dark.Vertical.TScrollbar",
            background=THEME["surface_alt"],
            troughcolor=THEME["bg"],
            bordercolor=THEME["bg"],
            arrowcolor=THEME["text"],
            relief="flat"
        )
        style.map(
            "Dark.Vertical.TScrollbar",
            background=[("active", THEME["accent"]), ("pressed", THEME["accent_hover"])]
        )

        # Progress bar
        style.configure(
            "Dark.Horizontal.TProgressbar",
            troughcolor=THEME["surface"],
            background=THEME["accent_green"],
            bordercolor=THEME["surface"],
            thickness=6
        )

    # ------------------ UI Construction ------------------
    def _build_ui(self):
        # 1. Header Frame
        header = tk.Frame(self.root, bg=THEME["surface"], padx=24, pady=18)
        header.pack(fill="x")

        title_row = tk.Frame(header, bg=THEME["surface"])
        title_row.pack(fill="x")

        icon_lbl = tk.Label(
            title_row, text="✓", font=("Segoe UI", 20, "bold"),
            bg=THEME["surface"], fg=THEME["accent_green"]
        )
        icon_lbl.pack(side="left", padx=(0, 10))

        title_lbl = tk.Label(
            title_row, text="Task Master", font=("Segoe UI", 20, "bold"),
            bg=THEME["surface"], fg=THEME["text"]
        )
        title_lbl.pack(side="left")

        subtitle_lbl = tk.Label(
            title_row, text="To-Do List Manager", font=("Segoe UI", 11),
            bg=THEME["surface"], fg=THEME["text_muted"]
        )
        subtitle_lbl.pack(side="left", padx=(10, 0), pady=(6, 0))

        # Progress bar & stats
        self.stats_lbl = tk.Label(
            header, text="0 of 0 tasks completed (0%)",
            font=("Segoe UI", 10), bg=THEME["surface"], fg=THEME["text_muted"]
        )
        self.stats_lbl.pack(anchor="w", pady=(10, 4))

        self.progress_bar = ttk.Progressbar(
            header, style="Dark.Horizontal.TProgressbar",
            mode="determinate", maximum=100, value=0
        )
        self.progress_bar.pack(fill="x", pady=(0, 4))

        # 2. Add Task Area
        add_frame = tk.Frame(self.root, bg=THEME["bg"], padx=20, pady=14)
        add_frame.pack(fill="x")

        entry_container = tk.Frame(
            add_frame, bg=THEME["entry_bg"],
            highlightbackground=THEME["entry_border"], highlightthickness=1, padx=8, pady=4
        )
        entry_container.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.task_entry = tk.Entry(
            entry_container, font=("Segoe UI", 12),
            bg=THEME["entry_bg"], fg=THEME["text"],
            insertbackground=THEME["text"], relief="flat"
        )
        self.task_entry.pack(fill="x", ipady=4)
        self.task_entry.bind("<Return>", lambda _: self.add_task())
        self.task_entry.focus_set()

        add_btn = tk.Button(
            add_frame, text="+ Add Task", font=("Segoe UI", 10, "bold"),
            bg=THEME["accent"], fg="#11111b", activebackground=THEME["accent_hover"],
            activeforeground="#11111b", relief="flat", padx=16, pady=7,
            cursor="hand2", command=self.add_task
        )
        add_btn.pack(side="right")

        # 3. Filter & Search Controls
        controls_frame = tk.Frame(self.root, bg=THEME["bg"], padx=20, pady=4)
        controls_frame.pack(fill="x")

        # Filter buttons container
        self.filter_btn_frame = tk.Frame(controls_frame, bg=THEME["bg"])
        self.filter_btn_frame.pack(side="left")

        self.filter_btns = {}
        for mode, label in [("all", "All"), ("active", "Active"), ("completed", "Done")]:
            btn = tk.Button(
                self.filter_btn_frame, text=label, font=("Segoe UI", 9, "bold"),
                relief="flat", padx=10, pady=4, cursor="hand2",
                command=lambda m=mode: self.set_filter(m)
            )
            btn.pack(side="left", padx=(0, 6))
            self.filter_btns[mode] = btn

        # Search bar container
        search_box = tk.Frame(
            controls_frame, bg=THEME["entry_bg"],
            highlightbackground=THEME["entry_border"], highlightthickness=1, padx=6, pady=2
        )
        search_box.pack(side="right")

        search_icon = tk.Label(
            search_box, text="🔍", font=("Segoe UI", 9),
            bg=THEME["entry_bg"], fg=THEME["text_muted"]
        )
        search_icon.pack(side="left", padx=(2, 4))

        search_entry = tk.Entry(
            search_box, textvariable=self.search_query, font=("Segoe UI", 9),
            bg=THEME["entry_bg"], fg=THEME["text"],
            insertbackground=THEME["text"], relief="flat", width=14
        )
        search_entry.pack(side="left", ipady=2)

        self._update_filter_button_styles()

        # 4. Scrollable Tasks List View
        list_container = tk.Frame(self.root, bg=THEME["bg"], padx=20, pady=6)
        list_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            list_container, bg=THEME["bg"], highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            list_container, orient="vertical", command=self.canvas.yview,
            style="Dark.Vertical.TScrollbar"
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg=THEME["bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Mouse wheel support
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 5. Bottom Toolbar
        bottom_bar = tk.Frame(self.root, bg=THEME["surface"], padx=20, pady=10)
        bottom_bar.pack(fill="x", side="bottom")

        clear_done_btn = tk.Button(
            bottom_bar, text="Clear Completed", font=("Segoe UI", 9),
            bg=THEME["surface_alt"], fg=THEME["text"], activebackground=THEME["surface_hover"],
            activeforeground=THEME["text"], relief="flat", padx=10, pady=5,
            cursor="hand2", command=self.clear_completed
        )
        clear_done_btn.pack(side="left", padx=(0, 6))

        mark_all_btn = tk.Button(
            bottom_bar, text="Mark All Done", font=("Segoe UI", 9),
            bg=THEME["surface_alt"], fg=THEME["text"], activebackground=THEME["surface_hover"],
            activeforeground=THEME["text"], relief="flat", padx=10, pady=5,
            cursor="hand2", command=self.mark_all_done
        )
        mark_all_btn.pack(side="left", padx=(0, 6))

        delete_all_btn = tk.Button(
            bottom_bar, text="Delete All", font=("Segoe UI", 9),
            bg=THEME["surface_alt"], fg=THEME["accent_red"],
            activebackground=THEME["accent_red"], activeforeground="#11111b",
            relief="flat", padx=10, pady=5, cursor="hand2", command=self.delete_all
        )
        delete_all_btn.pack(side="left")

        # Status Label
        self.status_var = tk.StringVar(value=f"Loaded {len(self.tasks)} tasks from {FILE}")
        status_lbl = tk.Label(
            bottom_bar, textvariable=self.status_var,
            font=("Segoe UI", 8), bg=THEME["surface"], fg=THEME["text_muted"]
        )
        status_lbl.pack(side="right")

    def _on_mousewheel(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def set_filter(self, mode):
        self.filter_mode = mode
        self._update_filter_button_styles()
        self.render_tasks()

    def _update_filter_button_styles(self):
        for mode, btn in self.filter_btns.items():
            if mode == self.filter_mode:
                btn.configure(
                    bg=THEME["accent"], fg="#11111b",
                    activebackground=THEME["accent_hover"], activeforeground="#11111b"
                )
            else:
                btn.configure(
                    bg=THEME["surface_alt"], fg=THEME["text_muted"],
                    activebackground=THEME["surface_hover"], activeforeground=THEME["text"]
                )

    # ------------------ Task Operations ------------------
    def add_task(self):
        title = self.task_entry.get().strip()
        if not title:
            return
        self.tasks.append({"title": title, "done": False})
        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.render_tasks()

    def toggle_task(self, idx):
        self.tasks[idx]["done"] = not self.tasks[idx]["done"]
        self.save_tasks()
        self.render_tasks()

    def edit_task(self, idx):
        current_title = self.tasks[idx]["title"]
        new_title = simpledialog.askstring(
            "Edit Task", "Update task description:",
            initialvalue=current_title, parent=self.root
        )
        if new_title is not None and new_title.strip():
            self.tasks[idx]["title"] = new_title.strip()
            self.save_tasks()
            self.render_tasks()

    def delete_task(self, idx):
        deleted = self.tasks.pop(idx)
        self.save_tasks()
        self.render_tasks()
        self.status_var.set(f"Deleted '{deleted['title']}'")

    def clear_completed(self):
        completed_count = sum(1 for t in self.tasks if t.get("done"))
        if completed_count == 0:
            messagebox.showinfo("To-Do List", "No completed tasks to clear.", parent=self.root)
            return
        if messagebox.askyesno(
            "Clear Completed",
            f"Are you sure you want to remove {completed_count} completed task(s)?",
            parent=self.root
        ):
            self.tasks = [t for t in self.tasks if not t.get("done")]
            self.save_tasks()
            self.render_tasks()

    def mark_all_done(self):
        for t in self.tasks:
            t["done"] = True
        self.save_tasks()
        self.render_tasks()

    def delete_all(self):
        if not self.tasks:
            return
        if messagebox.askyesno(
            "Delete All",
            "Are you sure you want to delete ALL tasks?",
            parent=self.root
        ):
            self.tasks.clear()
            self.save_tasks()
            self.render_tasks()

    # ------------------ Render Task Cards ------------------
    def render_tasks(self):
        # Clear existing card widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Update stats
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.get("done"))
        pct = int((completed / total) * 100) if total > 0 else 0
        self.stats_lbl.configure(text=f"{completed} of {total} tasks completed ({pct}%)")
        self.progress_bar["value"] = pct

        # Filter tasks
        query = self.search_query.get().strip().lower()
        visible_items = []
        for real_idx, task in enumerate(self.tasks):
            if self.filter_mode == "active" and task.get("done"):
                continue
            if self.filter_mode == "completed" and not task.get("done"):
                continue
            if query and query not in task.get("title", "").lower():
                continue
            visible_items.append((real_idx, task))

        # Empty state
        if not visible_items:
            empty_frame = tk.Frame(self.scrollable_frame, bg=THEME["bg"], pady=60)
            empty_frame.pack(fill="x")

            if query:
                msg = f"No tasks matching '{query}'"
                submsg = "Try a different search keyword"
                icon = "🔍"
            elif self.filter_mode == "active":
                msg = "All caught up!"
                submsg = "No active pending tasks right now."
                icon = "🎉"
            elif self.filter_mode == "completed":
                msg = "No completed tasks"
                submsg = "Complete a task to see it here."
                icon = "📋"
            else:
                msg = "Your task list is empty"
                submsg = "Add a new task above to get started!"
                icon = "✨"

            tk.Label(
                empty_frame, text=icon, font=("Segoe UI", 34),
                bg=THEME["bg"], fg=THEME["accent"]
            ).pack()
            tk.Label(
                empty_frame, text=msg, font=("Segoe UI", 13, "bold"),
                bg=THEME["bg"], fg=THEME["text"]
            ).pack(pady=(6, 2))
            tk.Label(
                empty_frame, text=submsg, font=("Segoe UI", 10),
                bg=THEME["bg"], fg=THEME["text_muted"]
            ).pack()
            return

        # Render each visible task card
        for real_idx, task in visible_items:
            is_done = task.get("done", False)

            card = tk.Frame(
                self.scrollable_frame,
                bg=THEME["surface"] if not is_done else THEME["surface_alt"],
                highlightbackground=THEME["border"],
                highlightthickness=1,
                padx=12, pady=10
            )
            card.pack(fill="x", pady=4, padx=2)

            # Checkbox indicator button
            check_char = "✓" if is_done else " "
            check_fg = THEME["accent_green"] if is_done else THEME["text_muted"]
            check_bg = "#233329" if is_done else THEME["entry_bg"]

            chk_btn = tk.Button(
                card, text=check_char, font=("Segoe UI", 11, "bold"),
                width=2, height=1, relief="flat", cursor="hand2",
                bg=check_bg, fg=check_fg, activebackground=THEME["surface_hover"],
                command=lambda idx=real_idx: self.toggle_task(idx)
            )
            chk_btn.pack(side="left", padx=(0, 10))

            # Task Title Label
            title_font = ("Segoe UI", 11, "overstrike") if is_done else ("Segoe UI", 11)
            title_fg = THEME["text_done"] if is_done else THEME["text"]

            lbl = tk.Label(
                card, text=task["title"], font=title_font,
                bg=card["bg"], fg=title_fg, anchor="w", wraplength=380, justify="left"
            )
            lbl.pack(side="left", fill="x", expand=True)

            # Double click label to edit
            lbl.bind("<Double-Button-1>", lambda _, idx=real_idx: self.edit_task(idx))

            # Action buttons
            actions_frame = tk.Frame(card, bg=card["bg"])
            actions_frame.pack(side="right")

            # Edit button
            edit_btn = tk.Button(
                actions_frame, text="✎", font=("Segoe UI", 10),
                bg=card["bg"], fg=THEME["accent_yellow"], relief="flat",
                cursor="hand2", activebackground=THEME["surface_hover"],
                activeforeground=THEME["accent_yellow"], padx=6, pady=2,
                command=lambda idx=real_idx: self.edit_task(idx)
            )
            edit_btn.pack(side="left", padx=2)

            # Delete button
            del_btn = tk.Button(
                actions_frame, text="✕", font=("Segoe UI", 10, "bold"),
                bg=card["bg"], fg=THEME["accent_red"], relief="flat",
                cursor="hand2", activebackground=THEME["surface_hover"],
                activeforeground=THEME["accent_red"], padx=6, pady=2,
                command=lambda idx=real_idx: self.delete_task(idx)
            )
            del_btn.pack(side="left", padx=2)


def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
