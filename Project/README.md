# Huffman Compressor Project

This project combines a C++ Huffman Coding backend with a modern Python/Flask web interface.

## Prerequisites

1.  **C++ Compiler** (MinGW, Visual Studio, etc.)
2.  **Python 3.x**
3.  **Flask** library for Python

## Setup Instructions

### 1. Compile the C++ Backend
You must compile `main.cpp` into an executable named `main.exe`.

**Using g++ in terminal:**
```bash
g++ main.cpp -o main.exe
```

**Using Visual Studio:**
Open `main.cpp` in Visual Studio and build it. Rename the resulting `.exe` to `main.exe` and place it in this folder (`d:\3rd Semester\Data Structures\Project`).

### 2. Install Flask
Open your terminal/command prompt in this folder and run:
```bash
pip install flask
```

### 3. Run the Web Interface
Run the Python server:
```bash
python app.py
```

### 4. Use the App
Open your web browser and go to:
http://127.0.0.1:5000

## Features
- **Compress**: Upload text files to compress them using Huffman coding.
- **Decompress**: Upload compressed (`.huf` or `.bin`) files to restore the original text.
- **Visuals**: A clean White, Red, and Black theme specific to your request.
