"""
CodSoft Task 4: Rock-Paper-Scissors Game (GUI Edition)
A modern, animated arcade Rock-Paper-Scissors game with live statistics, streak tracker, and game modes.
"""

import random
import tkinter as tk
from tkinter import ttk, messagebox

THEME = {
    "bg": "#0f111a",
    "surface": "#171a26",
    "surface_alt": "#202536",
    "surface_hover": "#2c3349",
    "border": "#2d354d",
    "text": "#f8fafc",
    "text_muted": "#94a3b8",
    "accent_player": "#38bdf8",   # Cyan
    "accent_comp": "#f43f5e",     # Rose / Pink
    "accent_win": "#10b981",      # Emerald
    "accent_lose": "#ef4444",     # Red
    "accent_tie": "#f59e0b",      # Amber
    "btn_rock": "#8b5cf6",        # Purple
    "btn_paper": "#06b6d4",       # Teal
    "btn_scissors": "#ec4899"     # Pink
}

CHOICE_INFO = {
    "rock": {"emoji": "🪨", "label": "Rock", "beats": "scissors", "verb": "crushes"},
    "paper": {"emoji": "📄", "label": "Paper", "beats": "rock", "verb": "covers"},
    "scissors": {"emoji": "✂️", "label": "Scissors", "beats": "paper", "verb": "cuts"}
}


class RockPaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors • CodSoft Task 4")
        self.root.geometry("680x800")
        self.root.minsize(580, 680)
        self.root.configure(bg=THEME["bg"])

        # Game state
        self.user_score = 0
        self.comp_score = 0
        self.ties = 0
        self.total_rounds = 0
        self.current_streak = 0
        self.best_streak = 0
        self.target_score = 0  # 0 = Endless / Free play
        self.history = []

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # 1. Top Header with title and mode selector
        header = tk.Frame(self.root, bg=THEME["surface"], padx=20, pady=14)
        header.pack(fill="x")

        top_row = tk.Frame(header, bg=THEME["surface"])
        top_row.pack(fill="x")

        title_lbl = tk.Label(
            top_row, text="🎮 Rock • Paper • Scissors",
            font=("Segoe UI", 18, "bold"), bg=THEME["surface"], fg=THEME["text"]
        )
        title_lbl.pack(side="left")

        # Game mode dropdown / radio
        mode_frame = tk.Frame(top_row, bg=THEME["surface"])
        mode_frame.pack(side="right")

        tk.Label(
            mode_frame, text="Mode:", font=("Segoe UI", 9),
            bg=THEME["surface"], fg=THEME["text_muted"]
        ).pack(side="left", padx=(0, 6))

        self.mode_var = tk.StringVar(value="Free Play")
        mode_combo = ttk.Combobox(
            mode_frame, textvariable=self.mode_var,
            values=["Free Play", "First to 3", "First to 5", "First to 10"],
            state="readonly", width=11, font=("Segoe UI", 9)
        )
        mode_combo.pack(side="left")
        mode_combo.bind("<<ComboboxSelected>>", self._on_mode_change)

        # 2. Scoreboard Cards
        score_strip = tk.Frame(self.root, bg=THEME["bg"], padx=20, pady=12)
        score_strip.pack(fill="x")

        for c in range(4):
            score_strip.columnconfigure(c, weight=1)

        # Score widgets
        self.score_card_you = self._create_stat_card(
            score_strip, 0, "YOU (Player)", "0", THEME["accent_player"]
        )
        self.score_card_comp = self._create_stat_card(
            score_strip, 1, "COMPUTER", "0", THEME["accent_comp"]
        )
        self.score_card_ties = self._create_stat_card(
            score_strip, 2, "TIES", "0", THEME["accent_tie"]
        )
        self.score_card_streak = self._create_stat_card(
            score_strip, 3, "STREAK", "0 🔥", THEME["accent_win"]
        )

        # 3. Duel Arena Display
        arena_frame = tk.Frame(
            self.root, bg=THEME["surface"],
            highlightbackground=THEME["border"], highlightthickness=1,
            padx=16, pady=20
        )
        arena_frame.pack(fill="x", padx=20, pady=(0, 14))

        arena_grid = tk.Frame(arena_frame, bg=THEME["surface"])
        arena_grid.pack(fill="x")
        arena_grid.columnconfigure(0, weight=4)
        arena_grid.columnconfigure(1, weight=2)
        arena_grid.columnconfigure(2, weight=4)

        # Player Duel Slot
        player_col = tk.Frame(arena_grid, bg=THEME["surface"])
        player_col.grid(row=0, column=0, sticky="nsew")

        tk.Label(
            player_col, text="👤 YOUR MOVE", font=("Segoe UI", 10, "bold"),
            bg=THEME["surface"], fg=THEME["accent_player"]
        ).pack()

        self.player_move_card = tk.Label(
            player_col, text="❓", font=("Segoe UI", 48),
            bg=THEME["surface_alt"], fg=THEME["text"],
            width=3, height=1, relief="flat", highlightbackground=THEME["border"], highlightthickness=1
        )
        self.player_move_card.pack(pady=10)

        self.player_move_name = tk.Label(
            player_col, text="Choose below...", font=("Segoe UI", 11),
            bg=THEME["surface"], fg=THEME["text_muted"]
        )
        self.player_move_name.pack()

        # VS Center
        vs_col = tk.Frame(arena_grid, bg=THEME["surface"])
        vs_col.grid(row=0, column=1, sticky="nsew")

        tk.Label(
            vs_col, text="VS", font=("Segoe UI", 22, "bold"),
            bg=THEME["surface"], fg=THEME["text_muted"]
        ).pack(pady=(28, 4))

        self.round_badge = tk.Label(
            vs_col, text="Round 0", font=("Segoe UI", 9, "bold"),
            bg=THEME["surface_alt"], fg=THEME["text_muted"], padx=8, pady=3
        )
        self.round_badge.pack()

        # Computer Duel Slot
        comp_col = tk.Frame(arena_grid, bg=THEME["surface"])
        comp_col.grid(row=0, column=2, sticky="nsew")

        tk.Label(
            comp_col, text="🤖 COMPUTER", font=("Segoe UI", 10, "bold"),
            bg=THEME["surface"], fg=THEME["accent_comp"]
        ).pack()

        self.comp_move_card = tk.Label(
            comp_col, text="❓", font=("Segoe UI", 48),
            bg=THEME["surface_alt"], fg=THEME["text"],
            width=3, height=1, relief="flat", highlightbackground=THEME["border"], highlightthickness=1
        )
        self.comp_move_card.pack(pady=10)

        self.comp_move_name = tk.Label(
            comp_col, text="Waiting...", font=("Segoe UI", 11),
            bg=THEME["surface"], fg=THEME["text_muted"]
        )
        self.comp_move_name.pack()

        # Banner for Outcome
        self.banner_frame = tk.Frame(
            arena_frame, bg=THEME["surface_alt"], padx=14, pady=10,
            highlightbackground=THEME["border"], highlightthickness=1
        )
        self.banner_frame.pack(fill="x", pady=(16, 0))

        self.result_title = tk.Label(
            self.banner_frame, text="Make your move to start the battle!",
            font=("Segoe UI", 13, "bold"), bg=THEME["surface_alt"], fg=THEME["text"]
        )
        self.result_title.pack()

        self.result_subtitle = tk.Label(
            self.banner_frame, text="Rock beats Scissors • Scissors beat Paper • Paper beats Rock",
            font=("Segoe UI", 9), bg=THEME["surface_alt"], fg=THEME["text_muted"]
        )
        self.result_subtitle.pack(pady=(2, 0))

        # 4. Interactive Choice Buttons
        buttons_frame = tk.Frame(self.root, bg=THEME["bg"], padx=20)
        buttons_frame.pack(fill="x", pady=(0, 14))

        for c in range(3):
            buttons_frame.columnconfigure(c, weight=1)

        choices = [
            ("rock", "🪨", "ROCK", "[R] Crushes Scissors", THEME["btn_rock"]),
            ("paper", "📄", "PAPER", "[P] Covers Rock", THEME["btn_paper"]),
            ("scissors", "✂️", "SCISSORS", "[S] Cuts Paper", THEME["btn_scissors"]),
        ]

        for idx, (move, emoji, name, desc, color) in enumerate(choices):
            btn_card = tk.Frame(
                buttons_frame, bg=THEME["surface"],
                highlightbackground=color, highlightthickness=2, padx=10, pady=12
            )
            btn_card.grid(row=0, column=idx, sticky="nsew", padx=6)

            e_lbl = tk.Label(
                btn_card, text=emoji, font=("Segoe UI", 32),
                bg=THEME["surface"], fg=THEME["text"]
            )
            e_lbl.pack()

            n_lbl = tk.Label(
                btn_card, text=name, font=("Segoe UI", 12, "bold"),
                bg=THEME["surface"], fg=color
            )
            n_lbl.pack(pady=(4, 2))

            d_lbl = tk.Label(
                btn_card, text=desc, font=("Segoe UI", 8),
                bg=THEME["surface"], fg=THEME["text_muted"]
            )
            d_lbl.pack()

            # Make whole card clickable
            for w in (btn_card, e_lbl, n_lbl, d_lbl):
                w.configure(cursor="hand2")
                w.bind("<Button-1>", lambda _, m=move: self.play_round(m))

        # 5. History & Match Stats
        history_frame = tk.Frame(
            self.root, bg=THEME["surface"],
            highlightbackground=THEME["border"], highlightthickness=1,
            padx=16, pady=12
        )
        history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        hist_top = tk.Frame(history_frame, bg=THEME["surface"])
        hist_top.pack(fill="x", pady=(0, 6))

        tk.Label(
            hist_top, text="Match History", font=("Segoe UI", 10, "bold"),
            bg=THEME["surface"], fg=THEME["text"]
        ).pack(side="left")

        self.winrate_lbl = tk.Label(
            hist_top, text="Win Rate: 0.0%", font=("Segoe UI", 9),
            bg=THEME["surface"], fg=THEME["accent_player"]
        )
        self.winrate_lbl.pack(side="right")

        self.history_listbox = tk.Listbox(
            history_frame, bg=THEME["surface_alt"], fg=THEME["text"],
            font=("Consolas", 10), relief="flat", highlightthickness=0, height=5,
            selectbackground=THEME["surface_hover"]
        )
        self.history_listbox.pack(fill="both", expand=True)

        # 6. Bottom Controls
        bottom_bar = tk.Frame(self.root, bg=THEME["surface"], padx=20, pady=10)
        bottom_bar.pack(fill="x", side="bottom")

        reset_btn = tk.Button(
            bottom_bar, text="🔄 Reset Game & Scores", font=("Segoe UI", 9, "bold"),
            bg=THEME["surface_alt"], fg=THEME["text"],
            activebackground=THEME["surface_hover"], relief="flat",
            padx=14, pady=6, cursor="hand2", command=self.reset_game
        )
        reset_btn.pack(side="left")

        tk.Label(
            bottom_bar, text="Shortcut keys: [R] Rock  [P] Paper  [S] Scissors",
            font=("Segoe UI", 8), bg=THEME["surface"], fg=THEME["text_muted"]
        ).pack(side="right")

    def _create_stat_card(self, parent, col, title, initial_val, color):
        frame = tk.Frame(
            parent, bg=THEME["surface"],
            highlightbackground=THEME["border"], highlightthickness=1,
            padx=12, pady=10
        )
        frame.grid(row=0, column=col, sticky="nsew", padx=4)

        t_lbl = tk.Label(
            frame, text=title, font=("Segoe UI", 8, "bold"),
            bg=THEME["surface"], fg=THEME["text_muted"]
        )
        t_lbl.pack()

        val_lbl = tk.Label(
            frame, text=initial_val, font=("Segoe UI", 16, "bold"),
            bg=THEME["surface"], fg=color
        )
        val_lbl.pack(pady=(2, 0))
        return val_lbl

    def _bind_keys(self):
        self.root.bind("<r>", lambda _: self.play_round("rock"))
        self.root.bind("<R>", lambda _: self.play_round("rock"))
        self.root.bind("<p>", lambda _: self.play_round("paper"))
        self.root.bind("<P>", lambda _: self.play_round("paper"))
        self.root.bind("<s>", lambda _: self.play_round("scissors"))
        self.root.bind("<S>", lambda _: self.play_round("scissors"))

    def _on_mode_change(self, event):
        val = self.mode_var.get()
        if "3" in val:
            self.target_score = 3
        elif "5" in val:
            self.target_score = 5
        elif "10" in val:
            self.target_score = 10
        else:
            self.target_score = 0
        self.reset_game()

    # ---------------- Game Logic ----------------
    def play_round(self, user_choice):
        # Check target score
        if self.target_score > 0 and (self.user_score >= self.target_score or self.comp_score >= self.target_score):
            messagebox.showinfo(
                "Match Finished",
                "The target score was reached! Click 'Reset Game' to start a new match.",
                parent=self.root
            )
            return

        comp_choice = random.choice(list(CHOICE_INFO.keys()))
        self.total_rounds += 1
        self.round_badge.configure(text=f"Round {self.total_rounds}")

        # Update visuals
        u_info = CHOICE_INFO[user_choice]
        c_info = CHOICE_INFO[comp_choice]

        self.player_move_card.configure(text=u_info["emoji"])
        self.player_move_name.configure(text=u_info["label"])
        self.comp_move_card.configure(text=c_info["emoji"])
        self.comp_move_name.configure(text=c_info["label"])

        # Decide winner
        if user_choice == comp_choice:
            result = "tie"
            self.ties += 1
            self.current_streak = 0
            title_text = "🤝 It's a Tie!"
            subtitle_text = f"Both chose {u_info['label']} ({u_info['emoji']})"
            banner_bg = "#292318"
            title_fg = THEME["accent_tie"]
            hist_badge = "TIE "
        elif u_info["beats"] == comp_choice:
            result = "win"
            self.user_score += 1
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
            title_text = f"🎉 You Won Round #{self.total_rounds}!"
            subtitle_text = f"{u_info['label']} {u_info['verb']} {c_info['label']}!"
            banner_bg = "#12281e"
            title_fg = THEME["accent_win"]
            hist_badge = "WIN "
        else:
            result = "lose"
            self.comp_score += 1
            self.current_streak = 0
            title_text = f"🤖 Computer Won Round #{self.total_rounds}!"
            subtitle_text = f"{c_info['label']} {c_info['verb']} {u_info['label']}!"
            banner_bg = "#2b1419"
            title_fg = THEME["accent_lose"]
            hist_badge = "LOSS"

        # Update Banner
        self.banner_frame.configure(bg=banner_bg)
        self.result_title.configure(text=title_text, bg=banner_bg, fg=title_fg)
        self.result_subtitle.configure(text=subtitle_text, bg=banner_bg)

        # Update Scoreboard
        self.score_card_you.configure(text=str(self.user_score))
        self.score_card_comp.configure(text=str(self.comp_score))
        self.score_card_ties.configure(text=str(self.ties))
        streak_text = f"{self.current_streak} 🔥" if self.current_streak > 0 else "0"
        self.score_card_streak.configure(text=streak_text)

        # Update win rate
        winrate = (self.user_score / self.total_rounds * 100) if self.total_rounds > 0 else 0
        self.winrate_lbl.configure(text=f"Win Rate: {winrate:.1f}%")

        # History log
        log_line = (
            f"#{self.total_rounds:02d} [{hist_badge}] You: {u_info['emoji']} {u_info['label']:<8} "
            f"vs  Comp: {c_info['emoji']} {c_info['label']:<8} "
            f"-> Score {self.user_score}-{self.comp_score}"
        )
        self.history_listbox.insert(tk.END, log_line)
        self.history_listbox.see(tk.END)

        # Check for Match Victory in Target Mode
        if self.target_score > 0:
            if self.user_score >= self.target_score:
                messagebox.showinfo(
                    "🏆 CHAMPION!",
                    f"Congratulations! You won the match {self.user_score} to {self.comp_score}!\n"
                    f"Best Streak: {self.best_streak}",
                    parent=self.root
                )
            elif self.comp_score >= self.target_score:
                messagebox.showinfo(
                    "🤖 Match Over",
                    f"Computer won the match {self.comp_score} to {self.user_score}!\n"
                    f"Better luck next time!",
                    parent=self.root
                )

    def reset_game(self):
        self.user_score = 0
        self.comp_score = 0
        self.ties = 0
        self.total_rounds = 0
        self.current_streak = 0
        self.score_card_you.configure(text="0")
        self.score_card_comp.configure(text="0")
        self.score_card_ties.configure(text="0")
        self.score_card_streak.configure(text="0")
        self.winrate_lbl.configure(text="Win Rate: 0.0%")
        self.round_badge.configure(text="Round 0")
        self.player_move_card.configure(text="❓")
        self.player_move_name.configure(text="Choose below...")
        self.comp_move_card.configure(text="❓")
        self.comp_move_name.configure(text="Waiting...")
        self.banner_frame.configure(bg=THEME["surface_alt"])
        self.result_title.configure(
            text="Make your move to start the battle!",
            bg=THEME["surface_alt"], fg=THEME["text"]
        )
        self.result_subtitle.configure(
            text="Rock beats Scissors • Scissors beat Paper • Paper beats Rock",
            bg=THEME["surface_alt"]
        )
        self.history_listbox.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = RockPaperScissorsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
