

---

# 🔐 Password Security Tool — Analyzer & Wordlist Generator

This all-in-one Python tool combines **defensive** (password analysis) and **offensive** (custom wordlist generation) security features.
It supports **Command-Line Interface (CLI)**, an **Interactive Menu**, and a simple **Graphical User Interface (GUI)** built with Tkinter.

---

## ✨ Features

### 🛡️ Password Analysis

* **Strength Scoring:** Uses the `zxcvbn` library for realistic password strength scores (0–4).
* **Entropy Calculation:** Computes **Shannon entropy** in bits — a measure of password randomness.
* **Detailed Feedback:** Displays warnings and actionable suggestions to improve password strength.
* **Composition Breakdown:** Reports presence of lowercase, uppercase, digits, and symbols.
* **Crack Time Estimate:** Provides human-readable estimated crack time.

### 🔨 Wordlist Generation

* **Targeted Wordlists:** Build custom wordlists from personal data (names, pets, dates).
* **Automated Transformations:**

  * Capitalization patterns (`password`, `Password`, `PASSWORD`)
  * **Leetspeak** (`pa55word`, `p@ssw0rd`)
  * Year and number suffixes (`Password2025`, `123Password`)
  * Common separators (`name-date`, `name_pet`)
* **Performance-Aware:** Automatically limits list size with `--max` parameter.
* **Output Control:** Saves to `.txt` wordlist file for ethical security testing.

---

## 🧩 Requirements

* **Python 3.7+**
* **Dependencies:**

  ```bash
  pip install zxcvbn
  ```
* Tkinter is required for GUI mode (included with most Python distributions).

---

## 🚀 Usage

You can use the tool in **three different modes**:

---

### 🧭 1. Interactive Menu (Default)

If you run the script **without arguments**, the interactive text menu starts:

```bash
python security_tool.py
```

Menu options:

1️⃣ Launch GUI Mode
2️⃣ Analyze a Password
3️⃣ Generate Custom Wordlist
4️⃣ Exit

---

### ⚙️ 2. Command-Line Interface (CLI)

You can also run specific operations directly from the terminal.

#### 🔍 Analyze a Password

```bash
python security_tool.py analyze "P@ssw0rd123!"
```

#### 🧰 Generate a Custom Wordlist

```bash
python security_tool.py generate --name alice --pet fluffy --date 1998 --output mylist.txt --max 20000
```



---

### 🪟 3. GUI Mode (Graphical Interface)

To launch the GUI:

```bash
python security_tool.py --gui
```

**Features:**

* Password strength analyzer tab
* Wordlist generator tab
* Show/hide password toggle
* Save wordlists directly via file dialog



---

## 🧮 How It Works

### Entropy Calculation

Entropy is estimated using:

```
Entropy = len(password) × log₂(character_set_size)
```

Character set is determined by presence of lowercase, uppercase, digits, and symbols.

### Wordlist Expansion Strategy

1. Normalize base words (lowercase)
2. Add capitalization variants
3. Apply leetspeak substitutions
4. Append common suffixes/prefixes (years, numbers, special chars)
5. Combine words with `_` or `-`
6. Enforce a maximum (`--max`) limit

---

## 🛑 Ethical Disclaimer

⚠️ **Important Notice:**

This tool is provided for **educational and authorized security testing purposes only**.

* ✅ Use only with explicit permission from the system owner.
* ❌ Do **not** use against public or unauthorized systems.
* 🧩 Always comply with your local laws and organizational policies.

The author assumes **no liability** for misuse.

---

