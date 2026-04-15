# HUFFMAN PROJECT ZIPPER

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

### 🔗 [Live Demo: Huffman Engine on Railway](https://huffman-encoding-production.up.railway.app)

---

## 🚀 Project Overview

The **Huffman Project Zipper** is a full-stack, lossless compression utility. It bridges high-performance systems programming with a modern web interface to demonstrate the power of the **Huffman Coding Algorithm**. 

Built for speed and precision, the core engine handles binary file manipulation via **C++20**, while the **Python/Flask** orchestration layer provides a seamless, interactive user experience.

---

## 🛠️ Technical Architecture

### Core Engine
- **Language**: C++20
- **Algorithm**: Greedy Huffman Coding (Min-Heap Implementation)
- **Time Complexity**: O(n log n) for building, O(m log n) for encoding/decoding
- **Space Complexity**: O(n) for the frequency table and tree nodes

### Web Layer
- **Backend**: Python 3.10+ / Flask / Gunicorn
- **Frontend**: HTML5 / CSS3 / Vanilla JavaScript
- **Deployment**: containerized via Railway (Nixpacks)

---

## 📦 Local Setup & Installation

### 1. Compile the Backend
The C++ logic must be compiled into a binary before the web server starts.

**Windows:**
```powershell
g++ main.cpp -o main.exe
```

**Linux / macOS:**
```bash
g++ main.cpp -o huffman_engine
```

### 2. Environment Setup
Install the necessary Python dependencies:
```bash
pip install -r requirements.txt
```

### 3. Execution
Start the local server:
```bash
python main.py
```

---

## 📂 Repository Structure

```text
.
├── static/              # CSS, JS, and global UI assets
├── templates/           # HTML layout structures
├── uploads/             # Volatile storage for user input (ignored by git)
├── outputs/             # Volatile storage for processed results (ignored by git)
├── main.py              # Flask server and platform-agnostic bridge
├── main.cpp             # Core C++ Huffman logic
├── nixpacks.toml        # Railway build configuration
├── Procfile             # Process manager instructions
└── README.md            # Technical documentation
```

---

## 📖 Huffman Algorithm Summary

Huffman Coding is a prefix-free encoding method that achieves compression by assigning variable-length codes specifically to characters based on their frequency.

1.  **Frequency Analysis**: Maps characters to their occurrence counts.
2.  **Tree Building**: Uses a priority queue to iteratively merge the two least-frequent nodes into a binary tree.
3.  **Bit-mapping**: Traverses the resulting tree to generate optimal binary strings for each character.
4.  **Bit-streaming**: Replaces the source data with the binary maps and records the total bit length for lossless restoration.

---

## 👤 Author

**Muhammad Abdullah Mushtaq**  
Data Structures & Algorithms — Semester 3  
University Project, April 2026

---
