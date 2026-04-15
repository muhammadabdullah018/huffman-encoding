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

### 🚀 **Overview**
The **Huffman Project Zipper** is a full-stack compression utility. It leverages the efficiency of **Huffman Coding** implemented in C++ for heavy lifting, while providing a sleek, user-friendly interface powered by **Python/Flask**.

### ✨ **Key Features**
- 🛡️ **Lossless Compression**: 100% data integrity using Huffman Coding.
- ⚡ **Hybrid Architecture**: C++ speed meets Python flexibility.
- 🎨 **Modern UI**: Clean Red, White, and Black dashboard.
- 📂 **Multi-file Support**: Handles `.txt`, `.pdf`, `.json`, and more.
- 🔄 **Two-way Process**: Seamlessly compress and decompress files.

---

### 🛠️ **Tech Stack**
- **Logic Backend**: `C++20` 
  `[████████████████████] 100%`
- **Web Server**: `Python / Flask`
  `[██████████████░░░░░░] 70%`
- **Frontend**: `HTML5 / CSS3`
  `[██████████░░░░░░░░░░] 50%`

---

### 📦 **Installation & Setup**

#### **1. Compile the C++ Engine**
The C++ backend must be compiled into `main.exe` for the application to function correctly.
```bash
# Using G++
g++ Project/main.cpp -o Project/main.exe
```

#### **2. Initialize Python Environment**
Install the necessary web dependencies.
```bash
pip install flask
```

#### **3. Launch the Application**
Start the local development server.
```bash
python Project/app.py
```
📍 Access via: `http://127.0.0.1:5000`

---

### 📂 **Directory Structure**
```text
.
├── Project/
│   ├── static/          # CSS, JS, and Images
│   ├── templates/       # HTML Layouts
│   ├── uploads/         # Temporary user uploads (ignored by git)
│   ├── outputs/         # Processed files (ignored by git)
│   ├── app.py           # Flask Server
│   └── main.cpp         # Huffman Logic
├── .gitignore           # Git exclusion rules
└── README.md            # This file!
```

---

### 👤 **Author**
Developed for **Data Structures & Algorithms (3rd Semester)**.

---
