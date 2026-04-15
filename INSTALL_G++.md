# How to Install G++ (MinGW) for C++ Compilation

The application is currently running in **Python Fallback Mode** because a C++ compiler was not found. To enable the true high-performance C++ backend, file `main.cpp` must be compiled.

## Option 1: Install MinGW (Recommended)

1.  Download **MinGW-w64**: [https://sourceforge.net/projects/mingw-w64/](https://sourceforge.net/projects/mingw-w64/)
2.  Run the installer/installer script.
3.  **Critical Step**: You must add the `bin` folder to your System PATH.
    *   Search Windows for "Edit the system environment variables".
    *   Click "Environment Variables".
    *   Under "System variables", find `Path` -> Edit.
    *   Add the path to your `bin` folder (e.g., `C:\Program Files\mingw-w64\...\bin`).
4.  Restart your terminal/IDE.
5.  Type `g++ --version` to verify.

## Option 2: Use Visual Studio

If you have Visual Studio installed:
1.  Open **"Developer Command Prompt for VS 2022"** (Search in Start Menu).
2.  Navigate to this project folder:
    ```cmd
    cd "d:\3rd Semester\Data Structures\Project"
    ```
3.  Compile manually:
    ```cmd
    cl /EHsc main.cpp
    ```
4.  This creates `main.exe`. The app will now automatically use the C++ backend!
