# ⚡ HUFFMAN PROJECT ZIPPER ⚡

```text
  _   _ _   _ _____ _____ __  __     _    _   _ 
 | | | | | | |  ___|  ___|  \/  |   / \  | \ | |
 | |_| | | | | |_  | |_  | |\/| |  / _ \ |  \| |
 |  _  | |_| |  _| |  _| | |  | | / ___ \| |\  |
 |_| |_|\___/|_|   |_|   |_|  |_|/_/   \_\_| \_|

  ____ ___  ____  _____   ____  _____ ____  
 / ___/ _ \|  _ \| ____| |  _ \| ____/ ___| 
| |  | | | | | | |  _|   | |_) |  _| \___ \ 
| |__| |_| | |_| | |___  |  _ <| |___ ___) |
 \____\___/|____/|_____| |_| \_\_____|____/ 
```

> **A high-performance file compression engine featuring a C++ backend and a modern Flask web interface.**

---

## 🚀 Overview

The **Huffman Project Zipper** is a full-stack compression utility built around one of computer science's most elegant algorithms. It leverages the raw efficiency of **Huffman Coding** implemented in **C++20** for the heavy lifting, while wrapping everything in a clean, user-friendly interface powered by **Python/Flask**.

No data is lost. No quality is sacrificed. Just pure, lossless compression — fast.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🛡️ **Lossless Compression** | 100% data integrity guaranteed via Huffman Coding |
| ⚡ **Hybrid Architecture** | C++ speed meets Python flexibility |
| 🎨 **Modern UI** | Clean Red, White & Black dashboard |
| 📂 **Multi-file Support** | Handles `.txt`, `.pdf`, `.json`, and more |
| 🔄 **Two-way Processing** | Seamlessly compress and decompress files |

---

## 🛠️ Tech Stack

```
C++20          [████████████████████] 100%  — Core compression logic
Python / Flask [██████████████░░░░░░]  70%  — Web server & API layer
HTML5 / CSS3   [██████████░░░░░░░░░░]  50%  — Frontend interface
```

---

## 📦 Installation & Setup

### Prerequisites
- **G++ compiler** (C++20 support required)
- **Python 3.8+**
- **pip**

---

### Step 1 — Compile the C++ Engine

The C++ backend must be compiled into `main.exe` before the app can run.

```bash
g++ Project/main.cpp -o Project/main.exe
```

> ⚠️ **Note:** If you're on Linux/macOS, output to `main` (no `.exe`) and update the path reference in `app.py` accordingly.

---

### Step 2 — Set Up Python Environment

Install the required web dependencies:

```bash
pip install flask
```

---

### Step 3 — Launch the Application

```bash
python Project/app.py
```

📍 Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 📂 Directory Structure

```
.
├── Project/
│   ├── static/          # CSS, JS, and image assets
│   ├── templates/       # HTML layout files (Jinja2)
│   ├── uploads/         # Temporary user uploads  ← git ignored
│   ├── outputs/         # Compressed/decompressed results  ← git ignored
│   ├── app.py           # Flask web server
│   └── main.cpp         # Huffman coding engine (C++20)
├── .gitignore           # Git exclusion rules
└── README.md            # You're reading it
```

> 📌 `uploads/` and `outputs/` are intentionally excluded from version control — they hold runtime-generated files only.

---

## 🧠 How Huffman Coding Works

Huffman Coding is a **greedy algorithm** that assigns shorter binary codes to more frequently occurring characters, and longer codes to rarer ones. The result:

1. **Frequency analysis** — count how often each character appears
2. **Priority queue** — build a min-heap of character frequencies
3. **Tree construction** — merge the two lowest-frequency nodes repeatedly
4. **Code generation** — traverse the tree to assign binary codes
5. **Encoding** — replace each character with its binary code

The encoded output is always smaller than or equal to the original for any real-world input.

---

## ⚙️ Usage

1. Open the web interface at `http://127.0.0.1:5000`
2. Upload a file (`.txt`, `.pdf`, `.json`, etc.)
3. Choose **Compress** or **Decompress**
4. Download your processed file from the outputs panel

---

## 👤 Author

**Muhammad Abdullah Mushtaq**  
Data Structures & Algorithms — 3rd Semester  
April 2026

---

## 📄 License

This project was developed for academic purposes. All rights reserved.
