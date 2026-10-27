# CODSOFT Python Development Internship

A collection of interactive desktop applications developed as part of the **CodSoft Python Development Internship**.

Each application is built as a self-contained Graphical User Interface (GUI) powered by Python's built-in `tkinter` and `ttk` libraries. **No external pip packages or heavy third-party frameworks are required**—all scripts run out of the box on standard Python installations.

---

## 📁 Repository Structure

```text
codsoft-internship/
├── .gitignore                      # Git ignore configuration (Python cache, tasks.json, IDE files)
├── README.md                       # Comprehensive documentation and project guide
├── task1_todo_list.py              # Task 1: Graphical To-Do List Application
├── task2_calculator.py             # Task 2: Modern Desktop Calculator
├── task3_password_generator.py     # Task 3: Secure Password Generator with Entropy Meter
└── task4_rock_paper_scissors.py    # Task 4: Interactive Rock-Paper-Scissors Arena
```

---

## 🚀 Projects Overview

| Task | Script | Description | Key Highlights |
|---|---|---|---|
| **Task 1** | [`task1_todo_list.py`](task1_todo_list.py) | To-Do List Manager | JSON persistence, live progress bar, search bar, active/completed filters, inline editing |
| **Task 2** | [`task2_calculator.py`](task2_calculator.py) | Modern Calculator | Arithmetic, powers, roots, history panel with recall, keyboard bindings, error protection |
| **Task 3** | [`task3_password_generator.py`](task3_password_generator.py) | Secure Password Generator | `secrets` module, entropy calculation, visual strength bar, presets, clipboard copy |
| **Task 4** | [`task4_rock_paper_scissors.py`](task4_rock_paper_scissors.py) | Rock-Paper-Scissors Game | Duel arena, live scoreboard, win streaks, match modes (First to 3/5/10), match history |

---

## 📌 Project Details & Features

### 1. Task 1: To-Do List Application ([`task1_todo_list.py`](task1_todo_list.py))

A productivity and task management desktop application featuring automatic JSON persistence and a modern Catppuccin Mocha-inspired dark palette.

* **Persistent Storage**: Automatically saves and loads tasks from a local `tasks.json` file.
* **Live Progress Tracking**: Visual progress bar and percentage indicator that dynamically updates as tasks are completed.
* **Smart Filtering & Search**:
  * Filter tabs: **All**, **Active**, and **Done**.
  * Instant search box that filters visible tasks in real-time.
* **Task Operations**:
  * Quick add via entry box or pressing <kbd>Enter</kbd>.
  * Single-click toggle button to mark tasks complete (with strikethrough styling).
  * Double-click any task label or click the ✎ button to edit the description in place.
  * Individual delete button (✕).
* **Batch Controls**: *Clear Completed*, *Mark All Done*, and *Delete All* with confirmation dialogs.

**How to run:**
```bash
python task1_todo_list.py
```

---

### 2. Task 2: Simple Calculator ([`task2_calculator.py`](task2_calculator.py))

A desktop calculator designed with a slate-charcoal interface, dual expression display, and advanced mathematical operations.

* **Dual Display**: Displays the current expression at the top with large dynamic font scaling for the active result.
* **Supported Operations**:
  * Core arithmetic: Addition (`+`), Subtraction (`-`), Multiplication (`×`), Division (`÷`).
  * Advanced operations: Exponentiation ($x^y$), Square ($x^2$), Square Root ($\sqrt{x}$), Modulo (`%`).
  * Sign negation (`±`), clear entry (`CE`), clear all (`C`), and backspace (`⌫`).
* **Operation Chaining**: Smoothly evaluates continuous operations without requiring intermediate `=` presses.
* **Defensive Math Safeguards**: Built-in protections against division by zero, modulo by zero, negative square roots, and numeric overflow errors.
* **Collapsible History Log**: Toggleable side panel logging all calculations with double-click support to recall results into the active display.
* **Full Keyboard Support**: Operate entirely via keyboard (`0-9`, `+`, `-`, `*`, `/`, `%`, `^`, <kbd>Enter</kbd>, <kbd>Backspace</kbd>, <kbd>Escape</kbd>).

**How to run:**
```bash
python task2_calculator.py
```

---

### 3. Task 3: Password Generator ([`task3_password_generator.py`](task3_password_generator.py))

A security-focused password generation utility utilizing Python's cryptographically secure `secrets` module to produce high-entropy credentials.

* **Cryptographic Security**: Generates non-deterministic, cryptographically strong passwords using `secrets.choice()` and `SystemRandom().shuffle()`.
* **Guaranteed Character Inclusion**: Guarantees that at least one character from each enabled character type is included in the generated password.
* **Customization Parameters**:
  * Length slider ranging from 4 to 64 characters.
  * Quick length presets: **8**, **12**, **16**, **24**, and **32**.
  * Toggles for Uppercase (`A-Z`), Lowercase (`a-z`), Digits (`0-9`), and Special Symbols (`!@#$%...`).
  * Option to avoid ambiguous characters (`0`, `O`, `l`, `1`, `I`).
* **Strength & Entropy Analysis**:
  * Computes real-time Shannon entropy ($L \times \log_2(\text{pool\_size})$) in bits.
  * Visual 4-tier colored strength meter (*Very Weak*, *Weak*, *Good*, *Strong*).
* **Convenience Features**:
  * 1-click clipboard copy with animated `✓ Copied!` confirmation.
  * Show/hide password masking toggle (👁️).
  * Session history box with double-click support to recall and re-copy previously generated passwords.

**How to run:**
```bash
python task3_password_generator.py
```

---

### 4. Task 4: Rock-Paper-Scissors Game ([`task4_rock_paper_scissors.py`](task4_rock_paper_scissors.py))

An interactive arcade duel game featuring animated battle banners, live win tracking, and match tournament modes.

* **Duel Arena**: Visual matchup cards showcasing player and computer moves with large emojis and descriptive action verbs (*crushes*, *covers*, *cuts*).
* **Multiple Game Modes**:
  * **Free Play** (Endless casual mode)
  * **First to 3** (Match format)
  * **First to 5** (Tournament format)
  * **First to 10** (Marathon format)
  * Automatic match winner popup dialog when the target score is attained.
* **Live Statistics Dashboard**:
  * Real-time counters for Player Wins, Computer Wins, and Ties.
  * Active win streak tracker with 🔥 badge and best streak retention.
  * Live win rate percentage calculation.
* **Interaction**: Clickable move cards and keyboard hotkeys (<kbd>R</kbd> for Rock, <kbd>P</kbd> for Paper, <kbd>S</kbd> for Scissors).
* **Chronological Match History**: Detailed scrollable history log tracking round numbers, choices, and scores.
* **Scoreboard Reset**: 1-click game state reset.

**How to run:**
```bash
python task4_rock_paper_scissors.py
```

---

## 🛠️ Requirements & Setup

### Prerequisites
* **Python 3.8 or higher**
* Standard Python installation (Tkinter is included by default with standard Python installers on Windows and macOS).

> *Note for Linux users: If Tkinter is not pre-installed, install it via `sudo apt install python3-tk`.*

### Installation & Execution

1. **Clone or download the repository:**
   ```bash
   git clone <repository-url>
   cd "codsoft internship"
   ```

2. **Run any application directly:**
   ```bash
   # Task 1: To-Do List Application
   python task1_todo_list.py

   # Task 2: Calculator
   python task2_calculator.py

   # Task 3: Password Generator
   python task3_password_generator.py

   # Task 4: Rock-Paper-Scissors Game
   python task4_rock_paper_scissors.py
   ```

---

## 💻 Technologies Used

* **Language**: Python 3
* **GUI Toolkit**: Tkinter & TTK (`ttk.Style`, `ttk.Progressbar`, `ttk.Scale`, `ttk.Combobox`, `ttk.Scrollbar`)
* **Standard Modules**: `json`, `math`, `secrets`, `random`, `string`, `os`
* **Zero Third-Party Dependencies**: Completely standalone and portable
